# Agrega el beneficio Club Cipolletti a las piezas del Cyber. Uso: python3 socios.py <salida>
import os, sys, importlib.util
sp = importlib.util.spec_from_file_location('piezas', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'piezas.py'))
P = importlib.util.module_from_spec(sp); sp.loader.exec_module(P)
from playwright.sync_api import sync_playwright
import base64
from PIL import Image
import io as _io
_e=Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','club','escudo-club-cipolletti.png')).convert('RGBA'); _e.thumbnail((400,400)); _b=_io.BytesIO(); _e.save(_b,'PNG')
ESCUDO='data:image/png;base64,'+base64.b64encode(_b.getvalue()).decode()

P.CSS += '''
.socio{position:relative;z-index:3;display:flex;gap:22px;align-items:center;border-radius:22px;padding:22px 28px;margin-top:34px;font-size:27px;line-height:1.3;font-weight:500}
.socio img{height:96px;width:auto;flex:none;filter:drop-shadow(0 2px 6px rgba(0,0,0,.25))}
.socio .pct{color:inherit}
.socio b{font-weight:800;display:block}
.hist .socio{font-size:32px;padding:26px 32px}.hist .socio img{height:112px}
.azul .socio{background:rgba(7,9,13,.24);border:2px solid rgba(255,255,255,.55);color:#fff}.azul .socio .pct{color:#fff}
.claro .socio{background:#fff;border:2px solid #1565FF;color:#0B0D12}.claro .socio .pct{color:#1565FF}
.post td{padding:18px 0}.hist td{padding:25px 0}
.foto .socio{background:rgba(7,9,13,.55);border:2px solid #2B7BFF;color:#fff}.foto .socio .pct{color:#2B7BFF}
'''
FR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'fotos-reales')
for _k in ('st_6650_caminando','st_4028_puente','st_6649_traje','st_4031_mancuernas'):
    P.F[_k] = (lambda r: (lambda: P.foto(r)))(os.path.join(FR, _k + '.jpg'))
# fotos nuevas para no repetir siempre las mismas
FOTOS = {
 '2026-10-30-post-se-viene-cyber': ('st_6650_caminando', '62% 30%'),
 '2026-11-02-post-suscripciones-4': ('st_4028_puente', '50% 45%'),
 '2026-11-03-post-whatsapp': ('st_6649_traje', '50% 35%'),
 '2026-11-03-a-historia': ('st_4031_mancuernas', '50% 25%'),
}
SOCIO = f'<div class="socio"><img src="{ESCUDO}"><span><b>¿Sos socio/a del Club Cipolletti?</b>Tenés <b style="display:inline">10% off</b> en tu primer mes presentando el carnet.<small style="display:block;opacity:.75;font-size:.8em;margin-top:4px">No acumulable con otras promociones.</small></span></div>'

def antes(c, marca):  # inserta antes de la primera aparición de marca
    i = c.index(marca); return c[:i] + SOCIO + c[i:]
def al_final(c): return c + SOCIO
def tras_sub(c):
    i = c.index('</p>', c.index('class="sub"')) + 4; return c[:i] + SOCIO + c[i:]

PM = {  # posteos
 '2026-10-30-post-se-viene-cyber': tras_sub,
 '2026-11-01-post-manana-arranca': tras_sub,
 '2026-11-02-post-suscripciones-1': tras_sub,
 '2026-11-02-post-suscripciones-3': al_final,
 '2026-11-02-post-suscripciones-4': tras_sub,
 '2026-11-03-post-whatsapp': tras_sub,
 '2026-11-04-post-para-quedarse': lambda c: tras_sub(c).replace('margin-top:300px','margin-top:240px'),
}
HM = {  # historias
 '2026-10-30-a-historia': al_final,
 '2026-10-30-b-historia': tras_sub,
 '2026-11-02-a-historia': tras_sub,
 '2026-11-02-b-historia': lambda c: antes(c, '<div class="linea">'),
 '2026-11-03-a-historia': tras_sub,
 '2026-11-04-a-historia': tras_sub,
 '2026-11-04-b-historia': lambda c: antes(c, '<div class="hueco">'),
}
out = sys.argv[1]; os.makedirs(out, exist_ok=True)
with sync_playwright() as pw:
    b = pw.chromium.launch()
    for tabla, mods, tipo, h in ((P.POSTS, PM, 'post', 1350), (P.HIST, HM, 'hist', 1920)):
        pg = b.new_page(viewport={'width': 1080, 'height': h})
        for k, f in mods.items():
            est, cuerpo, img, pos = tabla[k]
            if k in FOTOS: img, pos = FOTOS[k]
            pg.set_content(P.html(P.pieza(tipo, est, f(cuerpo), img, pos))); pg.wait_for_timeout(150)
            pg.locator('.pz').screenshot(path=f'{out}/{k}-club.png')
            sz = pg.evaluate("(()=>{const z=document.querySelector('.pz');return [z.scrollHeight,z.clientHeight]})()")
            if sz[0] > sz[1]: print('DESBORDA', k, sz)
    b.close()
print('ok')
