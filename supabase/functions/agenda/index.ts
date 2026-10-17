// Agenda de asesorías. El turno se confirma recién cuando Mercado Pago aprueba el pago.
// GET                      → turnos libres de las próximas semanas
// GET  ?token=...          → estado de una reserva (vuelta del pago y página de cancelación)
// POST {accion:"reservar"} → guarda el horario unos minutos y devuelve el link de pago
// POST {accion:"pagar"}    → nuevo link de pago para una reserva pendiente
// POST {accion:"cancelar"} → cancela con el token que llega en el mail
import { admin, cors, json, mp, SITE_URL } from "../_shared/comun.ts";
import { AVISOS, enviar, escapar, plantilla } from "../_shared/mail.ts";
import { cuando, ESPERA_PAGO_MIN, liberarVencidas, PRECIO_ASESORIA } from "../_shared/reservas.ts";

const HORAS = [17, 18, 19];            // inicio de cada turno de 1 hora (hora de Argentina)
const OFFSET_AR = 3;                   // Argentina = UTC-3, sin horario de verano
const ANTICIPACION_MS = 24 * 3600e3;   // mínimo un día de anticipación
const DIAS_ADELANTE = 21;              // cuántos días se muestran
const MAX_POR_PERSONA = 2;             // reservas futuras por mail

type DB = ReturnType<typeof admin>;

function texto(v: unknown, max: number): string {
  return typeof v === "string" ? v.trim().slice(0, max) : "";
}
const esToken = (t: string) => /^[0-9a-f-]{36}$/i.test(t);

/** Todos los turnos posibles (sin mirar si están ocupados). */
function turnosPosibles(bloqueados: Set<string>): string[] {
  const ahora = Date.now();
  const hoyAR = new Date(ahora - OFFSET_AR * 3600e3);
  const base = Date.UTC(hoyAR.getUTCFullYear(), hoyAR.getUTCMonth(), hoyAR.getUTCDate());
  const salida: string[] = [];
  for (let d = 0; d <= DIAS_ADELANTE; d++) {
    const dia = new Date(base + d * 86400e3);
    const sem = dia.getUTCDay();
    if (sem === 0 || sem === 6) continue;
    const fecha = dia.toISOString().slice(0, 10);
    if (bloqueados.has(fecha)) continue;
    for (const h of HORAS) {
      const inicio = new Date(base + d * 86400e3 + (h + OFFSET_AR) * 3600e3);
      if (inicio.getTime() - ahora >= ANTICIPACION_MS) salida.push(inicio.toISOString());
    }
  }
  return salida;
}

async function libres(db: DB): Promise<string[]> {
  await liberarVencidas(db);
  const [{ data: bloq }, { data: ocup }] = await Promise.all([
    db.from("dias_bloqueados").select("fecha"),
    db.from("reservas").select("inicio").in("estado", ["pendiente", "confirmada"]).gte("inicio", new Date().toISOString()),
  ]);
  const bloqueados = new Set((bloq ?? []).map((b) => String(b.fecha)));
  const ocupados = new Set((ocup ?? []).map((r) => new Date(r.inicio).toISOString()));
  return turnosPosibles(bloqueados).filter((t) => !ocupados.has(t));
}

// deno-lint-ignore no-explicit-any
async function linkDePago(r: Record<string, any>): Promise<string | null> {
  const vuelta = `${SITE_URL}/agenda.html?r=${r.token}`;
  const res = await mp("/checkout/preferences", {
    method: "POST",
    body: JSON.stringify({
      items: [{
        id: "asesoria",
        title: `Asesoría Visión Alfa · ${cuando(r.inicio)}`,
        quantity: 1,
        unit_price: PRECIO_ASESORIA,
        currency_id: "ARS",
      }],
      payer: { email: r.email, name: r.nombre },
      external_reference: `reserva|${r.id}`,
      back_urls: { success: `${vuelta}&pago=ok`, pending: `${vuelta}&pago=pendiente`, failure: `${vuelta}&pago=error` },
      auto_return: "approved",
      notification_url: `${Deno.env.get("SUPABASE_URL")}/functions/v1/mp-webhook`,
      statement_descriptor: "VISION ALFA",
      // Solo medios que se acreditan al instante: el horario no puede quedar guardado días.
      payment_methods: { excluded_payment_types: [{ id: "ticket" }, { id: "atm" }] },
      expires: true,
      expiration_date_to: new Date(new Date(r.vence).getTime() - 3 * 3600e3).toISOString().replace("Z", "-03:00"),
    }),
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok || !data.init_point) {
    console.error("preference asesoria", res.status, data);
    return null;
  }
  return data.init_point;
}

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors });
  const db = admin();

  if (req.method === "GET") {
    const token = new URL(req.url).searchParams.get("token");
    if (token) {
      if (!esToken(token)) return json({ error: "El link no es válido." }, 400);
      await liberarVencidas(db);
      const { data } = await db.from("reservas").select("inicio, estado, nombre, email, vence").eq("token", token).maybeSingle();
      if (!data) return json({ error: "No encontramos esa reserva." }, 404);
      return json({ ...data, cuando: cuando(data.inicio) });
    }
    return json({ turnos: await libres(db) });
  }

  if (req.method !== "POST") return json({ error: "Método no permitido" }, 405);
  const body = await req.json().catch(() => ({}));

  // ---------- Cancelar (desde el mail de confirmación) ----------
  if (body.accion === "cancelar") {
    const token = texto(body.token, 40);
    if (!esToken(token)) return json({ error: "El link no es válido." }, 400);
    const { data } = await db.from("reservas").select("*").eq("token", token).maybeSingle();
    if (!data) return json({ error: "No encontramos esa reserva." }, 404);
    if (data.estado !== "confirmada") return json({ ok: true, ya: true });
    if (new Date(data.inicio).getTime() < Date.now()) return json({ error: "Ese turno ya pasó." }, 400);
    const conTiempo = new Date(data.inicio).getTime() - Date.now() >= 24 * 3600e3;
    await db.from("reservas").update({ estado: "cancelada" }).eq("id", data.id);
    const c = cuando(data.inicio);
    const nota = conTiempo
      ? "Canceló con más de 24 horas: corresponde devolverle el pago o pasarla a otro horario."
      : "Canceló con menos de 24 horas de anticipación.";
    await enviar({
      para: AVISOS, responderA: data.email,
      asunto: `Turno cancelado: ${data.nombre} · ${c}`,
      texto: `${data.nombre} (${data.email}, WhatsApp ${data.whatsapp}) canceló la asesoría del ${c}.\n${nota}\nOperación de Mercado Pago: ${data.pago_id ?? "-"}\nEl horario quedó libre otra vez.`,
      html: plantilla("Se canceló un turno", `<p><strong>${escapar(data.nombre)}</strong> (${escapar(data.email)}, WhatsApp ${escapar(data.whatsapp ?? "")}) canceló la asesoría del <strong>${escapar(c)}</strong>.</p><p><strong>${nota}</strong></p><p>Operación de Mercado Pago: ${escapar(data.pago_id ?? "-")}</p><p style="color:#6B7069;font-size:14px">El horario quedó libre otra vez. Respondé este mail para escribirle.</p>`),
    });
    return json({ ok: true, conTiempo });
  }

  // ---------- Nuevo link de pago para una reserva pendiente ----------
  if (body.accion === "pagar") {
    const token = texto(body.token, 40);
    if (!esToken(token)) return json({ error: "El link no es válido." }, 400);
    await liberarVencidas(db);
    const { data: r } = await db.from("reservas").select("*").eq("token", token).maybeSingle();
    if (!r) return json({ error: "No encontramos esa reserva." }, 404);
    if (r.estado === "confirmada") return json({ error: "Esta reserva ya está pagada y confirmada." }, 400);
    if (r.estado !== "pendiente") return json({ error: "Pasó el tiempo para pagar y el horario se liberó. Elegí un horario de nuevo." }, 409);
    const url = await linkDePago(r);
    if (!url) return json({ error: "No se pudo conectar con Mercado Pago. Probá de nuevo en unos minutos." }, 502);
    return json({ url });
  }

  // ---------- Reservar: guarda el horario y devuelve el link de pago ----------
  if (body.accion !== "reservar") return json({ error: "Acción desconocida" }, 400);
  if (texto(body.sitio, 10)) return json({ error: "No pudimos procesar la reserva." }, 400); // campo trampa para robots

  const inicio = texto(body.inicio, 40);
  const nombre = texto(body.nombre, 120);
  const email = texto(body.email, 160).toLowerCase();
  const whatsapp = texto(body.whatsapp, 40);
  const tema = texto(body.tema, 1000);

  if (nombre.length < 2) return json({ error: "Completá tu nombre." }, 400);
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) return json({ error: "Revisá el mail: parece que le falta algo." }, 400);
  if (whatsapp.replace(/\D/g, "").length < 8) return json({ error: "Dejanos un WhatsApp con código de área." }, 400);

  const iso = (() => { try { return new Date(inicio).toISOString(); } catch { return ""; } })();
  if (!iso || !(await libres(db)).includes(iso)) {
    return json({ error: "Ese horario ya no está disponible. Elegí otro, por favor." }, 409);
  }

  const ahora = new Date().toISOString();
  const [{ count: confirmadas }, { count: pendientes }] = await Promise.all([
    db.from("reservas").select("id", { count: "exact", head: true }).eq("email", email).eq("estado", "confirmada").gte("inicio", ahora),
    db.from("reservas").select("id", { count: "exact", head: true }).eq("email", email).eq("estado", "pendiente"),
  ]);
  if ((confirmadas ?? 0) >= MAX_POR_PERSONA) {
    return json({ error: "Ya tenés turnos reservados. Si necesitás otro, escribinos a visionalfa.arg@gmail.com." }, 400);
  }
  if ((pendientes ?? 0) > 0) {
    // Si dejó un pago a medias, se libera ese horario y se toma el nuevo.
    await db.from("reservas").update({ estado: "vencida" }).eq("email", email).eq("estado", "pendiente");
  }

  const vence = new Date(Date.now() + ESPERA_PAGO_MIN * 60e3).toISOString();
  const { data: r, error } = await db.from("reservas")
    .insert({ inicio: iso, nombre, email, whatsapp, tema, estado: "pendiente", vence })
    .select("*").single();
  if (error) {
    if (error.code === "23505") return json({ error: "Alguien acaba de elegir ese horario. Elegí otro, por favor." }, 409);
    console.error(error);
    return json({ error: "No pudimos guardar la reserva. Probá de nuevo." }, 500);
  }

  const url = await linkDePago(r);
  if (!url) {
    await db.from("reservas").update({ estado: "vencida" }).eq("id", r.id);
    return json({ error: "No se pudo conectar con Mercado Pago. Probá de nuevo en unos minutos." }, 502);
  }
  return json({ url, token: r.token, minutos: ESPERA_PAGO_MIN });
});
