"""Header e footer del profile README, tema scuro e chiaro.
Scena synthwave: sole a righe all'orizzonte, griglia prospettica in movimento, scanline, cursore.
Uso: python gen_header.py <cartella assets>  ->  header.svg, footer.svg, header-light.svg, footer-light.svg
"""
import sys, os
OUT = sys.argv[1]
W, H, HY = 800, 130, 104  # HY = orizzonte

THEMES = {
  'dark': dict(
    bg=('#04020e', '#0d0820'), pink='#ff2d78', violet='#b44fff', teal='#00f5ff', sub='#9b93c8',
    title=('#ff2d78', '#ff6eb4', '#00f5ff'), ghost_op='.35', sun_op=('.30', '.45'), stripe='#06030f',
    grid_v_op='.16', grid_h_op='.55', scan_op='.06', edge_op='.55', glow=True),
  'light': dict(
    bg=('#ffffff', '#fbf5ff'), pink='#d6125a', violet='#7b2fc4', teal='#00838f', sub='#5b5680',
    title=('#d6125a', '#7b2fc4', '#00838f'), ghost_op='.28', sun_op=('.18', '.28'), stripe='#ffffff',
    grid_v_op='.10', grid_h_op='.35', scan_op='.07', edge_op='.7', glow=False),
}

def grid(t):
    out = [f'<line x1="0" y1="{HY}" x2="{W}" y2="{HY}" stroke="url(#horizon)" stroke-width="1.2"/>']
    for k in range(-12, 13):
        out.append(f'<line x1="{W/2 + k*18:.0f}" y1="{HY}" x2="{W/2 + k*70:.0f}" y2="{H}" stroke="{t["violet"]}" stroke-opacity="{t["grid_v_op"]}"/>')
    # linee orizzontali che scorrono verso chi guarda, accelerando come in prospettiva
    dur, n = 2.4, 4
    for i in range(n):
        b = f'begin="{-dur * i / n:.2f}s" dur="{dur}s" repeatCount="indefinite"'
        spline = 'calcMode="spline" keySplines="0.55 0 1 0.6"'
        out.append(
            f'<line x1="0" x2="{W}" y1="{HY}" y2="{HY}" stroke="{t["pink"]}">'
            f'<animate attributeName="y1" values="{HY};{H + 2}" {b} {spline}/>'
            f'<animate attributeName="y2" values="{HY};{H + 2}" {b} {spline}/>'
            f'<animate attributeName="stroke-opacity" values="0;{t["grid_h_op"]}" {b}/>'
            f'</line>')
    return '\n    '.join(out)

def sun(t):
    cx, r = W/2, 62
    lo, hi = t['sun_op']
    stripes = ''.join(f'<rect x="{cx-r}" y="{y}" width="{2*r}" height="{h}" fill="{t["stripe"]}"/>' for y, h in ((80, 2), (88, 3), (96, 4)))
    return (f'<g clip-path="url(#sunclip)" opacity="{lo}">'
            f'<animate attributeName="opacity" values="{lo};{hi};{lo}" dur="4s" repeatCount="indefinite"/>'
            f'<circle cx="{cx}" cy="{HY}" r="{r}" fill="url(#sun)"/>{stripes}</g>')

def svg(theme, footer=False):
    t = THEMES[theme]
    glow_def = ('<filter id="glow" x="-10%" y="-40%" width="120%" height="180%"><feGaussianBlur stdDeviation="4" result="b"/>'
                '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>') if t['glow'] else ''
    glow = ' filter="url(#glow)"' if t['glow'] else ''
    t1, t2, t3 = t['title']
    content = f'''    <rect width="{W}" height="{H}" fill="url(#bg)"/>
    {sun(t)}
    <rect x="0" y="0" width="{W}" height="3" fill="{t["violet"]}" opacity="{t["scan_op"]}"><animateTransform attributeName="transform" type="translate" from="0,-3" to="0,{H+3}" dur="3.5s" repeatCount="indefinite"/></rect>
    {grid(t)}
    <polyline points="16,34 16,16 34,16" fill="none" stroke="{t["pink"]}" stroke-width="2"/>
    <polyline points="{W-34},16 {W-16},16 {W-16},34" fill="none" stroke="{t["teal"]}" stroke-width="2"/>
    <polyline points="16,{H-34} 16,{H-16} 34,{H-16}" fill="none" stroke="{t["teal"]}" stroke-width="2"/>
    <polyline points="{W-34},{H-16} {W-16},{H-16} {W-16},{H-34}" fill="none" stroke="{t["pink"]}" stroke-width="2"/>
    <g font-family="'Courier New',monospace" font-weight="bold" text-anchor="middle" font-size="40" letter-spacing="10">
      <text x="{W/2 + 2.5}" y="64" fill="{t["teal"]}" fill-opacity="{t["ghost_op"]}">VITO IANNONE</text>
      <text x="{W/2}" y="62" fill="url(#title)"{glow}>VITO IANNONE</text>
    </g>
    <text x="{W/2}" y="90" text-anchor="middle" font-family="'Courier New',monospace" font-size="12" font-weight="bold" fill="{t["sub"]}" letter-spacing="5">FE TEAM LEAD  ·  FULLSTACK  ·  UI/UX</text>
    <rect x="574" y="80" width="9" height="2" fill="{t["pink"]}"><animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/></rect>'''
    if footer:  # riflesso capovolto e attenuato dell'header
        content = f'    <g transform="scale(1,-1) translate(0,-{H})" opacity=".45">\n{content}\n    </g>'
    return f'''<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Vito Iannone">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{t["bg"][0]}"/><stop offset="1" stop-color="{t["bg"][1]}"/></linearGradient>
    <linearGradient id="edge" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{t["pink"]}"/><stop offset=".5" stop-color="{t["violet"]}"/><stop offset="1" stop-color="{t["teal"]}"/></linearGradient>
    <linearGradient id="title" x1="0" y1="0" x2="1" y2="0"><stop offset=".1" stop-color="{t1}"/><stop offset=".55" stop-color="{t2}"/><stop offset=".9" stop-color="{t3}"/></linearGradient>
    <linearGradient id="horizon" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{t["pink"]}" stop-opacity="0"/><stop offset=".5" stop-color="{t["pink"]}" stop-opacity=".7"/><stop offset="1" stop-color="{t["teal"]}" stop-opacity="0"/></linearGradient>
    <linearGradient id="sun" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffb347"/><stop offset=".5" stop-color="{t["pink"]}"/><stop offset="1" stop-color="{t["violet"]}"/></linearGradient>
    <clipPath id="card"><rect width="{W}" height="{H}" rx="12"/></clipPath>
    <clipPath id="sunclip"><rect x="0" y="0" width="{W}" height="{HY}"/></clipPath>
    {glow_def}
  </defs>
  <g clip-path="url(#card)">
{content}
  </g>
  <rect x=".75" y=".75" width="{W-1.5}" height="{H-1.5}" rx="11.5" fill="none" stroke="url(#edge)" stroke-width="1.5" stroke-opacity="{t["edge_op"]}"/>
</svg>
'''

for theme, suffix in (('dark', ''), ('light', '-light')):
    for kind, footer in (('header', False), ('footer', True)):
        name = f'{kind}{suffix}.svg'
        open(os.path.join(OUT, name), 'w', encoding='utf-8').write(svg(theme, footer))
        print(name)
