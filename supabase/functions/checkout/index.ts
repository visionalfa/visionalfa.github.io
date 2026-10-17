// Crea el pago en Mercado Pago para el producto elegido y devuelve el link para pagar.
import { admin, cors, json, mp, SITE_URL, usuario } from "../_shared/comun.ts";

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors });
  if (req.method !== "POST") return json({ error: "Método no permitido" }, 405);

  const db = admin();
  const user = await usuario(req, db);
  if (!user?.email) return json({ error: "Iniciá sesión para comprar" }, 401);

  const { producto } = await req.json().catch(() => ({ producto: null }));
  const { data: p } = await db
    .from("productos")
    .select("id, nombre, tipo, precio")
    .eq("id", producto)
    .eq("activo", true)
    .maybeSingle();
  if (!p) return json({ error: "Ese producto no existe" }, 400);

  const referencia = `${user.id}|${p.id}`;
  const vuelta = `${SITE_URL}/cuenta.html`;
  const webhook = `${Deno.env.get("SUPABASE_URL")}/functions/v1/mp-webhook`;

  try {
    if (p.tipo === "membresia") {
      // Suscripción con cobro automático todos los meses.
      const r = await mp("/preapproval", {
        method: "POST",
        body: JSON.stringify({
          reason: p.nombre,
          external_reference: referencia,
          payer_email: user.email,
          back_url: `${vuelta}?pago=suscripcion`,
          status: "pending",
          auto_recurring: {
            frequency: 1,
            frequency_type: "months",
            transaction_amount: Number(p.precio),
            currency_id: "ARS",
          },
        }),
      });
      const data = await r.json();
      if (!r.ok || !data.init_point) {
        console.error("preapproval", r.status, data);
        return json({ error: "No se pudo crear la suscripción. Probá de nuevo en unos minutos." }, 502);
      }
      return json({ url: data.init_point });
    }

    // Pago único: ebook suelto o acceso de por vida.
    const r = await mp("/checkout/preferences", {
      method: "POST",
      body: JSON.stringify({
        items: [{ id: p.id, title: p.nombre, quantity: 1, unit_price: Number(p.precio), currency_id: "ARS" }],
        payer: { email: user.email },
        external_reference: referencia,
        back_urls: {
          success: `${vuelta}?pago=ok`,
          pending: `${vuelta}?pago=pendiente`,
          failure: `${vuelta}?pago=error`,
        },
        auto_return: "approved",
        notification_url: webhook,
        statement_descriptor: "VISION ALFA",
      }),
    });
    const data = await r.json();
    if (!r.ok || !data.init_point) {
      console.error("preference", r.status, data);
      return json({ error: "No se pudo crear el pago. Probá de nuevo en unos minutos." }, 502);
    }
    return json({ url: data.init_point });
  } catch (e) {
    console.error(e);
    return json({ error: "No se pudo conectar con Mercado Pago" }, 502);
  }
});
