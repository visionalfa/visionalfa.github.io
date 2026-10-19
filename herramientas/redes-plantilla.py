# Plantilla de imágenes para Instagram (1080x1350) con la estética de Visión Alfa.
# Uso: python3 herramientas/redes-plantilla.py <carpeta_salida>. Editá el diccionario "posts" con el contenido de la semana.
# Tipos de fondo: verde, papel, mostaza (en mostaza usar marca("#1F3D2B","#F4F3EE")).
from playwright.sync_api import sync_playwright
import sys
LOGO='<svg width="74" height="56" viewBox="0 8 64 48"><path d="M4 14 L17 50 L30 14" fill="none" stroke="{a}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/><path d="M34 50 L47 14 L60 50" fill="none" stroke="{b}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/></svg>'
BASE='''<!doctype html><html><head><meta charset="utf-8"><style>
*{box-sizing:border-box;margin:0}
body{width:1080px;height:1350px;font-family:Inter,sans-serif;overflow:hidden}
.p{width:1080px;height:1350px;padding:84px 86px;display:flex;flex-direction:column;position:relative}
.verde{background:#1F3D2B;color:#F4F3EE}.papel{background:#F4F3EE;color:#16231B}.mostaza{background:#E3A82B;color:#1F3D2B}
.marca{display:flex;align-items:center;gap:18px;font-family:'Inter Display';font-weight:800;font-size:38px;letter-spacing:-.02em}
.eye{font-weight:600;letter-spacing:.14em;text-transform:uppercase;font-size:28px;color:#E3A82B;margin-top:auto}
.mostaza .eye{color:#1F3D2B}
h1{font-family:'Inter Display';font-weight:800;letter-spacing:-.035em;line-height:1.0;font-size:104px;margin-top:22px}
h1 em{font-style:normal;color:#E3A82B}
.mostaza h1 em{color:#F4F3EE}
.papel h1{color:#1F3D2B}.papel h1 em{color:#C98F17}
.sub{font-size:38px;line-height:1.35;margin-top:30px;opacity:.9;max-width:860px}
.pie{margin-top:auto;display:flex;justify-content:space-between;align-items:center;font-size:30px;font-weight:600}
.pill{background:#E3A82B;color:#1F3D2B;border-radius:999px;padding:18px 34px;font-weight:700;font-size:32px}
.papel .pill,.mostaza .pill{background:#1F3D2B;color:#F4F3EE}
.lista{margin-top:40px;display:flex;flex-direction:column;gap:22px}
.item{display:flex;gap:24px;align-items:flex-start;font-size:36px;line-height:1.3}
.item b{flex:none;width:58px;height:58px;border-radius:50%;background:#E3A82B;color:#1F3D2B;display:flex;align-items:center;justify-content:center;font-family:'Inter Display';font-size:28px;font-weight:800}
.papel .item b{background:#1F3D2B;color:#E3A82B}
.team{display:grid;grid-template-columns:1fr 1fr;gap:22px;margin-top:44px}
.m{background:rgba(244,243,238,.08);border:2px solid rgba(244,243,238,.18);border-radius:28px;padding:28px}
.m i{display:flex;width:76px;height:76px;border-radius:50%;align-items:center;justify-content:center;font-style:normal;font-family:'Inter Display';font-weight:800;font-size:28px;margin-bottom:16px}
.m strong{display:block;font-family:'Inter Display';font-size:32px;letter-spacing:-.01em;line-height:1.1}
.m span{display:block;font-size:24px;opacity:.75;margin-top:6px;line-height:1.3}
.tapa{position:absolute;right:86px;top:250px;width:330px;height:460px;background:#E3A82B;border-radius:12px 24px 24px 12px;box-shadow:-14px 0 0 #C98F17 inset,0 30px 60px rgba(0,0,0,.35);padding:34px;display:flex;flex-direction:column;transform:rotate(4deg)}
.tapa small{font-weight:700;font-size:22px;display:flex;justify-content:space-between;color:#1F3D2B}
.tapa div{margin-top:auto;font-family:'Inter Display';font-weight:800;font-size:46px;line-height:1.02;color:#1F3D2B;letter-spacing:-.02em}
</style></head><body>{body}</body></html>'''
def marca(fg='#F4F3EE', b='#E3A82B'):
    return '<div class="marca">'+LOGO.replace('{a}',fg).replace('{b}',b)+'visión alfa</div>'
posts={
'01-ebook-web': ('verde', marca()+'''
<div class="tapa"><small><span>visión alfa</span><span>07</span></small><div>Tu web de ventas con IA</div></div>
<div class="eye" style="margin-top:560px">Nuevo ebook · N.º 7</div>
<h1>Tu web de ventas,<br><em>hecha con IA.</em></h1>
<p class="sub">Sin saber programar, sin pagar abono y publicada gratis. Paso a paso, con los prompts listos.</p>
<div class="pie"><span>visionalfa.github.io</span><span class="pill">$25.000</span></div>'''),
'02-prompts': ('papel', marca('#1F3D2B')+'''
<div class="eye" style="color:#C98F17;margin-top:70px">Guardalo para después</div>
<h1 style="font-size:92px">3 prompts para<br><em>vender más</em> hoy</h1>
<div class="lista">
<div class="item"><b>1</b><span>“Escribime 5 respuestas para cuando un cliente dice <strong>‘está caro’</strong>, sin bajar el precio.”</span></div>
<div class="item"><b>2</b><span>“Convertí esta lista de productos en <strong>descripciones que vendan</strong>: beneficio, no característica.”</span></div>
<div class="item"><b>3</b><span>“Armame un mensaje para <strong>volver a contactar</strong> a clientes que no compran hace 2 meses.”</span></div>
</div>
<div class="pie" style="color:#1F3D2B"><span>Más de 40 prompts en el ebook N.º 1</span><span class="pill">IA para vender más</span></div>'''),
'03-equipo': ('verde', marca()+'''
<div class="eye" style="margin-top:60px">Equipo interdisciplinario</div>
<h1 style="font-size:86px">Emprender no es<br>solo vender. <em>No estás solo.</em></h1>
<div class="team">
<div class="m"><i style="background:#E3A82B;color:#1F3D2B">FC</i><strong>Florentina Cecchini</strong><span>Emprendimiento, ventas e IA</span></div>
<div class="m"><i style="background:#F4F3EE;color:#1F3D2B">CT</i><strong>Carla Tanzi</strong><span>Psicóloga · Orientación vocacional</span></div>
<div class="m"><i style="background:#2E5A40;color:#F4F3EE">MD</i><strong>Marcelo De los Santos</strong><span>Coach ontológico · Equipos</span></div>
<div class="m"><i style="background:#E7EAE3;color:#1F3D2B">JC</i><strong>Juliana Cecchini</strong><span>Asuntos públicos e inversión social</span></div>
</div>
<div class="pie"><span>Reservá online · pagás con Mercado Pago</span><span class="pill">Ver el equipo</span></div>'''),
'04-cv': ('mostaza', marca('#1F3D2B','#F4F3EE')+'''
<div class="eye" style="margin-top:110px">Recurso gratis</div>
<h1 style="font-size:100px">¿Buscás tu<br><em>primer trabajo?</em></h1>
<p class="sub" style="color:#1F3D2B">Armá tu CV en 10 minutos y descargalo en PDF. Gratis, desde el celular y sin registrarte.</p>
<div class="lista" style="margin-top:44px">
<div class="item"><b style="background:#1F3D2B;color:#E3A82B">✓</b><span>Modelo de CV listo para completar</span></div>
<div class="item"><b style="background:#1F3D2B;color:#E3A82B">✓</b><span>Guía para la entrevista y dónde buscar</span></div>
<div class="item"><b style="background:#1F3D2B;color:#E3A82B">✓</b><span>Mensajes para escribirle a empresas</span></div>
</div>
<div class="pie" style="color:#1F3D2B"><span>Link en la bio</span><span class="pill">Recursos gratis</span></div>'''),
'05-web-automatizada': ('verde', marca()+'''
<div class="eye" style="margin-top:90px">¿Te gusta lo que ves?</div>
<h1 style="font-size:96px">Te ayudo a crear<br>una web como la mía,<br><em>con todo automatizado.</em></h1>
<div class="lista">
<div class="item"><b>✓</b><span>Ventas y cobros con Mercado Pago</span></div>
<div class="item"><b>✓</b><span>Agenda online y mails automáticos</span></div>
<div class="item"><b>✓</b><span>Todas las reuniones que hagan falta</span></div>
<div class="item"><b>✓</b><span>Acceso ilimitado a todos los ebooks</span></div>
</div>
<div class="pie"><span>Pago único · reservá en la web</span><span class="pill">$500.000</span></div>'''),
}
out=sys.argv[1]
with sync_playwright() as pw:
    b=pw.chromium.launch(); p=b.new_page(viewport={'width':1080,'height':1350})
    for k,(cls,body) in posts.items():
        p.set_content(BASE.replace('{body}', f'<div class="p {cls}">{body}</div>')); p.wait_for_timeout(200)
        p.screenshot(path=f'{out}/{k}.png'); print(k)
    b.close()
