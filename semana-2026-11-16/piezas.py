# PowerFit · semana del 16 al 22 de noviembre de 2026.
# Reusa estilos de semana-2026-11-06/piezas.py (que usa cyber-2026/piezas.py) y las ilustraciones de la serie.
# Fotos: material nuevo del Drive subido por Flor el 14/11 (fotos-reales/d14_*).
# Uso: python3 piezas.py <salida>
import os, sys, importlib.util
from playwright.sync_api import sync_playwright

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.join(AQUI, '..')
sp = importlib.util.spec_from_file_location('sem', os.path.join(RAIZ, 'semana-2026-11-06', 'piezas.py'))
S = importlib.util.module_from_spec(sp); sp.loader.exec_module(S)
P, H = S.P, S.H
sys.path.insert(0, os.path.join(RAIZ, 'serie-electrofitness-y'))
from ilus import ILUS
FR = os.path.join(RAIZ, 'fotos-reales')
for n in os.listdir(FR):
    if n[:-4] not in P.F:
        P.F[n[:-4]] = (lambda r: (lambda: P.foto(r)))(os.path.join(FR, n))

P.CSS += '''
.ilus-h{position:absolute;z-index:2;top:250px;right:70px;width:420px;height:420px;filter:drop-shadow(0 0 30px rgba(43,123,255,.35))}
'''
PIE = '<div class="pie" style="margin-top:36px"><span>Córdoba 340 · Cipolletti</span><span class="boton">{}</span></div>'
STK = '<div style="height:330px"></div>'   # lugar libre para el sticker

POSTS = {
 '2026-11-17-post-traje-hace-todo': ('claro', '<div class="eye" style="margin-top:190px">Mitos y dudas</div><h1>¿El traje<br>hace todo<br><em>solo?</em></h1><p class="sub">No. Vos hacés movimientos simples y el traje suma estímulo a esos músculos. La profe va regulando la intensidad toda la clase.</p>' + H + '<div class="linea"></div><div class="pie" style="margin-top:28px"><span>Córdoba 340 · Cipolletti</span><span class="boton">Probalo gratis</span></div>', None, None),
 '2026-11-19-post-primera-clase': ('azul', '<div class="eye" style="margin-top:240px">Clase de prueba gratis</div><h1>Tu primera<br>clase, <em>sin<br>misterio</em></h1><p class="sub">Primero charlamos y hacemos una evaluación previa. Después te ponemos el traje y la profe arranca suave, ajustando todo a vos.</p>' + H + PIE.format('Reservá tu clase →'), None, None),
 '2026-11-20-post-que-se-siente': ('foto', H + '<div class="eye">Lo que más nos preguntan</div><h1>¿Qué se<br><em>siente?</em></h1><p class="sub">Un cosquilleo que se va poniendo más intenso. La profe regula la intensidad con vos durante toda la clase.</p>', 'd14_e195_mujer_traje_concentrada', '50% 20%'),
 '2026-11-22-post-el-lunes-arranco': ('foto', H + '<div class="eye">Domingo</div><h1>¿El lunes<br><em>arrancás?</em></h1><p class="sub">Empezá por algo corto: 20 minutos, la profe al lado y la primera clase gratis.</p>' + PIE.format('Link en la bio →'), 'd14_1471_sentadilla_barra_profe', '60% 30%'),
}

HIST = {
 '2026-11-17-a-historia': ('claro', '<div class="eye" style="margin-top:120px">Encuesta</div><h1>¿El traje<br>hace todo<br><em>solo?</em></h1>' + H + '<div class="linea"></div>', None, None),
 '2026-11-17-b-historia': ('foto', H + '<div class="eye">Mitos y dudas</div><h1>Vos te movés,<br>el traje <em>suma</em></h1><p class="sub">Movimientos simples, la profe al lado y 20 minutos.</p>', 'd14_e6c1_abdominales_mancuernas', '45% 50%'),
 '2026-11-18-a-historia': ('oscuro', '<div class="ilus-h">' + ILUS['arco']('#2B7BFF', 'rgba(43,123,255,.18)') + '</div><div style="height:520px"></div><div class="eye">Serie · Nueva entrega</div><h1>Electro<br>fitness<br>y <em>fútbol</em></h1><p class="sub">Ya está en el feed. Pasá a verla y contanos si jugás.</p>' + H, None, None),
 '2026-11-18-b-historia': ('foto', H + '<div class="eye">Encuesta</div><h1>¿Jugás al<br><em>fútbol?</em></h1>' + STK, 'd14_c032_skipping_sonrisa', '50% 30%'),
 '2026-11-19-a-historia': ('foto', H + '<div class="eye">En cada clase</div><h1>La profe<br>te <em>corrige</em></h1><p class="sub">Te muestra cada movimiento y lo ajusta a vos.</p>', 'd14_e724_profe_corrige_remo', '50% 30%'),
 '2026-11-19-b-historia': ('claro', '<div class="eye" style="margin-top:120px">Encuesta</div><h1>¿Vendrías<br>con una<br><em>amiga?</em></h1>' + H + '<div class="linea"></div>', None, None),
 '2026-11-20-a-historia': ('foto', H + '<div class="eye">Para arrancar</div><h1>Reservá tu<br>clase <em>gratis</em></h1><p class="sub">Tocá el link, completá el formulario y elegí tu horario.</p><div style="height:110px"></div>', 'd14_9d5f_step_up_mancuernas', '40% 35%'),
 '2026-11-20-b-historia': ('oscuro', '<div class="eye" style="margin-top:160px">Un tip para tu clase</div><h1>Ni con la<br>panza llena<br><em>ni vacía</em></h1><p class="sub">No conviene entrenar recién comido ni con el estómago vacío. Traé ropa cómoda y zapatillas, del resto nos encargamos.</p>' + H, None, None),
}

PORTADAS = {
 'reel-reservar-portada-claro': ('claro', H + '<div class="eye">Clase de prueba gratis</div><h1 style="font-size:190px">Reservar<br>es así de<br><em>fácil</em></h1><p class="sub">Link en la bio, formulario y elegís tu horario.</p>' + H),
}

CAPAS = {
 'r5-a': P.capa('¿Querés<br><em>probar?</em>'),
 'r5-b': P.capa('Tocás el link<br><em>de la bio</em>'),
 'r5-c': P.capa('Completás el<br><em>formulario</em>'),
 'r5-d': P.capa('Elegís tu<br><em>horario</em>'),
 'r5-fin': P.fin('Y listo,<br><em style="color:#07090D">te esperamos</em>', 'Tu primera clase es gratis. 20 minutos con la profe al lado.', 'Córdoba 340 · Cipolletti'),
}

if __name__ == '__main__':
    out = sys.argv[1]; os.makedirs(out + '/capas', exist_ok=True)
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        for tabla, tipo, h in ((POSTS, 'post', 1350), (HIST, 'hist', 1920)):
            pg = b.new_page(viewport={'width': 1080, 'height': h})
            for k, (est, cuerpo, img, pos) in tabla.items():
                pg.set_content(P.html(S.pieza(tipo, est, cuerpo, img, pos))); pg.wait_for_timeout(250)
                pg.locator('.pz').screenshot(path=f'{out}/{k}.png')
                sz = pg.evaluate("(()=>{const z=document.querySelector('.pz');return [z.scrollHeight,z.clientHeight]})()")
                if sz[0] > sz[1] + 2: print('DESBORDA', k, sz)
        pg = b.new_page(viewport={'width': 1080, 'height': 1920})
        for k, (est, cuerpo) in PORTADAS.items():
            pg.set_content(P.html(S.pieza('hist', est, cuerpo))); pg.wait_for_timeout(250)
            pg.locator('.pz').screenshot(path=f'{out}/{k}.jpg', type='jpeg', quality=92)
        for k, inner in CAPAS.items():
            pg.set_content(P.html(inner)); pg.wait_for_timeout(150)
            pg.screenshot(path=f'{out}/capas/{k}.png', omit_background=True)
        b.close()
    print('ok')
