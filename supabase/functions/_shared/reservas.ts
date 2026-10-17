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

function ics(id: string, inicio: string, resumen: string, detalle: string, horas = 1): string {
  const f = (d: Date) => d.toISOString().replace(/[-:]/g, "").replace(/\.\d{3}/, "");
  const ini = new Date(inicio);
  const fin = new Date(ini.getTime() + horas * 3600e3);
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
  const { data: r } = await db.from("reservas").select("*, servicios(*)").eq("id", reservaId).maybeSingle();
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
  const conEbook = r.servicios?.incluye_ebook ? await darEbook(db, r.email, r.servicios.incluye_ebook, pagoId) : false;
  await mailsConfirmacion({ ...r, pago_id: pagoId, monto }, conEbook);
  return true;
}

/** Habilita un ebook al mail de la reserva (crea la cuenta si todavía no existe). */
async function darEbook(db: SupabaseClient, email: string, productoId: string, pagoId: string): Promise<boolean> {
  try {
    let userId: string | null = null;
    const nuevo = await db.auth.admin.createUser({ email, email_confirm: true });
    if (nuevo.data?.user) userId = nuevo.data.user.id;
    else {
      // Ya tenía cuenta: se busca por mail.
      for (let page = 1; page <= 20 && !userId; page++) {
        const { data } = await db.auth.admin.listUsers({ page, perPage: 200 });
        const u = data?.users?.find((x) => (x.email ?? "").toLowerCase() === email.toLowerCase());
        if (u) userId = u.id;
        if (!data?.users?.length || data.users.length < 200) break;
      }
    }
    if (!userId) return false;
    const { error } = await db.from("accesos").upsert(
      { user_id: userId, producto_id: productoId, estado: "activo", mp_referencia: `reserva_${pagoId}`, actualizado: new Date().toISOString() },
      { onConflict: "mp_referencia" },
    );
    return !error;
  } catch (e) {
    console.error("darEbook", e);
    return false;
  }
}

/** Si devuelven o desconocen el pago, se libera el horario (y se quita el ebook incluido). */
export async function anularPorDevolucion(db: SupabaseClient, reservaId: string) {
  const { data: r } = await db.from("reservas").select("pago_id").eq("id", reservaId).maybeSingle();
  await db.from("reservas").update({ estado: "cancelada" }).eq("id", reservaId).in("estado", ["confirmada", "pendiente"]);
  if (r?.pago_id) await db.from("accesos").update({ estado: "inactivo" }).eq("mp_referencia", `reserva_${r.pago_id}`);
}

async function mailsConfirmacion(r: Reserva, conEbook: boolean) {
  const sv = r.servicios ?? {};
  const prof = sv.profesional ?? "Visión Alfa";
  const nombreSv = sv.nombre ?? "Asesoría";
  const horas = Number(sv.duracion ?? 1);
  const dur = horas === 1 ? "1 hora" : `${horas} horas`;
  const c = cuando(r.inicio);
  const linkCancelar = `${SITE_URL}/agenda.html?cancelar=${r.token}`;
  const wa = String(r.whatsapp ?? "").replace(/\D/g, "");
  const monto = Number(r.monto ?? sv.precio ?? PRECIO_ASESORIA).toLocaleString("es-AR");
  const ebookTxt = conEbook
    ? `Ya tenés habilitado el ebook incluido: entrá a ${SITE_URL}/cuenta.html con este mail para leerlo.`
    : "";

  await enviar({
    para: AVISOS, responderA: r.email,
    asunto: `Nueva reserva pagada · ${prof} · ${r.nombre} · ${c}`,
    texto: `Nueva reserva pagada\n\nServicio: ${nombreSv} (${dur})\nCon: ${prof}\nCuándo: ${c}\nNombre: ${r.nombre}\nMail: ${r.email}\nWhatsApp: ${r.whatsapp}\nPago: $${monto} (Mercado Pago, operación ${r.pago_id})\nTema: ${r.tema || "(no indicó)"}${conEbook ? "\nEbook incluido: habilitado" : ""}\n\nRespondé este mail para mandarle el link de la videollamada.`,
    html: plantilla("Nueva reserva pagada", `
<p style="font-size:18px;margin:0 0 6px"><strong>${escapar(c)}</strong> · ${dur}</p>
<p style="margin:0 0 16px">${escapar(nombreSv)} · con <strong>${escapar(prof)}</strong></p>
<p style="margin:0"><strong>Nombre:</strong> ${escapar(r.nombre)}<br><strong>Mail:</strong> ${escapar(r.email)}<br>
<strong>WhatsApp:</strong> <a href="https://wa.me/${wa}">${escapar(r.whatsapp ?? "")}</a><br>
<strong>Pago:</strong> $${monto} · Mercado Pago, operación ${escapar(String(r.pago_id))}${conEbook ? "<br><strong>Ebook incluido:</strong> habilitado" : ""}</p>
<p><strong>Tema:</strong><br>${escapar(r.tema || "(no indicó)").replace(/\n/g, "<br>")}</p>
<p style="color:#6B7069;font-size:14px">Respondé este mail para mandarle el link de la videollamada. El archivo adjunto lo agrega a tu calendario.</p>`),
    ics: ics(r.id, r.inicio, `${nombreSv} con ${r.nombre}`, `Profesional: ${prof}\nMail: ${r.email} · WhatsApp: ${r.whatsapp}\nTema: ${r.tema ?? ""}`, horas),
  });

  await enviar({
    para: r.email,
    asunto: `Tu turno con ${prof}: ${c}`,
    texto: `Hola, ${r.nombre}:\n\nRecibimos tu pago y tu turno quedó confirmado.\n\n${nombreSv} con ${prof}\n${c} (hora de Argentina) · ${dur}\n\nAntes del encuentro te escribimos con el link de la videollamada.\n${ebookTxt}\n\nSi no podés asistir, cancelá con al menos 24 horas de anticipación desde acá: ${linkCancelar}\n\n¡Nos vemos!\nVisión Alfa`,
    html: plantilla("¡Tu turno está confirmado!", `
<p>Hola, ${escapar(r.nombre)}:</p>
<p>Recibimos tu pago. Te esperamos el:</p>
<p style="font-size:18px"><strong>${escapar(c)}</strong> (hora de Argentina)<br>${escapar(nombreSv)} con ${escapar(prof)} · ${dur}</p>
<p>Antes del encuentro te escribimos con el link de la videollamada. El archivo adjunto lo agrega a tu calendario.</p>
${conEbook ? `<p style="background:#F4F3EE;border-radius:12px;padding:14px 16px"><strong>Tu ebook ya está habilitado.</strong> Entrá a <a href="${SITE_URL}/cuenta.html" style="color:#1F3D2B">Mi cuenta</a> con este mail para leerlo.</p>` : ""}
<p>Si no podés asistir, <a href="${linkCancelar}" style="color:#1F3D2B">cancelá desde acá</a> con al menos 24 horas de anticipación y te devolvemos el pago o te pasamos a otro horario.</p>
<p>¡Nos vemos!<br>Visión Alfa</p>`),
    ics: ics(r.id, r.inicio, `${nombreSv} · Visión Alfa`, `Con ${prof}. Videollamada de ${dur}. El link llega por mail.`, horas),
  });
}

async function avisoSinTurno(r: Reserva, pagoId: string) {
  const c = cuando(r.inicio);
  await enviar({
    para: AVISOS, responderA: r.email,
    asunto: `Atención: pago recibido sin turno · ${r.servicios?.profesional ?? ""} · ${r.nombre}`,
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
