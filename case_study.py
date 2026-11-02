"""Saturn case study #1, the Now tab (/case-studies/saturn-home/; the Nike/ads story will be its own page): a deck of full-screen "slides".

Desktop: every slide is laid out on a fixed 1728×1117 art board (the Figma frame) that is scaled to the
window, and the deck runs in one of two modes, switched with the toggle at the top:
  - Scroll mode: scrolling steps through the slides (scroll-jacked, like the homepage), with snapping.
  - Slide mode: a presentation — arrow keys / space / buttons, the page itself doesn't scroll.
Some slides have several steps: the slide stays put and the 3D phone spins to a new screen.
Phones: the same slides stack into a normal scrolling page.

Copy is Natalie's (Figma 1248:6613). [Bracketed] text and grey boxes are placeholders she will replace.
"""
import html

E = html.escape
ASSET = 'assets/cs/saturn/'

# chapters for the outline at the top right; each slide names its chapter
from saturn_scenes import CHAPTERS

# background colour of each slide, sampled down the Figma page (deep purple at the top → blue at the end)
BG = {'hero': '#15082e', 'context': '#191239', 'before': '#1c1a41', 'problem': '#202349', 'research': '#232b52',
      'hunch': '#253159', 'build': '#283961', 'gallery': '#2a4067', 'lessons': '#2e4970', 'results': '#304e76'}


def pill(t):
    return f'<span class="cs-pill">{E(t)}</span>'


def checks(label, items, colour):
    li = ''.join(f'<li data-a>{t}</li>' for t in items)
    return f'<div class="cs-checks" style="--bar:{colour}"><p class="cs-checks-h" data-a>{label}</p><ul>{li}</ul></div>'


def slide(key, chapter, inner, steps=1, cls=''):
    return (f'<section class="cs-slide cs-{key} {cls}" data-key="{key}" data-chapter="{chapter}" data-steps="{steps}" '
            f'data-bg="{BG[key]}" aria-label="{key}"><div class="cs-fit">{inner}</div></section>')


def phone_slot(screens, label):
    """Where the 3D phone stands on this slide. `screens` = one texture per step (None = grey 'asset needed')."""
    data = ','.join(s or '' for s in screens)
    # phones (no WebGL / mobile layout) get flat screens in a CSS frame instead
    flat = ''.join(
        (f'<img src="{{base}}{s}" alt="" loading="lazy">' if s else '<span class="cs-gray">Screen needed</span>')
        for s in screens)
    return f'<div class="cs-phone-slot" data-screens="{data}" aria-label="{E(label)}"><div class="cs-flat">{flat}</div></div>'


META = [('Role', 'Lead Designer'), ('Industry', 'Social'), ('Designs circa', '2022–2025'),
        ('Employment type', 'Full-time'), ('Exit', 'Acquired by Snap')]
TITLE = 'Saturn: From class timer to calendar'
LEDE = 'A case study in turning a beloved single-purpose utility for high-school students into a calendar platform teenagers actually use.'


def hero_copy(heading='h1'):
    a = ' data-a' if heading != 'h1' else ''
    return f'''<div class="cs-hero-copy">
        <div class="cs-hero-top">
          <{heading} class="cs-title"{a}><img src="{{base}}assets/cs/saturn/v4/saturn-logo.webp" alt="Saturn" width="608" height="120"><span class="vh">: From class timer to calendar</span></{heading}>
          <p class="cs-lede"{a}>{E(LEDE)}</p>
        </div>
        <dl class="cs-meta">{''.join(f'<div{a}><dt>{x}</dt><dd>{y}</dd></div>' for x, y in META)}</dl>
      </div>'''


def slides():
    from saturn_scenes import slides as v4
    return v4()


def case_study_saturn():
    from build import head, nav, SITE_FOOTER
    base = '../../'
    body = ''.join(slides()).replace('{base}', base)
    outline = '<span class="cs-line"></span>'.join(f'<button data-chapter="{i}">{c}</button>' for i, c in enumerate(CHAPTERS))
    toggle = '''<div class="cs-mode" role="radiogroup" aria-label="How to read this case study">
          <button role="radio" data-mode="scroll" aria-checked="true">Scroll</button>
          <button role="radio" data-mode="slides" aria-checked="false">Slides</button>
        </div>'''
    intro = f'''<section class="cs-intro" aria-label="{E(TITLE)}">
    <div class="cs-intro-board">
      {hero_copy().replace('{base}', base)}
      <div class="cs-video"><video src="{base}{ASSET}teaser.mp4" poster="{base}{ASSET}teaser-poster.jpg" muted loop playsinline autoplay preload="metadata"></video></div>
    </div>
  </section>'''
    return head(f'{TITLE} — Natalie Rose Taylor', base,
                'Saturn: how a beloved single-purpose class timer for high schoolers got a true home screen, then a calendar students actually use.') .replace(
        '</head>', f'<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@700&family=Plus+Jakarta+Sans:wght@700;800&display=swap" rel="stylesheet"><link rel="stylesheet" href="{base}css/cs.css"><meta name="robots" content="noindex"></head>') + f'''
<body class="cs-page is-scroll" data-base="{base}">
{nav(base, light=True)}
<div class="cs-bar">
  <a class="logo cs-satlogo" href="#top" aria-label="Saturn case study, back to the top"><img src="{base}assets/cs/saturn/v4/saturn-logo.webp" alt="saturn" width="203" height="40"></a>
  <nav class="cs-outline" aria-label="Chapters">{outline}</nav>
  {toggle}
</div>
<main class="cs" id="top">
  {intro}
  <div class="cs-track">
    <div class="cs-deck">
      <canvas class="cs-gl" aria-hidden="true"></canvas>
      <div class="cs-board">{body}

      </div>
      <div class="cs-ctrl" aria-label="Slide controls">
        <button class="cs-prev" aria-label="Previous slide"><svg viewBox="0 0 24 24"><path d="M15 18L9 12L15 6"/></svg></button>
        <span class="cs-count" aria-live="polite">1 / 1</span>
        <button class="cs-next" aria-label="Next slide"><svg viewBox="0 0 24 24"><path d="M9 6L15 12L9 18"/></svg></button>
        <span class="cs-keys">← → or space</span>
      </div>
      <div class="cs-progress"><i></i></div>
      <div class="cs-hint">Scroll<i></i></div>
    </div>
  </div>
</main>
{SITE_FOOTER}
<script src="{base}js/vendor/gsap.min.js"></script>
<script src="{base}js/vendor/lenis.min.js"></script>
<script type="importmap">{{"imports":{{"three":"{base}js/vendor/three.module.min.js"}}}}</script>
<script type="module" src="{base}js/cs.js"></script>
</body></html>'''
