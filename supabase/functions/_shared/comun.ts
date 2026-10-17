import { createClient, type SupabaseClient, type User } from "npm:@supabase/supabase-js@2.49.4";

export const SITE_URL = Deno.env.get("SITE_URL") ?? "https://visionalfa.github.io";
const SUPABASE_URL = Deno.env.get("SUPABASE_URL")!;
const SERVICE_ROLE = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;

export const cors = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
};

export function json(body: unknown, status = 200): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { ...cors, "Content-Type": "application/json; charset=utf-8" },
  });
}

/** Cliente con permisos de servidor: solo se usa dentro de las funciones. */
export function admin(): SupabaseClient {
  return createClient(SUPABASE_URL, SERVICE_ROLE, {
    auth: { persistSession: false, autoRefreshToken: false },
  });
}

/** Devuelve el usuario que inició sesión, a partir del token que manda la web. */
export async function usuario(req: Request, db: SupabaseClient): Promise<User | null> {
  const token = (req.headers.get("Authorization") ?? "").replace(/^Bearer\s+/i, "");
  if (!token) return null;
  const { data, error } = await db.auth.getUser(token);
  if (error) return null;
  return data.user;
}

/** Llamada a la API de Mercado Pago con el token secreto del vendedor. */
export async function mp(path: string, init: RequestInit = {}): Promise<Response> {
  const token = Deno.env.get("MP_ACCESS_TOKEN");
  if (!token) throw new Error("Falta configurar MP_ACCESS_TOKEN");
  return await fetch(`https://api.mercadopago.com${path}`, {
    ...init,
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
      ...(init.headers ?? {}),
    },
  });
}
