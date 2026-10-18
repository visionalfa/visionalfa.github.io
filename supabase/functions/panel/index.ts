// Panel de ventas privado: solo para los mails cargados en la tabla admins.
import { admin, cors, json, usuario } from "../_shared/comun.ts";

const ZONA_OFFSET_H = 3; // Argentina = UTC-3

// deno-lint-ignore no-explicit-any
type Fila = Record<string, any>;

function inicioDiaAR(d = new Date()): Date {
  const ar = new Date(d.getTime() - ZONA_OFFSET_H * 3600e3);
  return new Date(Date.UTC(ar.getUTCFullYear(), ar.getUTCMonth(), ar.getUTCDate()) + ZONA_OFFSET_H * 3600e3);
}

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors });
  const db = admin();
  const user = await usuario(req, db);
  if (!user?.email) return json({ error: "Entrá con tu mail para ver el panel." }, 401);
  const { data: esAdmin } = await db.from("admins").select("email").eq("email", user.email.toLowerCase()).maybeSingle();
  if (!esAdmin) return json({ error: "Este panel es privado." }, 403);

  const [{ data: pagos }, { data: productos }, { data: servicios }, { data: reservas }, { data: accesos }, { data: arrep }] = await Promise.all([
    db.from("pagos").select("id, user_id, producto_id, estado, monto, detalle, creado").order("creado", { ascending: false }).limit(500),
    db.from("productos").select("id, nombre, tipo"),
    db.from("servicios").select("id, nombre, profesional"),
    db.from("reservas").select("inicio, fin, estado, nombre, email, whatsapp, tema, servicio_id, pago_id, monto")
      .eq("estado", "confirmada").gte("fin", new Date().toISOString()).order("inicio").limit(100),
    db.from("accesos").select("producto_id, estado"),
    db.from("arrepentimientos").select("codigo, nombre, email, creado").order("creado", { ascending: false }).limit(20),
  ]);

  const nombreProd = new Map<string, string>();
  (productos ?? []).forEach((p) => nombreProd.set(p.id, p.nombre));
  (servicios ?? []).forEach((s) => nombreProd.set(s.id, `${s.nombre} · ${s.profesional}`));
  nombreProd.set("asesoria", "Reserva de agenda");

  // Mails de compradores
  const ids = [...new Set((pagos ?? []).map((p) => p.user_id).filter(Boolean))];
  const mails = new Map<string, string>();
  await Promise.all(ids.slice(0, 200).map(async (id) => {
    const { data } = await db.auth.admin.getUserById(id);
    if (data?.user?.email) mails.set(id, data.user.email);
  }));
  // Reservas pagadas: nombre del servicio y mail de quien reservó
  const reservaIds = (pagos ?? []).map((p) => p.detalle?.reserva_id).filter(Boolean);
  const infoReserva = new Map<string, Fila>();
  if (reservaIds.length) {
    const { data } = await db.from("reservas").select("id, email, servicio_id").in("id", reservaIds);
    (data ?? []).forEach((r) => infoReserva.set(r.id, r));
  }

  const ventas = (pagos ?? []).filter((p) => p.estado === "approved" && !String(p.producto_id ?? "").startsWith("prueba")).map((p) => {
    const r = p.detalle?.reserva_id ? infoReserva.get(p.detalle.reserva_id) : null;
    const prod = r?.servicio_id ?? p.producto_id;
    return {
      fecha: p.creado,
      producto: nombreProd.get(prod) ?? prod ?? "-",
      producto_id: prod,
      monto: Number(p.monto ?? 0),
      cliente: r?.email ?? (p.user_id ? mails.get(p.user_id) : null) ?? "-",
      operacion: p.id,
    };
  });
  const devueltos = (pagos ?? []).filter((p) => ["refunded", "charged_back", "cancelled"].includes(p.estado)).length;

  const hoy = inicioDiaAR();
  const hace7 = new Date(hoy.getTime() - 6 * 86400e3);
  const ar = new Date(Date.now() - ZONA_OFFSET_H * 3600e3);
  const mes = new Date(Date.UTC(ar.getUTCFullYear(), ar.getUTCMonth(), 1) + ZONA_OFFSET_H * 3600e3);
  const sumar = (desde: Date | null) => {
    const v = ventas.filter((x) => !desde || new Date(x.fecha) >= desde);
    return { cantidad: v.length, total: v.reduce((a, b) => a + b.monto, 0) };
  };

  const porProducto = new Map<string, { producto: string; cantidad: number; total: number }>();
  ventas.forEach((v) => {
    const k = v.producto;
    const e = porProducto.get(k) ?? { producto: k, cantidad: 0, total: 0 };
    e.cantidad++; e.total += v.monto; porProducto.set(k, e);
  });

  // Ventas por día, últimos 30 días (hora de Argentina)
  const dias: { dia: string; total: number; cantidad: number }[] = [];
  for (let i = 29; i >= 0; i--) {
    const d0 = new Date(hoy.getTime() - i * 86400e3), d1 = new Date(d0.getTime() + 86400e3);
    const v = ventas.filter((x) => { const f = new Date(x.fecha); return f >= d0 && f < d1; });
    dias.push({ dia: new Date(d0.getTime() - ZONA_OFFSET_H * 3600e3).toISOString().slice(0, 10), total: v.reduce((a, b) => a + b.monto, 0), cantidad: v.length });
  }

  const { data: usuarios } = await db.auth.admin.listUsers({ page: 1, perPage: 1 });
  const activos = (accesos ?? []).filter((a) => a.estado === "activo");

  return json({
    resumen: { hoy: sumar(hoy), semana: sumar(hace7), mes: sumar(mes), total: sumar(null), devueltos },
    porProducto: [...porProducto.values()].sort((a, b) => b.total - a.total),
    dias,
    ventas: ventas.slice(0, 50),
    reservas: (reservas ?? []).map((r) => ({ ...r, servicio: nombreProd.get(r.servicio_id) ?? r.servicio_id })),
    clientes: {
      cuentas: (usuarios as Fila)?.total ?? null,
      membresias: activos.filter((a) => a.producto_id === "membresia").length,
      vitalicios: activos.filter((a) => a.producto_id === "vitalicio").length,
    },
    arrepentimientos: arrep ?? [],
  });
});
