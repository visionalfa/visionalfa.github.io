# Uso: python3 herramientas/reel-plantilla.py <carpeta_frames_temporal> <salida.mp4>
# Editá la lista ESC (inicio, fin, color de fondo, html) y DUR. Máximo ~4 líneas por escena, 2,5-3 s por escena.
# Reel animado (1080x1920, 30 fps) con la estética de Visión Alfa: escenas de texto con animaciones.
from playwright.sync_api import sync_playwright
import sys, subprocess, os
out_dir, mp4 = sys.argv[1], sys.argv[2]
LOGO = lambda a='#F4F3EE', b='#E3A82B', w=90: f'<svg width="{w}" height="{int(w*.75)}" viewBox="0 8 64 48"><path d="M4 14 L17 50 L30 14" fill="none" stroke="{a}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/><path d="M34 50 L47 14 L60 50" fill="none" stroke="{b}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/></svg>'
# (inicio, fin, fondo, html)
ESC = [
 (0.0, 2.8, '#1F3D2B', '<div class="eye">Guardalo 📌</div><h1 class="big">3 errores que<br>te hacen <em>perder<br>ventas</em></h1><div class="flecha">👇</div>'),
 (2.8, 5.8, '#F4F3EE', '<div class="num">1</div><h1 class="dark">Responder<br><em>“precio por<br>privado”</em></h1><p class="sub dark">Mucha gente no pregunta. Se va.</p>'),
 (5.8, 8.8, '#E3A82B', '<div class="num n2">2</div><h1 class="dark">Poner el precio<br>mirando a la<br><em class="v">competencia</em></h1><p class="sub dark">Sin saber cuánto te queda a vos.</p>'),
 (8.8, 11.8, '#F4F3EE', '<div class="num">3</div><h1 class="dark">No volver a<br>escribirle a quien<br><em>ya te compró</em></h1><p class="sub dark">Es el cliente más fácil de recuperar.</p>'),
 (11.8, 15.0, '#1F3D2B', '<div class="logo">'+LOGO()+'</div><h1 class="big">Cómo evitarlos,<br><em>paso a paso</em></h1><p class="sub">Ebooks para emprendedores argentinos</p><div class="cta">Link en la bio</div>'),
]
DUR = 15.0; FPS = 30
CSS = '''*{margin:0;box-sizing:border-box}body{width:1080px;height:1920px;overflow:hidden;font-family:Inter,sans-serif}
.e{position:absolute;inset:0;display:flex;flex-direction:column;justify-content:center;padding:0 100px;opacity:0}
h1{font-family:'Inter Display';font-weight:800;letter-spacing:-.035em;line-height:1.02;font-size:124px;color:#F4F3EE}
h1.big{font-size:132px} h1 em{font-style:normal;color:#E3A82B} h1.dark{color:#1F3D2B} h1.dark em{color:#C98F17} h1 em.v{color:#F4F3EE}
.eye{font-weight:700;letter-spacing:.14em;text-transform:uppercase;font-size:40px;color:#E3A82B;margin-bottom:30px}
.sub{font-size:52px;line-height:1.3;margin-top:44px;color:#F4F3EE;opacity:.9} .sub.dark{color:#1F3D2B}
.num{font-family:'Inter Display';font-weight:800;font-size:300px;line-height:1;color:#E3A82B;margin-bottom:10px} .n2{color:#1F3D2B}
.flecha{font-size:140px;margin-top:60px}
.logo{margin-bottom:50px}
.cta{margin-top:70px;align-self:flex-start;background:#E3A82B;color:#1F3D2B;border-radius:999px;padding:30px 54px;font-weight:800;font-size:50px}
.marca{position:absolute;left:100px;bottom:200px;display:flex;align-items:center;gap:16px;font-family:'Inter Display';font-weight:800;font-size:40px;color:#F4F3EE;opacity:.9}
.barra{position:absolute;left:0;bottom:0;height:14px;background:#E3A82B}
'''
html = '<!doctype html><html><head><meta charset="utf-8"><style>'+CSS+'</style></head><body id="b">'
for i,(a,b,bg,h) in enumerate(ESC):
    html += f'<div class="e" id="e{i}" style="background:{bg}">{h}</div>'
html += '<div class="barra" id="barra"></div></body></html>'
JS = '''(t)=>{const E=%s;
const ease=x=>1-Math.pow(1-x,3);
E.forEach(([a,b],i)=>{const el=document.getElementById('e'+i);
 if(t<a||t>=b){el.style.opacity=0;return}
 el.style.opacity=1;
 const kids=[...el.children]; kids.forEach((k,j)=>{const d=a+0.12*j; const p=Math.min(1,Math.max(0,(t-d)/0.45)); const e=ease(p);
   k.style.opacity=e; k.style.transform=`translateY(${(1-e)*60}px)`;});
 const sal=Math.min(1,Math.max(0,(b-t)/0.25)); if(i<E.length-1) el.style.opacity=sal;
});
document.getElementById('barra').style.width=(t/%s*100)+'%%';}''' % ([[a,b] for a,b,_,_ in ESC], DUR)
with sync_playwright() as pw:
    br = pw.chromium.launch(); p = br.new_page(viewport={'width':1080,'height':1920})
    p.set_content(html); p.wait_for_timeout(300)
    n = int(DUR*FPS)
    for f in range(n):
        p.evaluate(JS, f/FPS); p.screenshot(path=f'{out_dir}/f{f:04d}.jpg', type='jpeg', quality=92)
    br.close()
subprocess.run(['ffmpeg','-y','-loglevel','error','-framerate',str(FPS),'-i',f'{out_dir}/f%04d.jpg','-f','lavfi','-i','anullsrc=r=44100:cl=stereo','-shortest','-c:v','libx264','-pix_fmt','yuv420p','-profile:v','high','-crf','20','-c:a','aac','-movflags','+faststart',mp4],check=True)
print('ok', os.path.getsize(mp4))
