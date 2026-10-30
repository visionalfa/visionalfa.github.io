# PowerFit · semana 6 al 14 de noviembre de 2026.
# Reusa estilos de cyber-2026/piezas.py y el recuadro del Club Cipolletti de cyber-2026/socios.py.
# Uso: python3 piezas.py <salida>
import os, sys, base64, io, importlib.util
from PIL import Image
from playwright.sync_api import sync_playwright

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.join(AQUI, '..')
sp = importlib.util.spec_from_file_location('piezas', os.path.join(RAIZ, 'cyber-2026', 'piezas.py'))
P = importlib.util.module_from_spec(sp); sp.loader.exec_module(P)

FR = os.path.join(RAIZ, 'fotos-reales')
for n in os.listdir(FR):
    if n.startswith('ft_'):
        P.F[n[:-4]] = (lambda r: (lambda: P.foto(r)))(os.path.join(FR, n))

_e = Image.open(os.path.join(RAIZ, 'club', 'escudo-club-cipolletti.png')).convert('RGBA')
_b = io.BytesIO(); _e.save(_b, 'PNG')
ESCUDO = 'data:image/png;base64,' + base64.b64encode(_b.getvalue()).decode()

P.CSS += '''
.socio{position:relative;z-index:3;display:flex;gap:22px;align-items:center;border-radius:22px;padding:22px 28px;margin-top:34px;font-size:27px;line-height:1.3;font-weight:500}
.socio img{height:96px;width:auto;flex:none;filter:drop-shadow(0 2px 6px rgba(0,0,0,.25))}
.socio b{font-weight:800;display:block}
.hist .socio{font-size:32px;padding:26px 32px}.hist .socio img{height:112px}
.azul .socio{background:rgba(7,9,13,.24);border:2px solid rgba(255,255,255,.55);color:#fff}
.claro .socio{background:#fff;border:2px solid #1565FF;color:#0B0D12}
.foto .socio{background:rgba(7,9,13,.55);border:2px solid #2B7BFF;color:#fff}
.escudo-xl{position:relative;z-index:3;height:430px;width:auto;filter:drop-shadow(0 18px 40px rgba(0,0,0,.35))}
.hist .escudo-xl{height:520px}
.faq-n{font-family:'Inter Display';font-style:italic;font-weight:900;font-size:120px;color:#1565FF;line-height:1;position:relative;z-index:3}
.oscuro{background:radial-gradient(120% 80% at 80% 10%,#123A8F 0%,#0A1530 45%,#07090D 100%);color:#fff}
.oscuro .bg-r{position:absolute;right:-220px;top:220px;width:900px;height:1125px;fill:rgba(43,123,255,.12);z-index:1}
.oscuro h1 em{font-style:italic;color:#2B7BFF}
.oscuro .eye{color:#8EB6FF}
.oscuro .boton{background:#1565FF;color:#fff}
.oscuro .marca .r{fill:#2B7BFF}
.oscuro .socio{background:rgba(255,255,255,.06);border:2px solid #2B7BFF;color:#fff}
'''
_pieza = P.pieza
def pieza(tipo, estilo, cuerpo, img=None, pos='center'):
    if estilo == 'oscuro':
        bg = '<svg viewBox="0 0 40 50" class="bg-r"><path d="M26 1 L5 29 L18 29 L13 49 L35 19 L22 19 Z"/></svg>'
        return f'<div class="pz {tipo} oscuro">{bg}{P.marca()}{cuerpo}</div>'
    return _pieza(tipo, estilo, cuerpo, img, pos)

SOCIO = f'<div class="socio"><img src="{ESCUDO}"><span><b>¿Sos socio/a del Club Cipolletti?</b>Tenés <b style="display:inline">10% off</b> en tu primer mes presentando el carnet.<small style="display:block;opacity:.75;font-size:.8em;margin-top:4px">No acumulable con otras promociones.</small></span></div>'
H = '<div class="hueco"></div>'
PIE = '<div class="pie"><span>Córdoba 340 · Cipolletti</span><span class="boton">{}</span></div>'

POSTS = {
 '2026-11-06-post-solo-20-minutos': ('foto', H + '<div class="eye">Lo que todos dicen</div><h1>¿Solo<br><em>20 minutos?</em></h1><p class="sub">Eso piensan antes de probar. Después de la primera clase nos cuentan otra cosa.</p>', 'ft_6732_barra_arriba', '50% 30%'),
 '2026-11-08-post-todo-el-cuerpo': ('claro', '<div class="eye" style="margin-top:200px">Cómo funciona</div><h1>Todo el<br>cuerpo<br><em>a la vez</em></h1><p class="sub">Los electrodos del traje activan los músculos mientras hacés movimientos simples. Por eso 20 minutos rinden tanto.</p>' + H + '<div class="linea"></div><div class="pie" style="margin-top:28px"><span>Córdoba 340 · Cipolletti</span><span class="boton">Probalo gratis</span></div>', None, None),
 '2026-11-09-post-para-hombres': ('foto', H + '<div class="eye">Una duda que llega seguido</div><h1>¿Es solo para<br><em>mujeres?</em></h1><p class="sub">Para nada. Viene gente muy distinta, y la profe arma el entrenamiento según cada persona.</p>', 'ft_6731_barra_sonrisa', '50% 22%'),
 '2026-11-10-post-se-cobra-solo': ('foto', H + '<h1>Tu plan<br>se cobra<br><em>solo</em></h1><p class="sub">Cada 2 meses, 15% menos. Cada 3 meses, 20% menos. Pedinos el link por WhatsApp.</p>' + SOCIO, 'ft_6735_kettle_noche', '50% 48%'),
 '2026-11-11-post-no-entrenas-sola': ('foto', H + '<div class="eye">Grupos de hasta 3</div><h1>No entrenás<br><em>sola</em></h1><p class="sub">La profe está al lado toda la clase: te corrige, ajusta la intensidad y te acompaña a tu ritmo.</p>', 'ft_6723_profe_explica', '50% 28%'),
 '2026-11-12-post-club-cipolletti': ('azul', f'<div class="eye" style="margin-top:70px">Beneficio para socios</div><div style="display:flex;justify-content:center;margin-top:40px"><img class="escudo-xl" src="{ESCUDO}"></div><h1 style="font-size:124px;margin-top:40px">¿Sos socio/a del<br><em>Club Cipolletti?</em></h1><p class="sub">Tenés 10% off en tu primer mes presentando el carnet.<br><span style="font-size:.7em;opacity:.8">No acumulable con otras promociones.</span></p>' + H, None, None),
 '2026-11-13-post-preguntas-1': ('oscuro', '<div class="eye" style="margin-top:300px">Antes de tu primera clase</div><h1>Lo que más<br>nos<br><em>preguntan</em></h1>' + H + '<div class="pie"><span>Deslizá</span><span class="boton">Ver respuestas →</span></div>', None, None),
 '2026-11-13-post-preguntas-2': ('claro', '<div class="faq-n" style="margin-top:220px">01</div><h1 style="font-size:132px">¿Necesito<br><em>experiencia?</em></h1><p class="sub">No. La profe te va guiando desde el primer minuto, aunque nunca hayas entrenado.</p>' + H + '<div class="linea"></div>', None, None),
 '2026-11-13-post-preguntas-3': ('claro', '<div class="faq-n" style="margin-top:220px">02</div><h1 style="font-size:132px">¿Qué tengo<br>que <em>traer?</em></h1><p class="sub">Ropa cómoda y zapatillas. Del resto nos encargamos nosotras.</p>' + H + '<div class="linea"></div>', None, None),
 '2026-11-13-post-preguntas-4': ('claro', '<div class="faq-n" style="margin-top:220px">03</div><h1 style="font-size:132px">¿Cuántas veces<br>por <em>semana?</em></h1><p class="sub">Una, dos o tres. Lo charlamos según lo que busques y cómo te vayas sintiendo.</p>' + H + '<div class="linea"></div>', None, None),
 '2026-11-13-post-preguntas-5': ('oscuro', '<div class="eye" style="margin-top:300px">¿Te quedó otra duda?</div><h1>Probalo<br><em>gratis</em></h1><p class="sub">Tocá el link de la bio, completá el formulario y elegí tu horario.</p>' + H + PIE.format('Reservá tu clase →'), None, None),
}

HIST = {
 '2026-11-06-a-historia': ('claro', '<div class="eye" style="margin-top:120px">Encuesta</div><h1>¿Ya probaste<br><em>electro<br>fitness?</em></h1>' + H + '<div class="linea"></div>', None, None),
 '2026-11-06-b-historia': ('foto', H + '<div class="eye">Así queda el traje</div><h1>Listo para<br><em>arrancar</em></h1><p class="sub">Vos venís con ropa cómoda. El traje te lo ponemos acá.</p>', 'ft_6726_selfie_traje', '45% 40%'),
 '2026-11-09-a-historia': ('foto', H + '<div class="eye">Lunes</div><h1>Arrancamos<br>la <em>semana</em></h1><p class="sub">¿Y vos? La primera clase es gratis.</p>', 'ft_6725_discos', '50% 30%'),
 '2026-11-09-b-historia': ('azul', '<div class="eye" style="margin-top:120px">Contanos</div><h1>¿Qué te<br>gustaría<br><em>saber?</em></h1>' + H, None, None),
 '2026-11-10-a-historia': ('claro', '<div class="eye" style="margin-top:120px">Sincerate</div><h1 style="font-size:150px">¿Cuántas<br>ganas tenés<br>de <em>arrancar?</em></h1>' + H + '<div class="linea"></div>', None, None),
 '2026-11-10-b-historia': ('oscuro', '<div class="eye" style="margin-top:120px">Suscripciones</div><h1>Siguen<br>con <em>descuento</em></h1><p class="sub">Cada 2 meses, 15% menos. Cada 3 meses, 20% menos. Pedinos el link por WhatsApp.</p>' + SOCIO + H, None, None),
 '2026-11-11-a-historia': ('foto', H + '<div class="eye">PowerFit</div><h1>¿Te<br><em>sumás?</em></h1><p class="sub">La primera clase es gratis. Link en la bio.</p>', 'ft_6724_parada', '50% 25%'),
 '2026-11-11-b-historia': ('claro', '<div class="eye" style="margin-top:120px">Para arrancar</div><h1>Reservá tu<br>clase<br><em>gratis</em></h1><p class="sub">Tocá el link, completá el formulario y elegí tu horario.</p>' + H + '<div class="linea"></div>', None, None),
 '2026-11-12-a-historia': ('azul', '<div class="eye" style="margin-top:120px">Encuesta</div><h1>¿Cuándo<br>entrenás<br><em>mejor?</em></h1>' + H, None, None),
 '2026-11-12-b-historia': ('foto', H + '<div class="eye">En cada clase</div><h1>La profe<br><em>ajusta todo</em></h1><p class="sub">La intensidad se va regulando durante la clase. Vos vas a tu ritmo.</p>', 'ft_6728_kettle_profe', '40% 25%'),
 '2026-11-13-a-historia': ('azul', f'<div class="eye" style="margin-top:100px">Beneficio para socios</div><div style="display:flex;justify-content:center;margin-top:40px"><img class="escudo-xl" src="{ESCUDO}"></div><h1 style="font-size:130px;margin-top:40px">Socios del<br><em>Club Cipolletti</em></h1><p class="sub">10% off en tu primer mes presentando el carnet.<br><span style="font-size:.7em;opacity:.8">No acumulable con otras promociones.</span></p>' + H, None, None),
 '2026-11-13-b-historia': ('oscuro', '<div class="eye" style="margin-top:120px">La semana que viene</div><h1>¿Arrancás<br><em>con nosotras?</em></h1>' + H, None, None),
}

def capa_fin(h, sub, boton):
    return P.fin(h, sub, boton)

CAPAS = {
 'r3-a': P.capa('Así es una<br>clase en <em>PowerFit</em>'),
 'r3-b': P.capa('Hasta <em>3 personas</em>'),
 'r3-c': P.capa('La profe<br><em>siempre al lado</em>'),
 'r3-d': P.capa('20 minutos<br><em>y listo</em>'),
 'r3-fin': P.fin('¿Te sumás a<br>la <em style="color:#07090D">próxima?</em>', 'Tu primera clase es gratis. Reservala desde el link de la bio.', 'Córdoba 340 · Cipolletti'),
 'r4-a': P.capa('Esto es<br><em>el traje</em>'),
 'r4-b': P.capa('Electrodos que<br><em>activan</em> los músculos'),
 'r4-c': P.capa('Movimientos<br><em>simples</em>'),
 'r4-d': P.capa('Todo el cuerpo<br><em>trabajando</em>'),
 'r4-fin': P.fin('Probalo<br><em style="color:#07090D">gratis</em>', 'Link en la bio. Completás el formulario y elegís tu horario.', 'Córdoba 340 · Cipolletti'),
}

if __name__ == '__main__':
    out = sys.argv[1]; os.makedirs(out + '/capas', exist_ok=True)
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        for tabla, tipo, h in ((POSTS, 'post', 1350), (HIST, 'hist', 1920)):
            pg = b.new_page(viewport={'width': 1080, 'height': h})
            for k, (est, cuerpo, img, pos) in tabla.items():
                pg.set_content(P.html(pieza(tipo, est, cuerpo, img, pos))); pg.wait_for_timeout(200)
                pg.locator('.pz').screenshot(path=f'{out}/{k}.png')
                sz = pg.evaluate("(()=>{const z=document.querySelector('.pz');return [z.scrollHeight,z.clientHeight]})()")
                if sz[0] > sz[1] + 2: print('DESBORDA', k, sz)
        pg = b.new_page(viewport={'width': 1080, 'height': 1920})
        for k, inner in CAPAS.items():
            pg.set_content(P.html(inner)); pg.wait_for_timeout(150)
            pg.screenshot(path=f'{out}/capas/{k}.png', omit_background=True)
        b.close()
    print('ok')
