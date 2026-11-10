# Versiones con foto real de fondo de piezas ya programadas que eran de fondo liso
# (pedido de Flor 10/11: mechar fondos lisos con fotos para que el feed se vea más real).
# Fotos: cuadros y fotos nuevas del Drive, variando personas (pedido de Flor: no siempre las mismas).
# Uso: python3 piezas_con_fotos.py <salida>
import os, sys, importlib.util
from playwright.sync_api import sync_playwright

AQUI = os.path.dirname(os.path.abspath(__file__))
sp = importlib.util.spec_from_file_location('sem', os.path.join(AQUI, 'piezas.py'))
S = importlib.util.module_from_spec(sp); sp.loader.exec_module(S)
P, H = S.P, S.H
FR = os.path.join(AQUI, '..', 'fotos-reales')
for n in os.listdir(FR):
    if n.startswith('st_') and n[:-4] not in P.F:
        P.F[n[:-4]] = (lambda r: (lambda: P.foto(r)))(os.path.join(FR, n))

POSTS = {
 '2026-11-13-post-preguntas-1-foto': ('foto', H + '<div class="eye">Antes de tu primera clase</div><h1>Lo que más<br>nos <em>preguntan</em></h1><div class="pie" style="margin-top:40px"><span>Deslizá</span><span class="boton">Ver respuestas →</span></div>', 'wa_profe_explica_equilibrio_pared_3', '50% 35%'),
 '2026-11-13-post-preguntas-5-foto': ('foto', H + '<div class="eye">¿Te quedó otra duda?</div><h1>Probalo<br><em>gratis</em></h1><p class="sub">Tocá el link de la bio, completá el formulario y elegí tu horario.</p>' + S.PIE.format('Reservá tu clase →').replace('class="pie"', 'class="pie" style="margin-top:40px"'), 'ft_9aab_dos_alumnas', '50% 60%'),
 'electrofitness-y-running-1-foto': ('foto', H + '<div class="eye">Serie · Electrofitness y…</div><h1>Electrofitness<br>y <em>running</em></h1><p class="sub">Si salís a correr, esto te puede ayudar a correr mejor y a llegar con más piernas a la próxima salida.</p><div class="pie" style="margin-top:40px"><span>Deslizá</span><span class="boton">Ver más →</span></div>', 'wa_bisagra_una_pierna_pared_3', '50% 55%'),
 'electrofitness-y-running-5-foto': ('foto', H + '<div class="eye">PowerFit</div><h1>No reemplaza<br>tus <em>salidas</em></h1><p class="sub">Las complementa. 20 minutos, una o dos veces por semana, y la profe arma el plan según cómo venís corriendo.</p><div class="pie" style="margin-top:40px"><span>Córdoba 340 · Cipolletti</span><span class="boton">Clase gratis →</span></div>', 'st_4030_profe_press', '50% 30%'),
}
HIST = {
 '2026-11-10-b-historia-foto': ('foto', H + '<div class="eye">Suscripciones</div><h1>Siguen<br>con <em>descuento</em></h1><p class="sub">Cada 2 meses, 15% menos. Cada 3 meses, 20% menos. Pedinos el link por WhatsApp.</p>' + S.SOCIO, 'wa_c522_sonrisa_profe', '50% 25%'),
 '2026-11-11-b-historia-foto': ('foto', H + '<div class="eye">Para arrancar</div><h1>Reservá tu<br>clase <em>gratis</em></h1><p class="sub">Tocá el link, completá el formulario y elegí tu horario.</p>', 'st_4030_profe_al_lado', '50% 30%'),
 '2026-11-12-a-historia-foto': ('foto', H + '<div class="eye">Encuesta</div><h1>¿Cuándo<br>entrenás<br><em>mejor?</em></h1><div style="height:260px"></div>', 'st_7cb4_abdominales_ventanal', '50% 40%'),
 '2026-11-13-b-historia-foto': ('foto', H + '<div class="eye">La semana que viene</div><h1>¿Arrancás<br><em>con nosotras?</em></h1><p class="sub">La primera clase es gratis. Link en la bio.</p>', 'wa_c522_kettle_arriba', '50% 20%'),
}

if __name__ == '__main__':
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        for tabla, tipo, h in ((POSTS, 'post', 1350), (HIST, 'hist', 1920)):
            pg = b.new_page(viewport={'width': 1080, 'height': h})
            for k, (est, cuerpo, img, pos) in tabla.items():
                pg.set_content(P.html(S.pieza(tipo, est, cuerpo, img, pos))); pg.wait_for_timeout(250)
                pg.locator('.pz').screenshot(path=f'{out}/{k}.png')
                sz = pg.evaluate("(()=>{const z=document.querySelector('.pz');return [z.scrollHeight,z.clientHeight]})()")
                if sz[0] > sz[1] + 2: print('DESBORDA', k, sz)
        b.close()
    print('ok')
