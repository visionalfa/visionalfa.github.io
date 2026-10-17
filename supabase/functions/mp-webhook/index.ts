// Recibe los avisos de Mercado Pago y da o quita accesos según corresponda.
// Nunca confía en los datos del aviso: siempre consulta el pago real en la API de Mercado Pago.
import { admin, json, mp } from "../_shared/comun.ts";

async function firmaValida(req: Request, dataId: string | null): Promise<boolean> {
  const secreto = Deno.env.get("MP_WEBHOOK_SECRET");
  if (!secreto) return true; // Sin clave configurada no se puede verificar (solo para pruebas iniciales).
  const firma = req.headers.get("x-signature") ?? "";
  // Algunos avisos llegan sin firma. No es un riesgo: igual se consulta el pago real en Mercado Pago.
  if (!firma) return true;
  const requestId = req.headers.get("x-request-id") ?? "";
  const partes = Object.fromEntries(
    firma.split(",").map((p) => p.trim().split("=", 2) as [string, string]),
  );
  const ts = partes["ts"];
  const v1 = partes["v1"];
  if (!ts || !v1) return false;

  let manifiesto = "";
  if (dataId) manifiesto += `id:${/^[a-z0-9]+$/i.test(dataId) ? dataId.toLowerCase() : dataId};`;
  if (requestId) manifiesto += `request-id:${requestId};`;
  manifiesto += `ts:${ts};`;

  const clave = await crypto.subtle.importKey(
    "raw",
    new TextEncoder().encode(secreto),
    { name: "HMAC", hash: "SHA-256" },
    false,
    ["sign"],
  );
  const bytes = new Uint8Array(await crypto.subtle.sign("HMAC", clave, new TextEncoder().encode(manifiesto)));
  const calculada = Array.from(bytes).map((b) => b.toString(16).padStart(2, "0")).join("");
  if (calculada.length !== v1.length) return false;
  let diferencia = 0;
  for (let i = 0; i < calculada.length; i++) diferencia |= calculada.charCodeAt(i) ^ v1.charCodeAt(i);
  return diferencia === 0;
}

function separarReferencia(ref: string | null | undefined): { userId: string | null; productoId: string | null } {
  const [userId, productoId] = (ref ?? "").split("|");
  const esUuid = /^[0-9a-f-]{36}$/i.test(userId ?? "");
  return { userId: esUuid ? userId : null, productoId: productoId || null };
}

Deno.serve(async (req) => {
  if (req.method !== "POST") return json({ ok: true });

  const url = new URL(req.url);
  const body = await req.json().catch(() => ({}));
  const tipo: string | null = body?.type ?? url.searchParams.get("type") ?? url.searchParams.get("topic");
  const dataIdUrl = url.searchParams.get("data.id") ?? url.searchParams.get("id");
  const dataId: string | null = dataIdUrl ?? (body?.data?.id != null ? String(body.data.id) : null);

  if (!(await firmaValida(req, dataIdUrl ?? dataId))) {
    console.warn("Firma inválida", { tipo, dataId });
    return json({ error: "firma inválida" }, 401);
  }
  if (!tipo || !dataId) return json({ ok: true });

  const db = admin();
  const ahora = new Date().toISOString();

  try {
    if (tipo === "payment") {
      const r = await mp(`/v1/payments/${encodeURIComponent(dataId)}`);
      if (!r.ok) {
        console.error("payment", r.status, await r.text());
        return json({ error: "no se pudo consultar el pago" }, 500); // Mercado Pago reintenta
      }
      const pago = await r.json();
      const { userId, productoId } = separarReferencia(pago.external_reference);

      await db.from("pagos").upsert({
        id: String(pago.id),
        user_id: userId,
        producto_id: productoId,
        estado: pago.status,
        monto: pago.transaction_amount,
        detalle: {
          status_detail: pago.status_detail,
          payment_type: pago.payment_type_id,
          preapproval_id: pago.metadata?.preapproval_id ?? pago.point_of_interaction?.transaction_data?.subscription_id ?? null,
        },
        actualizado: ahora,
      });

      // Los cobros mensuales de la membresía se manejan con el aviso de la suscripción.
      const { data: producto } = productoId
        ? await db.from("productos").select("tipo").eq("id", productoId).maybeSingle()
        : { data: null };
      if (!userId || !producto || producto.tipo === "membresia") return json({ ok: true });

      const referencia = `pago_${pago.id}`;
      if (pago.status === "approved") {
        await db.from("accesos").upsert(
          {
            user_id: userId,
            // Cualquier producto de tipo "de por vida" da el acceso completo.
            producto_id: producto.tipo === "vitalicio" ? "vitalicio" : productoId,
            estado: "activo",
            mp_referencia: referencia,
            actualizado: ahora,
          },
          { onConflict: "mp_referencia" },
        );
      } else if (["refunded", "charged_back", "cancelled"].includes(pago.status)) {
        await db.from("accesos").update({ estado: "inactivo", actualizado: ahora }).eq("mp_referencia", referencia);
      }
      return json({ ok: true });
    }

    if (tipo === "subscription_preapproval" || tipo === "preapproval") {
      const r = await mp(`/preapproval/${encodeURIComponent(dataId)}`);
      if (!r.ok) {
        console.error("preapproval", r.status, await r.text());
        return json({ error: "no se pudo consultar la suscripción" }, 500);
      }
      const sub = await r.json();
      const { userId } = separarReferencia(sub.external_reference);
      if (!userId) return json({ ok: true });

      // authorized = activa y cobrándose. paused / cancelled = sin acceso.
      const estado = sub.status === "authorized" ? "activo" : "inactivo";
      if (sub.status === "pending") return json({ ok: true }); // todavía no terminó de suscribirse
      await db.from("accesos").upsert(
        { user_id: userId, producto_id: "membresia", estado, mp_referencia: `sub_${sub.id}`, actualizado: ahora },
        { onConflict: "mp_referencia" },
      );
      return json({ ok: true });
    }

    return json({ ok: true });
  } catch (e) {
    console.error(e);
    return json({ error: "error interno" }, 500);
  }
});
