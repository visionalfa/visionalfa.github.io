# Carrusel de láminas 1080x1350. Uso: python3 herramientas/carrusel-plantilla.py <salida>
# Carrusel "Diccionario de IA" (1080x1350 por lámina)
from playwright.sync_api import sync_playwright
import sys
def logo(a='#F4F3EE', b='#E3A82B', w=66):
    return f'<svg width="{w}" height="{int(w*.75)}" viewBox="0 8 64 48"><path d="M4 14 L17 50 L30 14" fill="none" stroke="{a}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/><path d="M34 50 L47 14 L60 50" fill="none" stroke="{b}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/></svg>'
CSS='''*{margin:0;box-sizing:border-box}body{width:1080px;height:1350px;overflow:hidden;font-family:Inter,sans-serif}
.p{width:1080px;height:1350px;padding:84px 90px;display:flex;flex-direction:column;position:relative}
.verde{background:#1F3D2B;color:#F4F3EE}.papel{background:#F4F3EE;color:#16231B}.mostaza{background:#E3A82B;color:#1F3D2B}
.top{display:flex;justify-content:space-between;align-items:center}
.marca{display:flex;align-items:center;gap:16px;font-family:'Inter Display';font-weight:800;font-size:34px;letter-spacing:-.02em}
.n{font-weight:700;font-size:28px;opacity:.6}
.eye{font-weight:700;letter-spacing:.14em;text-transform:uppercase;font-size:28px;color:#E3A82B;margin-top:auto}
.papel .eye{color:#C98F17}
h1{font-family:'Inter Display';font-weight:800;letter-spacing:-.035em;line-height:1;font-size:118px;margin-top:20px}
h1 em{font-style:normal;color:#E3A82B}
.papel h1{color:#1F3D2B}
.term{font-family:'Inter Display';font-weight:800;letter-spacing:-.035em;font-size:112px;line-height:1;color:#1F3D2B;margin-top:120px}
.pron{font-size:30px;color:#4A5A50;margin-top:14px;font-weight:500}
.def{font-size:46px;line-height:1.32;margin-top:46px;color:#16231B}
.def b{color:#1F3D2B}
.ej{margin-top:auto;background:#fff;border:2px solid #DAD8CF;border-left:12px solid #E3A82B;border-radius:24px;padding:32px 38px;font-size:34px;line-height:1.38;color:#16231B}
.ej span{display:block;font-weight:700;font-size:24px;letter-spacing:.12em;text-transform:uppercase;color:#C98F17;margin-bottom:8px}
.sub{font-size:40px;line-height:1.35;margin-top:34px;opacity:.9}
.desliza{margin-top:auto;display:flex;justify-content:space-between;align-items:center;font-size:32px;font-weight:600}
.pill{background:#E3A82B;color:#1F3D2B;border-radius:999px;padding:18px 34px;font-weight:800;font-size:32px}
.mostaza .pill{background:#1F3D2B;color:#F4F3EE}
.lista{margin-top:46px;display:flex;flex-wrap:wrap;gap:16px}
.lista span{border:2px solid rgba(244,243,238,.35);border-radius:999px;padding:12px 26px;font-size:32px;font-weight:600}
'''
def top(cls, i, n):
    a,b = (('#1F3D2B','#F4F3EE') if cls=='mostaza' else (('#1F3D2B','#E3A82B') if cls=='papel' else ('#F4F3EE','#E3A82B')))
    return f'<div class="top"><div class="marca">{logo(a,b)}visión alfa</div><div class="n">{i}/{n}</div></div>'
def tapa(parte, terminos):
    chips=''.join(f'<span>{t}</span>' for t in terminos)
    return ('verde', f'<div class="eye">Parte {parte} · Guardalo 📌</div><h1>Diccionario<br>de IA para<br><em>emprendedores</em></h1><div class="lista">{chips}</div><div class="desliza"><span>Sin palabras raras, prometido</span><span class="pill">Deslizá →</span></div>')
def termino(t, pron, d, ej):
    return ('papel', f'<div class="term">{t}</div>' + (f'<div class="pron">{pron}</div>' if pron else '') + f'<p class="def">{d}</p><div class="ej"><span>En tu negocio</span>{ej}</div>')
def cierre(txt):
    return ('mostaza', f'<div class="eye" style="color:#1F3D2B">¿Te sirvió?</div><h1 style="font-size:100px">{txt}</h1><p class="sub">Aprendé a usar la IA para vender más, con más de 40 prompts listos, en el ebook <b>“IA para vender más”</b>.</p><div class="desliza"><span>Link en la bio</span><span class="pill">Guardalo 📌</span></div>')
CARR = {
 'parte1': [
  tapa(1, ['IA generativa','Prompt','Contexto','Chatbot','Alucinación']),
  termino('IA generativa','', 'Inteligencia artificial que <b>crea contenido nuevo</b>: textos, imágenes, audio o video. ChatGPT, Claude y Gemini son ejemplos.', 'Te escribe la descripción de un producto, un mail para un cliente o las ideas para tus publicaciones del mes.'),
  termino('Prompt','', 'La <b>instrucción que le das a la IA</b>. Cuanto más clara y completa, mejor es la respuesta.', '❌ “Escribime un post”<br>✅ “Escribime un post para Instagram de mi panadería en Neuquén, tono cercano, sobre la promo de facturas de los martes.”'),
  termino('Contexto','', 'La <b>información que le das a la IA antes de pedirle algo</b>: qué vendés, a quién, dónde y con qué tono.', 'Armá una “ficha de tu negocio” y pegala al principio de cada chat. La diferencia en las respuestas es enorme.'),
  termino('Chatbot','', 'Un programa con el que <b>conversás por mensajes</b>. Puede ser una IA o un sistema de respuestas armadas.', 'Responde las preguntas de siempre (horarios, envíos, precios) en tu web o tu WhatsApp, a cualquier hora.'),
  termino('Alucinación','', 'Cuando la IA <b>inventa un dato y lo dice con total seguridad</b>. No miente a propósito: completa lo que no sabe.', 'Revisá siempre precios, fechas, leyes y datos antes de publicar algo que escribió la IA.'),
  cierre('Ahora sí,<br>que no te agarre<br><em style="font-style:normal;color:#F4F3EE">desprevenido</em>'),
 ],
 'parte2': [
  tapa(2, ['Modelo de lenguaje','Automatización','Agente de IA','Plantilla de prompt','Sesgo']),
  termino('Modelo de lenguaje','también “LLM”', 'El <b>“cerebro” detrás de ChatGPT, Claude o Gemini</b>. Aprendió de muchísimos textos y por eso puede escribir, resumir y responder.', 'No necesitás entender cómo funciona por dentro: con saber pedirle bien, alcanza.'),
  termino('Automatización','', 'Hacer que una <b>tarea se haga sola</b>, sin que tengas que estar vos.', 'Un mail de confirmación cuando alguien compra, un recordatorio de turno o tus publicaciones programadas.'),
  termino('Agente de IA','', 'Una IA que <b>no solo responde: hace tareas por vos</b> en varios pasos, como buscar información, completar un formulario o mandar un mensaje.', 'Le pedís “armame las publicaciones de la semana y programalas” y lo hace de punta a punta.'),
  termino('Plantilla de prompt','', 'Un prompt armado con <b>espacios para completar</b> que reusás cada vez.', '“Escribime la descripción de [producto], que cuesta [precio], para [tipo de cliente], en tono [tono].”'),
  termino('Sesgo','', 'La IA puede <b>repetir ideas generales o prejuicios</b> de los textos de los que aprendió.', 'Si te sugiere algo que no encaja con tu cliente o con tu zona, corregilo: vos conocés tu negocio mejor que nadie.'),
  cierre('Ya hablás<br>el idioma<br><em style="font-style:normal;color:#F4F3EE">de la IA</em> 🤖'),
 ],
}
out=sys.argv[1]
with sync_playwright() as pw:
    b=pw.chromium.launch(); p=b.new_page(viewport={'width':1080,'height':1350})
    for k,slides in CARR.items():
        n=len(slides)
        for i,(cls,body) in enumerate(slides,1):
            p.set_content(f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="p {cls}">{top(cls,i,n)}{body}</div></body></html>'); p.wait_for_timeout(150)
            p.screenshot(path=f'{out}/{k}-{i}.png')
    b.close()
print('ok')
