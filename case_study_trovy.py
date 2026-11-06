"""Trovy case study (/case-studies/trovy-design-engineer/), v2 — Natalie's redesign in Figma
(xsFoIEpsO6xISuYx8oFAyU, section "Trovy" 1505:103725).

Same deck as Saturn (cs.js / cs.css): Scroll or Slides mode on desktop, stacked page on phones. Each slide is a
v4 "scene": a 1728×1021 board (the Figma frame minus its 96px bar) of blocks placed at Figma coordinates with
`ab()`; on phones the blocks fall back into normal flow in source order.

Each slide has its own background (data-bg); cs.js crossfades a full-viewport layer per slide when the deck
has `data-bgs`. Handwritten notes are images captured from Figma (the font, Figma Hand, isn't on the web).
Live bits: the 3D card (js/card3d.js), the application prototype (/proto/trovy-apply/), the homepage build
(/proto/trovy-home/) and the Renovate before/after slider (cs.js).
"""
import html

E = html.escape
ASSET = 'assets/cs/trovy/'
V2 = ASSET + 'v2/'
CHAPTERS = ['Context', 'Homepage', 'Renovate', 'Takeaways']

INK = '#000b22'
CREAM = 'linear-gradient(180deg,#fef0d4 0%,#fdf3df 45%,#f8f8f8 100%)'
BG = {
    # title: the row of houses sits on the bottom edge of the screen, with its note, as part of the background
    # (W = the houses' width: the full window, or wider on short windows; they start 54% down and crop at the bottom)
    'hero': ('url({base}' + V2 + 'note-title.webp) left calc(50vw + max(100vw,150vh) * .1128) top calc(54vh + max(100vw,150vh) * .0515) / calc(max(100vw,150vh) * .1042) auto no-repeat,'
             'url({base}' + V2 + 'houses.webp) center top 54vh / max(100vw,150vh) auto no-repeat,'
             'linear-gradient(180deg,#a8d3ff 0%,#fff1d2 68.65%)'),
    'context': 'linear-gradient(180deg,#fdba1f 0%,#fb793a 50%,#9079ff 100%)',
    'apply': 'linear-gradient(180deg,#9079ff 0%,#fb793a 100%)',
    'job2': 'linear-gradient(180deg,#fb793a 0%,#fdba1f 100%)',
    'brand': '#ffd435',
    'ads': 'linear-gradient(180deg,#ffd435 0%,#fb793a 55%,#9079ff 100%)',
    'home': 'linear-gradient(180deg,#fee3a5 0%,#f9f9fb 100%)',
    'renovate': CREAM, 'flow': CREAM, 'process': CREAM,
    'learned': 'linear-gradient(180deg,#fef0d4 0%,#ffcd5c 100%)',
    'thanks': 'linear-gradient(180deg,#ffcd5c 0%,#fb793a 100%)',
}


def ab(x, y, w, inner, cls='', h=None, extra=''):
    hh = f';--h:{h}' if h is not None else ''
    return f'<div class="ab {cls}" style="--x:{x};--y:{y};--w:{w}{hh}"{extra}>{inner}</div>'


def scene(key, chapter, inner, cls=''):
    return (f'<section class="cs-slide cs-v4 tv2 cs-{key} {cls}" data-key="{key}" data-chapter="{chapter}" data-steps="1" '
            f'data-bg="{BG[key]}" aria-label="{key}"><div class="cs-fit"><div class="cs-scene">{inner}</div></div></section>')


def note(name, x, y, w, alt):
    """A handwritten note + arrow from the Figma file (frame coordinates → scene: y - 96)."""
    return ab(x, y - 96, w, f'<img class="tv-note" data-a src="{{base}}{V2}note-{name}.webp" alt="{E(alt)}">', 'tv-noteab')


def pic(src, alt, cls=''):
    return f'<img class="{cls}" data-a src="{{base}}{src}" alt="{E(alt)}" loading="lazy">'


META = [('Role', 'Founding Designer'), ('Industry', 'Fintech · Home equity'), ('Designs circa', '2025–2026'),
        ('Employment type', 'Full-time'), ('Built with', 'HTML/CSS/JS, AI coding agents [+ stack]')]
TITLE = 'Trovy: From designer to design engineer'
LEDE = 'How I went from handing engineering Figma files to shipping production code at a fintech startup.'


def hero_copy(heading='h1'):
    a = ' data-a' if heading != 'h1' else ''
    logo = (f'<span class="tv-logo"{a}><img src="{{base}}{ASSET}trovy-icon.svg" alt="" width="74" height="67">'
            f'<img src="{{base}}{ASSET}trovy-wordmark.svg" alt="" width="179" height="61"></span>')
    return f'''<div class="cs-hero-copy tv-hero-copy">
        <div class="tv-hero-top">
          <{heading} class="cs-title tv-title">{logo}<span class="tv-sr">{E(TITLE)}</span></{heading}>
          <p class="cs-lede tv-lede"{a}>{E(LEDE)}</p>
        </div>
        <hr class="tv-rule"{a}>
        <dl class="cs-meta">{''.join(f'<div{a}><dt>{x}</dt><dd>{y}</dd></div>' for x, y in META)}</dl>
      </div>'''


def slides():
    hero = scene('hero', 0, ab(60, 52, 1608, hero_copy(heading='h2')))

    context = scene('context', 0,
        ab(359, 168, 1010, f'''<h2 class="sh64" data-a>Your home equity, in your wallet.<sup class="tv-tm">™</sup></h2>
          <p class="tv-b22 tv-ctx-p" data-a>In 2025, I joined as the founding and sole designer, and shipped the brand, the card, the application, the account dashboard, the marketing site and the ads. What started as a traditional design role morphed into something new.</p>''', 'tc')
        + ab(554, 275, 620, f'''<button type="button" class="tv-card3d" data-a data-glb="{ASSET}card.glb" aria-label="The gold Trovy Mastercard in 3D. Tap to spin it.">
            <img class="tv-card3d-flat" src="{{base}}{ASSET}card.webp" alt="" width="620" height="620">
            <i class="tv-card3d-shadow" aria-hidden="true"></i>
            <canvas aria-hidden="true"></canvas>
            <span class="tv-card3d-hint" aria-hidden="true">Tap to spin</span>
          </button>''')
        + note('ctxA', 1233, 166, 150, 'Handwritten note: I came up with that!')
        + note('ctxB', 1104, 829, 144, 'Handwritten note: Figma + Claude'))

    # Job 1: the application prototype in a phone
    apply = scene('apply', 0,
        ab(60, 251, 780, '''<h2 class="sh64" data-a>Job 1: Relentlessly alleviate friction.</h2>
          <p class="tv-b22 tv-mt56" data-a>Trovy went from 0–100MM PMV in one year of operation by relentlessly alleviating friction in the application flow. A HELOC is one of the cheapest ways to borrow, but it usually means weeks of paperwork and a draw request every time you need money. Trovy is a fully online HELOC, with your line available on a card. I owned the E2E application flow and the online account.</p>
          <p class="tv-cta tv-mt56" data-a>Tap through the prequal flow to see for yourself.</p>''')
        + ab(1109, 77, 399, '''<div class="tv-phone" data-a><iframe data-src="{base}proto/trovy-apply/" title="Interactive prototype of the Trovy application" tabindex="-1"></iframe></div>
          <p class="tv-hint" data-a>Live prototype · tap through it</p>''', 'tc')
        + note('apply', 1523, 166, 150, 'Handwritten note: Figma + Claude'))

    job2 = scene('job2', 0,
        ab(1110, 250, 560, '''<h2 class="sh64" data-a>Job 2: Go beyond table stakes.</h2>
          <p class="tv-b22 tv-mt56" data-a>I designed the application flow, and all the table-stakes experiences that managing financial product required within weeks, working on a close iteration loop with Operations, Product, and Engineering. From that foundation we were able to launch new features and optimizations quickly.</p>''')
        + ab(40, 120, 1010, pic(V2 + 'laptop-dash.webp', 'The Trovy account dashboard on a laptop: credit available, quick actions and account setup', 'tv-fill'), h=607))

    brand_imgs = ''.join(f'<img data-a src="{{base}}{V2}brand-{i:02d}.webp" alt="" loading="lazy">' for i in range(1, 13))
    brand = scene('brand', 0,
        ab(-83, 82, 1894, '''<div class="tv-split"><h2 class="sh64" data-a>Who’s that brand?</h2>
          <p class="tv-b24 tr" data-a>I wanted to break out of the fintech blue/green palette and develop a memorable fintech brand with a provocative signature color. Trovy Gold was reminiscent of sunshine in your backyard, or, a treasure trove.</p></div>''', 'tv-bleed')
        + ab(-89, 269, 1906, f'<div class="tv-brandgrid" role="img" aria-label="Twelve Trovy brand pieces: logos, the gold palette, the card, ads and a billboard">{brand_imgs}</div>', 'tv-bleed'))

    # the story ads: rebuilt in HTML with light motion (proto/trovy-ads/), shown as a swipe through Instagram Stories
    ads = scene('ads', 0,
        ab(60, 251, 780, '''<h2 class="sh64" data-a>So, now they’re gold. But can regulated ads be bold?</h2>
          <p class="tv-b22 tv-mt56" data-a>I explored how the new branding manifests in social media with some directional ads for the marketing team. HELOCs are regulated products, and ads require rigorous legal review from external parties. The design process was aided by integrations with Claude and Notion, so nothing was ever misrepresented or not properly footnoted.</p>''')
        + ab(1109, 77, 399, '''<div class="tv-phone" data-a><video data-src="{base}''' + V2 + '''story-ads.mp4" poster="{base}''' + V2 + '''story-ads-poster.jpg" muted loop playsinline preload="none" aria-label="Twelve Trovy story ads playing one after another in an Instagram Stories screen, swiped through like a viewer would"></video></div>
          <p class="tv-hint" data-a>Screen recording · Instagram Stories</p>''', 'tc'))

    home = scene('home', 1,
        ab(60, 188, 434, '''<h2 class="sh48" data-a>Code without Figma? That’s not the vibe.</h2>
          <p class="tv-b22 tv-mt56" data-a>A designer’s superpower is the ability to succinctly communicate ideas visually. LLMs’ domain is words, and they don’t quite understand the adage “A picture says a thousand words.”</p>
          <p class="tv-b22 tv-mt33" data-a>I always start in Figma, but 75% of my time is spent tweaking and reacting in Claude Code. Here’s my first project: a new marketing site.</p>
          <a class="tv-link tv-mt56" data-a href="{base}proto/trovy-home/" target="_blank" rel="noopener">Open the build full size ↗</a>''')
        + ab(552, 123, 1116, '''<div class="tv-browser2" data-a>
            <div class="tv-browser-bar"><i></i><i></i><i></i><span>trovy.com</span></div>
            <iframe data-src="{base}proto/trovy-home/" title="The coded Trovy homepage, live" loading="lazy" tabindex="-1"></iframe>
          </div>
          <p class="tv-hint" data-a>Live build · scroll inside the frame</p>''', 'tc'))

    renovate = scene('renovate', 2,
        ab(605, 317, 1036, pic(V2 + 'ren-laptop.webp', 'Renovate with Trovy on a laptop: a warm minimalist kitchen design with its versions, estimate and Renault chat', 'tv-fill'), 'tv-behind', h=671)
        + ab(227, 82, 1275, '''<h2 class="sh48" data-a style="text-wrap:balance">Renovate with Trovy was my first large design engineer project.</h2>
          <p class="tv-b28 tv-mt32" data-a>Renovation is the biggest reason homeowners tap their equity, and the point where they are least sure what they want, what it costs and whom to hire.</p>''', 'tc')
        + ab(86, 389, 234, pic(V2 + 'ren-phone.webp', 'Renovate with Trovy on a phone: the kitchen design with a before/after slider', 'tv-fill'), h=586)
        + ab(378, 373, 494, f'''<div class="tv-ba" data-a style="--p:43.7%" role="group" aria-label="Before and after: drag to compare">
            <img src="{{base}}{V2}ren-before.webp" alt="The kitchen before: oak cabinets and tile floor" draggable="false">
            <div class="tv-ba-after"><img src="{{base}}{V2}ren-after.webp" alt="The kitchen after: sage cabinets, brass hardware and wood floor" draggable="false"></div>
            <span class="tv-ba-pill">Before</span><span class="tv-ba-pill tv-ba-pill--after">After</span>
            <input class="tv-ba-range" type="range" min="0" max="100" step="0.1" value="43.7" aria-label="Before/after slider">
            <i class="tv-ba-line" aria-hidden="true"><b><img src="{{base}}{V2}drag.svg" alt=""></b></i>
          </div>''', h=335))

    steps = [('m-upload-photo', 'Start with your room', 'Add a photo and say what should change.'),
             ('m-chat-intent', 'Plan it with Renault', 'A few quick questions: scope, style, budget.'),
             ('m-chat-plan-summary', 'Approve the plan', 'Renault writes a project plan. Edit it or generate now.'),
             ('m-design-ready', 'See your new room', 'Drawn on your own photo, with a before/after slider.'),
             ('m-ready-shop', 'Price it and shop it', 'Materials and labor, each product pinned and linked.')]
    flow = scene('flow', 2,
        ab(60, 64, 1608, '''<div class="tv-split"><h2 class="sh48" data-a>0-1 in one week</h2>
          <p class="tv-b24 tr tv-w760" data-a>Go from your room’s photo to an AI-generated plan, a rendered design, a cost estimate and a shopping list, with the Trovy line as the way to pay for it.</p></div>''')
        + ab(60, 198, 1608, '<ol class="tv-steps2">' + ''.join(
            f'<li data-a><img src="{{base}}{ASSET}{f}.webp" alt="" loading="lazy" width="289" height="626"><h3>{E(h)}</h3><p>{E(p)}</p></li>'
            for f, h, p in steps) + '</ol>'))

    team = [('Team', 'Me, an engineer, a PM', 'We all started on the project concurrently.'),
            ('Process', 'Figma to code to Figma to code', 'I move into code early, working in VS Code, the Claude Code app or Claude in the terminal depending on the task. Many design decisions after that get made in the running build.'),
            ('Tools', 'Claude, Figma, Notion, Slack', '...and ChatGPT and Gemini for video or photo assets.')]
    process = scene('process', 2,
        ab(60, 171, 1608, f'''<div class="tv-procrow">
          <div class="tv-proctext"><h2 class="sh56" data-a>The project and the process</h2>
            <ol class="tv-process">{''.join(f'<li data-a><p class="tv-process-k">{E(k)}</p><h3>{E(t)}</h3><p>{E(p)}</p></li>' for k, t, p in team)}</ol></div>
          <figure class="tv-procfig" data-a><img src="{{base}}{ASSET}process-vscode.webp" alt="VS Code with Claude Code open on the Trovy frontend: the Homeowner Toolkit chat beside a Renovate visual-QA screenshot of Renault asking for a photo of the kitchen" width="1600" height="1003" loading="lazy">
            <figcaption>Claude Code in VS Code, on the Renovate visual-QA captures</figcaption></figure>
        </div>''')
        + note('process', 1111, 140, 197, 'Handwritten note: Getting used to these interfaces'))

    lessons = [('Design input makes the difference.', 'Say less, and send a Figma link. It’s much faster as a seasoned designer for me to describe my ideas in this way, and Claude’s output is better for it.'),
               ('Sweat the small stuff?', 'I used to sweat it in Figma, now I sweat it in code. Figma gives the project direction, code gives it clarity. Claude can help uncover states or conditions I hadn’t fleshed out yet, and we can go back and forth in this way.'),
               ('Source of truth is the kicker.', 'Is it Figma? Is it code? Is it somewhere else? This has been the main friction point. I’m constantly writing back to Figma from Claude, and vice versa. I think all teams are grappling with this issue.'),
               ('Integrate everything your organization can.', 'If all the decisions are being made in Slack, documented in Notion and visualized in Figma, and you connect it all with Claude, the whole company has context about decisions. No meetings???'),
               ('Define ownership and who makes the final call.', 'In an environment in which anyone can “code” or “design”, ownership must be declared. Also provide that context to your coding agent, so it knows whose version wins when there’s a merge conflict.'),
               ('If everyone can ‘do it all’, judgement is everything.', 'Sure, we can now do whatever we want at high speed. But that’s not what successful products/businesses do. “Okay” will become the new floor, and “Incredible” will be the expectation for top companies.')]
    learned = scene('learned', 3,
        ab(60, 47, 1608, f'''<div class="tv-learned">
          <div class="tv-split"><h2 class="sh56" data-a>What I’ve learned so far</h2>
            <p class="tv-b28 tr" data-a>I got my environment set up over the summer of 2026. Here are my takeaways so far on the new way of working.</p></div>
          <div class="tv-lessons">{''.join(f'<div data-a><h3>{E(h)}</h3><p>{E(p)}</p></div>' for h, p in lessons)}</div>
        </div>''', h=870)
        + note('learned', 789, 984, 197, 'Handwritten note: I wrote all this myself, wow'))

    # end: same as the Saturn case study's last scene
    thanks = scene('thanks', 3,
        ab(212, 330, 1304, '<h2 class="sh96" data-a>Questions?</h2>', 'tc')
        + ab(564, 520, 600, '<div class="cs-end" data-a><a href="{base}case-studies/saturn-home/" class="cs-endbtn">Next: Saturn</a></div>', 'tc'))

    return [hero, context, apply, job2, brand, ads, home, renovate, flow, process, learned, thanks]


def case_study_trovy():
    from build import head, nav, SITE_FOOTER
    base = '../../'
    body = ''.join(slides()).replace('{base}', base)
    intro_copy = hero_copy().replace('{base}', base)
    outline = '<span class="cs-line"></span>'.join(f'<button data-chapter="{i}">{c}</button>' for i, c in enumerate(CHAPTERS))
    toggle = '''<div class="cs-mode" role="radiogroup" aria-label="How to read this case study">
          <button role="radio" data-mode="scroll" aria-checked="true">Scroll</button>
          <button role="radio" data-mode="slides" aria-checked="false">Slides</button>
        </div>'''
    intro = f'''<section class="cs-intro" aria-label="{E(TITLE)}">
    <div class="cs-intro-board">
      {intro_copy}
      <div class="cs-video tv-hero-img"><img src="{base}{ASSET}hero.webp" alt="The redesigned Trovy homepage: ‘Let your home take you higher’, a house carried by balloons" width="1600" height="900"></div>
    </div>
  </section>'''
    return head(f'{TITLE} — Natalie Rose Taylor', base,
                'How I went from Figma handoffs to shipping production code at Trovy: the homepage redesign and Renovate with Trovy.').replace(
        '</head>', f'<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@700&family=Plus+Jakarta+Sans:wght@700&display=swap" rel="stylesheet"><link rel="stylesheet" href="{base}css/cs.css"></head>') + f'''
<body class="cs-page cs-page--trovy is-scroll" data-base="{base}">
{nav(base)}
<div class="cs-bar">
  <a class="logo cs-satlogo tv-barlogo" href="#top" aria-label="Trovy case study, back to the top"><img src="{base}{V2}bar-icon.svg" alt="" width="31" height="28"><img src="{base}{V2}bar-wordmark.svg" alt="Trovy" width="75" height="26"></a>
  <nav class="cs-outline" aria-label="Chapters">{outline}</nav>
  {toggle}
</div>
<main class="cs" id="top">
  {intro}
  <div class="cs-track">
    <div class="cs-deck" data-bgs>
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
<script type="module" src="{base}js/card3d.js"></script>
</body></html>'''
