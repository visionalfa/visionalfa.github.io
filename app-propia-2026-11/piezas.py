# PowerFit · lanzamiento de la app propia de turnos (desde el lunes 16/11/2026).
# Reusa los estilos de semana-2026-11-06/piezas.py (que a su vez usa cyber-2026/piezas.py).
# Las pantallas del celu son capturas reales de la app con datos de prueba (alumna ficticia "Sofía").
# Uso: python3 piezas.py <salida>
import os, sys, base64, importlib.util
from playwright.sync_api import sync_playwright

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.join(AQUI, '..')
sp = importlib.util.spec_from_file_location('sem', os.path.join(RAIZ, 'semana-2026-11-06', 'piezas.py'))
S = importlib.util.module_from_spec(sp); sp.loader.exec_module(S)
P, H = S.P, S.H
FR = os.path.join(RAIZ, 'fotos-reales')
for n in os.listdir(FR):
    if n[:-4] not in P.F:
        P.F[n[:-4]] = (lambda r: (lambda: P.foto(r)))(os.path.join(FR, n))

def b64(n):
    return 'data:image/png;base64,' + base64.b64encode(open(os.path.join(AQUI, n), 'rb').read()).decode()

P.CSS += '''
.cel{position:relative;z-index:3;width:400px;height:760px;border-radius:58px;background:#05070B;padding:16px;box-shadow:0 30px 70px rgba(0,0,0,.55),0 0 0 3px #22304A;margin:0 auto}
.cel div{width:100%;height:100%;border-radius:44px;background-size:100% auto;background-position:top;background-repeat:no-repeat;background-color:#07090D}
.hist .cel{width:380px;height:730px}
.post .cel{width:380px;height:740px;margin:0}
.fila{display:flex;gap:44px;align-items:center;position:relative;z-index:3}
.fila .txt{flex:1}
.pasos{position:relative;z-index:3;margin-top:40px;display:flex;flex-direction:column;gap:26px}
.pasos div{border-radius:26px;padding:30px 34px;font-size:38px;line-height:1.3;font-weight:500}
.claro .pasos div{background:#fff;border:2px solid #1565FF;color:#0B0D12}
.pasos b{display:block;font-weight:800;margin-bottom:6px}
'''
CEL = lambda n: f'<div class="cel"><div style="background-image:url({b64(n)})"></div></div>'
PIE = '<div class="pie" style="margin-top:36px"><span>Córdoba 340 · Cipolletti</span><span class="boton">{}</span></div>'

POSTS = {
 '2026-11-14-post-app-1': ('foto', H + '<div class="eye">Desde el lunes 16</div><h1>Tenemos<br>nuestra<br><em>propia app</em></h1><p class="sub">Tus turnos, tu plan y tus clases, en el celu.</p><div class="pie" style="margin-top:40px"><span>Deslizá</span><span class="boton">Ver más →</span></div>', 'ft_6734_grupo_profe', '50% 30%'),
 '2026-11-14-post-app-2': ('oscuro', '<div class="eye" style="margin-top:30px">Reservar es así de fácil</div><div class="fila" style="margin-top:40px"><div class="txt"><h1 style="font-size:118px">Elegís<br>día y<br><em>horario</em></h1><p class="sub" style="font-size:32px">Y si te surge algo, lo cambiás o lo cancelás hasta 1 hora antes.</p></div>' + CEL('cel-reservar.png') + '</div>' + PIE.format('Desde el lunes'), None, None),
 '2026-11-14-post-app-3': ('claro', '<div class="eye" style="margin-top:30px">Todo a la vista</div><div class="fila" style="margin-top:40px"><div class="txt"><h1 style="font-size:118px">Tus<br>clases<br>y tu <em>plan</em></h1><p class="sub" style="font-size:32px">Cuántas clases te quedan, cuándo vence tu plan y tus próximos turnos.</p></div>' + CEL('cel-inicio.png') + '</div>' + PIE.format('Desde el lunes'), None, None),
 '2026-11-14-post-app-4': ('foto', H + '<div class="eye">¿Cómo entro?</div><h1>Revisá<br>tu <em>mail</em></h1><p class="sub">Te mandamos el link por mail y por WhatsApp. Entrá con el mismo mail que nos diste. ¿No te llegó? Escribinos.</p>' + PIE.format('WhatsApp →'), 'wa_profe_muestra_colchoneta_1', '50% 30%'),
}
HIST = {
 '2026-11-14-historia-app': ('foto', H + '<div class="eye">Desde el lunes 16</div><h1>Tus turnos<br>en nuestra<br><em>app</em></h1><p class="sub">Revisá tu mail: ahí está el link para entrar.</p>', 'ft_6726_selfie_traje', '50% 25%'),
 '2026-11-16-a-historia-app': ('oscuro', '<div class="eye" style="margin-top:70px">Hoy arranca</div><h1 style="font-size:150px">Reservá<br>desde la <em>app</em></h1><p class="sub">Entrá con el link que te mandamos.</p><div style="margin-top:24px">' + CEL('cel-inicio.png') + '</div>', None, None),
 '2026-11-16-b-historia-app': ('claro', '<div class="eye" style="margin-top:40px">Un tip</div><h1>Guardala<br>en tu <em>celu</em></h1><div class="pasos"><div><b>iPhone</b>Abrila en Safari, tocá Compartir y después “Agregar a inicio”.</div><div><b>Android</b>Abrila en Chrome, tocá los tres puntitos y después “Agregar a pantalla principal”.</div></div><p class="sub">Así la abrís como cualquier app, con un toque.</p>', None, None),
}

if __name__ == '__main__':
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        for tabla, tipo, h in ((POSTS, 'post', 1350), (HIST, 'hist', 1920)):
            pg = b.new_page(viewport={'width': 1080, 'height': h})
            for k, (est, cuerpo, img, pos) in tabla.items():
                pg.set_content(P.html(S.pieza(tipo, est, cuerpo, img, pos))); pg.wait_for_timeout(300)
                pg.locator('.pz').screenshot(path=f'{out}/{k}.png')
                sz = pg.evaluate("(()=>{const z=document.querySelector('.pz');return [z.scrollHeight,z.clientHeight]})()")
                if sz[0] > sz[1] + 2: print('DESBORDA', k, sz)
        b.close()
    print('ok')
