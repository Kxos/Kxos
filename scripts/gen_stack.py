"""Genera assets/stack.svg (EN) e assets/stack-it.svg (IT) in stile synthwave."""
import sys, os
from xml.sax.saxutils import escape

OUT = sys.argv[1]
W, PAD, LABEL_W, CHIP_H, GAP, FS = 840, 28, 200, 24, 8, 12
CW = 7.4  # larghezza stimata di un carattere monospace a 12px
FONT = "'Share Tech Mono','SFMono-Regular',Consolas,'Liberation Mono','Courier New',monospace"
THEMES = {
  'dark':  dict(c={'pink': '#ff2d78', 'cyan': '#00f5ff', 'violet': '#b44fff', 'gold': '#ffd93d'}, bg=('#04020e', '#0d0820'), text='#f0ecff', muted='#4a4470', title='#ff2d78', edge=('#ff2d78', '#b44fff', '#00f5ff')),
  'light': dict(c={'pink': '#d6125a', 'cyan': '#00838f', 'violet': '#7b2fc4', 'gold': '#b7791f'}, bg=('#ffffff', '#fbf5ff'), text='#241c3d', muted='#b3aed0', title='url(#edge)', edge=('#d6125a', '#7b2fc4', '#00838f')),
}

# Stesso ordine, numerazione e colori della sezione Skills del sito.
ROWS = {
  'en': ('// TECH STACK', [
    ('FRONT END', 'pink', ['React 17→19', 'Next.js 14→16', 'Angular 21', 'TypeScript', 'Tailwind CSS 4', 'Bootstrap Italia', 'next-intl', 'Transloco']),
    ('TESTING & QUALITY', 'pink', ['Vitest', 'Jest', 'Testing Library', 'JUnit 5', 'JaCoCo', 'ESLint', 'axe-core']),
    ('BACK END', 'gold', ['Java 11→25', 'Spring Boot 2→4', 'Apache Camel', 'RabbitMQ', 'JPA', 'Oracle', 'PostgreSQL']),
    ('APIS & INTEGRATION', 'cyan', ['GraphQL', 'Apollo Client', 'OpenAPI contract-first', 'openapi-generator', 'BFF']),
    ('DELIVERY & DEVOPS', 'cyan', ['Docker', 'Kubernetes', 'Helm', 'Jenkins', 'SonarQube', 'GitLab', 'GitHub Actions']),
    ('IDENTITY & ACCESS', 'violet', ['OIDC / OAuth2', 'Keycloak', 'next-auth', 'angular-oauth2-oidc', 'SPID', 'CIE']),
    ('WAYS OF WORKING', 'violet', ['Git (rebase, PR)', 'Code review', 'Scrum', 'Claude Code', 'ADR · C4']),
  ]),
  'it': ('// STACK', [
    ('FRONTEND', 'pink', ['React 17→19', 'Next.js 14→16', 'Angular 21', 'TypeScript', 'Tailwind CSS 4', 'Bootstrap Italia', 'next-intl', 'Transloco']),
    ('TEST E QUALITÀ', 'pink', ['Vitest', 'Jest', 'Testing Library', 'JUnit 5', 'JaCoCo', 'ESLint', 'axe-core']),
    ('BACKEND', 'gold', ['Java 11→25', 'Spring Boot 2→4', 'Apache Camel', 'RabbitMQ', 'JPA', 'Oracle', 'PostgreSQL']),
    ('API E INTEGRAZIONE', 'cyan', ['GraphQL', 'Apollo Client', 'OpenAPI contract-first', 'openapi-generator', 'BFF']),
    ('DELIVERY E DEVOPS', 'cyan', ['Docker', 'Kubernetes', 'Helm', 'Jenkins', 'SonarQube', 'GitLab', 'GitHub Actions']),
    ('IDENTITÀ E ACCESSO', 'violet', ['OIDC / OAuth2', 'Keycloak', 'next-auth', 'angular-oauth2-oidc', 'SPID', 'CIE']),
    ('METODO', 'violet', ['Git (rebase, PR)', 'Code review', 'Scrum', 'Claude Code', 'ADR · C4']),
  ]),
}

def build(lang, theme):
    T = THEMES[theme]
    COLORS = T["c"]
    light = theme == 'light'
    chip_fill, chip_fo, chip_so = ('#ffffff', '1', '0.6') if light else (None, '0.07', '0.45')
    title, rows = ROWS[lang]
    body, y = [], 78
    x0, xmax = PAD + LABEL_W, W - PAD
    for i, (label, accent, chips) in enumerate(rows):
        color = COLORS[accent]
        if not light:
            chip_fill = color
        row_top, x, line = y, x0, 0
        placed = []
        for c in chips:
            w = len(c) * CW + 22
            if x + w > xmax:
                x, line = x0, line + 1
            placed.append((x, row_top + line * (CHIP_H + GAP), w, c))
            x += w + GAP
        row_h = (line + 1) * (CHIP_H + GAP) - GAP
        # label
        body.append(f'<text x="{PAD}" y="{row_top + 16}" font-size="11" letter-spacing="2" fill="{color}" filter="url(#soft)"><tspan font-size="14" font-weight="bold">{i + 1:02d}</tspan><tspan dx="8">{escape(label)}</tspan></text>')
        for cx, cy, w, c in placed:
            body.append(f'<rect x="{cx:.1f}" y="{cy}" width="{w:.1f}" height="{CHIP_H}" rx="3" fill="{chip_fill}" fill-opacity="{chip_fo}" stroke="{color}" stroke-opacity="{chip_so}"/>')
            body.append(f'<text x="{cx + w/2:.1f}" y="{cy + 16}" text-anchor="middle" font-size="{FS}" fill="{T["text"]}">{escape(c)}</text>')
        y = row_top + row_h
        if i < len(rows) - 1:
            body.append(f'<line x1="{PAD}" y1="{y + 11}" x2="{W - PAD}" y2="{y + 11}" stroke="url(#sep)" stroke-width="1"/>')
        y += 22
    H = y + 12
    out = f'''<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{escape(title)}">
  <title>{escape(title + ': ' + '; '.join(l + ' - ' + ', '.join(c) for l, _, c in rows))}</title>
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{T["bg"][0]}"/><stop offset=".5" stop-color="{T["bg"][1]}"/><stop offset="1" stop-color="{T["bg"][0]}"/></linearGradient>
    <linearGradient id="edge" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{T["edge"][0]}"/><stop offset=".5" stop-color="{T["edge"][1]}"/><stop offset="1" stop-color="{T["edge"][2]}"/></linearGradient>
    <linearGradient id="sep" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{T["edge"][0]}" stop-opacity="0"/><stop offset=".5" stop-color="{T["edge"][1]}" stop-opacity=".35"/><stop offset="1" stop-color="{T["edge"][2]}" stop-opacity="0"/></linearGradient>
    <filter id="glow"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
    <filter id="soft"><feGaussianBlur stdDeviation="1.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  </defs>
  <rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="12" fill="url(#bg)" stroke="url(#edge)" stroke-opacity=".55"/>
  <polyline points="14,30 14,14 30,14" fill="none" stroke="{T["edge"][0]}" stroke-width="2" filter="url(#soft)"/>
  <polyline points="{W-30},14 {W-14},14 {W-14},30" fill="none" stroke="{T["edge"][2]}" stroke-width="2" filter="url(#soft)"/>
  <polyline points="14,{H-30} 14,{H-14} 30,{H-14}" fill="none" stroke="{T["edge"][0]}" stroke-width="2" filter="url(#soft)"/>
  <polyline points="{W-30},{H-14} {W-14},{H-14} {W-14},{H-30}" fill="none" stroke="{T["edge"][2]}" stroke-width="2" filter="url(#soft)"/>
  <g font-family="{FONT}">
    <text x="{W/2}" y="44" text-anchor="middle" font-size="16" letter-spacing="5" fill="{T["title"]}" filter="url(#glow)">{escape(title)}</text>
    {chr(10).join('    ' + b for b in body)}
  </g>
</svg>
'''
    if light:
        out = out.replace(' filter="url(#glow)"', '').replace(' filter="url(#soft)"', '')
        out = out.replace('font-size="11" letter-spacing="2"', 'font-size="11" font-weight="bold" letter-spacing="2"')
        dots = '<pattern id="dots" width="16" height="16" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="#7b2fc4" fill-opacity=".09"/></pattern>'
        out = out.replace('</defs>', '  ' + dots + chr(10) + '  </defs>', 1)
        out = out.replace('stroke="url(#edge)" stroke-opacity=".55"/>', 'stroke="url(#edge)" stroke-opacity=".7" stroke-width="1.5"/>' + chr(10) + '  <rect x="2" y="2" width="%d" height="%d" rx="11" fill="url(#dots)"/>' % (W-4, H-4), 1)
        out = out.replace('font-size="16" letter-spacing="5"', 'font-size="16" font-weight="bold" letter-spacing="5"')
    return out

for lang, base in (('en', 'stack'), ('it', 'stack-it')):
    for theme in ('dark', 'light'):
        name = base + ('-light' if theme == 'light' else '') + '.svg'
        with open(os.path.join(OUT, name), 'w', encoding='utf-8') as f:
            f.write(build(lang, theme))
        print(name)
