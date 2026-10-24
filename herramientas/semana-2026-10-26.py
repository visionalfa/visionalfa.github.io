# Contenido de la semana del 26/10 al 1/11/2026: posts, historias y reels con ilustraciones.
# Uso: python3 herramientas/semana-2026-10-26.py <carpeta_salida>
# Genera los archivos con el nombre final que van en redes/ (AAAA-MM-DD-...).
from playwright.sync_api import sync_playwright
import sys, os, base64, subprocess, tempfile
sys.path.insert(0, os.path.dirname(__file__))
from ilustraciones import ILU

OUT = sys.argv[1]
REDES = os.path.join(os.path.dirname(__file__), '..', 'redes')

def logo(a='#F4F3EE', b='#E3A82B', w=64):
    return f'<svg width="{w}" height="{int(w*.75)}" viewBox="0 8 64 48"><path d="M4 14 L17 50 L30 14" fill="none" stroke="{a}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/><path d="M34 50 L47 14 L60 50" fill="none" stroke="{b}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/></svg>'

def marca(cls):
    a, b = {'verde': ('#F4F3EE', '#E3A82B'), 'papel': ('#1F3D2B', '#E3A82B'), 'mostaza': ('#1F3D2B', '#F4F3EE')}[cls]
    return f'<div class="marca">{logo(a, b)}visión alfa</div>'

def ilu(nombre, w, estilo=''):
    return f'<div class="ilu" style="{estilo}">{ILU[nombre](w)}</div>'

def foto(path, ancho=600, alto=750):
    # Marcador: la imagen se incrusta al renderizar (puede ser un post que se genera en este mismo script)
    return f'<div class="post" style="width:{ancho}px;height:{alto}px"><img src="@@{path}@@"></div>'

def incrustar(html):
    import re
    def r(m):
        path = m.group(1); ext = 'jpeg' if path.endswith('.jpg') else 'png'
        return f'data:image/{ext};base64,' + base64.b64encode(open(path, 'rb').read()).decode()
    return re.sub(r'@@(.+?)@@', r, html)

COMUN = '''*{box-sizing:border-box;margin:0}
body{font-family:Inter,sans-serif;overflow:hidden}
.verde{background:#1F3D2B;color:#F4F3EE}.papel{background:#F4F3EE;color:#16231B}.mostaza{background:#E3A82B;color:#1F3D2B}
.marca{display:flex;align-items:center;gap:16px;font-family:'Inter Display';font-weight:800;font-size:36px;letter-spacing:-.02em}
.eye{font-weight:700;letter-spacing:.14em;text-transform:uppercase;font-size:30px;color:#E3A82B}
.papel .eye{color:#C98F17}.mostaza .eye{color:#1F3D2B}
h1{font-family:'Inter Display';font-weight:800;letter-spacing:-.035em;line-height:1.0;margin-top:22px}
h1 em{font-style:normal;color:#E3A82B}.papel h1{color:#1F3D2B}.papel h1 em{color:#C98F17}.mostaza h1 em{color:#F4F3EE}
.sub{line-height:1.35;opacity:.92}
.caja{border-radius:32px;padding:38px 44px;line-height:1.35}
.verde .caja{background:rgba(244,243,238,.08);border:2px solid rgba(244,243,238,.2)}
.papel .caja{background:#fff;border:2px solid #DAD8CF}
.mostaza .caja{background:rgba(31,61,43,.08);border:2px solid rgba(31,61,43,.25)}
.caja b{color:#E3A82B}.papel .caja b{color:#C98F17}.mostaza .caja b{color:#1F3D2B}
.lista{display:flex;flex-direction:column}
.it{display:flex;gap:24px;align-items:flex-start;line-height:1.3}
.it i{flex:none;font-style:normal;border-radius:50%;background:#E3A82B;color:#1F3D2B;display:flex;align-items:center;justify-content:center;font-family:'Inter Display';font-weight:800}
.papel .it i,.mostaza .it i{background:#1F3D2B;color:#E3A82B}
.it small{display:block;opacity:.75;font-size:.78em;margin-top:4px}
.pill{background:#E3A82B;color:#1F3D2B;border-radius:999px;font-weight:800}
.papel .pill,.mostaza .pill{background:#1F3D2B;color:#F4F3EE}
.ilu svg{display:block}
.post{border-radius:28px;overflow:hidden;box-shadow:0 30px 70px rgba(0,0,0,.35);align-self:center;transform:rotate(-2deg)}
.post img{width:100%;height:100%;display:block;object-fit:cover}
'''

# ---------- POSTS 1080x1350 ----------
CSS_POST = COMUN + '''body{width:1080px;height:1350px}
.p{width:1080px;height:1350px;padding:84px 86px;display:flex;flex-direction:column;position:relative}
.eye{margin-top:44px} h1{font-size:92px}
.sub{font-size:36px;margin-top:26px;max-width:880px}
.lista{gap:20px;margin-top:36px} .it{font-size:34px} .it i{width:56px;height:56px;font-size:26px}
.pie{margin-top:auto;display:flex;justify-content:space-between;align-items:center;font-size:28px;font-weight:600}
.pill{padding:18px 32px;font-size:28px}
.ilu{position:absolute;right:60px;top:56px}
'''
POSTS = {
'2026-10-27-post-precios': ('papel', f'''{ilu('etiqueta', 330)}
<div class="eye" style="margin-top:230px">Antes de poner un precio</div>
<h1>Hacé esta<br><em>cuenta</em> primero</h1>
<div class="lista">
<div class="it"><i>1</i><span>Lo que te cuesta el producto<small>Materia prima o mercadería</small></span></div>
<div class="it"><i>2</i><span>Los gastos que se olvidan<small>Packaging, envío y comisión de cobro</small></span></div>
<div class="it"><i>3</i><span>Tu tiempo<small>Sí, también cuenta</small></span></div>
<div class="it"><i>4</i><span>La ganancia que querés que te quede</span></div>
</div>
<p class="sub" style="font-size:32px;margin-top:30px">Recién ahí mirá a la competencia, para saber dónde estás parado.</p>
<div class="pie" style="color:#1F3D2B"><span>Ebook N.º 4</span><span class="pill">Precios que dejan ganancia</span></div>'''),
'2026-10-29-post-whatsapp': ('verde', f'''{ilu('celular', 340, 'top:40px')}
<div class="eye" style="margin-top:250px">Guardalo 📌</div>
<h1>Te preguntan<br>el precio por<br><em>WhatsApp</em></h1>
<p class="sub">No respondas solo el número. Armalo en 3 partes:</p>
<div class="lista">
<div class="it"><i>$</i><span>El precio, claro y sin vueltas</span></div>
<div class="it"><i>+</i><span>Qué incluye: envío, cuotas, garantía</span></div>
<div class="it"><i>→</i><span>Un próximo paso: “¿Te lo reservo?”</span></div>
</div>
<div class="pie"><span>Ebook N.º 5</span><span class="pill">Vender por WhatsApp e Instagram</span></div>'''),
'2026-10-30-post-comercios': ('mostaza', f'''{ilu('comercio', 330)}
<div class="eye" style="margin-top:250px">Lo que veo en la calle</div>
<h1 style="font-size:84px">4 cosas que mira<br>un <em>comercio</em><br>antes de comprarte</h1>
<div class="lista">
<div class="it"><i>1</i><span>Un precio mayorista claro y por escrito</span></div>
<div class="it"><i>2</i><span>Cuánto le queda a él al revenderlo</span></div>
<div class="it"><i>3</i><span>Que cumplas fechas, cantidades y calidad</span></div>
<div class="it"><i>4</i><span>Que reponer sea fácil: pedido mínimo y entrega</span></div>
</div>
<div class="pie"><span>Ebook N.º 6</span><span class="pill">Cómo venderle a comercios</span></div>'''),
}

# ---------- HISTORIAS 1080x1920 ----------
# Zonas seguras: ~250px libres arriba y abajo. Sin stickers: cada historia lleva la info completa (pedido de Flor).
CSS_H = COMUN + '''body{width:1080px;height:1920px}
.s{width:1080px;height:1920px;padding:330px 90px 300px;display:flex;flex-direction:column;justify-content:center;position:relative}
.s>.marca{position:absolute;left:90px;top:250px}
.eye{margin-top:40px;font-size:32px} h1{font-size:100px}
.sub{font-size:42px;margin-top:34px}
.caja{margin-top:44px;font-size:40px}
.lista{gap:28px;margin-top:44px} .it{font-size:40px} .it i{width:64px;height:64px;font-size:30px}
.cta{margin-top:56px;align-self:flex-start;padding:26px 44px;font-size:38px}
.pista{margin-top:46px;font-size:36px;font-weight:600;opacity:.75}
.ilu{align-self:center;margin-top:30px}
.post{margin-top:44px}
'''
def hueco(txt, h=380):
    return f'<p class="pista">{txt}</p><div style="height:{h}px"></div>'

def lista(items):
    return '<div class="lista">' + ''.join(f'<div class="it"><i>{n}</i><span>{t}</span></div>' for n, t in items) + '</div>'

def cta(t):
    return f'<div class="pill cta">{t}</div>'

# (clave, fondo, html). Las claves llevan fecha y letra del horario (a, b, c, d).
HIST = [
# Lunes 26
('2026-10-26-a-historia-semana', 'papel', f'''{ilu('checklist', 465)}<div class="eye">Esta semana en el perfil</div><h1>Lo que se<br><em>viene</em> 👇</h1>
''' + lista([('L', 'Diccionario de IA · parte 2'), ('M', 'Cómo poner precios'), ('M', 'Cómo pedirle bien a la IA'), ('J', 'Qué responder por WhatsApp'), ('V', 'Qué mira un comercio antes de comprarte')])),
('2026-10-26-b-historia-diccionario', 'verde', '<div class="eye">Post nuevo</div><h1>Diccionario de IA<br><em>parte 2</em> 🤖</h1>' + foto(f'{REDES}/2026-10-26-post-diccionario-ia-2-1.png') + cta('Guardalo para después 📌')),
('2026-10-26-c-historia-alucinacion', 'mostaza', f'''{ilu('robot', 460)}<div class="eye">Palabra de IA</div><h1><em>Alucinación</em></h1><p class="sub">Es cuando la IA inventa un dato y te lo dice con total seguridad, como si fuera cierto.</p><div class="caja">Ejemplo: le pedís el horario de un local o una cifra y te da una que <b>suena bien pero no existe</b>.</div>'''),
('2026-10-26-d-historia-chequear', 'verde', f'''{ilu('lupa', 558)}<div class="eye">Por eso</div><h1>La IA puede<br><em>inventar datos</em></h1><p class="sub">Y te los dice con total seguridad. Se llama alucinación.</p>
<div class="caja">Antes de publicar un <b>precio, una fecha o una cifra</b> que te dio la IA, chequealo vos.</div>'''),
# Martes 27
('2026-10-27-a-historia-costo-unidad', 'papel', f'''{ilu('etiqueta', 440)}<div class="eye">Primer paso</div><h1>¿Sabés cuánto<br>te cuesta hacer<br><em>cada producto?</em></h1><p class="sub">Si la respuesta es “más o menos”, empezá por acá:</p>''' + lista([('1', 'Anotá todo lo que usás para hacer una unidad'), ('2', 'Poné al lado lo que te sale cada cosa'), ('3', 'Sumalo: ese es tu costo por unidad')])),
('2026-10-27-b-historia-precios', 'verde', '<div class="eye">Post nuevo</div><h1>Antes de poner<br>un precio, <em>hacé<br>esta cuenta</em></h1>' + foto(f'{OUT}/2026-10-27-post-precios.png', 560, 700) + cta('Guardalo 📌')),
('2026-10-27-c-historia-gastos', 'mostaza', f'''{ilu('caja', 527)}<div class="eye">Los que más se olvidan</div><h1>3 gastos que casi<br>nadie <em>suma</em><br>al precio</h1>''' + lista([('1', 'El packaging'), ('2', 'El envío'), ('3', 'La comisión de la plataforma de cobro')])),
('2026-10-27-d-historia-subir-precios', 'papel', f'''{ilu('bolsa', 420)}<div class="eye">Cuando toca aumentar</div><h1>Subir precios<br><em>sin vueltas</em></h1>''' + lista([('1', 'Avisá antes y con fecha'), ('2', 'Contá el motivo en una línea, sin pedir disculpas'), ('3', 'Recordá todo lo que incluye tu producto')]) + '<p class="pista">¿Te cuesta aumentar? Respondé esta historia 💬</p>'),
# Miércoles 28
('2026-10-28-a-historia-ia-google', 'verde', f'''{ilu('bloques', 589)}<div class="eye">Hoy en el feed</div><h1>¿Le escribís a la<br>IA como si fuera<br><em>Google?</em></h1><p class="sub">Un buen pedido tiene 4 partes. Al mediodía te muestro cuáles.</p>'''),
('2026-10-28-b-historia-reel-rctf', 'papel', '<div class="eye">Reel nuevo</div><h1>Cómo pedirle<br>a la IA <em>que te<br>responda bien</em></h1>' + foto(f'{OUT}/2026-10-28-reel-rctf-portada.jpg', 430, 764) + cta('Miralo en el perfil 👆')),
('2026-10-28-c-historia-que-ia', 'mostaza', f'''{ilu('robot', 440)}<div class="eye">¿Cuál uso?</div><h1>¿Qué IA <em>usar</em><br>para empezar?</h1>''' + lista([('✓', 'ChatGPT'), ('✓', 'Gemini'), ('✓', 'Claude')]) + '<div class="caja">Todas tienen versión gratis. Lo que más cambia el resultado es <b>cómo le pedís</b>.</div>'),
('2026-10-28-d-historia-cyber-aviso', 'verde', f'''{ilu('calendario', 558)}<div class="eye">Para agendar</div><h1>Del 2 al 4 de<br>noviembre hay<br><em>Cyber Monday</em></h1>
<div class="caja">📘 Cada ebook: <b>$17.500</b> (en vez de $25.000)<br>♾️ Acceso de por vida: <b>$60.000</b> (en vez de $90.000)</div>'''),
# Jueves 29
('2026-10-29-a-historia-preguntas-perfil', 'papel', f'''{ilu('celular', 420)}<div class="eye">Te ahorra mensajes</div><h1>Dejá estas<br>respuestas en<br>tu <em>perfil</em></h1>''' + lista([('1', 'Precio'), ('2', 'Envíos y zonas'), ('3', 'Medios de pago'), ('4', 'Horarios')]) + '<p class="pista">¿Qué te preguntan más a vos? Respondé esta historia 💬</p>'),
('2026-10-29-b-historia-whatsapp', 'verde', '<div class="eye">Post nuevo</div><h1>¿Qué respondés<br>cuando te piden<br><em>el precio?</em></h1>' + foto(f'{OUT}/2026-10-29-post-whatsapp.png', 560, 700) + cta('Guardalo 📌')),
('2026-10-29-c-historia-cual-vende', 'mostaza', '<div class="eye">¿Cuál vende más?</div><h1>Misma pregunta,<br><em>dos respuestas</em></h1><div class="caja" style="margin-top:56px">❌ “Precio por privado.”</div><div class="caja" style="margin-top:28px;background:#1F3D2B;color:#F4F3EE;border:0">✅ “Sale $18.000 con envío incluido. <b style=\'color:#E3A82B\'>¿Te lo reservo?</b>”</div><p class="sub" style="margin-top:44px">La segunda da el precio, suma lo que incluye y propone un próximo paso.</p>'),
('2026-10-29-d-historia-respuestas-rapidas', 'papel', f'''{ilu('celular', 527)}<div class="eye">Truco de WhatsApp Business</div><h1>Guardá tus<br><em>respuestas<br>rápidas</em></h1>
<div class="caja">Escribís la respuesta una vez, la guardás con un atajo y después la mandás tipeando <b>/</b> y el atajo.</div>'''),
# Viernes 30
('2026-10-30-a-historia-antes-comercios', 'verde', f'''{ilu('comercio', 440)}<div class="eye">¿Querés venderle a comercios?</div><h1>Tené esto<br><em>claro antes</em></h1>''' + lista([('1', 'Tu precio mayorista'), ('2', 'Cuánto le queda al comercio al revenderlo'), ('3', 'Tu pedido mínimo')])),
('2026-10-30-b-historia-comercios', 'papel', '<div class="eye">Post nuevo</div><h1>Qué mira un<br>comercio <em>antes<br>de comprarte</em></h1>' + foto(f'{OUT}/2026-10-30-post-comercios.png', 560, 700) + cta('Guardalo 📌')),
('2026-10-30-c-historia-visita', 'mostaza', f'''{ilu('caja', 496)}<div class="eye">Antes de la visita</div><h1>Lo que tenés<br>que <em>llevar</em></h1>''' + lista([('1', 'Tu lista de precios mayoristas, por escrito'), ('2', 'Una muestra del producto'), ('3', 'Cómo te hacen el pedido y en cuánto llega')])),
('2026-10-30-d-historia-asesoria', 'verde', f'''{ilu('flor', 558)}<div class="eye">Asesoría</div><h1>¿Querés revisar<br><em>tu caso</em> conmigo?</h1>
<div class="caja">Videollamada de <b>1 hora</b> · <b>$60.000</b><br>De lunes a viernes, de 17 a 20 hs.</div><div class="pill cta">Reservá en la web → Equipo</div>'''),
# Sábado 31
('2026-10-31-a-historia-cyber-post', 'verde', '<div class="eye">Ya está en el feed</div><h1>Cyber Monday<br><em>2 al 4 de nov.</em></h1>' + foto(f'{REDES}/2026-10-31-post-cyber-anuncio.png', 560, 700) + cta('Guardalo para acordarte 📌')),
('2026-10-31-b-historia-de-por-vida', 'papel', f'''{ilu('libros', 527)}<div class="eye">Acceso de por vida</div><h1>Qué <em>incluye</em></h1>''' + lista([('✓', 'Los 7 ebooks publicados'), ('✓', 'Todos los que salgan en el futuro'), ('✓', 'Las actualizaciones, para siempre')]) +
 '<div class="caja">En el Cyber Monday: <b>$60.000</b> en vez de $90.000. Un solo pago.</div>'),
('2026-10-31-c-historia-donde-leer', 'mostaza', f'''{ilu('pantallas', 460)}<div class="eye">Los ebooks</div><h1>Se leen donde<br>te quede <em>cómodo</em></h1>''' + lista([('📱', 'En el celular'), ('💻', 'En la compu')]) + '<div class="caja">Entrás a <b>Mi cuenta</b> con tu mail y los tenés ahí.</div>'),
('2026-10-31-d-historia-como-comprar', 'verde', f'''{ilu('laptop', 527)}<div class="eye">Paso a paso</div><h1>Cómo es comprar<br>un <em>ebook</em></h1>''' + lista([('1', 'Lo elegís en la web'), ('2', 'Pagás con Mercado Pago'), ('3', 'Apenas se acredita, lo leés desde Mi cuenta')])),
# Domingo 1
('2026-11-01-a-historia-resumen', 'papel', f'''{ilu('checklist', 465)}<div class="eye">Lo que vimos esta semana</div><h1>Para <em>guardar</em> 📌</h1>''' + lista([
    ('1', 'Precio = costo + gastos + tu tiempo + ganancia'), ('2', 'Un buen prompt: rol, contexto, tarea y formato'),
    ('3', 'Por WhatsApp: precio + qué incluye + próximo paso'), ('4', 'Para venderle a un comercio, llevá tu lista mayorista por escrito')])),
('2026-11-01-b-historia-quien-soy', 'mostaza', f'''{ilu('flor', 440)}<div class="eye">Quién está detrás</div><h1>¡Hola, soy <em>Flor</em>!</h1><p class="sub">Trabajo en consumo masivo y recorro comercios de la Patagonia. Armé esta web con inteligencia artificial y en los ebooks comparto lo que voy aprendiendo.</p>'''),
('2026-11-01-c-historia-reel-cyber', 'verde', '<div class="eye">Reel nuevo</div><h1>Mañana arranca<br>el <em>Cyber Monday</em></h1>' + foto(f'{OUT}/2026-11-01-reel-cyber-manana-portada.jpg', 430, 764) + cta('Miralo en el perfil 👆')),
]

# ---------- REELS 1080x1920, 30 fps ----------
CSS_R = '''*{margin:0;box-sizing:border-box}body{width:1080px;height:1920px;overflow:hidden;font-family:Inter,sans-serif}
.e{position:absolute;inset:0;display:flex;flex-direction:column;justify-content:center;padding:0 100px;opacity:0}
h1{font-family:'Inter Display';font-weight:800;letter-spacing:-.035em;line-height:1.02;font-size:116px;color:#F4F3EE}
h1 em{font-style:normal;color:#E3A82B} h1.dark{color:#1F3D2B} h1.dark em{color:#C98F17} h1 em.v{color:#F4F3EE}
.eye{font-weight:700;letter-spacing:.14em;text-transform:uppercase;font-size:40px;color:#E3A82B;margin-bottom:30px} .eye.dark{color:#1F3D2B}
.sub{font-size:50px;line-height:1.3;margin-top:40px;color:#F4F3EE;opacity:.92} .sub.dark{color:#1F3D2B}
.ej{margin-top:44px;background:#fff;border-left:14px solid #E3A82B;border-radius:28px;padding:34px 40px;font-size:42px;line-height:1.35;color:#16231B}
.letra{font-family:'Inter Display';font-weight:800;font-size:240px;line-height:1;color:#E3A82B} .letra.v{color:#1F3D2B}
.ilu{align-self:center;margin-bottom:50px} .ilu svg{display:block}
.cta{margin-top:70px;align-self:flex-start;background:#E3A82B;color:#1F3D2B;border-radius:999px;padding:30px 54px;font-weight:800;font-size:48px}
.barra{position:absolute;left:0;bottom:0;height:14px;background:#E3A82B}
'''
def rilu(n, w=420):
    return f'<div class="ilu">{ILU[n](w)}</div>'

REELS = {
'2026-10-28-reel-rctf': [
 (0.0, 3.0, '#1F3D2B', rilu('robot', 460) + '<h1>¿La IA te<br>responde<br><em>cualquier cosa?</em></h1>'),
 (3.0, 6.4, '#F4F3EE', '<div class="letra">R</div><h1 class="dark">Rol: decile<br><em>quién es</em></h1><div class="ej">“Sos vendedora de una tienda de ropa.”</div>'),
 (6.4, 9.8, '#E3A82B', '<div class="letra v">C</div><h1 class="dark">Contexto: contale<br><em class="v">tu situación</em></h1><div class="ej">“Vendo por Instagram, mis clientas tienen entre 25 y 40 años.”</div>'),
 (9.8, 13.2, '#F4F3EE', '<div class="letra">T</div><h1 class="dark">Tarea: pedile<br><em>una sola cosa</em></h1><div class="ej">“Escribí 3 respuestas para cuando me dicen que está caro.”</div>'),
 (13.2, 16.6, '#E3A82B', '<div class="letra v">F</div><h1 class="dark">Formato: decile<br><em class="v">cómo lo querés</em></h1><div class="ej">“Cortas, con voseo y sin emojis.”</div>'),
 (16.6, 20.0, '#1F3D2B', rilu('bloques', 380) + '<h1>Más de 40 prompts<br><em>listos para copiar</em></h1><p class="sub">Ebook N.º 1 · IA para vender más</p><div class="cta">Link en la bio</div>'),
],
'2026-11-01-reel-cyber-manana': [
 (0.0, 3.2, '#1F3D2B', rilu('calendario', 460) + '<div class="eye">Cyber Monday en Visión Alfa</div><h1>Del lunes 2 al<br><em>miércoles 4</em><br>de noviembre</h1>'),
 (3.2, 6.4, '#F4F3EE', rilu('libros', 420) + '<div class="eye" style="color:#C98F17">Cada ebook</div><h1 class="dark"><em>$17.500</em></h1><p class="sub dark">En vez de $25.000</p>'),
 (6.4, 9.6, '#E3A82B', rilu('bolsa', 420) + '<div class="eye dark">Acceso de por vida</div><h1 class="dark"><em class="v">$60.000</em></h1><p class="sub dark">Toda la colección, en vez de $90.000</p>'),
 (9.6, 13.0, '#F4F3EE', '<div class="eye" style="color:#C98F17">7 guías prácticas</div><h1 class="dark" style="font-size:66px;line-height:1.2;white-space:nowrap">IA para vender más<br>Emprender desde cero<br>Excel para emprendedores<br>Precios que dejan ganancia<br>Vender por WhatsApp e IG<br>Cómo venderle a comercios<br><em>Tu web de ventas con IA</em></h1>'),
 (13.0, 16.0, '#1F3D2B', '<h1>Arranca<br><em>mañana</em> 📘</h1><p class="sub">Del 2 al 4 de noviembre en la web</p><div class="cta">Link en la bio</div>'),
],
}

def navegador(pw):
    try:
        return pw.chromium.launch()
    except Exception:
        return pw.chromium.launch(executable_path='/opt/pw-browsers/chromium-1243/chrome-linux64/chrome')

def reel(p, nombre, esc, fps=30):
    dur = esc[-1][1]
    html = '<!doctype html><html><head><meta charset="utf-8"><style>' + CSS_R + '</style></head><body>'
    for i, (a, b, bg, h) in enumerate(esc):
        html += f'<div class="e" id="e{i}" style="background:{bg}">{h}</div>'
    html += '<div class="barra" id="barra"></div></body></html>'
    js = '''(t)=>{const E=%s;const ease=x=>1-Math.pow(1-x,3);
E.forEach(([a,b],i)=>{const el=document.getElementById('e'+i);
 if(t<a||t>=b){el.style.opacity=0;return} el.style.opacity=1;
 [...el.children].forEach((k,j)=>{const d=a+0.12*j;const p=Math.min(1,Math.max(0,(t-d)/0.45));const e=ease(p);
   k.style.opacity=e;k.style.transform=`translateY(${(1-e)*60}px)`;});
 const sal=Math.min(1,Math.max(0,(b-t)/0.25)); if(i<E.length-1) el.style.opacity=sal;});
document.getElementById('barra').style.width=(t/%s*100)+'%%';}''' % ([[a, b] for a, b, _, _ in esc], dur)
    p.set_viewport_size({'width': 1080, 'height': 1920})
    p.set_content(html); p.wait_for_timeout(300)
    tmp = tempfile.mkdtemp()
    for f in range(int(dur * fps)):
        p.evaluate(js, f / fps); p.screenshot(path=f'{tmp}/f{f:04d}.jpg', type='jpeg', quality=92)
    # Portada: primera escena ya armada
    p.evaluate(js, 1.6); p.screenshot(path=f'{OUT}/{nombre}-portada.jpg', type='jpeg', quality=92)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(fps), '-i', f'{tmp}/f%04d.jpg', '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=stereo',
                    '-shortest', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-profile:v', 'high', '-crf', '20', '-c:a', 'aac', '-movflags', '+faststart', f'{OUT}/{nombre}.mp4'], check=True)
    subprocess.run(['rm', '-rf', tmp])

solo = sys.argv[2] if len(sys.argv) > 2 else 'todo'
with sync_playwright() as pw:
    b = navegador(pw); p = b.new_page(viewport={'width': 1080, 'height': 1350})
    if solo in ('todo', 'posts'):
        for k, (cls, body) in POSTS.items():
            p.set_viewport_size({'width': 1080, 'height': 1350})
            p.set_content(f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS_POST}</style></head><body><div class="p {cls}">{marca(cls)}{body}</div></body></html>')
            p.wait_for_timeout(200); p.screenshot(path=f'{OUT}/{k}.png'); print(k)
    if solo in ('todo', 'reels'):
        for k, esc in REELS.items():
            reel(p, k, esc); print(k)
    if solo in ('todo', 'historias'):
        for k, cls, body in HIST:
            p.set_viewport_size({'width': 1080, 'height': 1920})
            p.set_content(incrustar(f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS_H}</style></head><body><div class="s {cls}">{marca(cls)}{body}</div></body></html>'))
            p.wait_for_timeout(200); p.screenshot(path=f'{OUT}/{k}.png'); print(k)
    b.close()
