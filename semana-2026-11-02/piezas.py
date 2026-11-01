# PowerFit · semana 2 al 8 de noviembre de 2026.
# La semana ya estaba casi completa en Metricool (Cyber + semana-2026-11-06); solo faltaba la historia del jueves 5/11 13:38.
# Reusa estilos de semana-2026-11-06/piezas.py (que se apoya en cyber-2026/piezas.py).
# Uso: python3 piezas.py <salida>
import os, sys, importlib.util
from playwright.sync_api import sync_playwright

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.join(AQUI, '..')
sp = importlib.util.spec_from_file_location('sem', os.path.join(RAIZ, 'semana-2026-11-06', 'piezas.py'))
S = importlib.util.module_from_spec(sp); sp.loader.exec_module(S)
P = S.P

from PIL import Image
import io, base64
def recorte(ruta, caja, ancho=1100):
    im = Image.open(ruta).convert('RGB').crop(caja)
    im.thumbnail((ancho, ancho * 2))
    b = io.BytesIO(); im.save(b, 'JPEG', quality=90)
    return 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()

FOTO = recorte(os.path.join(RAIZ, 'fotos-reales', 'st_4027_profe_plancha.jpg'), (0, 400, 900, 1557))

P.CSS += '''
.marco{position:relative;z-index:3;margin-top:44px;flex:none;border-radius:34px;overflow:hidden;height:700px;background-size:100% 100%;border:2px solid rgba(43,123,255,.55);box-shadow:0 30px 70px rgba(0,0,0,.45)}
'''

HIST = {
 '2026-11-05-a-historia': ('oscuro',
   '<div class="eye" style="margin-top:40px">Antes de arrancar</div>'
   '<h1 style="font-size:132px;white-space:nowrap">Primero,<br><em>te conocemos</em></h1>'
   '<p class="sub" style="font-size:38px">En tu primera clase la profe hace una evaluación previa y, según cada caso, te pedimos apto médico. Así arma el plan para vos.</p>'
   f'<div class="marco" style="background-image:url({FOTO})"></div>' + S.H),
}

if __name__ == '__main__':
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={'width': 1080, 'height': 1920})
        for k, (est, cuerpo) in HIST.items():
            pg.set_content(P.html(S.pieza('hist', est, cuerpo))); pg.wait_for_timeout(250)
            pg.locator('.pz').screenshot(path=f'{out}/{k}.png')
            sz = pg.evaluate("(()=>{const z=document.querySelector('.pz');return [z.scrollHeight,z.clientHeight]})()")
            if sz[0] > sz[1] + 2: print('DESBORDA', k, sz)
        b.close()
    print('ok')
