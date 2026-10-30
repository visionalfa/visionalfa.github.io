# Arma los reels de la semana: python3 reels.py <salida_piezas> <carpeta_videos>
import os, subprocess, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); FR = os.path.join(AQUI, '..', 'fotos-reales')
out, vids = sys.argv[1], sys.argv[2]
REELS = {
 'reel-asi-es-una-clase': [('foto', 'ft_6736_grupo3', 'r3-a'), ('foto', 'ft_6729_abdominales', 'r3-b'), ('foto', 'ft_6734_grupo_profe', 'r3-c'), ('video', 'IMG_6650.MOV:0.3', 'r3-d'), ('fin', None, 'r3-fin')],
 'reel-el-traje': [('video', 'IMG_6648.MOV:0', 'r4-a'), ('video', 'IMG_6649.MOV:1.5', 'r4-b'), ('foto', 'ft_6733_trx', 'r4-c'), ('foto', 'ft_6728_kettle_profe', 'r4-d'), ('fin', None, 'r4-fin')],
}
D = 3.0; X = 0.3
def run(c): subprocess.run(c, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
for nombre, segs in REELS.items():
    parts = []
    for i, (tipo, src, capa) in enumerate(segs):
        p = f'{out}/_{nombre}_{i}.mp4'; cp = f'{out}/capas/{capa}.png'
        base = 'scale=1188:2112:force_original_aspect_ratio=increase,crop=1188:2112,'
        if tipo == 'foto':
            vf = f"[0:v]{base}crop=1080:1920:x='(iw-ow)/2':y='(ih-oh)*t/{D}',eq=contrast=1.07:saturation=0.9,format=yuv420p[b];[b][1:v]overlay=0:0"
            run(['ffmpeg','-y','-loop','1','-t',str(D),'-i',f'{FR}/{src}.jpg','-i',cp,'-filter_complex',vf,'-r','30','-t',str(D),'-c:v','libx264','-pix_fmt','yuv420p','-an',p])
        elif tipo == 'video':
            f, ss = src.split(':')
            vf = f"[0:v]setpts=1.15*PTS,{base}crop=1080:1920,eq=contrast=1.07:saturation=0.9,fps=30,format=yuv420p,tpad=stop_mode=clone:stop_duration=3[b];[b][1:v]overlay=0:0"
            run(['ffmpeg','-y','-ss',ss,'-i',f'{vids}/{f}','-i',cp,'-filter_complex',vf,'-t',str(D),'-c:v','libx264','-pix_fmt','yuv420p','-an',p])
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
    run(['ffmpeg','-y','-ss','1.2','-i',f'{out}/{nombre}.mp4','-frames:v','1','-q:v','2',f'{out}/{nombre}-portada.jpg'])
    for q in parts: os.remove(q)
    print(nombre, round(total, 1), 's')
