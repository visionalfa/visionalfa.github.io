# Reel de suscripciones (fijo, sin mencionar el Cyber). Uso: python3 reel_suscripciones.py <salida>
# Usa los videos nuevos de videos-reales/ (wa_*) y los estilos de cyber-2026/piezas.py.
import os, sys, subprocess, importlib.util
from playwright.sync_api import sync_playwright

AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.join(AQUI, '..')
sp = importlib.util.spec_from_file_location('piezas', os.path.join(RAIZ, 'cyber-2026', 'piezas.py'))
P = importlib.util.module_from_spec(sp); sp.loader.exec_module(P)
VR = os.path.join(RAIZ, 'videos-reales')

CAPAS = {
 'rs-a': P.capa('Tu plan,<br><em>en automático</em>'),
 'rs-b': P.capa('Cada 2 meses<br><em>15% menos</em>'),
 'rs-c': P.capa('Cada 3 meses<br><em>20% menos</em>'),
 'rs-d': P.capa('Se cobra solo<br>con <em>Mercado Pago</em>'),
 'rs-fin': P.fin('Pedinos<br>tu <em style="color:#07090D">link</em>', 'Escribinos por WhatsApp y te lo pasamos. El descuento queda fijo.', 'Córdoba 340 · Cipolletti'),
}
SEGS = [('wa_kettlebell_frente.mp4', 0.5, 'rs-a'), ('wa_trx_remo_a.mp4', 1.0, 'rs-b'),
        ('wa_sentadilla_barra.mp4', 0.8, 'rs-c'), ('wa_profe_muestra_colchoneta.mp4', 0.5, 'rs-d'), (None, 0, 'rs-fin')]
NOMBRE = 'reel-suscripciones'; D = 3.0; X = 0.3

def run(c): subprocess.run(c, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

if __name__ == '__main__':
    out = sys.argv[1]; os.makedirs(out + '/capas', exist_ok=True)
    with sync_playwright() as pw:
        b = pw.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1920})
        for k, inner in CAPAS.items():
            pg.set_content(P.html(inner)); pg.wait_for_timeout(150)
            pg.screenshot(path=f'{out}/capas/{k}.png', omit_background=True)
        b.close()
    parts = []
    for i, (vid, ss, capa) in enumerate(SEGS):
        p = f'{out}/_{NOMBRE}_{i}.mp4'; cp = f'{out}/capas/{capa}.png'
        if vid:
            vf = ("[0:v]setpts=1.15*PTS,scale=1188:2112:force_original_aspect_ratio=increase,crop=1188:2112,crop=1080:1920,"
                  "eq=contrast=1.05:saturation=0.95,fps=30,format=yuv420p,tpad=stop_mode=clone:stop_duration=3[b];[b][1:v]overlay=0:0")
            run(['ffmpeg', '-y', '-ss', str(ss), '-i', f'{VR}/{vid}', '-i', cp, '-filter_complex', vf, '-t', str(D),
                 '-c:v', 'libx264', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', '-an', p])
        else:
            run(['ffmpeg', '-y', '-loop', '1', '-t', str(D), '-i', cp, '-vf', 'format=yuv420p', '-r', '30',
                 '-c:v', 'libx264', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', '-an', p])
        parts.append(p)
    ins = sum([['-i', q] for q in parts], [])
    fc, prev, off = '', '0:v', 0.0
    for j in range(1, len(parts)):
        off += D - X; lab = f'v{j}'
        fc += f'[{prev}][{j}:v]xfade=transition=fade:duration={X}:offset={off:.2f}[{lab}];'; prev = lab
    total = D * len(parts) - X * (len(parts) - 1)
    run(['ffmpeg', '-y', *ins, '-f', 'lavfi', '-t', f'{total:.2f}', '-i', 'anullsrc=r=44100:cl=stereo',
         '-filter_complex', fc.rstrip(';'), '-map', f'[{prev}]', '-map', f'{len(parts)}:a', '-c:v', 'libx264',
         '-preset', 'veryfast', '-crf', '19', '-pix_fmt', 'yuv420p', '-r', '30', '-c:a', 'aac', '-shortest',
         '-movflags', '+faststart', f'{out}/{NOMBRE}.mp4'])
    run(['ffmpeg', '-y', '-ss', '1.2', '-i', f'{out}/{NOMBRE}.mp4', '-frames:v', '1', '-q:v', '2', f'{out}/{NOMBRE}-portada.jpg'])
    for q in parts: os.remove(q)
    print(NOMBRE, round(total, 1), 's')
