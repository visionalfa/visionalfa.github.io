// Lógica compartida de la agenda: horarios, mails y confirmación por pago.
import type { SupabaseClient } from "npm:@supabase/supabase-js@2.49.4";
import { SITE_URL } from "./comun.ts";
import { AVISOS, enviar, escapar, plantilla } from "./mail.ts";

export const PRECIO_ASESORIA = 60000;
export const ESPERA_PAGO_MIN = 30;      // minutos que se guarda el horario mientras pagan
export const ZONA = "America/Argentina/Buenos_Aires";

export function cuando(iso: string): string {
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

/** Pasa a "vencida" las reservas pendientes cuyo tiempo para pagar terminó. */
export async function liberarVencidas(db: SupabaseClient) {
  await db.from("reservas").update({ estado: "vencida" })
    .eq("estado", "pendiente").lt("vence", new Date().toISOString());
}

// deno-lint-ignore no-explicit-any
type Reserva = Record<string, any>;

/**
 * Se llama cuando Mercado Pago aprueba el pago de una reserva.
 * Devuelve true si la reserva quedó confirmada.
 */
export async function confirmarPorPago(db: SupabaseClient, reservaId: string, pagoId: string, monto: number): Promise<boolean> {
  const { data: r } = await db.from("reservas").select("*").eq("id", reservaId).maybeSingle();
  if (!r) return false;
  if (r.estado === "confirmada" || r.estado === "pagada_sin_turno") return r.estado === "confirmada"; // aviso repetido

  // Si venció mientras pagaba, se confirma igual si el horario sigue libre.
  const { error } = await db.from("reservas")
    .update({ estado: "confirmada", pago_id: pagoId, monto })
    .eq("id", reservaId).in("estado", ["pendiente", "vencida", "cancelada"]);

  if (error) {
    // El horario lo tomó otra persona (índice único): queda pagada sin turno.
    await db.from("reservas").update({ estado: "pagada_sin_turno", pago_id: pagoId, monto }).eq("id", reservaId);
    await avisoSinTurno(r, pagoId);
    return false;
  }
  await mailsConfirmacion({ ...r, pago_id: pagoId, monto });
  return true;
}

/** Si devuelven o desconocen el pago, se libera el horario. */
export async function anularPorDevolucion(db: SupabaseClient, reservaId: string) {
  await db.from("reservas").update({ estado: "cancelada" }).eq("id", reservaId).in("estado", ["confirmada", "pendiente"]);
}

async function mailsConfirmacion(r: Reserva) {
  const c = cuando(r.inicio);
  const linkCancelar = `${SITE_URL}/agenda.html?cancelar=${r.token}`;
  const wa = String(r.whatsapp ?? "").replace(/\D/g, "");
  const monto = Number(r.monto ?? PRECIO_ASESORIA).toLocaleString("es-AR");

  await enviar({
    para: AVISOS, responderA: r.email,
    asunto: `Nueva asesoría pagada: ${r.nombre} · ${c}`,
    texto: `Nueva asesoría reservada y pagada\n\nCuándo: ${c}\nNombre: ${r.nombre}\nMail: ${r.email}\nWhatsApp: ${r.whatsapp}\nPago: $${monto} (Mercado Pago, operación ${r.pago_id})\nTema: ${r.tema || "(no indicó)"}\n\nRespondé este mail para mandarle el link de la videollamada.`,
    html: plantilla("Nueva asesoría reservada y pagada", `
<p style="font-size:18px;margin:0 0 16px"><strong>${escapar(c)}</strong> · 1 hora</p>
<p style="margin:0"><strong>Nombre:</strong> ${escapar(r.nombre)}<br><strong>Mail:</strong> ${escapar(r.email)}<br>
<strong>WhatsApp:</strong> <a href="https://wa.me/${wa}">${escapar(r.whatsapp ?? "")}</a><br>
<strong>Pago:</strong> $${monto} · Mercado Pago, operación ${escapar(String(r.pago_id))}</p>
<p><strong>Tema:</strong><br>${escapar(r.tema || "(no indicó)").replace(/\n/g, "<br>")}</p>
<p style="color:#6B7069;font-size:14px">Respondé este mail para mandarle el link de la videollamada. El archivo adjunto lo agrega a tu calendario.</p>`),
    ics: ics(r.id, r.inicio, `Asesoría con ${r.nombre}`, `Mail: ${r.email} · WhatsApp: ${r.whatsapp}\nTema: ${r.tema ?? ""}`),
  });

  await enviar({
    para: r.email,
    asunto: `Tu asesoría con Visión Alfa: ${c}`,
    texto: `Hola, ${r.nombre}:\n\nRecibimos tu pago y tu asesoría quedó confirmada para el ${c} (hora de Argentina). Dura 1 hora y es por videollamada.\n\nAntes del encuentro te escribimos con el link de la videollamada.\n\nSi no podés asistir, cancelá con al menos 24 horas de anticipación desde acá: ${linkCancelar}\n\n¡Nos vemos!\nVisión Alfa`,
    html: plantilla("¡Tu asesoría está confirmada!", `
<p>Hola, ${escapar(r.nombre)}:</p>
<p>Recibimos tu pago. Te esperamos el:</p>
<p style="font-size:18px"><strong>${escapar(c)}</strong> (hora de Argentina)<br>1 hora · videollamada</p>
<p>Antes del encuentro te escribimos con el link de la videollamada. El archivo adjunto lo agrega a tu calendario.</p>
<p>Si no podés asistir, <a href="${linkCancelar}" style="color:#1F3D2B">cancelá desde acá</a> con al menos 24 horas de anticipación y te devolvemos el pago o te pasamos a otro horario.</p>
<p>¡Nos vemos!<br>Visión Alfa</p>`),
    ics: ics(r.id, r.inicio, "Asesoría Visión Alfa", "Videollamada de 1 hora. El link llega por mail."),
  });
}

async function avisoSinTurno(r: Reserva, pagoId: string) {
  const c = cuando(r.inicio);
  await enviar({
    para: AVISOS, responderA: r.email,
    asunto: `Atención: pago recibido sin turno · ${r.nombre}`,
    texto: `${r.nombre} (${r.email}, WhatsApp ${r.whatsapp}) pagó la asesoría del ${c}, pero el pago llegó cuando el horario ya lo había tomado otra persona. Operación de Mercado Pago: ${pagoId}. Escribile para pasarla a otro horario o devolverle el pago.`,
    html: plantilla("Pago recibido sin turno", `<p><strong>${escapar(r.nombre)}</strong> (${escapar(r.email)}, WhatsApp ${escapar(r.whatsapp ?? "")}) pagó la asesoría del <strong>${escapar(c)}</strong>, pero el pago llegó cuando el horario ya lo había tomado otra persona.</p><p>Operación de Mercado Pago: ${escapar(pagoId)}.</p><p>Escribile para pasarla a otro horario o devolverle el pago.</p>`),
  });
  await enviar({
    para: r.email,
    asunto: "Recibimos tu pago: coordinemos tu asesoría",
    texto: `Hola, ${r.nombre}:\n\nRecibimos tu pago, pero el horario del ${c} se ocupó mientras pagabas. Te vamos a escribir para elegir otro horario o devolverte el dinero, como prefieras.\n\nVisión Alfa`,
    html: plantilla("Recibimos tu pago", `<p>Hola, ${escapar(r.nombre)}:</p><p>Recibimos tu pago, pero el horario del <strong>${escapar(c)}</strong> se ocupó mientras pagabas.</p><p>Te vamos a escribir para elegir otro horario o devolverte el dinero, como prefieras.</p><p>Visión Alfa</p>`),
  });
}
