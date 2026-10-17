// Entrega el contenido de un ebook solo si el cliente tiene acceso
// (lo compró, tiene la membresía activa o el acceso de por vida).
// Los ebooks se publican cifrados en la web y solo esta función puede abrirlos.
import { admin, cors, json, SITE_URL, usuario } from "../_shared/comun.ts";
import { descifrar } from "../_shared/descifrar.ts";

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors });

  const db = admin();
  const user = await usuario(req, db);
  if (!user) return json({ error: "Iniciá sesión para leer" }, 401);

  const libro = new URL(req.url).searchParams.get("libro") ?? "";
  const { data: ebook } = await db
    .from("productos")
    .select("id, archivo")
    .eq("id", libro)
    .eq("tipo", "ebook")
    .maybeSingle();
  if (!ebook?.archivo) return json({ error: "Ese ebook no existe" }, 404);

  const { data: accesos } = await db
    .from("accesos")
    .select("id")
    .eq("user_id", user.id)
    .eq("estado", "activo")
    .in("producto_id", [ebook.id, "membresia", "vitalicio"])
    .limit(1);
  if (!accesos?.length) return json({ error: "Todavía no tenés acceso a este ebook" }, 403);

  try {
    // Se agrega la fecha para leer siempre la última versión publicada.
    const r = await fetch(`${SITE_URL}/ebooks/${encodeURIComponent(ebook.archivo)}.enc.json?v=${Date.now()}`);
    if (!r.ok) throw new Error(`No se encontró el archivo (${r.status})`);
    const html = await descifrar(await r.json());
    return json({ html });
  } catch (e) {
    console.error("ebook", e);
    return json({ error: "El ebook no está disponible en este momento. Probá de nuevo en unos minutos." }, 500);
  }
});
