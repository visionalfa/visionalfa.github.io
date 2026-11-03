# Feed mezclado (pedido de Flor 2/11): que blanco / azul / oscuro / foto no queden en líneas en la grilla.
# Regla: ninguna pieza del feed repite estilo con la anterior ni con la de 3 lugares antes (la de arriba en la grilla).
# Cambios: 3/11 pasa a oscuro, 10/11 a claro, y los reels del 6/11 y 14/11 llevan portada clara.
# Uso: python3 mezcla.py <salida>
import os, sys, importlib.util
from playwright.sync_api import sync_playwright
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.join(AQUI, '..')
sp = importlib.util.spec_from_file_location('sem', os.path.join(RAIZ, 'semana-2026-11-06', 'piezas.py'))
S = importlib.util.module_from_spec(sp); sp.loader.exec_module(S); P = S.P
H = S.H

POSTS = {
 '2026-11-03-post-whatsapp-oscuro': ('oscuro',
   '<div class="eye" style="margin-top:210px">Suscripciones PowerFit</div><h1>¿Dudas?<br><em>Escribinos</em></h1>'
   '<p class="sub">Te pasamos el link de tu plan por WhatsApp y te ayudamos a elegir el que más te sirve.</p>' + S.SOCIO + H +
   '<div class="pie"><span>Córdoba 340 · Cipolletti</span><span class="boton">WhatsApp en la bio →</span></div>'),
 '2026-11-10-post-se-cobra-solo-claro': ('claro',
   '<div class="eye" style="margin-top:150px">Suscripciones PowerFit</div><h1>Tu plan<br>se cobra <em>solo</em></h1>'
   '<p class="sub">Cada 2 meses, 15% menos. Cada 3 meses, 20% menos. Pedinos el link por WhatsApp.</p>' + S.SOCIO + H +
   '<div class="linea"></div><div class="pie" style="margin-top:28px"><span>Córdoba 340 · Cipolletti</span><span class="boton">WhatsApp en la bio</span></div>'),
}
PORTADAS = {
 'reel-20-minutos-portada-claro': ('claro', H + '<div class="eye">Lo que todos preguntan</div><h1 style="font-size:190px">¿20<br>minutos<br><em>alcanzan?</em></h1><p class="sub">Todo el cuerpo, con la profe al lado.</p>' + H),
 'reel-el-traje-portada-claro': ('claro', H + '<div class="eye">Cómo funciona</div><h1 style="font-size:200px">Esto es<br><em>el traje</em></h1><p class="sub">Electrodos que activan los músculos mientras te movés.</p>' + H),
}
if __name__ == '__main__':
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        for tabla, tipo, h, ext in ((POSTS, 'post', 1350, 'png'), (PORTADAS, 'hist', 1920, 'jpg')):
            pg = b.new_page(viewport={'width': 1080, 'height': h})
            for k, (est, cuerpo) in tabla.items():
                pg.set_content(P.html(S.pieza(tipo, est, cuerpo))); pg.wait_for_timeout(250)
                kw = {'type': 'jpeg', 'quality': 92} if ext == 'jpg' else {}
                pg.locator('.pz').screenshot(path=f'{out}/{k}.{ext}', **kw)
                sz = pg.evaluate("(()=>{const z=document.querySelector('.pz');return [z.scrollHeight,z.clientHeight]})()")
                if sz[0] > sz[1] + 2: print('DESBORDA', k, sz)
        b.close()
    print('ok')
