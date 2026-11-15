# Reel del sábado 21/11 (cómo reservar la clase gratis): python3 reels.py <salida_piezas>
# Reusa la lógica de semana-2026-11-06/reels.py (tomas de 3 s con paneo, texto grande, cierre azul y audio silencioso).
import os, subprocess, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); FR = os.path.join(AQUI, '..', 'fotos-reales')
out = sys.argv[1]
REELS = {
 'reel-reservar-clase-gratis': [('foto', 'd14_4a52_entrada_en_calor', 'r5-a'), ('foto', 'd14_2b46_profe_y_alumno_remo', 'r5-b'),
                                ('foto', 'd14_28ef_espejo_abdominales', 'r5-c'), ('foto', 'd14_da80_espejo_lateral', 'r5-d'), ('fin', None, 'r5-fin')],
}
D = 3.2; X = 0.3
def run(c): subprocess.run(c, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
for nombre, segs in REELS.items():
    parts = []
    for i, (tipo, src, capa) in enumerate(segs):
        p = f'{out}/_{nombre}_{i}.mp4'; cp = f'{out}/capas/{capa}.png'
        base = 'scale=1188:2112:force_original_aspect_ratio=increase,crop=1188:2112,'
        if tipo == 'foto':
            vf = f"[0:v]{base}crop=1080:1920:x='(iw-ow)/2':y='(ih-oh)*t/{D}',eq=contrast=1.04,format=yuv420p[b];[b][1:v]overlay=0:0"
            run(['ffmpeg','-y','-loop','1','-t',str(D),'-i',f'{FR}/{src}.jpg','-i',cp,'-filter_complex',vf,'-r','30','-t',str(D),'-c:v','libx264','-pix_fmt','yuv420p','-an',p])
        else:
            run(['ffmpeg','-y','-loop','1','-t',str(D),'-i',cp,'-vf','format=yuv420p','-r','30','-c:v','libx264','-pix_fmt','yuv420p','-an',p])
        parts.append(p)
    ins = sum([['-i', q] for q in parts], [])
    fc, prev, off = '', '0:v', 0.0
    for j in range(1, len(parts)):
        off += D - X; lab = f'v{j}'
        fc += f'[{prev}][{j}:v]xfade=transition=fade:duration={X}:offset={off:.2f}[{lab}];'; prev = lab
    total = D * len(parts) - X * (len(parts) - 1)
    run(['ffmpeg','-y',*ins,'-f','lavfi','-t',f'{total:.2f}','-i','anullsrc=r=44100:cl=stereo','-filter_complex',fc.rstrip(';'),'-map',f'[{prev}]','-map',f'{len(parts)}:a','-c:v','libx264','-preset','medium','-crf','19','-pix_fmt','yuv420p','-r','30','-c:a','aac','-shortest','-movflags','+faststart',f'{out}/{nombre}.mp4'])
    for q in parts: os.remove(q)
    print(nombre, round(total, 1), 's')
