# Campaña PowerFit 26/10 al 4/11 (lanzamiento de suscripciones / Cyber PowerFit).
# Genera posteos 1080x1350, historias 1080x1920 y capas transparentes para videos.
# Uso: python3 piezas.py <salida>
import base64, io, os, sys
from PIL import Image, ImageOps, ImageEnhance
from playwright.sync_api import sync_playwright

BASE = os.path.dirname(os.path.abspath(__file__))
MEDIA = os.path.join(BASE, '..', 'drive', 'media')
ASSETS = os.path.join(BASE, 'assets')

def foto(ruta, ancho=1500, pos=None):
    im = ImageOps.exif_transpose(Image.open(ruta)).convert('RGB')
    im = ImageEnhance.Contrast(im).enhance(1.08)
    im = ImageEnhance.Color(im).enhance(0.88)
    im.thumbnail((ancho, ancho * 2))
    b = io.BytesIO(); im.save(b, 'JPEG', quality=90)
    return 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()

F = {
 'piso':   lambda: foto(os.path.join(MEDIA, '939A0568-C229-49A8-BD07-75A1708454DF.JPG')),
 'piso2':  lambda: foto(os.path.join(MEDIA, '498A0AB1-2E04-46A8-84FB-7A0A94BA52CA.JPG')),
 'piso3':  lambda: foto(os.path.join(MEDIA, '7ACBAC1D-2B5A-40B6-AF21-A917265E49FB.JPG')),
 'banco':  lambda: foto(os.path.join(ASSETS, 'st_IMG_4030_3.2.jpg')),
 'manc':   lambda: foto(os.path.join(ASSETS, 'st_IMG_4031_0.8.jpg')),
 'plancha':lambda: foto(os.path.join(ASSETS, 'st_IMG_4028_2.0.jpg')),
 'suelo':  lambda: foto(os.path.join(ASSETS, 'st_125C_1.5.jpg')),
 'senta':  lambda: foto(os.path.join(ASSETS, 'st_5F16_1.2.jpg')),
}
_cache = {}
def F_(k):
    if k not in _cache: _cache[k] = F[k]()
    return _cache[k]

RAYO = '<svg viewBox="0 0 40 50" class="r"><path d="M26 1 L5 29 L18 29 L13 49 L35 19 L22 19 Z"/></svg>'

CSS = '''
*{box-sizing:border-box;margin:0}
html,body{background:transparent}
body{font-family:Inter,sans-serif;-webkit-font-smoothing:antialiased}
.pz{position:relative;overflow:hidden;display:flex;flex-direction:column}
.post{width:1080px;height:1350px;padding:78px 84px 84px}
.hist{width:1080px;height:1920px;padding:250px 90px 330px}
/* marca */
.marca{display:flex;align-items:center;gap:14px;position:relative;z-index:3}
.marca .r{width:34px;height:44px;fill:#2B7BFF}
.marca b{font-family:'Inter Display';font-weight:900;font-style:italic;font-size:40px;letter-spacing:-.01em;line-height:1}
.marca b i{font-style:italic;color:#2B7BFF}
.marca small{display:block;font-size:15px;font-weight:600;letter-spacing:.42em;text-transform:uppercase;opacity:.7;margin-top:4px}
/* tipografía */
.eye{display:flex;align-items:center;gap:16px;font-weight:600;font-size:24px;letter-spacing:.32em;text-transform:uppercase;position:relative;z-index:3}
.eye:before{content:"";width:46px;height:3px;background:currentColor;opacity:.8}
h1{font-family:'Inter Display';font-weight:900;font-style:italic;text-transform:uppercase;line-height:.88;letter-spacing:-.015em;width:132%;transform:scaleX(.76);transform-origin:left top;position:relative;z-index:3;margin-top:22px}
.post h1{font-size:150px}
.hist h1{font-size:170px}
p.sub{font-size:38px;line-height:1.36;font-weight:500;max-width:880px;position:relative;z-index:3;margin-top:30px}
.hist p.sub{font-size:44px}
.pie{margin-top:auto;display:flex;justify-content:space-between;align-items:center;gap:20px;font-size:26px;font-weight:600;letter-spacing:.04em;position:relative;z-index:3}
.boton{display:inline-flex;align-items:center;gap:12px;border-radius:999px;padding:20px 34px;font-weight:800;font-size:30px;letter-spacing:0}
/* estilo azul */
.azul{background:linear-gradient(160deg,#1E6BFF 0%,#1157F2 55%,#0A43D0 100%);color:#fff}
.azul .bg-r{position:absolute;right:-190px;top:180px;width:900px;height:1125px;fill:rgba(255,255,255,.13);z-index:1}
.hist.azul .bg-r{top:380px;width:1000px;height:1250px}
.azul h1 em{font-style:italic;color:#07090D}
.azul .marca .r{fill:#fff}
.azul .marca b i{color:#07090D}
.azul .boton{background:#07090D;color:#fff}
/* estilo claro */
.claro{background:#F1EFE9;color:#0B0D12}
.claro .marca .r{fill:#1565FF}
.claro h1 em{font-style:italic;color:#1565FF}
.claro .eye{color:#1565FF}
.claro .boton{background:#1565FF;color:#fff}
.claro .linea{height:2px;background:#0B0D12;opacity:.85;position:relative;z-index:3}
/* estilo foto */
.foto{background:#07090D;color:#fff}
.foto .img{position:absolute;inset:0;background-size:cover;z-index:0}
.foto .velo{position:absolute;inset:0;z-index:1;background:linear-gradient(180deg,rgba(7,9,13,.62) 0%,rgba(7,9,13,.05) 22%,rgba(7,9,13,0) 40%,rgba(7,9,13,.78) 64%,rgba(7,9,13,.96) 100%)}
.foto .tinte{position:absolute;inset:0;z-index:1;background:linear-gradient(200deg,rgba(21,101,255,.28),rgba(21,101,255,0) 45%);mix-blend-mode:multiply}
.foto h1 em{font-style:italic;color:#2B7BFF;text-shadow:0 0 50px rgba(21,101,255,.45)}
.foto .eye{color:#8EB6FF}
.foto .boton{background:#1565FF;color:#fff;box-shadow:0 0 40px rgba(21,101,255,.55)}
.foto .marca small{opacity:.85}
/* tabla de precios */
table{width:100%;border-collapse:collapse;position:relative;z-index:3;margin-top:44px;font-variant-numeric:tabular-nums}
th{font-size:22px;letter-spacing:.14em;text-transform:uppercase;font-weight:700;text-align:right;padding:0 0 18px;opacity:.75}
th:first-child{text-align:left}
th span{display:block;color:#1565FF;opacity:1;letter-spacing:.06em;font-size:24px;margin-top:4px}
td{font-size:38px;font-weight:700;text-align:right;padding:26px 0;border-top:2px solid rgba(11,13,18,.18)}
td:first-child{text-align:left;font-family:'Inter Display';font-style:italic;font-weight:900;text-transform:uppercase;font-size:34px;line-height:1}
td small{display:block;font-family:Inter;font-style:normal;font-weight:600;font-size:20px;letter-spacing:.12em;opacity:.6;margin-top:6px}
.hist th{font-size:19px;letter-spacing:.08em}.hist th span{font-size:22px}.hist td{font-size:40px;padding:34px 0}.hist td:first-child{font-size:38px;width:230px}.hist td small{font-size:22px}
.nota{font-size:24px;opacity:.65;margin-top:26px;position:relative;z-index:3}
/* pasos sueltos */
.paso{display:flex;gap:26px;align-items:baseline;font-size:40px;line-height:1.3;font-weight:500;padding:26px 0;border-top:2px solid rgba(11,13,18,.16);position:relative;z-index:3}
.paso b{font-family:'Inter Display';font-style:italic;font-weight:900;color:#1565FF;font-size:44px;min-width:44px}
.hueco{flex:1}
/* capas para video */
.capa{width:1080px;height:1920px;position:relative;color:#fff;padding:250px 90px 0}
.capa .velo2{position:absolute;left:0;right:0;bottom:0;height:1000px;background:linear-gradient(180deg,rgba(7,9,13,0),rgba(7,9,13,.82) 65%,rgba(7,9,13,.92))}
.capa .velo3{position:absolute;left:0;right:0;top:0;height:420px;background:linear-gradient(180deg,rgba(7,9,13,.55),rgba(7,9,13,0))}
.capa .txt{position:absolute;left:90px;right:90px;bottom:420px}
.capa h1{font-size:168px}
.capa h1 em{font-style:italic;color:#2B7BFF;text-shadow:0 0 50px rgba(21,101,255,.5)}
.capa p.sub{font-size:46px}
.fin{background:linear-gradient(160deg,#1E6BFF,#0A43D0);color:#fff}
.fin .marca .r{fill:#fff}.fin .marca b i{color:#07090D}
'''

def marca(oscuro=False):
    return (f'<div class="marca">{RAYO}<div><b>POWER<i>FIT</i></b><small>Cipolletti</small></div></div>')

def pieza(tipo, estilo, cuerpo, img=None, pos='center'):
    extra = ''
    if estilo == 'azul':
        extra = f'<svg viewBox="0 0 40 50" class="bg-r"><path d="M26 1 L5 29 L18 29 L13 49 L35 19 L22 19 Z"/></svg>'
    if estilo == 'foto':
        extra = f'<div class="img" style="background-image:url({F_(img)});background-position:{pos}"></div><div class="tinte"></div><div class="velo"></div>'
    return f'<div class="pz {tipo} {estilo}">{extra}{marca()}{cuerpo}</div>'

def html(inner):
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{inner}</body></html>'

TABLA = '''<table>
<tr><th>Plan</th><th>Mensual</th><th>Cada 2 meses<span>−15%</span></th><th>Cada 3 meses<span>−20%</span></th></tr>
<tr><td>1 vez<small>por semana</small></td><td>$150.000</td><td>$255.000</td><td>$360.000</td></tr>
<tr><td>2 veces<small>por semana</small></td><td>$180.000</td><td>$306.000</td><td>$432.000</td></tr>
<tr><td>3 veces<small>por semana</small></td><td>$230.000</td><td>$391.000</td><td>$552.000</td></tr>
</table><p class="nota">Los descuentos son pagando con suscripción por Mercado Pago.</p>'''

# ---------- POSTEOS ----------
POSTS = {
 '2026-10-27-post-duele': ('foto', '<div class="hueco"></div><div class="eye">Lo que más nos preguntan</div><h1>¿Duele?</h1><p class="sub">Se siente como un cosquilleo que se va poniendo intenso. La profe va ajustando todo y vos vas a tu ritmo.</p>', 'suelo', '40% 50%'),
 '2026-10-28-post-a-tu-medida': ('foto', '<div class="hueco"></div><div class="eye">Grupos de hasta 3</div><h1>Una clase<br><em>a tu medida</em></h1><p class="sub">20 minutos, poquitas personas y la profe siempre al lado. Así es más fácil arrancar y no aflojar.</p>', 'piso', '58% 50%'),
 '2026-10-29-post-primera-clase': ('azul', '<div class="eye" style="margin-top:300px">Para arrancar</div><h1>Tu primera<br>clase es<br><em>gratis</em></h1><p class="sub">Tocá el link de la bio, completá el formulario y después elegís tu horario.</p><div class="pie"><span>Córdoba 340 · Cipolletti</span><span class="boton">Reservá tu clase →</span></div>', None, None),
 '2026-10-30-post-se-viene-cyber': ('foto', '<div class="hueco"></div><div class="eye">2 al 4 de noviembre</div><h1>Se viene el<br><em>Cyber PowerFit</em></h1><p class="sub">Algo para las que vienen pensando en arrancar. Activá las notificaciones.</p>', 'piso2', '55% 50%'),
 '2026-11-01-post-manana-arranca': ('claro', '<div class="eye" style="margin-top:250px">Cyber PowerFit · Lanzamiento</div><h1>Mañana<br><em>arranca</em></h1><p class="sub">Llegan las suscripciones: tu plan se cobra solo por Mercado Pago, y si elegís pagar cada 2 o 3 meses te sale menos.</p><div class="hueco"></div><div class="linea"></div><div class="pie" style="margin-top:28px"><span>Córdoba 340 · Cipolletti</span><span class="boton">Escribinos por WhatsApp</span></div>', None, None),
 '2026-11-02-post-suscripciones-1': ('azul', '<div class="eye" style="margin-top:300px">Cyber PowerFit · Novedad</div><h1>Llegaron las<br><em>suscripciones</em></h1><p class="sub">Elegís tu plan una vez y se cobra solo. Y si elegís cada 2 o 3 meses, te sale menos.</p><div class="pie"><span>Deslizá</span><span class="boton">Ver cómo funciona →</span></div>', None, None),
 '2026-11-02-post-suscripciones-2': ('claro', '<div class="eye" style="margin-top:110px">Cómo funciona</div><h1 style="font-size:140px">¿Cómo me<br><em>suscribo?</em></h1><div style="margin-top:56px"><div class="paso"><b>1</b><span>Elegís tu plan: 1, 2 o 3 veces por semana.</span></div><div class="paso"><b>2</b><span>Elegís cada cuánto pagar: todos los meses, cada 2 o cada 3.</span></div><div class="paso"><b>3</b><span>Nos escribís por WhatsApp y te pasamos el link de Mercado Pago.</span></div><div class="paso"><b>4</b><span>Pagás con tu tarjeta y después se cobra solo.</span></div></div>', None, None),
 '2026-11-02-post-suscripciones-3': ('claro', '<div class="eye" style="margin-top:110px">Valores</div><h1 style="font-size:140px">Planes <em>y precios</em></h1>' + TABLA, None, None),
 '2026-11-02-post-suscripciones-4': ('foto', '<div class="hueco"></div><div class="eye">Para suscribirte</div><h1>Escribinos<br>por <em>WhatsApp</em></h1><p class="sub">Te pasamos el link de tu plan y te ayudamos a elegir. Y si nunca viniste, la primera clase es gratis.</p>', 'plancha', '50% 40%'),
 '2026-11-03-post-whatsapp': ('foto', '<div class="hueco"></div><div class="eye">Suscripciones PowerFit</div><h1>¿Dudas?<br><em>Escribinos</em></h1><p class="sub">Te pasamos el link de tu plan por WhatsApp y te ayudamos a elegir el que más te sirve.</p><div class="pie" style="margin-top:40px"><span>Córdoba 340 · Cipolletti</span><span class="boton">WhatsApp en la bio →</span></div>', 'banco', '50% 22%'),
 '2026-11-04-post-para-quedarse': ('azul', '<div class="eye" style="margin-top:300px">Cyber PowerFit</div><h1>Llegaron<br>para<br><em>quedarse</em></h1><p class="sub">Los descuentos de las suscripciones no se terminan con el Cyber: cada 2 meses, 15% menos; cada 3 meses, 20% menos.</p><div class="pie"><span>Pedinos el link por WhatsApp</span></div>', None, None),
}

# ---------- HISTORIAS ----------
HIST = {
 '2026-10-26-a-historia': ('azul', '<div class="eye" style="margin-top:120px">Encuesta</div><h1>¿Cuánto<br>dura una<br><em>clase?</em></h1><div class="hueco"></div>', None, None),
 '2026-10-27-a-historia': ('claro', '<div class="eye" style="margin-top:120px">Contanos</div><h1>¿Qué te<br>frena para<br><em>probar?</em></h1><div class="hueco"></div><div class="linea"></div>', None, None),
 '2026-10-27-b-historia': ('azul', '<div class="hueco"></div><div class="eye">Lo que más nos preguntan</div><h1>¿Duele?</h1><p class="sub">Se siente como un cosquilleo que se va poniendo intenso. La profe va ajustando todo y vos vas a tu ritmo.</p>', None, None),
 '2026-10-28-a-historia': ('azul', '<div class="eye" style="margin-top:120px">Encuesta</div><h1>¿Qué te<br>gustaría<br><em>trabajar?</em></h1><div class="hueco"></div>', None, None),
 '2026-10-28-b-historia': ('foto', '<div class="hueco"></div><div class="eye">Para arrancar</div><h1>Tu primera<br>clase es<br><em>gratis</em></h1><p class="sub">Tocá el link, completá el formulario y elegí tu horario.</p><div style="height:220px"></div>', 'senta', '50% 35%'),
 '2026-10-29-b-historia': ('foto', '<div class="hueco"></div><div class="eye">Cyber PowerFit</div><h1>¿Todavía<br>no <em>probaste?</em></h1><p class="sub">Tu primera clase es gratis. Y cuando quieras quedarte, con la suscripción te sale menos.</p>', 'piso3', '50% 50%'),
 '2026-10-30-a-historia': ('azul', '<div class="hueco"></div><div class="eye">2 al 4 de noviembre</div><h1>Se viene<br>el <em>Cyber</em><br>PowerFit</h1>', None, None),
 '2026-10-30-b-historia': ('claro', '<div class="eye" style="margin-top:120px">Cyber PowerFit</div><h1 style="font-size:150px">Activá el<br><em>recordatorio</em></h1><p class="sub">Así te avisamos cuando arranca.</p><div class="hueco"></div><div class="linea"></div>', None, None),
 '2026-11-02-a-historia': ('azul', '<div class="eye" style="margin-top:120px">Cyber PowerFit · Lanzamiento</div><h1>Arrancó<br>el <em>Cyber</em></h1><p class="sub">Llegaron las suscripciones: se cobran solas por Mercado Pago. Cada 2 meses, 15% menos. Cada 3 meses, 20% menos. Pedinos el link por WhatsApp.</p><div class="hueco"></div>', None, None),
 '2026-11-02-b-historia': ('claro', '<div class="eye" style="margin-top:120px">Cyber PowerFit</div><h1 style="font-size:142px">Preguntanos<br>de las<br><em>suscripciones</em></h1><div class="hueco"></div><div class="linea"></div>', None, None),
 '2026-11-03-a-historia': ('foto', '<div class="hueco"></div><div class="eye">PowerFit</div><h1>Ellas ya<br><em>arrancaron</em></h1><p class="sub">¿Y vos? La primera clase es gratis.</p>', 'suelo', '40% 50%'),
 '2026-11-04-a-historia': ('azul', '<div class="eye" style="margin-top:120px">Cyber PowerFit</div><h1>Llegaron<br>para<br><em>quedarse</em></h1><p class="sub">Los descuentos de las suscripciones no se terminan con el Cyber. Cada 2 meses, 15% menos. Cada 3 meses, 20% menos.</p><div class="hueco"></div>', None, None),
 '2026-11-04-b-historia': ('claro', '<div class="eye" style="margin-top:60px">Valores</div><h1 style="font-size:150px">Planes<br><em>y precios</em></h1>' + TABLA + '<div class="hueco"></div><p class="nota" style="font-size:30px;opacity:.85">Pedinos el link por WhatsApp.</p>', None, None),
}

# ---------- CAPAS DE VIDEO (texto sobre video) ----------
def capa(h, sub=''):
    s = f'<p class="sub">{sub}</p>' if sub else ''
    return f'<div class="capa"><div class="velo3"></div><div class="velo2"></div>{marca()}<div class="txt"><h1>{h}</h1>{s}</div></div>'
def fin(h, sub, boton):
    return f'<div class="capa fin" style="padding-top:250px">{marca()}<div class="txt" style="bottom:auto;top:640px"><h1>{h}</h1><p class="sub">{sub}</p><span class="boton" style="margin-top:46px;display:inline-flex;background:#07090D;color:#fff">{boton}</span></div></div>'

CAPAS = {
 # reel 26/10
 'r1-a': capa('Así se entrena<br>en <em>PowerFit</em>'),
 'r1-b': capa('Todo el cuerpo<br><em>a la vez</em>'),
 'r1-c': capa('Con la profe<br><em>al lado</em>'),
 'r1-d': capa('20 minutos<br><em>y listo</em>'),
 'r1-fin': fin('¿Te dan ganas<br>de <em style="color:#07090D">probar?</em>', 'Tu primera clase es gratis. Reservala desde el link de la bio.', 'Córdoba 340 · Cipolletti'),
 # reel 31/10 (cyber)
 'r2-a': capa('Se viene<br>el <em>Cyber</em>'),
 'r2-b': capa('Llegan las<br><em>suscripciones</em>'),
 'r2-c': capa('Tu plan se<br>cobra <em>solo</em>'),
 'r2-fin': fin('Cyber<br><em style="color:#07090D">PowerFit</em>', 'Del 2 al 4 de noviembre. Cada 2 meses, 15% menos. Cada 3 meses, 20% menos.', 'Activá las notificaciones'),
 # historias en video
 'v26': capa('20 minutos.<br><em>Nada más.</em>', 'Todo el cuerpo trabajando y la profe al lado.'),
 'v29': capa('A tu<br><em>ritmo</em>', 'Grupos de hasta 3 personas.'),
 'v03': capa('Escribinos por<br><em>WhatsApp</em>', 'Te pasamos el link de tu plan y te ayudamos a elegir.'),
}

if __name__ == '__main__':
    out = sys.argv[1]; os.makedirs(out, exist_ok=True); os.makedirs(out + '/capas', exist_ok=True)
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={'width': 1080, 'height': 1350})
        for k, (est, cuerpo, img, pos) in POSTS.items():
            pg.set_content(html(pieza('post', est, cuerpo, img, pos))); pg.wait_for_timeout(150)
            pg.locator('.pz').screenshot(path=f'{out}/{k}.png')
        pg = b.new_page(viewport={'width': 1080, 'height': 1920})
        for k, (est, cuerpo, img, pos) in HIST.items():
            pg.set_content(html(pieza('hist', est, cuerpo, img, pos))); pg.wait_for_timeout(150)
            pg.locator('.pz').screenshot(path=f'{out}/{k}.png')
        for k, inner in CAPAS.items():
            pg.set_content(html(inner)); pg.wait_for_timeout(120)
            pg.screenshot(path=f'{out}/capas/{k}.png', omit_background=True)
        b.close()
    print('ok')
