# Ilustraciones de línea para la serie "Electrofitness y…" (SVG propio, estilo PowerFit).
# Cada función devuelve un <svg>. c = color de trazo, f = color de relleno suave.

def _svg(body, vb='0 0 200 200', c='#1565FF', f='#DCE7FF', w=8):
    return (f'<svg viewBox="{vb}" xmlns="http://www.w3.org/2000/svg" fill="none" stroke="{c}" '
            f'stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round" style="--f:{f}">{body}</svg>')

RAYO = '<path d="M0 0 L-14 20 L-4 20 L-8 36 L10 12 L0 12 Z" fill="currentColor" stroke="none"/>'

def corredor(c='#1565FF', f='#DCE7FF'):
    return _svg(f'''
  <circle cx="150" cy="100" r="62" fill="{f}" stroke="none"/>
  <g stroke-width="5" opacity=".55"><path d="M18 78h34M8 98h40M22 118h28"/></g>
  <circle cx="122" cy="34" r="14" fill="{c}" stroke="none"/>
  <path d="M114 52 L98 100"/>
  <path d="M110 60 L88 74 L74 92"/>
  <path d="M110 60 L134 74 L152 62"/>
  <path d="M98 100 L128 120 L120 158 L136 162"/>
  <path d="M98 100 L80 132 L52 140 L46 128"/>
  <g transform="translate(170 26)" style="color:{c}">{RAYO}</g>''', c=c, f=f)

def sentadilla(c='#1565FF', f='#DCE7FF'):
    return _svg(f'''
  <ellipse cx="104" cy="168" rx="70" ry="10" fill="{f}" stroke="none"/>
  <circle cx="92" cy="40" r="14" fill="{c}" stroke="none"/>
  <path d="M96 58 L112 104"/>
  <path d="M100 66 L140 74 L160 70"/>
  <path d="M112 104 L80 118 L84 160 L100 162"/>
  <path d="M112 104 L120 134 L132 160 L148 162" opacity=".55"/>
  <path d="M58 92c10-12 26-12 36 0" stroke-width="5" opacity=".6"/>
  <g transform="translate(46 112)" style="color:{c}">{RAYO}</g>''', c=c, f=f)

def cronometro(c='#1565FF', f='#DCE7FF'):
    return _svg(f'''
  <circle cx="100" cy="112" r="64" fill="{f}"/>
  <path d="M86 34h28M100 34v14M150 60l10-10"/>
  <path d="M100 112 L100 76" stroke-width="9"/>
  <path d="M100 112 L126 126" stroke-width="7"/>
  <circle cx="100" cy="112" r="6" fill="{c}" stroke="none"/>
  <path d="M18 186h40l10-18 14 32 12-26 8 12h80" stroke-width="5"/>''', vb='0 0 200 214', c=c, f=f)

def bateria(c='#1565FF', f='#DCE7FF'):
    return _svg(f'''
  <rect x="38" y="62" width="112" height="70" rx="14"/>
  <path d="M158 84v26" stroke-width="10"/>
  <rect x="52" y="76" width="56" height="42" rx="6" fill="{f}" stroke="none"/>
  <g transform="translate(104 72)" style="color:{c}">{RAYO}</g>
  <path d="M30 160c20-14 40 14 60 0s40 14 60 0s30 10 40 4" stroke-width="5" opacity=".6"/>
  <path d="M30 182c20-14 40 14 60 0s40 14 60 0s30 10 40 4" stroke-width="5" opacity=".35"/>''', c=c, f=f)

def pesa(c='#1565FF', f='#DCE7FF'):
    return _svg(f'''
  <ellipse cx="100" cy="186" rx="62" ry="9" fill="{f}" stroke="none"/>
  <path d="M68 92 C62 40 138 40 132 92" stroke-width="12"/>
  <circle cx="100" cy="126" r="54" fill="{f}" stroke-width="9"/>
  <g transform="translate(102 104) scale(1.5)" style="color:{c}">{RAYO}</g>
  <path d="M28 70l-14-6M26 100H10M172 70l14-6M174 100h16" stroke-width="6" opacity=".6"/>''', c=c, f=f)

ILUS = {'pesa': pesa, 'corredor': corredor, 'sentadilla': sentadilla, 'cronometro': cronometro, 'bateria': bateria}
