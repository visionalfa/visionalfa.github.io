// Actividad real de la web para el cartelito de la portada.
// Solo datos agregados y anónimos: nunca nombres, mails ni ciudades.
import { admin, cors, json } from "../_shared/comun.ts";

const DIA = 86400e3;
const MIN_VISITAS = 5;   // por debajo de esto no se muestra el número
const MIN_TESTS = 3;

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors });
  const db = admin();
  const ahora = Date.now();
  // Hoy desde la medianoche de Argentina (UTC-3)
  const hoyAR = new Date(ahora - 3 * 3600e3);
  const desdeHoy = new Date(Date.UTC(hoyAR.getUTCFullYear(), hoyAR.getUTCMonth(), hoyAR.getUTCDate()) + 3 * 3600e3).toISOString();
  const desdeSemana = new Date(ahora - 7 * DIA).toISOString();

  const [pagos, productos, vistasHoy, tests] = await Promise.all([
    db.from("pagos").select("producto_id, creado").eq("estado", "approved").gte("creado", new Date(ahora - 14 * DIA).toISOString())
      .order("creado", { ascending: false }).limit(10),
    db.from("productos").select("id, nombre").eq("activo", true),
    db.from("visitas").select("sesion").eq("evento", "vista").gte("creada", desdeHoy).limit(5000),
    db.from("visitas").select("sesion").eq("evento", "clic").like("detalle", "test:%").gte("creada", desdeSemana).limit(5000),
  ]);

  const nombres = new Map((productos.data ?? []).map((p) => [p.id, p.nombre]));
  const compras = (pagos.data ?? [])
    .filter((p) => p.producto_id && nombres.has(p.producto_id))
    .map((p) => ({ producto: nombres.get(p.producto_id), hace: Math.max(1, Math.round((ahora - new Date(p.creado).getTime()) / 60e3)) }));

  const visitantesHoy = new Set((vistasHoy.data ?? []).map((v) => v.sesion)).size;
  const testsSemana = new Set((tests.data ?? []).map((v) => v.sesion)).size;

  return new Response(JSON.stringify({
    compras,
    visitantesHoy: visitantesHoy >= MIN_VISITAS ? visitantesHoy : null,
    testsSemana: testsSemana >= MIN_TESTS ? testsSemana : null,
  }), { headers: { ...cors, "Content-Type": "application/json; charset=utf-8", "Cache-Control": "public, max-age=120" } });
});
