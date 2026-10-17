// Registra un pedido de arrepentimiento y devuelve el código de trámite.
import { admin, cors, json } from "../_shared/comun.ts";

function texto(v: unknown, max: number): string {
  return typeof v === "string" ? v.trim().slice(0, max) : "";
}

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors });
  if (req.method !== "POST") return json({ error: "Método no permitido" }, 405);

  const body = await req.json().catch(() => ({}));
  const nombre = texto(body.nombre, 120);
  const email = texto(body.email, 160).toLowerCase();
  const operacion = texto(body.operacion, 120);
  const detalle = texto(body.detalle, 1000);

  if (nombre.length < 2) return json({ error: "Completá tu nombre." }, 400);
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) return json({ error: "Revisá el mail: parece que le falta algo." }, 400);

  const letras = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789";
  const azar = crypto.getRandomValues(new Uint8Array(8));
  const codigo = "VA-" + Array.from(azar, (b) => letras[b % letras.length]).join("");

  const { error } = await admin().from("arrepentimientos").insert({ codigo, nombre, email, operacion, detalle });
  if (error) {
    console.error(error);
    return json({ error: "No pudimos registrar el pedido. Probá de nuevo o escribinos a visionalfa.arg@gmail.com." }, 500);
  }
  return json({ codigo });
});
