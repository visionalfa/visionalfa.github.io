// Agenda del equipo. El turno se confirma recién cuando Mercado Pago aprueba el pago.
// GET  ?servicio=id        → datos del servicio y turnos libres de las próximas semanas
// GET  ?servicios=1        → lista de servicios activos
// GET  ?token=...          → estado de una reserva (vuelta del pago y página de cancelación)
// POST {accion:"reservar"} → guarda el horario unos minutos y devuelve el link de pago
// POST {accion:"pagar"}    → nuevo link de pago para una reserva pendiente
// POST {accion:"cancelar"} → cancela con el token que llega en el mail
import { admin, cors, json, mp, SITE_URL } from "../_shared/comun.ts";
import { AVISOS, enviar, escapar, plantilla } from "../_shared/mail.ts";
import { confirmarIncluida, cuando, ESPERA_PAGO_MIN, liberarVencidas, mailProfesional } from "../_shared/reservas.ts";

const OFFSET_AR = 3;                   // Argentina = UTC-3, sin horario de verano
const ANTICIPACION_MS = 24 * 3600e3;   // mínimo un día de anticipación
const DIAS_ADELANTE = 21;              // cuántos días se muestran
const MAX_POR_PERSONA = 3;             // reservas futuras por mail y por servicio
const CAMPOS_SERVICIO = "id, agenda, profesional, nombre, descripcion, precio, duracion, hora_desde, hora_hasta, dias, modalidad, incluye_ebook, reuniones_incluidas";

type DB = ReturnType<typeof admin>;
// deno-lint-ignore no-explicit-any
type Fila = Record<string, any>;

function texto(v: unknown, max: number): string {
  return typeof v === "string" ? v.trim().slice(0, max) : "";
}
const esToken = (t: string) => /^[0-9a-f-]{36}$/i.test(t);

async function servicio(db: DB, id: string): Promise<Fila | null> {
  if (!/^[a-z0-9-]{1,60}$/.test(id)) return null;
  const { data } = await db.from("servicios").select(CAMPOS_SERVICIO).eq("id", id).eq("activo", true).maybeSingle();
  return data;
}

/** Turnos posibles del servicio (sin mirar si están ocupados). */
function turnosPosibles(s: Fila, bloqueados: Set<string>): { inicio: number; fin: number }[] {
  const ahora = Date.now();
  const hoyAR = new Date(ahora - OFFSET_AR * 3600e3);
  const base = Date.UTC(hoyAR.getUTCFullYear(), hoyAR.getUTCMonth(), hoyAR.getUTCDate());
  const dias: number[] = s.dias ?? [1, 2, 3, 4, 5];
  const salida: { inicio: number; fin: number }[] = [];
  for (let d = 0; d <= DIAS_ADELANTE; d++) {
    const dia = base + d * 86400e3;
    if (!dias.includes(new Date(dia).getUTCDay())) continue;
    const fecha = new Date(dia).toISOString().slice(0, 10);
    if (bloqueados.has(fecha)) continue;
    for (let h = s.hora_desde; h + s.duracion <= s.hora_hasta; h++) {
      const inicio = dia + (h + OFFSET_AR) * 3600e3;
      if (inicio - ahora >= ANTICIPACION_MS) salida.push({ inicio, fin: inicio + s.duracion * 3600e3 });
    }
  }
  return salida;
}

async function libres(db: DB, s: Fila): Promise<string[]> {
  await liberarVencidas(db);
  const [{ data: bloq }, { data: ocup }] = await Promise.all([
    db.from("dias_bloqueados").select("fecha").in("agenda", ["", s.agenda]),
    db.from("reservas").select("inicio, fin").eq("agenda", s.agenda)
      .in("estado", ["pendiente", "confirmada"]).gte("fin", new Date().toISOString()),
  ]);
  const bloqueados = new Set((bloq ?? []).map((b) => String(b.fecha)));
  const ocupados = (ocup ?? []).map((r) => [new Date(r.inicio).getTime(), new Date(r.fin).getTime()]);
  return turnosPosibles(s, bloqueados)
    .filter((t) => !ocupados.some(([i, f]) => t.inicio < f && i < t.fin))
    .map((t) => new Date(t.inicio).toISOString());
}

let ultimoErrorMP = "";
async function linkDePago(r: Fila, s: Fila): Promise<string | null> {
  const vuelta = `${SITE_URL}/agenda.html?r=${r.token}`;
  const res = await mp("/checkout/preferences", {
    method: "POST",
    body: JSON.stringify({
      items: [{
        id: s.id,
        title: `${s.nombre} · ${s.profesional} · ${cuando(r.inicio)}`.slice(0, 250),
        quantity: 1,
        unit_price: Number(s.precio),
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
    console.error("preference reserva", res.status, data);
    ultimoErrorMP = `${res.status} ${data.message ?? ""}`.slice(0, 200);
    return null;
  }
  return data.init_point;
}

function publico(s: Fila) {
  const { agenda: _a, ...resto } = s;
  return resto;
}

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors });
  const db = admin();

  if (req.method === "GET") {
    const q = new URL(req.url).searchParams;
    const token = q.get("token");
    if (token) {
      if (!esToken(token)) return json({ error: "El link no es válido." }, 400);
      await liberarVencidas(db);
      const { data } = await db.from("reservas")
        .select("inicio, estado, nombre, email, vence, servicio_id, monto, servicios(nombre, profesional, duracion, incluye_ebook, reuniones_incluidas)")
        .eq("token", token).maybeSingle();
      if (!data) return json({ error: "No encontramos esa reserva." }, 404);
      return json({ ...data, cuando: cuando(data.inicio) });
    }
    if (q.get("servicios")) {
      const { data } = await db.from("servicios").select(CAMPOS_SERVICIO).eq("activo", true).order("orden");
      return json({ servicios: (data ?? []).map(publico) });
    }
    const s = await servicio(db, q.get("servicio") ?? "asesoria");
    if (!s) return json({ error: "Ese servicio no existe." }, 404);
    return json({ servicio: publico(s), turnos: await libres(db, s) });
  }

  if (req.method !== "POST") return json({ error: "Método no permitido" }, 405);
  const body = await req.json().catch(() => ({}));

  // ---------- Cancelar (desde el mail de confirmación) ----------
  if (body.accion === "cancelar") {
    const token = texto(body.token, 40);
    if (!esToken(token)) return json({ error: "El link no es válido." }, 400);
    const { data } = await db.from("reservas").select("*, servicios(nombre, profesional)").eq("token", token).maybeSingle();
    if (!data) return json({ error: "No encontramos esa reserva." }, 404);
    if (data.estado !== "confirmada") return json({ ok: true, ya: true });
    if (new Date(data.inicio).getTime() < Date.now()) return json({ error: "Ese turno ya pasó." }, 400);
    const conTiempo = new Date(data.inicio).getTime() - Date.now() >= 24 * 3600e3;
    const incluida = !data.pago_id && !Number(data.monto);
    await db.from("reservas").update({ estado: "cancelada" }).eq("id", data.id);
    const c = cuando(data.inicio);
    const sv = data.servicios ?? {};
    const nota = incluida
      ? "Era una reunión incluida en su acompañamiento: no hay pago para devolver."
      : conTiempo
      ? "Canceló con más de 24 horas: corresponde devolverle el pago o pasarla a otro horario."
      : "Canceló con menos de 24 horas de anticipación.";
    await enviar({
      para: AVISOS, responderA: data.email,
      asunto: `Turno cancelado: ${sv.profesional ?? ""} · ${data.nombre} · ${c}`,
      texto: `${data.nombre} (${data.email}, WhatsApp ${data.whatsapp}) canceló "${sv.nombre}" con ${sv.profesional} del ${c}.\n${nota}\nOperación de Mercado Pago: ${data.pago_id ?? "-"}\nEl horario quedó libre otra vez.`,
      html: plantilla("Se canceló un turno", `<p><strong>${escapar(data.nombre)}</strong> (${escapar(data.email)}, WhatsApp ${escapar(data.whatsapp ?? "")}) canceló <strong>${escapar(sv.nombre ?? "")}</strong> con ${escapar(sv.profesional ?? "")} del <strong>${escapar(c)}</strong>.</p><p><strong>${nota}</strong></p><p>Operación de Mercado Pago: ${escapar(data.pago_id ?? "-")}</p><p style="color:#6B7069;font-size:14px">El horario quedó libre otra vez. Respondé este mail para escribirle.</p>`),
    });
    const profMail = await mailProfesional(db, data.agenda);
    if (profMail) {
      await enviar({
        para: profMail, responderA: data.email,
        asunto: `Sesión cancelada: ${data.nombre} · ${c}`,
        texto: `${data.nombre} canceló la sesión de "${sv.nombre}" del ${c}. El horario quedó libre otra vez en tu agenda.`,
        html: plantilla("Se canceló una sesión", `<p><strong>${escapar(data.nombre)}</strong> canceló la sesión de <strong>${escapar(sv.nombre ?? "")}</strong> del <strong>${escapar(c)}</strong>.</p><p>El horario quedó libre otra vez en tu agenda.</p>`),
      });
    }
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
    const s = await servicio(db, r.servicio_id);
    if (!s) return json({ error: "Ese servicio ya no está disponible." }, 409);
    const url = await linkDePago(r, s);
    if (!url) return json({ error: "No se pudo conectar con Mercado Pago. Probá de nuevo en unos minutos.", detalle: ultimoErrorMP }, 502);
    return json({ url });
  }

  // ---------- Reservar: guarda el horario y devuelve el link de pago ----------
  if (body.accion !== "reservar") return json({ error: "Acción desconocida" }, 400);
  if (texto(body.sitio, 10)) return json({ error: "No pudimos procesar la reserva." }, 400); // campo trampa para robots

  const s = await servicio(db, texto(body.servicio, 60) || "asesoria");
  if (!s) return json({ error: "Ese servicio no existe." }, 400);
  const inicio = texto(body.inicio, 40);
  const nombre = texto(body.nombre, 120);
  const email = texto(body.email, 160).toLowerCase();
  const whatsapp = texto(body.whatsapp, 40);
  const tema = texto(body.tema, 1000);

  if (nombre.length < 2) return json({ error: "Completá tu nombre." }, 400);
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) return json({ error: "Revisá el mail: parece que le falta algo." }, 400);
  if (whatsapp.replace(/\D/g, "").length < 8) return json({ error: "Dejanos un WhatsApp con código de área." }, 400);

  const iso = (() => { try { return new Date(inicio).toISOString(); } catch { return ""; } })();
  if (!iso || !(await libres(db, s)).includes(iso)) {
    return json({ error: "Ese horario ya no está disponible. Elegí otro, por favor." }, 409);
  }

  const ahora = new Date().toISOString();
  const { count: confirmadas } = await db.from("reservas").select("id", { count: "exact", head: true })
    .eq("email", email).eq("servicio_id", s.id).eq("estado", "confirmada").gte("inicio", ahora);
  if ((confirmadas ?? 0) >= MAX_POR_PERSONA) {
    return json({ error: "Ya tenés varios turnos reservados. Si necesitás otro, escribinos a visionalfa.arg@gmail.com." }, 400);
  }
  // Acompañamiento ya pagado: las próximas reuniones se confirman sin cobrar de nuevo.
  let yaPago = false;
  if (s.reuniones_incluidas) {
    const { count } = await db.from("reservas").select("id", { count: "exact", head: true })
      .eq("email", email).eq("servicio_id", s.id).eq("estado", "confirmada").not("pago_id", "is", null);
    yaPago = (count ?? 0) > 0;
  }

  // Si dejó un pago a medias en esta agenda, se libera ese horario y se toma el nuevo.
  await db.from("reservas").update({ estado: "vencida" }).eq("email", email).eq("agenda", s.agenda).eq("estado", "pendiente");

  const vence = new Date(Date.now() + ESPERA_PAGO_MIN * 60e3).toISOString();
  const fin = new Date(new Date(iso).getTime() + s.duracion * 3600e3).toISOString();
  const { data: r, error } = await db.from("reservas")
    .insert({ inicio: iso, fin, servicio_id: s.id, agenda: s.agenda, nombre, email, whatsapp, tema, estado: "pendiente", vence })
    .select("*").single();
  if (error) {
    if (error.code === "23P01" || error.code === "23505") {
      return json({ error: "Alguien acaba de elegir ese horario. Elegí otro, por favor." }, 409);
    }
    console.error(error);
    return json({ error: "No pudimos guardar la reserva. Probá de nuevo." }, 500);
  }

  if (yaPago) {
    const ok = await confirmarIncluida(db, r.id);
    if (!ok) return json({ error: "No pudimos confirmar la reunión. Probá de nuevo." }, 500);
    return json({ incluida: true, token: r.token });
  }

  const url = await linkDePago(r, s);
  if (!url) {
    await db.from("reservas").update({ estado: "vencida" }).eq("id", r.id);
    return json({ error: "No se pudo conectar con Mercado Pago. Probá de nuevo en unos minutos.", detalle: ultimoErrorMP }, 502);
  }
  return json({ url, token: r.token, minutos: ESPERA_PAGO_MIN });
});
