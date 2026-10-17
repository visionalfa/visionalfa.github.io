// Abre un ebook cifrado con herramientas/cifrar-ebook.mjs usando la clave privada guardada en Supabase.
function base64(texto: string): Uint8Array {
  return Uint8Array.from(atob(texto), (c) => c.charCodeAt(0));
}

let clavePrivada: CryptoKey | null = null;

async function obtenerClave(): Promise<CryptoKey> {
  if (clavePrivada) return clavePrivada;
  const pem = Deno.env.get("EBOOKS_PRIVATE_KEY");
  if (!pem) throw new Error("Falta EBOOKS_PRIVATE_KEY");
  const der = base64(pem.replace(/-----[^-]+-----/g, "").replace(/\s+/g, ""));
  clavePrivada = await crypto.subtle.importKey("pkcs8", der, { name: "RSA-OAEP", hash: "SHA-256" }, false, ["decrypt"]);
  return clavePrivada;
}

export async function descifrar(sobre: { k: string; iv: string; data: string }): Promise<string> {
  const privada = await obtenerClave();
  const claveAes = await crypto.subtle.decrypt({ name: "RSA-OAEP" }, privada, base64(sobre.k));
  const aes = await crypto.subtle.importKey("raw", claveAes, { name: "AES-GCM" }, false, ["decrypt"]);
  const texto = await crypto.subtle.decrypt({ name: "AES-GCM", iv: base64(sobre.iv) }, aes, base64(sobre.data));
  return new TextDecoder().decode(texto);
}
