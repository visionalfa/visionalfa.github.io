# Contenido de la semana del 16/11 al 21/11/2026: posts, historias (todas automáticas, sin stickers) y reels.
# Uso: python3 herramientas/semana-2026-11-16.py <carpeta_salida>
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
'2026-11-16-post-idea-primera-venta': ('verde', f'''{ilu('bloques', 300)}
<div class="eye" style="margin-top:220px">Emprender desde cero</div>
<h1 style="font-size:82px">De la idea a tu<br><em>primera venta</em><br>en 4 pasos</h1>
<div class="lista" style="gap:16px">
<div class="it"><i>1</i><span>Validá la idea<small>Preguntale a quien te compraría, antes de invertir</small></span></div>
<div class="it"><i>2</i><span>Armá tu oferta<small>Qué vendés, para quién y qué incluye</small></span></div>
<div class="it"><i>3</i><span>Poné un precio que te deje ganancia</span></div>
<div class="it"><i>4</i><span>Conseguí tus primeros clientes<small>Empezá por tu círculo cercano</small></span></div>
</div>
<div class="pie"><span>Ebook N.º 2</span><span class="pill">Emprender desde cero</span></div>'''),
'2026-11-17-post-formula-excel-ia': ('papel', f'''{ilu('laptop', 300)}
<div class="eye" style="margin-top:220px">Excel + IA</div>
<h1 style="font-size:80px">¿No sabés qué<br>fórmula usar?<br><em>Pedísela a la IA</em></h1>
<div class="caja" style="margin-top:30px;font-size:30px">“Tengo una planilla con <b>fecha en A, producto en B y monto en C</b>. Dame la fórmula de Excel para sumar lo que vendí de <b>[producto]</b> y explicame cómo usarla.”</div>
<div class="lista" style="gap:12px;margin-top:28px">
<div class="it" style="font-size:30px"><i>+</i><span><b>SUMA</b>: el total vendido</span></div>
<div class="it" style="font-size:30px"><i>+</i><span><b>SUMAR.SI</b>: lo vendido de un producto</span></div>
<div class="it" style="font-size:30px"><i>+</i><span><b>CONTAR.SI</b>: cuántas ventas tuvo</span></div>
</div>
<div class="pie" style="color:#1F3D2B"><span>Ebook N.º 3</span><span class="pill">Excel para emprendedores</span></div>'''),
'2026-11-18-post-que-plan-te-conviene': ('mostaza', f'''{ilu('libros', 280)}
<div class="eye" style="margin-top:220px">Planes Visión Alfa</div>
<h1 style="font-size:82px">¿Qué plan<br>te <em>conviene?</em></h1>
<div class="lista" style="gap:20px">
<div class="it"><i>1</i><span><b>Ebook suelto · $25.000</b><small>Necesitás un tema puntual. Es tuyo para siempre.</small></span></div>
<div class="it"><i>2</i><span><b>Membresía · $15.000 por mes</b><small>Toda la colección mientras estés suscripto. Cancelás cuando quieras.</small></span></div>
<div class="it"><i>3</i><span><b>Acceso de por vida · $90.000</b><small>Un solo pago: todos los ebooks y los que salgan.</small></span></div>
</div>
<div class="pie" style="color:#1F3D2B"><span>Pagás con Mercado Pago</span><span class="pill">Link en la bio</span></div>'''),
'2026-11-19-post-antes-de-tu-web': ('papel', f'''{ilu('pantallas', 300)}
<div class="eye" style="margin-top:220px">Tu web con IA</div>
<h1 style="font-size:80px">Antes de pedirle<br>a la IA tu web,<br><em>tené esto listo</em></h1>
<div class="lista" style="gap:16px">
<div class="it"><i>1</i><span>Tus productos<small>Con precio, foto y una descripción corta</small></span></div>
<div class="it"><i>2</i><span>Cómo cobrás<small>Por ejemplo, Mercado Pago</small></span></div>
<div class="it"><i>3</i><span>Cómo entregás<small>Envíos, retiro, zonas</small></span></div>
<div class="it"><i>4</i><span>Cómo te contactan<small>WhatsApp, mail, Instagram</small></span></div>
</div>
<div class="pie" style="color:#1F3D2B"><span>Ebook N.º 7</span><span class="pill">Tu web de ventas con IA</span></div>'''),
'2026-11-20-post-web-acompanamiento': ('verde', f'''{ilu('laptop', 300)}
<div class="eye" style="margin-top:220px">Acompañamiento de 8 horas</div>
<h1 style="font-size:80px">Tu web automatizada:<br>la armamos<br><em>juntos, con IA</em></h1>
<div class="lista" style="gap:16px">
<div class="it"><i>✓</i><span>Como hice la mía, paso a paso</span></div>
<div class="it"><i>✓</i><span>4 encuentros de 2 horas por videollamada</span></div>
<div class="it"><i>✓</i><span>Acceso ilimitado a todos los ebooks</span></div>
<div class="it"><i>✓</i><span>De 17 a 20 hs, lo reservás en la web</span></div>
</div>
<div class="pie"><span>Link en la bio</span><span class="pill">$250.000 pago único</span></div>'''),
}

# ---------- HISTORIAS 1080x1920 ----------
# Zonas seguras: ~250px libres arriba y abajo. Las interactivas dejan un hueco() para el sticker.
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

HIST = [
# Lunes 16: 10:30 y 19:30 (las dos automáticas)
('2026-11-16-a-historia-primera-venta', 'papel', '<div class="eye">Post nuevo</div><h1>De la idea a tu<br><em>primera venta</em></h1>' + foto(f'{OUT}/2026-11-16-post-idea-primera-venta.png', 560, 700) + cta('Guardalo 📌')),
('2026-11-16-b-historia-validar', 'verde', f'''{ilu('lupa', 320)}<div class="eye">Validá sin gastar</div><h1>3 preguntas para<br>hacerle a quien<br><em>te compraría</em></h1>''' + lista([('1','¿Lo comprarías? ¿Para qué lo usarías?'),('2','¿Cuánto pagarías por esto?'),('3','¿Dónde lo buscarías o lo comprarías hoy?')]) + '<p class="pista">Hacéselas a 10 personas y anotá las respuestas.</p>'),
# Martes 17: 12:00 y 18:30
('2026-11-17-a-historia-tabla-excel', 'mostaza', f'''{ilu('checklist', 320)}<div class="eye">Atajo de Excel</div><h1>Convertí tu lista<br>en <em>tabla</em></h1><div class="caja">Parate en cualquier celda de tu lista y apretá <b>Ctrl + T</b>. Te quedan filtros en cada columna y la tabla crece sola cuando sumás filas.</div>'''),
('2026-11-17-b-historia-formula', 'verde', '<div class="eye">Post nuevo</div><h1>La fórmula que<br>no sabés, <em>pedísela<br>a la IA</em></h1>' + foto(f'{OUT}/2026-11-17-post-formula-excel-ia.png', 540, 675) + cta('Copiá el prompt 📌')),
# Miércoles 18: 10:30 y 19:30
('2026-11-18-a-historia-planes', 'verde', '<div class="eye">Post nuevo</div><h1>¿Qué plan<br>te <em>conviene?</em></h1>' + foto(f'{OUT}/2026-11-18-post-que-plan-te-conviene.png', 560, 700) + cta('Link en la bio')),
('2026-11-18-b-historia-test-perfil', 'papel', f'''{ilu('encuesta', 320)}<div class="eye">Recurso gratis</div><h1>Descubrí tu<br><em>perfil de<br>competencias</em></h1><p class="sub">10 preguntas. Te dice si sos Conector/a, Organizador/a, Creativo/a o Resolutivo/a, tus fortalezas y cómo contarlo en el CV y la entrevista.</p><div class="pill cta" style="font-size:36px">visionalfa.github.io/perfil.html</div><p class="pista">Es orientativo, no es un test psicológico.</p>'''),
# Jueves 19: 12:00 y 18:30
('2026-11-19-a-historia-prompt-web', 'mostaza', f'''{ilu('robot', 320)}<div class="eye">Prompt para copiar</div><h1>El primer pedido<br>para <em class="v">tu web</em></h1><div class="caja">“Tengo un emprendimiento de <b>[rubro]</b>. Armame la estructura de una web de una sola página: qué secciones lleva, un texto corto para cada una y un botón para escribirme por WhatsApp.”</div>'''),
('2026-11-19-b-historia-antes-web', 'papel', '<div class="eye">Post nuevo</div><h1>Antes de pedirle<br>tu web a la IA</h1>' + foto(f'{OUT}/2026-11-19-post-antes-de-tu-web.png', 560, 700) + cta('Revisá tu lista 📌')),
# Viernes 20: 10:30 y 19:30
('2026-11-20-a-historia-acompanamiento', 'verde', '<div class="eye">Acompañamiento de 8 horas</div><h1>Tu web,<br>armada <em>juntos</em></h1>' + foto(f'{OUT}/2026-11-20-post-web-acompanamiento.png', 560, 700) + cta('$250.000 · Link en la bio')),
('2026-11-20-b-historia-como-se-reserva', 'papel', f'''{ilu('laptop', 320)}<div class="eye">Acompañamiento de 8 horas</div><h1>Cómo se<br><em>reserva</em></h1>''' + lista([('1','Reservás y pagás la primera reunión en la agenda de la web'),('2','Las siguientes las reservás con el mismo mail, sin cargo'),('3','Hasta completar las 8 horas')]) + '<p class="pista">¿Dudas? Contame por mensaje.</p>'),
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
'2026-11-18-reel-ia-cliente': [
 (0.0, 3.0, '#1F3D2B', rilu('robot', 420) + '<div class="eye">Probalo con tu producto</div><h1>Pedile a la IA<br>que haga de<br><em>tu cliente</em></h1>'),
 (3.0, 6.0, '#F4F3EE', '<div class="letra">1</div><h1 class="dark">Contale qué<br><em>vendés</em></h1><p class="sub dark">Producto, precio y para quién es.</p>'),
 (6.0, 9.0, '#E3A82B', '<div class="letra v">2</div><h1 class="dark">Pedile que<br>sea un cliente<br><em class="v">que duda</em></h1><p class="sub dark">“¿Qué me preguntarías antes de comprar?”</p>'),
 (9.0, 12.0, '#F4F3EE', '<div class="letra">3</div><h1 class="dark">Anotá sus<br><em>dudas</em></h1><p class="sub dark">Y prepará una respuesta corta para cada una.</p>'),
 (12.0, 15.0, '#1F3D2B', rilu('libros', 340) + '<h1>Más prompts<br><em>listos para copiar</em></h1><p class="sub">En los ebooks de Visión Alfa</p><div class="cta">Link en la bio</div>'),
],
'2026-11-21-reel-web-que-venda': [
 (0.0, 3.0, '#1F3D2B', rilu('pantallas', 440) + '<div class="eye">Tu web de ventas</div><h1>3 cosas que<br>tu web tiene<br><em>que tener</em></h1>'),
 (3.0, 6.0, '#F4F3EE', '<div class="letra">1</div><h1 class="dark">Qué vendés y<br><em>a qué precio</em></h1><p class="sub dark">A la vista, sin tener que preguntar.</p>'),
 (6.0, 9.0, '#E3A82B', '<div class="letra v">2</div><h1 class="dark">Un botón<br>para <em class="v">pagar</em></h1><p class="sub dark">La mía cobra con Mercado Pago.</p>'),
 (9.0, 12.0, '#F4F3EE', '<div class="letra">3</div><h1 class="dark">Cómo<br><em>escribirte</em></h1><p class="sub dark">WhatsApp o mail, fácil de encontrar.</p>'),
 (12.0, 15.0, '#1F3D2B', rilu('laptop', 340) + '<h1>Armala con IA,<br><em>paso a paso</em></h1><p class="sub">Ebook N.º 7<br>Tu web de ventas con IA</p><div class="cta">Link en la bio</div>'),
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
