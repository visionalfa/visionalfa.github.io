# Ilustraciones planas en SVG con los colores de Visión Alfa, para usar en posts, historias y reels.
# Uso: from ilustraciones import ILU; ILU['celular'](300) devuelve un <svg> de 300px de ancho.
V, M, MO, P, B, D = '#1F3D2B', '#E3A82B', '#C98F17', '#F4F3EE', '#FFFFFF', '#16231B'
VC, VS = '#2E5A40', '#A9C2B0'   # verde claro y verde suave
PIEL, PELO = '#EDBF9A', '#3B2A20'

def _svg(w, inner, vb='0 0 400 400'):
    x, y, ww, hh = map(float, vb.split())
    return f'<svg width="{w}" height="{int(w*hh/ww)}" viewBox="{vb}" xmlns="http://www.w3.org/2000/svg">{inner}</svg>'

def chispa(x, y, s=1, c=M):
    return f'<path transform="translate({x} {y}) scale({s})" d="M0 -22 C3 -6 6 -3 22 0 C6 3 3 6 0 22 C-3 6 -6 3 -22 0 C-6 -3 -3 -6 0 -22Z" fill="{c}"/>'

def celular(w=300, fondo=P):
    return _svg(w, f'''
<circle cx="200" cy="210" r="170" fill="{VS}" opacity=".35"/>
<rect x="120" y="40" width="170" height="320" rx="30" fill="{D}"/>
<rect x="132" y="62" width="146" height="276" rx="18" fill="{fondo}"/>
<rect x="180" y="48" width="50" height="8" rx="4" fill="#33443A"/>
<rect x="144" y="84" width="96" height="40" rx="16" fill="{B}" stroke="#DAD8CF" stroke-width="2"/>
<rect x="156" y="98" width="62" height="8" rx="4" fill="#B9B7AE"/>
<rect x="170" y="136" width="96" height="52" rx="16" fill="{M}"/>
<rect x="182" y="150" width="70" height="8" rx="4" fill="{V}" opacity=".55"/><rect x="182" y="166" width="46" height="8" rx="4" fill="{V}" opacity=".55"/>
<rect x="144" y="200" width="84" height="40" rx="16" fill="{B}" stroke="#DAD8CF" stroke-width="2"/>
<rect x="156" y="214" width="52" height="8" rx="4" fill="#B9B7AE"/>
<rect x="160" y="252" width="106" height="52" rx="16" fill="{V}"/>
<rect x="172" y="266" width="80" height="8" rx="4" fill="{P}" opacity=".7"/><rect x="172" y="282" width="56" height="8" rx="4" fill="{M}"/>
<g transform="translate(300 96)"><circle r="44" fill="{M}"/><path d="M-20 -8 h40 a6 6 0 0 1 6 6 v18 a6 6 0 0 1 -6 6 h-22 l-12 10 v-10 h-6 a6 6 0 0 1 -6 -6 v-18 a6 6 0 0 1 6 -6z" fill="{V}"/></g>
{chispa(84, 300, .9)}''')

def etiqueta(w=300):
    return _svg(w, f'''
<circle cx="200" cy="210" r="170" fill="{VS}" opacity=".35"/>
<g transform="rotate(-14 200 190)">
<path d="M110 120 h150 l70 70 l-70 70 h-150 a16 16 0 0 1 -16 -16 v-108 a16 16 0 0 1 16 -16z" fill="{M}"/>
<circle cx="268" cy="190" r="14" fill="{P}"/>
<path d="M282 190 C320 170 340 120 330 80" fill="none" stroke="{V}" stroke-width="6" stroke-linecap="round"/>
<text x="168" y="214" text-anchor="middle" font-family="Inter Display" font-weight="800" font-size="72" fill="{V}">$</text>
</g>
<g transform="translate(96 300)"><ellipse cx="0" cy="14" rx="46" ry="14" fill="{MO}"/><rect x="-46" y="-6" width="92" height="20" fill="{MO}"/><ellipse cx="0" cy="-6" rx="46" ry="14" fill="{M}"/>
<ellipse cx="0" cy="-20" rx="46" ry="14" fill="{MO}"/><rect x="-46" y="-40" width="92" height="20" fill="{MO}"/><ellipse cx="0" cy="-40" rx="46" ry="14" fill="{M}"/></g>
<g transform="translate(286 268)"><rect x="-44" y="-56" width="88" height="112" rx="14" fill="{V}"/><rect x="-32" y="-44" width="64" height="26" rx="6" fill="{VS}"/>
{''.join(f'<rect x="{-32+c*24}" y="{-8+r*22}" width="16" height="14" rx="4" fill="{M if (r,c)==(2,2) else P}"/>' for r in range(3) for c in range(3))}</g>
{chispa(330, 70, .8)}''')

def robot(w=300):
    return _svg(w, f'''
<circle cx="200" cy="210" r="170" fill="{VS}" opacity=".35"/>
<line x1="200" y1="70" x2="200" y2="108" stroke="{V}" stroke-width="8" stroke-linecap="round"/><circle cx="200" cy="64" r="14" fill="{M}"/>
<rect x="112" y="106" width="176" height="140" rx="40" fill="{V}"/>
<rect x="132" y="128" width="136" height="94" rx="28" fill="{P}"/>
<circle cx="170" cy="172" r="14" fill="{V}"/><circle cx="230" cy="172" r="14" fill="{V}"/>
<path d="M180 200 Q200 214 220 200" fill="none" stroke="{V}" stroke-width="6" stroke-linecap="round"/>
<rect x="98" y="160" width="16" height="44" rx="8" fill="{M}"/><rect x="286" y="160" width="16" height="44" rx="8" fill="{M}"/>
<rect x="134" y="256" width="132" height="96" rx="30" fill="{V}"/>
<rect x="170" y="280" width="60" height="16" rx="8" fill="{M}"/><circle cx="182" cy="320" r="8" fill="{VS}"/><circle cx="218" cy="320" r="8" fill="{VS}"/>
{chispa(86, 96, 1.1)}{chispa(320, 290, .8)}{chispa(316, 92, .6, MO)}''')

def comercio(w=300):
    franjas = ''.join(f'<path d="M{70+i*44} 120 h44 v40 a22 22 0 0 1 -44 0z" fill="{M if i%2==0 else V}"/>' for i in range(6))
    return _svg(w, f'''
<circle cx="200" cy="210" r="170" fill="{VS}" opacity=".35"/>
<rect x="80" y="150" width="244" height="206" fill="{P}" stroke="{V}" stroke-width="6"/>
<rect x="62" y="96" width="280" height="28" rx="8" fill="{V}"/>
{franjas}
<rect x="104" y="200" width="100" height="90" rx="8" fill="{VS}" stroke="{V}" stroke-width="5"/>
<rect x="116" y="246" width="22" height="30" rx="4" fill="{M}"/><rect x="144" y="232" width="22" height="44" rx="4" fill="{V}"/><rect x="172" y="252" width="20" height="24" rx="4" fill="{MO}"/>
<rect x="226" y="200" width="76" height="156" rx="6" fill="{V}"/><circle cx="288" cy="282" r="6" fill="{M}"/>
<rect x="234" y="214" width="60" height="24" rx="6" fill="{M}"/><text x="264" y="232" text-anchor="middle" font-family="Inter" font-weight="800" font-size="12" fill="{V}">ABIERTO</text>
<rect x="40" y="352" width="324" height="10" rx="5" fill="{V}"/>
{chispa(340, 70, .8)}''')

def laptop(w=300):
    return _svg(w, f'''
<circle cx="200" cy="210" r="170" fill="{VS}" opacity=".35"/>
<rect x="76" y="94" width="248" height="168" rx="16" fill="{D}"/>
<rect x="90" y="108" width="220" height="140" rx="6" fill="{P}"/>
<rect x="90" y="108" width="220" height="24" fill="{V}"/><circle cx="104" cy="120" r="5" fill="{M}"/>
<rect x="104" y="146" width="96" height="14" rx="5" fill="{V}"/><rect x="104" y="168" width="70" height="8" rx="4" fill="#B9B7AE"/>
<rect x="104" y="190" width="58" height="22" rx="11" fill="{M}"/>
<rect x="214" y="144" width="82" height="88" rx="8" fill="{M}"/><rect x="226" y="156" width="58" height="40" rx="4" fill="{P}" opacity=".7"/><rect x="226" y="206" width="40" height="8" rx="4" fill="{V}"/>
<path d="M50 262 h300 l-20 28 h-260z" fill="{V}"/><rect x="176" y="264" width="48" height="8" rx="4" fill="{VC}"/>
<g transform="translate(316 300)"><circle r="40" fill="{M}"/><path d="M-20 -14 h8 l8 26 h22 l6 -18 h-32" fill="none" stroke="{V}" stroke-width="6" stroke-linejoin="round" stroke-linecap="round"/><circle cx="-2" cy="20" r="5" fill="{V}"/><circle cx="16" cy="20" r="5" fill="{V}"/></g>
{chispa(80, 300, .9)}''')

def libros(w=300):
    cols = [V, M, VC, MO, V, M, VC]
    hs = [210, 236, 196, 224, 244, 206, 228]
    lom = ''
    x = 62
    for i, (c, h) in enumerate(zip(cols, hs)):
        lom += f'<rect x="{x}" y="{340-h}" width="38" height="{h}" rx="6" fill="{c}"/><rect x="{x+8}" y="{340-h+20}" width="22" height="6" rx="3" fill="{P}" opacity=".7"/><text x="{x+19}" y="326" text-anchor="middle" font-family="Inter Display" font-weight="800" font-size="18" fill="{P}">{i+1}</text>'
        x += 41
    return _svg(w, f'<circle cx="200" cy="210" r="170" fill="{VS}" opacity=".35"/>{lom}<rect x="44" y="340" width="312" height="12" rx="6" fill="{D}"/>{chispa(340, 80, .9)}{chispa(70, 84, .6, MO)}')

def calendario(w=300, dias=(2, 3, 4), mes='NOVIEMBRE'):
    celdas = ''
    n = 1
    # noviembre 2026 arranca domingo: columnas L M M J V S D
    inicio = 6
    for k in range(35):
        r, c = divmod(k, 7)
        if k < inicio or n > 30:
            continue
        cx, cy = 92 + c * 36, 172 + r * 36
        on = n in dias
        celdas += f'<rect x="{cx-15}" y="{cy-15}" width="30" height="30" rx="8" fill="{M if on else "none"}"/><text x="{cx}" y="{cy+6}" text-anchor="middle" font-family="Inter" font-weight="{800 if on else 600}" font-size="16" fill="{V if on else "#4A5A50"}">{n}</text>'
        n += 1
    cab = ''.join(f'<text x="{92+i*36}" y="146" text-anchor="middle" font-family="Inter" font-weight="800" font-size="14" fill="{V}">{d}</text>' for i, d in enumerate('LMMJVSD'))
    return _svg(w, f'''
<circle cx="200" cy="210" r="170" fill="{VS}" opacity=".35"/>
<rect x="60" y="74" width="280" height="290" rx="22" fill="{B}" stroke="{V}" stroke-width="6"/>
<path d="M60 96 a22 22 0 0 1 22 -22 h236 a22 22 0 0 1 22 22 v22 h-280z" fill="{V}"/>
<text x="200" y="108" text-anchor="middle" font-family="Inter Display" font-weight="800" font-size="22" fill="{P}" letter-spacing="3">{mes}</text>
<rect x="108" y="58" width="14" height="34" rx="7" fill="{M}"/><rect x="278" y="58" width="14" height="34" rx="7" fill="{M}"/>
{cab}{celdas}{chispa(340, 330, .9)}''')

def lupa(w=300):
    return _svg(w, f'''
<circle cx="200" cy="210" r="170" fill="{VS}" opacity=".35"/>
<rect x="84" y="70" width="190" height="250" rx="16" fill="{B}" stroke="{V}" stroke-width="6"/>
{''.join(f'<rect x="108" y="{100+i*30}" width="{[140,110,128,90,120,70][i]}" height="10" rx="5" fill="{"#B9B7AE" if i!=2 else M}"/>' for i in range(6))}
<circle cx="250" cy="236" r="64" fill="{P}" fill-opacity=".6" stroke="{V}" stroke-width="16"/>
<rect x="290" y="284" width="26" height="86" rx="13" fill="{V}" transform="rotate(-42 303 327)"/>
<path d="M226 236 l16 16 l30 -34" fill="none" stroke="{M}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>''')

def checklist(w=300):
    filas = ''
    for i in range(4):
        y = 132 + i * 52
        ok = i < 2
        filas += f'<rect x="104" y="{y-18}" width="36" height="36" rx="10" fill="{M if ok else B}" stroke="{V}" stroke-width="5"/>'
        if ok:
            filas += f'<path d="M112 {y} l8 8 l14 -16" fill="none" stroke="{V}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>'
        filas += f'<rect x="156" y="{y-6}" width="{[130,104,120,92][i]}" height="12" rx="6" fill="{V if ok else "#B9B7AE"}"/>'
    return _svg(w, f'''
<circle cx="200" cy="210" r="170" fill="{VS}" opacity=".35"/>
<rect x="76" y="70" width="248" height="290" rx="22" fill="{P}" stroke="{V}" stroke-width="6"/>
<rect x="150" y="54" width="100" height="34" rx="12" fill="{V}"/>
{filas}
<g transform="translate(318 320) rotate(30)"><rect x="-12" y="-80" width="24" height="120" rx="6" fill="{M}"/><path d="M-12 40 l12 26 l12 -26z" fill="{PIEL}"/><rect x="-12" y="-80" width="24" height="18" fill="{MO}"/></g>''')

def caja(w=300):
    return _svg(w, f'''
<circle cx="200" cy="210" r="170" fill="{VS}" opacity=".35"/>
<path d="M90 160 l110 -50 l110 50 l-110 50z" fill="{MO}"/>
<path d="M90 160 v130 l110 50 v-130z" fill="{M}"/><path d="M310 160 v130 l-110 50 v-130z" fill="#D49A22"/>
<path d="M145 135 l110 50 v40 l-22 -10 v-40 l-110 -50z" fill="{P}" opacity=".85"/>
<g transform="translate(96 330)"><circle r="34" fill="{V}"/><text y="12" text-anchor="middle" font-family="Inter Display" font-weight="800" font-size="34" fill="{M}">%</text></g>
{chispa(330, 80, .9)}''')

def bolsa(w=300):
    return _svg(w, f'''
<circle cx="200" cy="210" r="170" fill="{VS}" opacity=".35"/>
<path d="M150 130 a50 50 0 0 1 100 0" fill="none" stroke="{V}" stroke-width="12" stroke-linecap="round"/>
<path d="M100 120 h200 l20 230 h-240z" fill="{M}"/>
<path d="M100 120 h200 l4 40 h-208z" fill="{MO}"/>
<g transform="translate(200 250)"><circle r="56" fill="{V}"/><text y="18" text-anchor="middle" font-family="Inter Display" font-weight="800" font-size="52" fill="{M}">%</text></g>
{chispa(84, 110, 1)}{chispa(336, 300, .8, V)}''')

def pantallas(w=300):
    return _svg(w, f'''
<circle cx="200" cy="210" r="170" fill="{VS}" opacity=".35"/>
<rect x="56" y="104" width="230" height="150" rx="14" fill="{D}"/><rect x="68" y="116" width="206" height="126" rx="6" fill="{P}"/>
<rect x="84" y="134" width="120" height="14" rx="6" fill="{V}"/>{''.join(f'<rect x="84" y="{160+i*18}" width="{[170,150,164,110][i]}" height="8" rx="4" fill="#B9B7AE"/>' for i in range(4))}
<path d="M36 254 h270 l-16 22 h-238z" fill="{V}"/>
<rect x="250" y="160" width="104" height="190" rx="18" fill="{D}"/><rect x="258" y="174" width="88" height="162" rx="10" fill="{P}"/>
<rect x="268" y="188" width="60" height="10" rx="5" fill="{V}"/>{''.join(f'<rect x="268" y="{208+i*14}" width="{[68,58,66,50,62][i]}" height="6" rx="3" fill="#B9B7AE"/>' for i in range(5))}
<rect x="268" y="290" width="50" height="22" rx="11" fill="{M}"/>
{chispa(340, 110, .9)}''')

def flor(w=300):
    # Ilustración de Flor (la misma de la web, sin el globo de diálogo)
    return _svg(w, f'''
<circle cx="200" cy="250" r="170" fill="{M}" opacity=".9"/>
<path d="M108 232 C98 140 150 92 200 92 C255 92 304 140 292 232 L300 336 C262 352 138 352 100 336 Z" fill="{PELO}"/>
<path d="M66 500 C72 410 124 372 200 372 C276 372 328 410 334 500 Z" fill="{V}"/>
<rect x="177" y="296" width="46" height="90" rx="20" fill="#DFA47E"/>
<path d="M168 374 L200 414 L232 374" fill="none" stroke="{M}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>
<ellipse cx="200" cy="232" rx="78" ry="92" fill="{PIEL}"/>
<path d="M118 220 C116 152 160 124 206 126 C252 128 288 160 283 222 C262 190 232 168 204 166 C178 186 148 204 118 220 Z" fill="{PELO}"/>
<path d="M160 226 Q172 218 184 224" fill="none" stroke="{PELO}" stroke-width="5" stroke-linecap="round"/>
<path d="M216 224 Q228 218 240 226" fill="none" stroke="{PELO}" stroke-width="5" stroke-linecap="round"/>
<ellipse cx="172" cy="248" rx="7" ry="9" fill="{D}"/><ellipse cx="228" cy="248" rx="7" ry="9" fill="{D}"/>
<circle cx="158" cy="276" r="13" fill="#E8857A" opacity="0.35"/><circle cx="242" cy="276" r="13" fill="#E8857A" opacity="0.35"/>
<path d="M201 254 Q208 270 198 274" fill="none" stroke="#B9805E" stroke-width="4" stroke-linecap="round"/>
<path d="M176 290 Q200 314 224 290 Z" fill="{D}"/>
<path d="M184 296 Q200 306 216 296" fill="none" stroke="{P}" stroke-width="4" stroke-linecap="round"/>''', '0 40 400 460')

def bloques(w=300):
    # Las 4 partes de un buen prompt: Rol, Contexto, Tarea, Formato
    filas = ''
    for i, (l, c) in enumerate([('R', V), ('C', M), ('T', VC), ('F', MO)]):
        y = 70 + i * 74
        filas += f'<rect x="{90+i*14}" y="{y}" width="{220-i*28}" height="62" rx="16" fill="{c}"/><text x="{121+i*14}" y="{y+43}" text-anchor="middle" font-family="Inter Display" font-weight="800" font-size="34" fill="{P if c in (V, VC) else V}">{l}</text>'
        filas += f'<rect x="{152+i*14}" y="{y+26}" width="{120-i*28}" height="10" rx="5" fill="{P}" opacity=".6"/>'
    return _svg(w, f'<circle cx="200" cy="210" r="170" fill="{VS}" opacity=".35"/>{filas}{chispa(330, 80, 1)}{chispa(76, 330, .7, V)}')

def encuesta(w=300):
    return _svg(w, f'''
<circle cx="200" cy="210" r="170" fill="{VS}" opacity=".35"/>
<rect x="70" y="100" width="260" height="210" rx="28" fill="{B}" stroke="{V}" stroke-width="6"/>
<rect x="96" y="128" width="150" height="14" rx="7" fill="{V}"/>
<rect x="96" y="166" width="208" height="46" rx="23" fill="{P}" stroke="#DAD8CF" stroke-width="3"/><rect x="96" y="166" width="140" height="46" rx="23" fill="{M}"/>
<rect x="96" y="230" width="208" height="46" rx="23" fill="{P}" stroke="#DAD8CF" stroke-width="3"/><rect x="96" y="230" width="72" height="46" rx="23" fill="{VS}"/>
<g transform="translate(316 312)"><circle r="40" fill="{V}"/><text y="14" text-anchor="middle" font-family="Inter Display" font-weight="800" font-size="40" fill="{M}">?</text></g>
{chispa(82, 82, .9)}''')

ILU = dict(celular=celular, etiqueta=etiqueta, robot=robot, comercio=comercio, laptop=laptop, libros=libros,
           calendario=calendario, lupa=lupa, checklist=checklist, caja=caja, bolsa=bolsa, pantallas=pantallas,
           flor=flor, bloques=bloques, encuesta=encuesta)
