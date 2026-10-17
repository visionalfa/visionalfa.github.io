// Cifra un ebook para publicarlo protegido: solo el sistema (con la clave privada guardada en Supabase) puede abrirlo.
// Uso: node herramientas/cifrar-ebook.mjs ruta/al/ebook.html nombre-del-archivo.html
import { readFileSync, writeFileSync } from "node:fs";
import crypto from "node:crypto";

const [, , entrada, nombre] = process.argv;
if (!entrada || !nombre) {
  console.error("Uso: node herramientas/cifrar-ebook.mjs ruta/al/ebook.html nombre-del-archivo.html");
  process.exit(1);
}
const publica = crypto.createPublicKey(readFileSync(new URL("../ebooks/clave-publica.pem", import.meta.url)));
const clave = crypto.randomBytes(32);
const iv = crypto.randomBytes(12);
const cifrador = crypto.createCipheriv("aes-256-gcm", clave, iv);
const datos = Buffer.concat([cifrador.update(readFileSync(entrada)), cifrador.final(), cifrador.getAuthTag()]);
const claveCifrada = crypto.publicEncrypt(
  { key: publica, padding: crypto.constants.RSA_PKCS1_OAEP_PADDING, oaepHash: "sha256" },
  clave,
);
const salida = new URL(`../ebooks/${nombre}.enc.json`, import.meta.url);
writeFileSync(salida, JSON.stringify({ v: 1, k: claveCifrada.toString("base64"), iv: iv.toString("base64"), data: datos.toString("base64") }));
console.log("Listo:", salida.pathname);
