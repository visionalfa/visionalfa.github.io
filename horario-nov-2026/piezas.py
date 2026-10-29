# Aviso de nuevo horario de tarde (desde noviembre 2026). Reusa el estilo de cyber-2026/piezas.py
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'cyber-2026'))
from piezas import pieza, html, CSS
from playwright.sync_api import sync_playwright

FILAS = '''<div style="margin-top:44px">
<div class="paso"><b style="min-width:230px">MAÑANA</b><span><strong>9 a 11 h</strong> · sigue igual</span></div>
<div class="paso"><b style="min-width:230px">TARDE</b><span><strong>16 a 21 h</strong> · nuevo</span></div>
</div>'''
FILAS_AZUL = FILAS.replace('class="paso"', 'class="paso" style="border-top-color:rgba(255,255,255,.35)"').replace('<b style="', '<b style="color:#07090D;')

PIEZAS = {
 '2026-10-29-post-horario': ('post', 'claro', '<div class="eye" style="margin-top:80px">Desde noviembre</div><h1>Nuevo horario<br>de <em>tarde</em></h1><p class="sub">Con el calor, movemos la tarde. A la mañana seguimos igual.</p>' + FILAS + '<div class="hueco"></div><div class="linea"></div><div class="pie" style="margin-top:28px"><span>Córdoba 340 · Cipolletti</span><span class="boton">Reservá desde la bio</span></div>'),
 '2026-10-30-historia-horario': ('hist', 'azul', '<div class="eye" style="margin-top:120px">Desde noviembre</div><h1>Nuevo<br>horario<br>de <em>tarde</em></h1><p class="sub">Por el calor, movemos la tarde. A la mañana seguimos igual.</p>' + FILAS_AZUL + '<div class="hueco"></div>'),
 '2026-11-01-historia-horario': ('hist', 'claro', '<div class="eye" style="margin-top:120px">Desde mañana</div><h1 style="font-size:150px">A la tarde,<br>de <em>16 a 21</em></h1><p class="sub">A la mañana, todo igual: de 9 a 11.</p><div class="hueco"></div><div class="linea"></div>'),
}

if __name__ == '__main__':
    out = os.path.dirname(os.path.abspath(__file__))
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        for k, (tipo, est, cuerpo) in PIEZAS.items():
            pg = b.new_page(viewport={'width': 1080, 'height': 1920 if tipo == 'hist' else 1350})
            pg.set_content(html(pieza(tipo, est, cuerpo))); pg.wait_for_timeout(200)
            pg.locator('.pz').screenshot(path=f'{out}/{k}.png')
        b.close()
    print('ok')
