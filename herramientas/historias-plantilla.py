# Plantilla de historias (1080x1920). Uso: python3 herramientas/historias-plantilla.py <salida> <carpeta_con_imagenes_de_posts>
# Historias interactivas: dejar un hueco() libre para el sticker y programarlas con autoPublish false.
# Historias de Instagram (1080x1920) con la estética de Visión Alfa.
# Zonas seguras: dejar libres ~250px arriba y abajo (ahí Instagram pone su interfaz).
from playwright.sync_api import sync_playwright
import sys
def logo(a='#F4F3EE', b='#E3A82B', w=64):
    return f'<svg width="{w}" height="{int(w*.75)}" viewBox="0 8 64 48"><path d="M4 14 L17 50 L30 14" fill="none" stroke="{a}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/><path d="M34 50 L47 14 L60 50" fill="none" stroke="{b}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/></svg>'
CSS='''*{box-sizing:border-box;margin:0}
body{width:1080px;height:1920px;font-family:Inter,sans-serif;overflow:hidden}
.s{width:1080px;height:1920px;padding:270px 90px 300px;display:flex;flex-direction:column;position:relative}
.verde{background:#1F3D2B;color:#F4F3EE}.papel{background:#F4F3EE;color:#16231B}.mostaza{background:#E3A82B;color:#1F3D2B}
.marca{display:flex;align-items:center;gap:16px;font-family:'Inter Display';font-weight:800;font-size:36px;letter-spacing:-.02em}
.eye{font-weight:700;letter-spacing:.14em;text-transform:uppercase;font-size:32px;color:#E3A82B;margin-top:120px}
.papel .eye{color:#C98F17}.mostaza .eye{color:#1F3D2B}
h1{font-family:'Inter Display';font-weight:800;letter-spacing:-.035em;line-height:1.0;font-size:112px;margin-top:26px}
h1 em{font-style:normal;color:#E3A82B}.papel h1{color:#1F3D2B}.papel h1 em{color:#C98F17}.mostaza h1 em{color:#F4F3EE}
.sub{font-size:44px;line-height:1.35;margin-top:40px;opacity:.92}
.caja{margin-top:56px;border-radius:36px;padding:44px 48px;font-size:42px;line-height:1.35}
.verde .caja{background:rgba(244,243,238,.08);border:2px solid rgba(244,243,238,.2)}
.papel .caja{background:#fff;border:2px solid #DAD8CF}
.mostaza .caja{background:rgba(31,61,43,.08);border:2px solid rgba(31,61,43,.25)}
.caja b{color:#E3A82B}.papel .caja b{color:#C98F17}.mostaza .caja b{color:#1F3D2B}
.lista{margin-top:50px;display:flex;flex-direction:column;gap:30px}
.it{display:flex;gap:26px;align-items:flex-start;font-size:42px;line-height:1.3}
.it i{flex:none;font-style:normal;width:66px;height:66px;border-radius:50%;background:#E3A82B;color:#1F3D2B;display:flex;align-items:center;justify-content:center;font-family:'Inter Display';font-weight:800;font-size:32px}
.papel .it i{background:#1F3D2B;color:#E3A82B}.mostaza .it i{background:#1F3D2B;color:#E3A82B}
.cta{margin-top:auto;align-self:flex-start;background:#E3A82B;color:#1F3D2B;border-radius:999px;padding:26px 44px;font-weight:800;font-size:40px}
.papel .cta,.mostaza .cta{background:#1F3D2B;color:#F4F3EE}
.flecha{font-size:120px;line-height:1;margin-top:40px}
.post{margin-top:56px;width:640px;height:800px;border-radius:28px;overflow:hidden;box-shadow:0 30px 70px rgba(0,0,0,.35);align-self:center;transform:rotate(-2deg)}
.pista{margin-top:60px;font-size:36px;font-weight:600;opacity:.75}
.hueco{margin-top:24px}
.post img{width:100%;height:100%;display:block}
'''
def page(cls, body, marca_colors=('#F4F3EE','#E3A82B')):
    m=f'<div class="marca">{logo(*marca_colors)}visión alfa</div>'
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="s {cls}">{m}{body}</div></body></html>'
import base64
def img(name):
    d=base64.b64encode(open(f"{sys.argv[2]}/{name}","rb").read()).decode()
    return f'<div class="post"><img src="data:image/png;base64,{d}"></div>'
def hueco(txt, h=430):
    return f'<p class="pista">{txt}</p><div class="hueco" style="height:{h}px"></div>'
H={
# Lunes 19
'19-a': ('verde', '<div class="eye">Nuevo en la web</div><h1>¿Viste el post<br>de hoy? <em>👀</em></h1>'+img('01-ebook-web.png')+'<div class="cta">Ebook N.º 7 · Link en la bio</div>'),
'19-b': ('papel', '<div class="eye">Encuesta</div><h1>¿Tu negocio tiene<br><em>web propia?</em></h1><p class="sub">Instagram es tu vidriera, pero no es tuya. Una web es tu local abierto las 24 horas.</p>'+hueco('Votá 👇')),
# Martes 20
'20-a': ('mostaza', '<div class="eye">Encuesta</div><h1>¿Respondés<br><em>“precio por<br>privado”?</em></h1><p class="sub">Contame la verdad 😅 Spoiler: te puede estar haciendo perder ventas.</p>'+hueco('Votá 👇'), ('#1F3D2B','#F4F3EE')),
'20-b': ('verde', '<div class="eye">Post nuevo</div><h1>3 prompts para<br><em>vender más</em></h1>'+img('02-prompts.png')+'<div class="cta">Guardalo para después 📌</div>'),
# Miércoles 21
'21-a': ('verde', '<div class="eye">Hoy en el feed</div><h1>Te presento<br><em>al equipo</em> 🤝</h1>'+img('03-equipo.png')+'<div class="cta">Link en la bio → Equipo</div>'),
'21-b': ('papel', '<div class="eye">Orientación vocacional</div><h1>¿No sabés<br>qué estudiar?</h1><p class="sub">O tenés un hijo o una hija que termina el secundario. <b>Carla Tanzi</b>, psicóloga, acompaña el proceso con sesiones semanales por videollamada.</p>'+hueco('Reservá acá 👇', 360)),
# Jueves 22
'22-a': ('papel', '<div class="eye">Del 1 al 🔥</div><h1>¿Cuánto sabés<br>lo que <em>ganás</em><br>por cada venta?</h1><p class="sub">Muchos ponen el precio mirando a la competencia y no saben cuánto les queda.</p>'+hueco('Movelo 👇', 360)),
'22-b': ('mostaza', '<div class="eye">Post nuevo · Gratis</div><h1>¿Buscás tu<br><em>primer trabajo?</em></h1>'+img('04-cv.png')+'<div class="cta">Armá tu CV · Link en la bio</div>', ('#1F3D2B','#F4F3EE')),
# Viernes 23
'23-a': ('verde', '<div class="eye">¿Te gusta lo que ves?</div><h1>Mi web vende<br><em>sola</em> 🤖</h1><div class="lista"><div class="it"><i>✓</i><span>Cobra con Mercado Pago</span></div><div class="it"><i>✓</i><span>Entrega los ebooks al instante</span></div><div class="it"><i>✓</i><span>Agenda turnos y manda los mails</span></div></div><div class="caja" style="margin-top:60px">Te enseño a hacer la tuya: <b>2 horas conmigo + el ebook</b> paso a paso.</div><div class="cta">$200.000 · Link en la bio</div>'),
'23-b': ('papel', '<div class="eye">Te leo</div><h1>¿Qué es lo que<br>más te cuesta<br>de <em>vender?</em></h1><p class="sub">Con tus respuestas armo los próximos contenidos.</p>'+hueco('Escribime acá 👇')),
}
out=sys.argv[1]
with sync_playwright() as pw:
    b=pw.chromium.launch(); p=b.new_page(viewport={'width':1080,'height':1920})
    for k,v in H.items():
        cls,body=v[0],v[1]; mc=v[2] if len(v)>2 else (('#1F3D2B','#E3A82B') if cls=='papel' else ('#F4F3EE','#E3A82B'))
        p.set_content(page(cls,body,mc)); p.wait_for_timeout(250)
        p.screenshot(path=f'{out}/historia-{k}.png'); print(k)
    b.close()
