# Placas de Instagram para PowerFit Cipolletti (posts 1080x1350, historias 1080x1920).
# Uso: python3 generar.py <carpeta_salida>
from playwright.sync_api import sync_playwright
import sys, base64, os

AZUL = '#1565FF'; CIAN = '#5CD3FF'; NEGRO = '#07090D'; BLANCO = '#F5F8FC'

def rayo(w=60):
    return (f'<svg width="{w}" height="{int(w*1.25)}" viewBox="0 0 40 50"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">'
            f'<stop offset="0" stop-color="{CIAN}"/><stop offset="1" stop-color="#0A5BD8"/></linearGradient></defs>'
            '<path d="M26 1 L5 29 L18 29 L13 49 L35 19 L22 19 Z" fill="url(#g)"/></svg>')

def marca(size=40):
    return (f'<div class="marca">{rayo(int(size*1.1))}<span style="font-size:{size}px">POWER<span class="az">FIT</span></span>'
            f'<small>Cipolletti</small></div>')

CSS = f'''*{{box-sizing:border-box;margin:0}}
body{{font-family:Inter,sans-serif;overflow:hidden;background:{NEGRO}}}
.p,.s{{display:flex;flex-direction:column;position:relative;color:{BLANCO};overflow:hidden;background:{NEGRO}}}
.p{{width:1080px;height:1350px;padding:80px 84px}}
.s{{width:1080px;height:1920px;padding:270px 90px 300px}}
.p::before,.s::before{{content:"";position:absolute;width:900px;height:900px;border-radius:50%;right:-380px;top:-320px;
  background:radial-gradient(circle,rgba(30,155,255,.38),rgba(30,155,255,0) 65%);pointer-events:none}}
.p.azul,.s.azul{{background:linear-gradient(150deg,#0B5ED7,#1E9BFF 60%,#5CD3FF)}}
.p.azul::before,.s.azul::before{{display:none}}
.marca{{display:flex;align-items:center;gap:14px;font-family:'Inter Display';font-weight:900;font-style:italic;letter-spacing:-.01em;position:relative}}
.marca small{{font-family:Inter;font-style:normal;font-weight:600;font-size:22px;letter-spacing:.18em;text-transform:uppercase;opacity:.7;margin-left:6px;align-self:center}}
.az{{color:{AZUL}}} .azul .az{{color:{NEGRO}}}
.eye{{font-weight:600;letter-spacing:.3em;text-transform:uppercase;font-size:26px;color:{BLANCO};opacity:.85;position:relative}}
.azul .eye{{color:{NEGRO}}}
h1{{font-family:'Inter Display';font-weight:900;font-style:italic;text-transform:uppercase;letter-spacing:-.02em;line-height:.9;font-size:108px;margin-top:22px;position:relative;width:128%;transform:scaleX(.78);transform-origin:left top}}
h1 em{{font-style:italic;color:{AZUL}}} .foto h1 em{{color:#2B7BFF}} .azul h1 em{{color:{NEGRO}}}
.sub{{font-size:38px;line-height:1.38;margin-top:30px;opacity:.9;max-width:880px;position:relative}}
.s .sub{{font-size:44px}}
.pie{{margin-top:auto;display:flex;justify-content:space-between;align-items:center;font-size:29px;font-weight:600;position:relative}}
.pill{{background:{AZUL};color:#fff;border-radius:999px;padding:18px 34px;font-weight:800;font-size:31px;box-shadow:0 0 40px rgba(30,155,255,.55)}}
.azul .pill{{background:{NEGRO};color:#fff;box-shadow:none}}
.lista{{margin-top:44px;display:flex;flex-direction:column;gap:24px;position:relative}}
.it{{display:flex;gap:24px;align-items:flex-start;font-size:37px;line-height:1.3}}
.s .it{{font-size:42px}}
.it b{{flex:none;width:60px;height:60px;border-radius:50%;background:{AZUL};color:#fff;display:flex;align-items:center;justify-content:center;font-family:'Inter Display';font-size:30px;font-weight:900;font-style:italic}}
.azul .it b{{background:{NEGRO}}}
.caja{{margin-top:46px;border-radius:30px;padding:36px 40px;font-size:36px;line-height:1.38;background:rgba(255,255,255,.06);border:2px solid rgba(92,211,255,.35);position:relative}}
.azul .caja{{background:rgba(7,9,13,.12);border-color:rgba(7,9,13,.35)}}
.caja strong{{color:{CIAN}}} .azul .caja strong{{color:{NEGRO}}}
.tag{{display:inline-block;font-weight:900;font-family:'Inter Display';font-style:italic;text-transform:uppercase;font-size:30px;padding:10px 24px;border-radius:999px;margin-bottom:22px}}
.mito{{background:#3A1418;color:#FF8A8A}} .verdad{{background:#0F3424;color:#6BE3A6}} .depende{{background:#3A2F0C;color:#FFD36B}}
.num{{position:absolute;top:84px;right:84px;font-weight:700;font-size:26px;opacity:.6}}
.grande{{font-family:'Inter Display';font-weight:900;font-style:italic;font-size:300px;line-height:.85;letter-spacing:-.05em;color:{AZUL};position:relative;text-shadow:0 0 60px rgba(30,155,255,.45)}}
.cta{{margin-top:auto;align-self:flex-start;background:{AZUL};color:#fff;border-radius:999px;padding:26px 44px;font-weight:800;font-size:40px;position:relative;box-shadow:0 0 50px rgba(30,155,255,.6)}}
.azul .cta{{background:{NEGRO};box-shadow:none}}
.post{{margin-top:56px;width:640px;height:800px;border-radius:28px;overflow:hidden;box-shadow:0 0 0 3px rgba(92,211,255,.5),0 30px 80px rgba(30,155,255,.35);align-self:center;transform:rotate(-2deg);position:relative}}
.post img{{width:100%;height:100%;display:block}}
.hueco{{height:300px}}
.pista{{font-size:36px;font-weight:600;opacity:.75;position:relative}}
.foto{{background-size:cover;background-position:center top}}
.foto::before{{display:none}}
.foto::after{{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(7,9,13,.55) 0%,rgba(7,9,13,.25) 30%,rgba(7,9,13,.82) 62%,rgba(7,9,13,.97) 100%);z-index:0}}
.foto>*{{position:relative;z-index:1}}
.grande{{font-style:italic}}
'''

def foto(nombre):
    ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fotos', nombre)
    return 'data:image/jpeg;base64,' + base64.b64encode(open(ruta, 'rb').read()).decode()

def html(cls, body, kind='p'):
    estilo = ''
    if cls.startswith('foto:'):
        estilo = f' style="background-image:url({foto(cls[5:])})"'
        cls = 'foto'
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="{kind} {cls}"{estilo}>{body}</div></body></html>'

LINK = 'Link en la bio'
posts = {
 '2026-10-19-post-que-es': ('foto:entrena.jpg', marca()+f'''
<div class="eye" style="margin-top:400px">Electrofitness · EMS</div>
<h1>¿Qué es el<br><em>electrofitness?</em></h1>
<p class="sub">Entrenás con un traje que envía impulsos eléctricos suaves a tus músculos mientras hacés ejercicios simples. Siempre guiado por un entrenador.</p>
<div class="caja">Resultado: <strong>más músculos trabajando a la vez</strong>, en una sesión corta y sin cargar peso.</div>
<div class="pie"><span>{LINK}</span><span class="pill">Clase de prueba gratis</span></div>'''),
 '2026-10-20-post-20-minutos': ('', marca()+f'''
<div class="grande" style="margin-top:110px">20’</div>
<h1 style="font-size:96px;margin-top:10px">20 minutos.<br><em>300 músculos activos.</em></h1>
<div class="lista">
<div class="it"><b>✓</b><span>Ideal si tenés poco tiempo</span></div>
<div class="it"><b>✓</b><span>Sin cargar peso en las articulaciones</span></div>
<div class="it"><b>✓</b><span>Con entrenador en cada sesión</span></div>
</div>
<div class="pie"><span>Córdoba 340 · Cipolletti</span><span class="pill">Probalo gratis</span></div>'''),
 '2026-10-22-post-clase-gratis': ('foto:pareja.jpg', marca()+f'''
<div class="eye" style="margin-top:440px">Para arrancar</div>
<h1 style="font-size:120px">Tu primera clase<br><em>es gratis.</em></h1>
<p class="sub">Elegís el horario que te queda cómodo desde el link de la bio y venís. Somos grupos chiquitos, de hasta 3 personas, así que la clase es a tu medida.</p>
<div class="pie"><span>Sin compromiso</span><span class="pill">Reservá tu clase</span></div>'''),
 '2026-10-23-post-para-quien': ('', marca()+f'''
<div class="eye" style="margin-top:120px">¿Es para mí?</div>
<h1 style="font-size:100px">El electrofitness<br>es <em>para vos si…</em></h1>
<div class="lista">
<div class="it"><b>⚡</b><span>Tenés poco tiempo para entrenar</span></div>
<div class="it"><b>⚡</b><span>Querés fortalecer y tonificar tu cuerpo</span></div>
<div class="it"><b>⚡</b><span>Volvés a entrenar después de un tiempo</span></div>
<div class="it"><b>⚡</b><span>Querés cuidar tu masa muscular con los años</span></div>
</div>
<div class="pie"><span>{LINK}</span><span class="pill">Primera clase gratis</span></div>'''),
 '2026-10-24-post-antes-de-tu-clase': ('', marca()+f'''
<div class="eye" style="margin-top:120px">Guardalo 📌</div>
<h1 style="font-size:100px">Antes de tu<br><em>primera clase</em></h1>
<div class="lista">
<div class="it"><b>1</b><span>Tomá bastante agua durante el día</span></div>
<div class="it"><b>2</b><span>No vengas recién comido ni con el estómago vacío</span></div>
<div class="it"><b>3</b><span>Contale al entrenador si tenés alguna lesión o condición de salud</span></div>
<div class="it"><b>4</b><span>Traé ganas: son solo 20 minutos ⚡</span></div>
</div>
<div class="pie"><span>Córdoba 340 · Cipolletti</span><span class="pill">Reservá gratis</span></div>'''),
}
mitos = [
 ('', marca()+'''<span class="num">1/6</span>
<div class="eye" style="margin-top:170px">Guardalo 📌</div>
<h1 style="font-size:124px">Mitos y verdades del <em>electrofitness</em></h1>
<p class="sub">Lo que más nos preguntan en el gimnasio, respondido.</p>
<div class="pie"><span>Sin vueltas</span><span class="pill">Deslizá →</span></div>'''),
 ('', marca(34)+'''<span class="num">2/6</span>
<div style="margin-top:150px"><span class="tag mito">MITO</span></div>
<h1 style="font-size:100px">“Duele.”</h1>
<p class="sub">Se siente como un cosquilleo o una contracción fuerte. El entrenador regula la intensidad según cómo te sentís, y arrancás de a poco.</p>'''),
 ('', marca(34)+'''<span class="num">3/6</span>
<div style="margin-top:150px"><span class="tag mito">MITO</span></div>
<h1 style="font-size:100px">“Con esto no hace falta comer bien.”</h1>
<p class="sub">El entrenamiento suma, pero los resultados también dependen de cómo comés, cómo dormís y de la constancia.</p>'''),
 ('', marca(34)+'''<span class="num">4/6</span>
<div style="margin-top:150px"><span class="tag verdad">VERDAD</span></div>
<h1 style="font-size:100px">“Sirve si tenés poco tiempo.”</h1>
<p class="sub">Las sesiones duran 20 minutos y trabajan muchos grupos musculares a la vez. Por eso es una de las formas más prácticas de entrenar.</p>'''),
 ('', marca(34)+'''<span class="num">5/6</span>
<div style="margin-top:150px"><span class="tag depende">DEPENDE</span></div>
<h1 style="font-size:100px">“Lo puede hacer cualquiera.”</h1>
<p class="sub">No se recomienda con cardiopatía grave, marcapasos o implantes metálicos, epilepsia, embarazo o posparto reciente, ni con heridas en la piel, entre otros casos. Por eso hacemos una evaluación previa y pedimos apto médico según cada caso.</p>'''),
 ('azul', marca()+'''<span class="num">6/6</span>
<div class="eye" style="margin-top:200px">¿Te quedó alguna duda?</div>
<h1 style="font-size:116px">Vení a <em>probarlo gratis.</em></h1>
<p class="sub">La mejor forma de sacarte las dudas es en una clase de prueba. Te explicamos todo antes de arrancar.</p>
<div class="pie"><span>Link en la bio</span><span class="pill">Reservá tu clase</span></div>'''),
]

def img_tag(path):
    return '<img src="data:image/png;base64,' + base64.b64encode(open(path, 'rb').read()).decode() + '">'

def historias(out):
    P = lambda n: img_tag(f'{out}/{n}.png')
    return {
     '2026-10-19-a-historia': ('', marca()+f'''<div class="eye" style="margin-top:110px">Nuevo en el feed</div>
<h1>¿Sabés qué es el <em>electrofitness?</em> 👀</h1><div class="post">{P("2026-10-19-post-que-es")}</div>
<div class="cta">Mirá el post ⚡</div>'''),
     '2026-10-19-b-historia': ('', marca()+'''<div class="eye" style="margin-top:140px">Encuesta</div>
<h1>¿Probaste alguna vez el <em>electrofitness?</em></h1>
<p class="sub">Contanos, queremos saber 👇</p><div class="hueco"></div>'''),
     '2026-10-20-a-historia': ('azul', marca()+'''<div class="eye" style="margin-top:140px">Encuesta</div>
<h1>¿Cuánto tiempo le dedicás a <em>entrenar</em> por semana?</h1>
<p class="sub">Spoiler: con 20 minutos por sesión alcanza para arrancar 😉</p><div class="hueco"></div>'''),
     '2026-10-20-b-historia': ('', marca()+f'''<div class="eye" style="margin-top:110px">Post nuevo</div>
<h1>20 minutos. <em>300 músculos.</em></h1><div class="post">{P("2026-10-20-post-20-minutos")}</div>
<div class="cta">Probalo gratis ⚡</div>'''),
     '2026-10-21-a-historia': ('', marca()+f'''<div class="eye" style="margin-top:110px">Hoy en el feed</div>
<h1>Mitos y verdades del <em>EMS</em> 🤔</h1><div class="post">{P("2026-10-21-post-mitos-1")}</div>
<div class="cta">Deslizá el post →</div>'''),
     '2026-10-21-b-historia': ('foto:pantalla.jpg', marca()+'''<div class="eye" style="margin-top:560px">Te leemos</div>
<h1>¿Qué te gustaría saber del <em>electrofitness?</em></h1>
<p class="sub">Dejanos tu pregunta y te respondemos por acá 👇</p><div class="hueco"></div>'''),
     '2026-10-22-a-historia': ('azul', marca()+f'''<div class="eye" style="margin-top:110px">Para arrancar</div>
<h1>Tu primera clase <em>es gratis</em> ⚡</h1><div class="post">{P("2026-10-22-post-clase-gratis")}</div>
<div class="cta">Mirá cómo reservar</div>'''),
     '2026-10-22-b-historia': ('', marca()+'''<div class="eye" style="margin-top:140px">Sin compromiso</div>
<h1>Reservá tu <em>clase de prueba</em> gratis</h1>
<p class="sub">Tocás el link, elegís tu horario y listo. Te esperamos 💙</p><div class="hueco"></div>'''),
     '2026-10-23-a-historia': ('foto:pareja.jpg', marca()+'''<div class="eye" style="margin-top:640px">Te esperamos</div>
<h1>Córdoba 340,<br><em>Cipolletti</em> 📍</h1>
<p class="sub">Clases de 20 minutos, en grupos de hasta 3 personas. Reservá tu clase gratis desde el link de la bio.</p>
<div class="cta">⚡ PowerFit Cipolletti</div>'''),
     '2026-10-23-b-historia': ('azul', marca()+'''<div class="eye" style="margin-top:140px">Viernes ⚡</div>
<h1>¿Cuántas ganas tenés de <em>arrancar</em> a entrenar?</h1>
<p class="sub">Movelo 👇</p><div class="hueco"></div>'''),
    }

out = sys.argv[1]; os.makedirs(out, exist_ok=True)
with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page(viewport={'width': 1080, 'height': 1350})
    for k, (cls, body) in posts.items():
        pg.set_content(html(cls, body)); pg.wait_for_timeout(150); pg.screenshot(path=f'{out}/{k}.png')
    for i, (cls, body) in enumerate(mitos, 1):
        pg.set_content(html(cls, body)); pg.wait_for_timeout(150); pg.screenshot(path=f'{out}/2026-10-21-post-mitos-{i}.png')
    pg = b.new_page(viewport={'width': 1080, 'height': 1920})
    for k, (cls, body) in historias(out).items():
        pg.set_content(html(cls, body, 's')); pg.wait_for_timeout(150); pg.screenshot(path=f'{out}/{k}.png')
    b.close()
print('ok')
