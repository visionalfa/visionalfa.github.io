// Agenda de asesorías.
// GET                      → turnos libres de las próximas semanas
// GET  ?token=...          → datos de una reserva (para la página de cancelación)
// POST {accion:"reservar"} → reserva un turno y avisa por mail
// POST {accion:"cancelar"} → cancela con el token que llega en el mail
import { admin, cors, json, SITE_URL } from "../_shared/comun.ts";
import { AVISOS, enviar, escapar, plantilla } from "../_shared/mail.ts";

const HORAS = [17, 18, 19];            // inicio de cada turno de 1 hora (hora de Argentina)
const OFFSET_AR = 3;                   // Argentina = UTC-3, sin horario de verano
const ANTICIPACION_MS = 24 * 3600e3;   // mínimo un día de anticipación
const DIAS_ADELANTE = 21;              // cuántos días se muestran
const MAX_POR_PERSONA = 2;             // reservas futuras por mail
const ZONA = "America/Argentina/Buenos_Aires";

function texto(v: unknown, max: number): string {
  return typeof v === "string" ? v.trim().slice(0, max) : "";
}

/** Todos los turnos posibles (sin mirar si están ocupados). */
function turnosPosibles(bloqueados: Set<string>): string[] {
  const ahora = Date.now();
  const hoyAR = new Date(ahora - OFFSET_AR * 3600e3); // "reloj" argentino expresado en UTC
  const base = Date.UTC(hoyAR.getUTCFullYear(), hoyAR.getUTCMonth(), hoyAR.getUTCDate());
  const salida: string[] = [];
  for (let d = 0; d <= DIAS_ADELANTE; d++) {
    const dia = new Date(base + d * 86400e3);
    const sem = dia.getUTCDay(); // 0 domingo … 6 sábado
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

async function libres(db: ReturnType<typeof admin>): Promise<string[]> {
  const [{ data: bloq }, { data: ocup }] = await Promise.all([
    db.from("dias_bloqueados").select("fecha"),
    db.from("reservas").select("inicio").eq("estado", "confirmada").gte("inicio", new Date().toISOString()),
  ]);
  const bloqueados = new Set((bloq ?? []).map((b) => String(b.fecha)));
  const ocupados = new Set((ocup ?? []).map((r) => new Date(r.inicio).toISOString()));
  return turnosPosibles(bloqueados).filter((t) => !ocupados.has(t));
}

function cuando(iso: string): string {
  const f = new Date(iso);
  const dia = new Intl.DateTimeFormat("es-AR", { timeZone: ZONA, weekday: "long", day: "numeric", month: "long" }).format(f);
  const hora = new Intl.DateTimeFormat("es-AR", { timeZone: ZONA, hour: "2-digit", minute: "2-digit", hour12: false }).format(f);
  return `${dia} a las ${hora} hs`;
}

function ics(id: string, inicio: string, resumen: string, detalle: string): string {
  const f = (d: Date) => d.toISOString().replace(/[-:]/g, "").replace(/\.\d{3}/, "");
  const ini = new Date(inicio);
  const fin = new Date(ini.getTime() + 3600e3);
  const limpio = (s: string) => s.replace(/[\\;,]/g, (c) => "\\" + c).replace(/\r?\n/g, "\\n");
  return [
    "BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Vision Alfa//Agenda//ES", "METHOD:PUBLISH",
    "BEGIN:VEVENT", `UID:${id}@visionalfa`, `DTSTAMP:${f(new Date())}`, `DTSTART:${f(ini)}`, `DTEND:${f(fin)}`,
    `SUMMARY:${limpio(resumen)}`, `DESCRIPTION:${limpio(detalle)}`, "END:VEVENT", "END:VCALENDAR",
  ].join("\r\n");
}

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors });
  const db = admin();

  if (req.method === "GET") {
    const token = new URL(req.url).searchParams.get("token");
    if (token) {
      if (!/^[0-9a-f-]{36}$/i.test(token)) return json({ error: "El link no es válido." }, 400);
      const { data } = await db.from("reservas").select("inicio, estado, nombre").eq("token", token).maybeSingle();
      if (!data) return json({ error: "No encontramos esa reserva." }, 404);
      return json({ inicio: data.inicio, estado: data.estado, nombre: data.nombre, cuando: cuando(data.inicio) });
    }
    return json({ turnos: await libres(db) });
  }

  if (req.method !== "POST") return json({ error: "Método no permitido" }, 405);
  const body = await req.json().catch(() => ({}));

  // ---------- Cancelar ----------
  if (body.accion === "cancelar") {
    const token = texto(body.token, 40);
    if (!/^[0-9a-f-]{36}$/i.test(token)) return json({ error: "El link no es válido." }, 400);
    const { data } = await db.from("reservas").select("*").eq("token", token).maybeSingle();
    if (!data) return json({ error: "No encontramos esa reserva." }, 404);
    if (data.estado === "cancelada") return json({ ok: true, ya: true });
    if (new Date(data.inicio).getTime() < Date.now()) return json({ error: "Ese turno ya pasó." }, 400);
    await db.from("reservas").update({ estado: "cancelada" }).eq("id", data.id);
    const c = cuando(data.inicio);
    await enviar({
      para: AVISOS, responderA: data.email,
      asunto: `Turno cancelado: ${data.nombre} · ${c}`,
      texto: `${data.nombre} (${data.email}) canceló la asesoría del ${c}. El horario quedó libre otra vez.`,
      html: plantilla("Se canceló un turno", `<p><strong>${escapar(data.nombre)}</strong> (${escapar(data.email)}) canceló la asesoría del <strong>${escapar(c)}</strong>.</p><p>El horario quedó libre otra vez en la agenda.</p>`),
    });
    return json({ ok: true });
  }

  // ---------- Reservar ----------
  if (body.accion !== "reservar") return json({ error: "Acción desconocida" }, 400);
  if (texto(body.sitio, 10)) return json({ ok: true }); // campo trampa para robots

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

  const { count } = await db.from("reservas").select("id", { count: "exact", head: true })
    .eq("email", email).eq("estado", "confirmada").gte("inicio", new Date().toISOString());
  if ((count ?? 0) >= MAX_POR_PERSONA) {
    return json({ error: "Ya tenés turnos reservados. Si necesitás otro, escribinos a visionalfa.arg@gmail.com." }, 400);
  }

  const { data: r, error } = await db.from("reservas")
    .insert({ inicio: iso, nombre, email, whatsapp, tema }).select("id, token").single();
  if (error) {
    if (error.code === "23505") return json({ error: "Alguien acaba de reservar ese horario. Elegí otro, por favor." }, 409);
    console.error(error);
    return json({ error: "No pudimos guardar la reserva. Probá de nuevo." }, 500);
  }

  const c = cuando(iso);
  const linkCancelar = `${SITE_URL}/agenda.html?cancelar=${r.token}`;
  const wa = whatsapp.replace(/\D/g, "");

  // Aviso para Visión Alfa
  const avisado = await enviar({
    para: AVISOS, responderA: email,
    asunto: `Nueva reserva: ${nombre} · ${c}`,
    texto: `Nueva asesoría reservada\n\nCuándo: ${c}\nNombre: ${nombre}\nMail: ${email}\nWhatsApp: ${whatsapp}\nTema: ${tema || "(no indicó)"}\n\nRespondé este mail para escribirle directamente y mandale el link de la videollamada.`,
    html: plantilla("Nueva asesoría reservada", `
<p style="font-size:18px;margin:0 0 16px"><strong>${escapar(c)}</strong> · 1 hora</p>
<p style="margin:0"><strong>Nombre:</strong> ${escapar(nombre)}<br><strong>Mail:</strong> ${escapar(email)}<br>
<strong>WhatsApp:</strong> <a href="https://wa.me/${wa}">${escapar(whatsapp)}</a></p>
<p><strong>Tema:</strong><br>${escapar(tema || "(no indicó)").replace(/\n/g, "<br>")}</p>
<p style="color:#6B7069;font-size:14px">Respondé este mail para escribirle directamente y mandale el link de la videollamada. El archivo adjunto lo agrega a tu calendario.</p>`),
    ics: ics(r.id, iso, `Asesoría con ${nombre}`, `Mail: ${email} · WhatsApp: ${whatsapp}\nTema: ${tema}`),
  });

  // Confirmación para quien reservó
  await enviar({
    para: email,
    asunto: `Tu asesoría con Visión Alfa: ${c}`,
    texto: `Hola, ${nombre}:\n\nTu asesoría quedó reservada para el ${c} (hora de Argentina). Dura 1 hora y es por videollamada.\n\nAntes del encuentro te escribimos con el link de la videollamada y los datos para el pago.\n\nSi no podés asistir, cancelá desde acá para liberar el horario: ${linkCancelar}\n\n¡Nos vemos!\nVisión Alfa`,
    html: plantilla("¡Tu asesoría quedó reservada!", `
<p>Hola, ${escapar(nombre)}:</p>
<p style="font-size:18px"><strong>${escapar(c)}</strong> (hora de Argentina)<br>1 hora · videollamada</p>
<p>Antes del encuentro te escribimos con el link de la videollamada y los datos para el pago. El archivo adjunto lo agrega a tu calendario.</p>
<p>Si no podés asistir, <a href="${linkCancelar}" style="color:#1F3D2B">cancelá desde acá</a> para liberar el horario.</p>
<p>¡Nos vemos!<br>Visión Alfa</p>`),
    ics: ics(r.id, iso, "Asesoría Visión Alfa", "Videollamada de 1 hora. El link llega por mail."),
  });

  return json({ ok: true, cuando: c, avisado });
});
