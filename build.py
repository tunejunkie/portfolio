"""Generates the static site into ./site from the templates below.
Run: python3 build.py   (no dependencies). Netlify publishes ./site as-is."""
import os, json, html
ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(ROOT, 'site')

CASES = [('saturn', 'Saturn', '2022–25'), ('trovy', 'Trovy', '2025–now'), ('upclose', 'UpClose', '2019–21')]
# case studies live elsewhere for now (open in a new tab); Trovy's isn't written yet, so its links go nowhere
CASE_URL = {
    'saturn': 'https://www.figma.com/proto/TfLHs6KosHbqvohQuOCKrF/Saturn-Case-Study?node-id=11-2804&viewport=1147%2C248%2C0.1&t=kBngw21bYzdQaSPf-1&scaling=contain&content-scaling=fixed&starting-point-node-id=11%3A2804&page-id=0%3A1&show-proto-sidebar=1',
    'upclose': 'https://docs.google.com/presentation/d/1EhMxjJ5FQsxnl-vreup7qm2kCwr8z8IQObILE_G_XuQ/edit?usp=sharing',
}
def case_attrs(slug):
    u = CASE_URL.get(slug)
    return f'href="{u}" target="_blank" rel="noopener"' if u else 'href="#" data-dud aria-disabled="true"'
GALLERIES = [  # slug, name, years  (grid order; gigmo is menu-only)
    ('candle', 'I Lit A Candle', '2026'), ('trovy', 'Trovy', '2025–Current'), ('wherei', 'WhereI AI', '2026'),
    ('monstro', 'Monstro', '2024'), ('saturn', 'Saturn', '2022–25'), ('kyn', 'Kyn', '2024'),
    ('transforce', 'TransForce', '2024'), ('honored', 'HonorEd', '2021'), ('abbott', 'Abbott', '2020'),
    ('upclose', 'UpClose', '2019–21'), ('adecco', 'Adecco', '2020–21'), ('monster', 'Monster', '2018–22'),
    ('gigmo', 'Gigmo', '2020'),
]
LINKEDIN = 'https://www.linkedin.com/in/natalierosetaylor/'
GITHUB = 'https://github.com/tunejunkie'
CHEV = '<svg viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'

def nav(base, light=False):
    cs = ''.join(f'<a {case_attrs(s)}>{n}<small>{y}</small></a>' for s, n, y in CASES)
    gl = ''.join(f'<a href="{base}screenshots/{s}/">{n}<small>{y}</small></a>' for s, n, y in GALLERIES)
    a = f'{base}assets/svg/'
    ab = (f'<a href="{base}#about" data-about>About me</a>'
          f'<a href="{base}#anecdotes" data-jump="anecdotes">Anecdotes</a>'
          f'<a href="{base}work-history/">Work History</a>'
          f'<a href="{LINKEDIN}" target="_blank" rel="noopener">Contact<small>LinkedIn</small></a>')
    return f'''<header class="nav{' nav--light' if light else ''}">
  <a class="logo" href="{base}" aria-label="Natalie Rose Taylor, home">
    <img class="on-light" src="{a}flower.svg" alt=""><img class="on-dark" src="{a}flower-light.svg" alt="">
    <span>Natalie<br>Rose Taylor</span></a>
  <ul class="menu">
    <li><button aria-haspopup="true">Case Studies {CHEV}</button><div class="dd">{cs}</div></li>
    <li><button aria-haspopup="true">Screenshots {CHEV}</button><div class="dd dd--grid">{gl}</div></li>
    <li><button aria-haspopup="true">About {CHEV}</button><div class="dd dd--about">{ab}</div></li>
  </ul>
  <div class="social">
    <a href="{LINKEDIN}" target="_blank" rel="noopener" aria-label="LinkedIn"><img class="on-light" src="{a}linkedin-dark.svg" alt=""><img class="on-dark" src="{a}linkedin-light.svg" alt=""></a>
    <a href="{GITHUB}" target="_blank" rel="noopener" aria-label="GitHub"><img class="on-light" src="{a}github-dark.svg" alt=""><img class="on-dark" src="{a}github-light.svg" alt=""></a>
  </div>
  <button class="burger" aria-label="Menu"><i></i><i></i><i></i></button>
</header>
<nav class="sheet" aria-label="Mobile menu">
  <button class="sheet-close" aria-label="Close menu">×</button>
  <h3>Case studies</h3>{''.join(f'<a {case_attrs(s)}>{n}</a>' for s, n, y in CASES)}
  <h3>Screenshots</h3><div class="grid2">{''.join(f'<a href="{base}screenshots/{s}/">{n}</a>' for s, n, y in GALLERIES)}</div>
  <h3>About</h3><a href="{base}#about" data-about>About me</a><a href="{base}#anecdotes" data-jump="anecdotes">Anecdotes</a><a href="{base}work-history/">Work History</a><a href="{LINKEDIN}" target="_blank" rel="noopener">Contact</a><a href="{GITHUB}" target="_blank" rel="noopener">GitHub</a>
</nav>'''

def head(title, base, desc='Natalie Rose Taylor — staff product designer in Brooklyn.'):
    return f'''<!doctype html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title><meta name="description" content="{html.escape(desc)}">
<link rel="icon" href="{base}assets/img/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Alan+Sans:wght@400;600;700&family=New+Amsterdam&family=Plus+Jakarta+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{base}css/main.css">
<meta property="og:title" content="{html.escape(title)}"><meta property="og:image" content="{base}assets/img/hero-profile.webp">
</head>'''

NPATH = open(os.path.join(ROOT, 'npath.txt')).read()
from loader_svg import flower_svg
from anecdotes import anecdotes_section

TEASERS = [
    dict(slug='saturn', name='Saturn', dark=False,
         body='The social calendar for high schoolers: classes, plans and friends on one screen. I led design for three years, from Series A to acquisition by Snap.',
         meta=[('68x', 'installs'), ('13x', 'sharing'), ('+47%', 'K-factor')]),
    dict(slug='trovy', name='Trovy', dark=True,
         body='A HELOC that works like a credit card. As founding designer I shaped all of it — the brand, the gold card, the application, the account dashboard and the ads.',
         meta=[('Seed → $100MM', 'PMV in one year'), ('0 → 1', 'end to end')]),
    dict(slug='upclose', name='UpClose', dark=False,
         body='Making plans shouldn’t take twenty messages. My own startup turned it into three questions, and a chatbot handles the back-and-forth for you.',
         meta=[('~1,000', 'users'), ('30k', 'App Store views'), ('5.0★', 'rating')]),
]

def gallery_cards(base=''):
    out = []
    for i, (slug, name, years) in enumerate(GALLERIES[:12]):
        out.append(f'''<li><a class="gal-card" href="{base}screenshots/{slug}/">
        <img src="{base}assets/thumbs/t{i+1:02d}.webp" alt="" loading="lazy" width="1000" height="1000">
        <span class="gal-over"><strong>{name}</strong><span>{years}</span></span></a></li>''')
    return ''.join(out)

def index():
    teasers = ''.join(f'''
    <article class="teaser{' is-dark' if t['dark'] else ''}" data-case="{t['slug']}">
      <span class="pill">Case study</span>
      <h2>{t['name']}</h2>
      <p>{t['body']}</p>
      <div class="meta">{''.join(f'<div><b>{a}</b><span>{b}</span></div>' for a, b in t['meta'])}</div>
      <a class="btn {'btn--dark' if t['dark'] else 'btn--primary'}" {case_attrs(t['slug'])}>Read Case Study</a>
    </article>''' for t in TEASERS)
    return head('Natalie Rose Taylor — Product Designer', '') + f'''
<body class="home">
<div class="loader" aria-hidden="true">{flower_svg()}</div>
{nav('')}
<main>
  <section class="stage" aria-label="Introduction and featured case studies">
    <div class="bg bg--hero"></div><div class="bg bg--saturn"></div><div class="bg bg--trovy"></div><div class="bg bg--upclose"></div>
    <canvas id="phones" aria-hidden="true"></canvas>
    <h1 class="hero-copy">
      <span class="line"><span class="w">AI-empowered digital</span></span>
      <span class="line"><span class="w">product</span><span class="hs"><img src="assets/img/hero-headshot-ellipse.webp" alt="Natalie"></span><span class="w">designer</span></span>
      <span class="line"><span class="w">based in Brooklyn.</span></span>
    </h1>
    {teasers}
    <p class="proc-copy">Specializing in native mobile, and going from 0-1.</p>
    <div class="scroll-hint">Scroll<i></i></div>
    <button class="tapzone" aria-label="Show the next screenshot" style="display:none"></button><div class="tap-hint" aria-live="polite"></div>
  </section>
  <section class="about" id="about" aria-label="About me">
    <div class="ab-pink"></div>
    <div class="ab-board">
      <div class="ab-circle"></div>
      <svg class="ab-map" viewBox="0 0 1728 1117" aria-hidden="true">
        {"".join(f'<path class="ab-line" fill="none" stroke="none"/><g class="ab-dots" fill="#F8F8F8"></g>' for i in range(3))}
      </svg>
      <img class="ab-out ab-out-wa" src="assets/svg/washington.svg" alt="">
      <img class="ab-out ab-out-ny" src="assets/svg/new-york.svg" alt="">
      <img class="ab-out ab-out-ca" src="assets/svg/california.svg" alt="">
      <span class="ab-lab ab-lab-sea">SEA</span><span class="ab-lab ab-lab-ny">NYC</span><span class="ab-lab ab-lab-sf">SFO</span>
      <img class="ab-ring" src="assets/svg/about-ring.svg" alt="">
      <img class="ab-portrait" src="assets/img/portrait.webp" alt="Portrait of Natalie Rose Taylor">
      {"".join(f'<figure class="ab-photo"><img src="assets/img/about-{9-i:02d}{"-anim" if 9-i in (6,9) else ""}.webp" loading="lazy" alt="Natalie: {t.lower()}"></figure>' for i,t in enumerate(['Cellist','Fine Artist','Wife','Mom','Traveler','Karaoke-er','Boater','Dog mom','Skater']))}
      <div class="ab-hello"><h2>Hello, I’m Natalie.</h2><a class="btn btn--stroke ab-btn" href="#about-more"><svg width="14" height="14" viewBox="0 0 16 16" fill="none"><path d="M8 3v10M3.5 8.5 8 13l4.5-4.5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>About Me</a></div>
      <p class="ab-t1">Seattle-raised New York transplant of 15 years.</p>
      <p class="ab-t2">*plus three career-building years in SF</p>
      <div class="ab-work">
        <div class="ab-work-head"><h2>12+ years of shipping consumer products.</h2><a class="btn btn--stroke" href="work-history/">See Work History</a></div>
        <div class="ab-logos" aria-label="Companies and products I've designed for"><img src="assets/logos/saturn.png" alt="Saturn"><img src="assets/logos/sofi.png" alt="SoFi"><img src="assets/logos/trovy.png" alt="Trovy"><img src="assets/logos/bcg.png" alt="BCG Digital Ventures"><img src="assets/logos/huge.png" alt="Huge"><img src="assets/logos/monster.png" alt="Monster"><img src="assets/logos/honor-ed.png" alt="Honor Education" class=tall></div>
        <div class="ab-logos"><img src="assets/logos/elephant-and-apple.png" alt="Elephant, for Apple"><img src="assets/logos/designMap.png" alt="DesignMap"><img src="assets/logos/transforce.png" alt="TransForce"><img src="assets/logos/adecco.png" alt="Adecco"><img src="assets/logos/upclose.png" alt="UpClose"><img src="assets/logos/radar.png" alt="Radar"></div>
      </div>
      <div class="ab-slash"><span>I’m a designer slash</span><strong class="ab-title" aria-live="polite">Cellist</strong></div>
    </div>
    <div class="scroll-hint is-light ab-hint">Scroll<i></i></div>
  </section>
  <section class="galleries" id="galleries" aria-labelledby="galleries-title">
    <div class="gal-head">
      <h2 id="galleries-title">Screenshot Galleries</h2>
      <p>UI is only one part of what I do, but I am prolific at it. <br>Enter a gallery to explore a project.</p>
    </div>
    <ul class="gal-grid">{gallery_cards()}</ul>
  </section>
  {anecdotes_section()}
  <section class="summary" id="summary" aria-label="Professional summary">
    <div class="summary-inner">
      <p class="summary-lede">Natalie Rose Taylor is a player-coach design leader experienced in shipping practical, delightful, and well-crafted design for startups and public companies alike. Currently transitioning to design engineering.</p>
      <p class="summary-contact">Please contact me on <a href="{LINKEDIN}" target="_blank" rel="noopener">LinkedIn</a> for any inquiries.</p>
    </div>
    <div class="wave" aria-label="Legal to work in the United States, Canada and Great Britain"><div class="wave-track"><span class="wave-item wave-label">Legal to work in</span><span class="wave-item wave-flag"><img src="assets/svg/flag-usa.svg" alt="United States" width="120" height="120"></span><span class="wave-item wave-label">Legal to work in</span><span class="wave-item wave-flag"><img src="assets/svg/flag-canada.svg" alt="Canada" width="120" height="120"></span><span class="wave-item wave-label">Legal to work in</span><span class="wave-item wave-flag"><img src="assets/svg/flag-gb.svg" alt="Great Britain" width="120" height="120"></span></div></div>
  </section>
</main>
<script src="js/vendor/gsap.min.js"></script>
<script src="js/vendor/ScrollTrigger.min.js"></script>
<script src="js/vendor/lenis.min.js"></script>
<script type="importmap">{{"imports":{{"three":"./js/vendor/three.module.min.js"}}}}</script>
<script type="module" src="js/home.js"></script>
</body></html>'''

from gallery_data import GAL, CAPTIONS, groups_for, BORDERED
CHEV_L = '<svg viewBox="0 0 24 24" fill="none"><path d="M15 18L9 12L15 6" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>'
CHEV_R = '<svg viewBox="0 0 24 24" fill="none"><path d="M9 6L15 12L9 18" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>'

def lum(h):
    r, g, b = (int(h[i:i+2], 16) / 255 for i in (1, 3, 5))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

WAVE_TOP = '<svg class="l3-wave l3-wave--top" viewBox="0 0 1728 124" preserveAspectRatio="none" aria-hidden="true"><path d="M0 46 C 360 -8, 760 -6, 1100 40 C 1380 78, 1600 70, 1728 52 L1728 0 L0 0 Z"/></svg>'
WAVE_BOT = '<svg class="l3-wave l3-wave--bot" viewBox="0 0 1728 124" preserveAspectRatio="none" aria-hidden="true"><path d="M0 64 C 300 6, 760 10, 1080 48 C 1360 82, 1580 84, 1728 58 L1728 124 L0 124 Z"/></svg>'

def gallery_page(slug, manifest):
    g = GAL[slug]; base = '../../'
    order = [x[0] for x in GALLERIES]; k = order.index(slug)
    prev, nxt = GALLERIES[k - 1], GALLERIES[(k + 1) % len(GALLERIES)]
    caps = CAPTIONS.get(slug)
    by = {}
    for j, it in enumerate(manifest[slug]):
        title, cap = (caps[j] if caps else (it['title'], it['caption']))
        by[it['src'][:3]] = dict(it, title=title, caption=cap)
    groups, ctx = groups_for(slug, manifest[slug])
    def fig(n, plat):
        it = by[n]; esc = html.escape
        crop = ' is-bordered' if n in BORDERED.get(slug, ()) else ''
        if it.get('alpha'): crop += ' is-alpha'
        if plat == 'o':
            frame = f'<div class="l3-frame l3-frame--o{crop}"><img src="{base}assets/galleries/{slug}/{it["src"]}" alt="{esc(it["title"])}" loading="lazy" width="{it["w"]}" height="{it["h"]}"></div>'
        else:
            frame = f'<div class="l3-frame l3-frame--{plat}{crop}"><div class="l3-view"><img src="{base}assets/galleries/{slug}/{it["src"]}" alt="{esc(it["title"])}" loading="lazy" width="{it["w"]}" height="{it["h"]}"></div></div>'
        cap = f'<span>{esc(it["caption"])}</span>' if it['caption'] else ''
        return f'<figure class="l3-fig">{frame}<figcaption><strong>{esc(it["title"])}</strong>{cap}</figcaption></figure>'
    secs = []
    for name, plat, nums in groups:
        if not nums: continue
        secs.append(f'''<section class="l3-sec"><div class="l3-label"><h2>{html.escape(name)}</h2><span>{len(nums)} screen{'s' if len(nums) > 1 else ''}</span></div>
      <div class="l3-grid l3-grid--{plat}">{''.join(fig(n, plat) for n in nums)}</div></section>''')
    if ctx:
        secs.append(f'''<section class="l3-sec"><div class="l3-label"><h2>In Context</h2><span>{len(ctx)} image{'s' if len(ctx) > 1 else ''}</span></div>
      <div class="l3-grid l3-grid--o">{''.join(fig(n, 'o') for n in ctx)}</div></section>''')
    meta = ''.join(f'<div><dt>{a}</dt><dd>{b}</dd></div>' for a, b in g['meta'])
    return head(f"{g['name']} Screenshots — Natalie Rose Taylor", base, g['sum']) + f'''
<body class="gallery" data-base="{base}">
{nav(base)}
<main class="l3">
  <header class="l3-top">
    <div class="l3-head">
      <h1>{g['name']}</h1>
      <p class="sum">{g['sum']}</p>
      <dl class="l3-meta">{meta}</dl>
    </div>
  </header>
  <div class="l3-body">
    {''.join(secs)}
  </div>
  {WAVE_BOT}
  <footer class="l3-foot"><div class="l3-foot-in">
    <a class="btn btn--stroke" href="{base}screenshots/{prev[0]}/">{CHEV_L}{prev[1]}</a>
    <p>I’m the sole designer on all screens displayed unless explicitly noted.</p>
    <a class="btn btn--stroke" href="{base}screenshots/{nxt[0]}/">{nxt[1]}{CHEV_R}</a>
  </div></footer>
</main>
<script>(function(){{function f(){{document.documentElement.style.setProperty('--s',Math.max(.55,Math.min(innerWidth/1728,innerHeight/1117)).toFixed(4))}}f();addEventListener('resize',f)}})()</script>
<script type="module" src="{base}js/gallery.js"></script>
</body></html>'''

from work_history import work_history

def write(path, s):
    p = os.path.join(SITE, path); os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'w').write(s)

if __name__ == '__main__':
    page = index()
    write('index.html', page)
    # artifact preview: same page without the document wrapper (the host adds its own)
    import re
    body = re.sub(r'^<!doctype html><html lang="en"><head>\s*<meta charset="utf-8"><meta name="viewport"[^>]*>', '', page)
    body = body.replace('</head>', '').replace('<body class="home">', '<script>document.body.classList.add("home")</script>').replace('</body></html>', '')
    write('_preview.html', body)
    manifest = json.load(open(os.path.join(SITE, 'assets/galleries/manifest.json')))
    for slug, _, _ in GALLERIES:
        write(f'screenshots/{slug}/index.html', gallery_page(slug, manifest))
    write('work-history/index.html', work_history())
    print('built')
