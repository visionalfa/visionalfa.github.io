// Entrega el contenido de un ebook solo si el cliente tiene acceso
// (lo compró, tiene la membresía activa o el acceso de por vida).
import { admin, cors, json, usuario } from "../_shared/comun.ts";

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

  const { data: archivo, error } = await db.storage.from("ebooks").download(ebook.archivo);
  if (error || !archivo) {
    console.error("storage", error);
    return json({ error: "El ebook no está disponible en este momento" }, 500);
  }
  return json({ html: await archivo.text() });
});
