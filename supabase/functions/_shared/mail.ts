// Envío de mails desde la cuenta de Gmail de la marca (contraseña de aplicación).
import nodemailer from "npm:nodemailer@6.9.16";

export const REMITENTE = "visionalfa.arg@gmail.com";
/** A dónde llegan los avisos internos (reservas, cancelaciones, arrepentimientos). */
export const AVISOS = Deno.env.get("AVISOS_EMAIL") ?? REMITENTE;

let transporte: ReturnType<typeof nodemailer.createTransport> | null = null;

function smtp() {
  if (transporte) return transporte;
  const clave = (Deno.env.get("GMAIL_APP_PASSWORD") ?? "").replace(/\s/g, "");
  if (!clave) throw new Error("Falta configurar GMAIL_APP_PASSWORD");
  transporte = nodemailer.createTransport({
    host: "smtp.gmail.com",
    port: 465,
    secure: true,
    auth: { user: REMITENTE, pass: clave },
  });
  return transporte;
}

export interface Mail {
  para: string;
  asunto: string;
  html: string;
  texto: string;
  responderA?: string;
  ics?: string;
}

export async function enviar(m: Mail): Promise<boolean> {
  try {
    await smtp().sendMail({
      from: { name: "Visión Alfa", address: REMITENTE },
      to: m.para,
      replyTo: m.responderA,
      subject: m.asunto,
      text: m.texto,
      html: m.html,
      icalEvent: m.ics ? { method: "PUBLISH", filename: "asesoria.ics", content: m.ics } : undefined,
    });
    return true;
  } catch (e) {
    console.error("No se pudo enviar el mail:", e);
    return false;
  }
}

export function escapar(s: string): string {
  return s.replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]!));
}

/** Plantilla simple con la estética de la marca. */
export function plantilla(titulo: string, cuerpo: string): string {
  return `<!doctype html><html lang="es"><body style="margin:0;background:#F4F3EE;font-family:Arial,Helvetica,sans-serif;color:#1C2B22">
<div style="max-width:560px;margin:0 auto;padding:28px 20px">
<div style="background:#1F3D2B;color:#F4F3EE;border-radius:16px 16px 0 0;padding:18px 24px;font-weight:bold;font-size:20px">
<span style="color:#F4F3EE">V</span><span style="color:#E3A82B">Λ</span>&nbsp; visión alfa</div>
<div style="background:#FFFFFF;border-radius:0 0 16px 16px;padding:24px;line-height:1.6;font-size:16px">
<h1 style="font-size:22px;color:#1F3D2B;margin:0 0 14px">${titulo}</h1>
${cuerpo}
</div>
<p style="font-size:13px;color:#6B7069;text-align:center;margin-top:18px">Visión Alfa · visionalfa.github.io</p>
</div></body></html>`;
}
