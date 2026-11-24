"""Tagline animata del profile README (sotto l'header): ruoli come chip neon + riga 'terminale'
che scrive, tiene e cancella le frasi in ciclo. Nessun servizio esterno.
Uso: python gen_tagline.py <cartella assets>
"""
import sys, os
from xml.sax.saxutils import escape
OUT = sys.argv[1]
W, H = 800, 96
FONT = "'Courier New',Courier,monospace"

TEXT = {
  'en': dict(roles=['FULL-STACK SOFTWARE ENGINEER', 'FRONT-END TEAM LEAD', 'BARI, ITALY'],
             lines=['React · Next.js · Angular · TypeScript', 'Spring Boot BFFs · OpenAPI · GraphQL', '// From contract to pixel.']),
  'it': dict(roles=['SOFTWARE ENGINEER FULL-STACK', 'FRONT-END TEAM LEAD', 'BARI, ITALIA'],
             lines=['React · Next.js · Angular · TypeScript', 'BFF Spring Boot · OpenAPI · GraphQL', '// Dal contratto al pixel.']),
}
THEMES = {
  'dark':  dict(accents=['#ff2d78', '#00f5ff', '#b44fff'], text='#f0ecff', term='#00f5ff', prompt='#ff2d78', chip_fo='.08', glow=True),
  'light': dict(accents=['#d6125a', '#00838f', '#7b2fc4'], text='#241c3d', term='#00838f', prompt='#d6125a', chip_fo='.06', glow=False),
}

# metrica monospace (Courier New: 0.6 em)
CHIP_FS, CHIP_LS = 12, 2.2
CHIP_CW = CHIP_FS * 0.6 + CHIP_LS
TERM_FS = 17
TERM_CW = TERM_FS * 0.6
TYPE, HOLD, ERASE, GAP = 0.055, 1.9, 0.6, 0.35  # secondi: per carattere, pausa, cancellazione, attesa

def pin(x, y, color):
    return (f'<path transform="translate({x:.1f},{y:.1f}) scale(.6)" fill="none" stroke="{color}" stroke-width="2.4" '
            f'd="M10 0C4.5 0 0 4.4 0 9.8 0 17.2 10 26 10 26s10-8.8 10-16.2C20 4.4 15.5 0 10 0z"/>'
            f'<circle cx="{x + 6:.1f}" cy="{y + 5.9:.1f}" r="2" fill="{color}"/>')

def chips(t, roles):
    pad, gap, h, y = 14, 12, 26, 8
    widths = [len(r) * CHIP_CW - CHIP_LS + 2 * pad + (19 if i == 2 else 0) for i, r in enumerate(roles)]
    x = (W - sum(widths) - gap * (len(roles) - 1)) / 2
    out = []
    for i, (r, w) in enumerate(zip(roles, widths)):
        c = t['accents'][i]
        out.append(f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="{h}" rx="4" fill="{c}" fill-opacity="{t["chip_fo"]}" stroke="{c}" stroke-opacity=".7"/>')
        tx = x + pad
        if i == 2:
            out.append(pin(tx, y + 6, c)); tx += 19
        glow = ' filter="url(#soft)"' if t['glow'] else ''
        out.append(f'<text x="{tx:.1f}" y="{y + 17.5}" font-size="{CHIP_FS}" font-weight="bold" letter-spacing="{CHIP_LS}" fill="{c}"{glow}>{escape(r)}</text>')
        x += w + gap
    return '\n    '.join(out)

def terminal(t, lines):
    y = 72
    maxw = max(len(l) for l in lines) * TERM_CW
    x0 = (W - maxw - 2 * TERM_CW) / 2          # centra la riga più lunga, prompt incluso
    tx = x0 + 2 * TERM_CW
    slots = [len(l) * TYPE + HOLD + ERASE + GAP for l in lines]
    cycle = sum(slots)
    out = [f'<text x="{x0:.1f}" y="{y}" font-size="{TERM_FS}" font-weight="bold" fill="{t["prompt"]}">&gt;</text>']
    start = 0.0
    for i, line in enumerate(lines):
        n = len(line)
        # fotogrammi (tempo, caratteri visibili, cursore visibile): scrittura, pausa, cancellazione
        frames = [(0.0, 0, 0)]
        if start > 0:
            frames.append((start, 0, 1))
        for k in range(1, n + 1):
            frames.append((start + k * TYPE, k, 1))
        t_hold_end = start + n * TYPE + HOLD
        erase_steps = 8
        for st in range(1, erase_steps):
            frames.append((t_hold_end + st * ERASE / erase_steps, round(n * (1 - st / erase_steps)), 1))
        frames.append((t_hold_end + ERASE, 0, 0))   # fine turno: testo e cursore spenti esplicitamente
        frames.append((cycle, 0, 0))
        if start == 0:
            frames[0] = (0.0, 0, 1)
        kt = ';'.join(f'{tm / cycle:.4f}' for tm, _, _ in frames)
        widths = ';'.join(f'{k * TERM_CW:.1f}' for _, k, _ in frames)
        xs = ';'.join(f'{tx + k * TERM_CW + 1:.1f}' for _, k, _ in frames)
        vis = ';'.join(str(v) for _, _, v in frames)
        anim = f'dur="{cycle:.2f}s" repeatCount="indefinite" calcMode="discrete" keyTimes="{kt}"'
        out.append(f'<clipPath id="c{i}"><rect x="{tx:.1f}" y="{y - TERM_FS}" height="{TERM_FS + 6}" width="0">'
                   f'<animate attributeName="width" values="{widths}" {anim}/></rect></clipPath>')
        glow = ' filter="url(#soft)"' if t['glow'] else ''
        out.append(f'<text x="{tx:.1f}" y="{y}" font-size="{TERM_FS}" fill="{t["term"]}" clip-path="url(#c{i})"{glow}>{escape(line)}</text>')
        # cursore: segue la scrittura, visibile solo nel turno della frase, lampeggia
        out.append(f'<g opacity="0"><animate attributeName="opacity" values="{vis}" {anim}/>'
                   f'<rect y="{y - TERM_FS + 3}" width="{TERM_CW * .9:.1f}" height="{TERM_FS}" fill="{t["prompt"]}" x="{tx:.1f}">'
                   f'<animate attributeName="x" values="{xs}" {anim}/>'
                   f'<animate attributeName="fill-opacity" values="1;1;0;0" keyTimes="0;.5;.5;1" dur="0.9s" repeatCount="indefinite"/></rect></g>')
        start += slots[i]
    return '\n    '.join(out)

def svg(lang, theme):
    t, tx = THEMES[theme], TEXT[lang]
    alt = ' · '.join(tx['roles']) + ' — ' + ' | '.join(tx['lines'])
    soft = ('<filter id="soft" x="-5%" y="-50%" width="110%" height="200%"><feGaussianBlur stdDeviation="1.6" result="b"/>'
            '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>') if t['glow'] else ''
    return f'''<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{escape(alt)}">
  <title>{escape(alt)}</title>
  <defs>{soft}</defs>
  <g font-family="{FONT}">
    {chips(t, tx['roles'])}
    {terminal(t, tx['lines'])}
  </g>
</svg>
'''

BADGES = {
  'portfolio': dict(label='PORTFOLIO', value='kxos.github.io', accent=0, icon='globe'),
  'linkedin':  dict(label='LINKEDIN',  value='Vito Iannone',   accent=1, icon='in'),
}

def badge(kind, theme):
    t, b = THEMES[theme], BADGES[kind]
    c = t['accents'][b['accent']]
    bg = '#0b0620' if theme == 'dark' else '#ffffff'
    fs_l, fs_v = 10, 13
    lw = len(b['label']) * (fs_l * .6 + 1.6)
    vw = len(b['value']) * (fs_v * .6 + .6)
    icon_w, h = 34, 34
    w = icon_w + 12 + lw + 10 + vw + 14
    if b['icon'] == 'globe':
        icon = (f'<g fill="none" stroke="{bg}" stroke-width="1.6"><circle cx="17" cy="17" r="8"/>'
                f'<ellipse cx="17" cy="17" rx="3.6" ry="8"/><path d="M9 17h16M10.5 13h13M10.5 21h13"/></g>')
    else:
        icon = f'<text x="17" y="22.5" text-anchor="middle" font-family="Arial,Helvetica,sans-serif" font-size="15" font-weight="bold" fill="{bg}">in</text>'
    glow = ' filter="url(#soft)"' if t['glow'] else ''
    soft = ('<defs><filter id="soft" x="-5%" y="-50%" width="110%" height="200%"><feGaussianBlur stdDeviation="1.2" result="b"/>'
            '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>') if t['glow'] else ''
    shadow = '' if t['glow'] else f'<rect x="2" y="3" width="{w - 2:.1f}" height="{h - 2}" rx="6" fill="{c}" fill-opacity=".12"/>'
    return f'''<svg width="{w + 2:.0f}" height="{h + 2}" viewBox="0 0 {w + 2:.0f} {h + 2}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{b['label'].title()}: {escape(b['value'])}">
  {soft}
  {shadow}
  <rect x=".75" y=".75" width="{w - .5:.1f}" height="{h - .5}" rx="6" fill="{bg}" stroke="{c}" stroke-width="1.5"/>
  <path d="M.75 6.75a6 6 0 0 1 6-6H{icon_w}V{h + .25}H6.75a6 6 0 0 1-6-6z" fill="{c}"/>
  {icon}
  <g font-family="{FONT}" font-weight="bold">
    <text x="{icon_w + 12}" y="22" font-size="{fs_l}" letter-spacing="1.6" fill="{t['text']}" fill-opacity=".6">{b['label']}</text>
    <text x="{icon_w + 12 + lw + 10:.1f}" y="22.5" font-size="{fs_v}" letter-spacing=".6" fill="{c}"{glow}>{escape(b['value'])}</text>
  </g>
</svg>
'''

for kind in BADGES:
    for theme, suf in (('dark', ''), ('light', '-light')):
        name = f'badge-{kind}{suf}.svg'
        open(os.path.join(OUT, name), 'w', encoding='utf-8').write(badge(kind, theme))
        print(name)

for lang, base in (('en', 'tagline'), ('it', 'tagline-it')):
    for theme, suf in (('dark', ''), ('light', '-light')):
        name = f'{base}{suf}.svg'
        open(os.path.join(OUT, name), 'w', encoding='utf-8').write(svg(lang, theme))
        print(name)
