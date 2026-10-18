// Registra una visita o un clic, de forma anónima.
import { admin, cors, json } from "../_shared/comun.ts";

const corto = (v: unknown, n: number) => (typeof v === "string" ? v.slice(0, n) : null);

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors });
  if (req.method !== "POST") return json({ ok: true });
  const b = await req.json().catch(() => ({}));
  const evento = b.evento === "clic" ? "clic" : "vista";
  const ua = req.headers.get("user-agent") ?? "";
  if (/bot|crawler|spider|preview|facebookexternalhit|headless/i.test(ua)) return json({ ok: true });
  await admin().from("visitas").insert({
    evento,
    pagina: corto(b.pagina, 80),
    origen: corto(b.origen, 40),
    dispositivo: b.dispositivo === "celular" ? "celular" : "compu",
    sesion: corto(b.sesion, 40),
    detalle: corto(b.detalle, 80),
  });
  return json({ ok: true });
});
