# Serie "Electrofitness y…": carrusel de 5 placas por tema.
# Uso: python3 piezas.py <tema> <salida>   (tema = clave de TEMAS)
import os, sys, importlib.util
from playwright.sync_api import sync_playwright

AQUI = os.path.dirname(os.path.abspath(__file__))
sp = importlib.util.spec_from_file_location('sem', os.path.join(AQUI, '..', 'semana-2026-11-06', 'piezas.py'))
S = importlib.util.module_from_spec(sp); sp.loader.exec_module(S)
P = S.P

P.CSS += '''
.serie{font-family:'Inter Display';font-style:italic;font-weight:900;text-transform:uppercase;letter-spacing:.02em;font-size:30px;color:#8EB6FF;position:relative;z-index:3}
.claro .serie{color:#1565FF}
.dato{position:relative;z-index:3;margin-top:36px;padding:22px 28px;border-left:6px solid #1565FF;background:rgba(21,101,255,.07);font-size:27px;line-height:1.35;font-weight:500;color:#2A2F3A}
.dato b{font-weight:800;color:#0B0D12}
.nro{font-family:'Inter Display';font-style:italic;font-weight:900;font-size:120px;color:#1565FF;line-height:1;position:relative;z-index:3}
'''
H = '<div class="hueco"></div>'

def tapa(tema, sub):
    return ('oscuro', f'<div class="eye" style="margin-top:250px">Serie · Electrofitness y…</div><h1 style="font-size:170px">Electro<br>fitness<br>y <em>{tema}</em></h1><p class="sub">{sub}</p>' + H + '<div class="pie"><span>Deslizá</span><span class="boton">Ver más →</span></div>')
def placa(n, titulo, texto, dato):
    return ('claro', f'<div class="serie" style="margin-top:150px">Electrofitness y…</div><div class="nro" style="margin-top:30px">{n:02d}</div><h1 style="font-size:124px">{titulo}</h1><p class="sub">{texto}</p><div class="dato">{dato}</div>' + H + '<div class="linea"></div>')
def cierre(titulo, texto):
    return ('oscuro', f'<div class="eye" style="margin-top:300px">PowerFit</div><h1>{titulo}</h1><p class="sub">{texto}</p>' + H + '<div class="pie"><span>Córdoba 340 · Cipolletti</span><span class="boton">Clase gratis →</span></div>')

TEMAS = {
 'running': [
   tapa('running', 'Si salís a correr, esto te puede ayudar a correr mejor y a llegar con más piernas a la próxima salida.'),
   placa(1, 'Piernas y<br>glúteos que<br><em>sostienen</em>', 'Más fuerza en glúteos, piernas y abdomen ayuda a que la zancada sea más estable y el cuerpo absorba mejor cada paso.', 'En el equipo i-motion hay programas de <b>fuerza</b> y uno específico de <b>glúteos</b> que la profe puede sumar a tu clase.'),
   placa(2, 'Más<br><em>resistencia</em>', 'Trabajar la resistencia muscular hace que el cansancio llegue más tarde, sobre todo en los últimos kilómetros.', 'El programa <b>Resistencia</b> está pensado para mejorar la resistencia a la fatiga y la capacidad aeróbica.'),
   placa(3, 'Y para<br>después:<br><em>recuperar</em>', 'Después de una salida larga, una sesión suave puede ayudar a que las piernas se sientan más livianas.', 'Los programas de recuperación como <b>Capillary</b> y <b>Drenaje</b> trabajan con impulsos suaves que activan la circulación.'),
   cierre('No reemplaza<br>tus <em>salidas</em>', 'Las complementa. 20 minutos, una o dos veces por semana, y la profe arma el plan según cómo venís corriendo.'),
 ],
}

if __name__ == '__main__':
    tema, out = sys.argv[1], sys.argv[2]; os.makedirs(out, exist_ok=True)
    with sync_playwright() as pw:
        b = pw.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1350})
        for i, (est, cuerpo) in enumerate(TEMAS[tema], 1):
            pg.set_content(P.html(S.pieza('post', est, cuerpo))); pg.wait_for_timeout(200)
            pg.locator('.pz').screenshot(path=f'{out}/electrofitness-y-{tema}-{i}.png')
            sz = pg.evaluate("(()=>{const z=document.querySelector('.pz');return [z.scrollHeight,z.clientHeight]})()")
            if sz[0] > sz[1] + 2: print('DESBORDA', i, sz)
        b.close()
    print('ok')
