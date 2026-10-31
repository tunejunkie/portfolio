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
CHAPTERS = ['Context', 'Problem', 'Solution', 'Impact']

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
TITLE = 'Saturn: A new home tab'
LEDE = 'A case study in turning a beloved single-purpose utility for high-school students into a calendar platform teenagers actually use — and the company’s first revenue.'


def hero_copy(heading='h1'):
    a = ' data-a' if heading != 'h1' else ''
    return f'''<div class="cs-hero-copy">
        <{heading} class="cs-title"{a}>{E(TITLE)}</{heading}>
        <p class="cs-lede"{a}>{E(LEDE)}</p>
        <dl class="cs-meta">{''.join(f'<div{a}><dt>{x}</dt><dd>{y}</dd></div>' for x, y in META)}</dl>
      </div>'''


def slides():
    # slides mode only: the title slide (no video). Scroll mode opens with the normal-scrolling intro instead.
    hero = slide('hero', 0, hero_copy(heading='h2'))

    context = slide('context', 0, f'''
      <div class="cs-col cs-col--text">
        <div class="cs-head"><h2 class="t64" data-a>Saturn exists because of this.</h2></div>
        <div class="cs-body" data-a>
          <p>The average American high-schooler’s schedule is a mess of conditional class order (“A-day / B-day”), rotating bell schedules, early releases and assemblies. Kids never know what today looks like.</p>
          <p>Saturn solved one thing super well: enter your school and classes once, and it tells you what class you’re in and how many minutes are left. That simple feature made it a viral back-to-school app — and a venture-backed company.</p>
        </div>
      </div>
      <img class="cs-bell cs-bell--a" data-a src="{{base}}{ASSET}bell-grant.webp" alt="Grant High School’s 2025–26 bell schedule: A/B, flex, early-release, assembly and finals variations" width="448" height="520">
      <img class="cs-bell cs-bell--b" data-a src="{{base}}{ASSET}bell-mission.webp" alt="Mission High School’s colour-coded weekly bell schedule" width="515" height="434">''')

    before = slide('before', 0, f'''
      <div class="cs-row">
        <div class="cs-col cs-col--text cs-w434">
          <div class="cs-head"><h2 class="t64" data-a>The app I inherited</h2></div>
          <p class="cs-body" data-a>Saturn was a class timer with a friends list. Students opened it between periods to see how long until the bell, and that habit made it a top back-to-school download every August.</p>
        </div>
        <div class="cs-screens">{''.join(f'<img data-a src="{{base}}{ASSET}before-{i}.webp" alt="" width="298" height="648">' for i in (1, 2, 3))}</div>
      </div>
      {checks('What was working?', ['Our moat: Propriety bell-schedule data for thousands of schools',
                                    'Highly retentive class timer feature drove DAU/WAU',
                                    'Onboarding flywheel with right incentives and timing'], '#3feaac')}''')

    H = '{base}' + ASSET + 'horse/'
    horse = f'''<div class="cs-horse" data-a aria-hidden="true">
          <i style="inset:8.33% 20.83% 68.75% 52.08%"><img src="{H}v0.svg" alt=""></i>
          <i style="inset:39.58% 75% 33.33% 6.25%"><img src="{H}v1.svg" alt=""></i>
          <i style="inset:81.25% 18.75% 14.58% 14.58%"><img src="{H}v2.svg" alt=""></i>
          <i style="inset:12.5% 6.25% 16.67% 20.83%"><img src="{H}v3.webp" alt=""></i>
          <i style="inset:77.08% 68.75% 10.42% 18.75%"><img src="{H}v4.svg" alt=""></i>
          <i style="inset:77.08% 22.92% 10.42% 64.58%"><img src="{H}v4.svg" alt=""></i>
          <i style="inset:20.83% 14.58% 75% 81.25%"><img src="{H}v5.svg" alt=""></i>
          <i style="inset:81.25% 27.08% 14.58% 68.75%"><img src="{H}v6.svg" alt=""></i>
          <i style="inset:81.25% 72.92% 14.58% 22.92%"><img src="{H}v6.svg" alt=""></i>
          <i style="inset:60.44% 55.21% 10.44% 41.93%"><img src="{H}v7.svg" alt=""></i>
          <i style="inset:60.44% 46.14% 10.44% 50.76%"><img src="{H}v8.svg" alt=""></i>
          <i style="inset:64.74% 47.81% 32.16% 43.36%"><img src="{H}v9.svg" alt=""></i>
          <i style="inset:70.7% 47.81% 26.19% 43.36%"><img src="{H}v9.svg" alt=""></i>
          <i style="inset:76.67% 47.81% 20.23% 43.36%"><img src="{H}v9.svg" alt=""></i>
          <i style="inset:82.58% 47.81% 14.32% 43.36%"><img src="{H}v9.svg" alt=""></i>
          <i style="inset:43.44% 46.06% 39.62% 42%"><img src="{H}door.svg" alt=""></i>
        </div>'''


    problem = slide('problem', 1, f'''
      <div class="cs-head"><h2 class="t56" data-a>Complacency was not an option.</h2></div>
      <p class="cs-body cs-body--wide" data-a>Saturn was a beloved app for what it was designed to do. But, <b>usage fell off a cliff after October</b> and stayed flat until July. Years of hacked-together UI with non-standard conventions threatened the strategy of competing with productivity tools. Without a second act, it wasn’t a venture-worthy product.</p>
      {checks('What wasn’t working?', ['Once students memorized their schedule, there was nothing left to do.',
                                      'The schedule was a list, as smart as a piece of paper. Friending had no clear purpose.',
                                      'The current UI made it difficult to promote other features or actions that could help the app evolve'], '#f42c50')}
      <div class="cs-trojan" role="img" aria-label="A Trojan horse; a drawbridge on its front leg drops open and students march out of it, saying: It’s just a timer. It’s just my class list. Why would I add a friend? It’s not a social network.">
        {horse}
        <i class="cs-hatch" aria-hidden="true"></i><i class="cs-bridge" aria-hidden="true"></i>
        <button class="cs-horse-btn" aria-label="Open the Trojan horse"></button><span class="cs-horse-hint" aria-hidden="true">Tap the horse</span>
        <div class="cs-army" aria-hidden="true" data-student="{H}student.svg"
             data-quotes="👎 “It’s just a timer.”|👎 “It’s just my class list.”|👎 “Why would I add a friend?”|👎 “It’s not a social network.”"></div>
      </div>''')

    cards = [('Nobody taps away from home.', 'No banner, badge or notification moved users to other tabs. If it wasn’t above the fold, it didn’t exist.'),
             ('After Oct 1, the timer is the whole app.', 'Every other screen was decoration. Any new bet had to live where the timer lived.'),
             ('One friend changes everything.', 'Students with ≥1 friend who compared schedules retained far better — [METRIC: retention lift]. Social wasn’t a nice-to-have; it was the retention lever.'),
             ('After-school life is busy — and unrecorded.', 'Sports, clubs, jobs. They “just remember.” We risked being a hammer looking for a nail.')]
    research = slide('research', 1, f'''
      <h2 class="t56" data-a>What students told us (and what the data confirmed)</h2>
      <div class="cs-cards">{''.join(f'<div class="cs-card" data-a><span class="cs-num">{i}</span><h3>{E(h)}</h3><p>{E(p)}</p></div>' for i, (h, p) in enumerate(cards, 1))}</div>''')

    # the hunch slide has three steps: the card swaps and the phone spins to a new screen each time.
    # Steps 2–3 are my draft from the earlier write-up (“why this over the alternatives”) — Natalie to confirm.
    hunches = [('Calendar shouldn’t be Home.', 'Students had never used one; we’d be teaching a behavior before earning the habit.'),
               ('A feed isn’t the answer.', 'Schools were banning social apps; “not a social network” was a feature, not a bug.'),
               ('The timer stays on top.', 'It was already best-in-class. Keeping it above the fold earned us the rest of the screen to experiment with.')]
    G = 'assets/galleries/saturn/'
    hunch = slide('hunch', 2, f'''
      <div class="cs-col cs-col--text cs-w647">
        <div class="cs-head"><h2 class="t80" data-a>My <em>hunches</em>, &amp; the pitch</h2></div>
        <div class="cs-swap" data-a>{''.join(f'<div class="cs-card cs-card--hunch" data-sub="{i}"><h3>{E(h)}</h3><p>{E(p)}</p></div>' for i, (h, p) in enumerate(hunches))}</div>
        <p class="cs-body" data-a>I pitched <b>separating the timer from the schedule</b> and giving the app a true home screen — a bento of live modules answering “what’s happening right now?”</p>
      </div>
      {phone_slot([G + '053.webp', G + '030.webp', G + '011.webp'], 'Saturn’s Now tab')}''', steps=3)

    build = slide('build', 2, f'''
      <div class="cs-col cs-col--text cs-w647">
        <div class="cs-head"><h2 class="t80" data-a>Some kind of short headline</h2></div>
        <p class="cs-body" data-a>[Summary Lorem ipsum dolor sit amet consectetur. Adipiscing nisi pharetra pellentesque arcu erat elit donec leo donec. Nibh faucibus amet ultricies ut faucibus enim pharetra est. Curabitur ut tempus nisl vel. Ut nec vitae auctor blandit. Risus arcu quis scelerisque mattis libero. Mattis ullamcorper elementum suspendisse fusce. Aenean tellus tortor nunc aliquet arcu morbi at semper urna.]</p>
      </div>
      {phone_slot([None, None, None], 'Placeholder phone')}''', steps=3)

    gallery = slide('gallery', 2, f'''
      <div class="cs-top">
        <div class="cs-head"><h2 class="t80" data-a>Some kind of short headline</h2></div>
        <p class="cs-body cs-w570" data-a>[Curabitur ut tempus nisl vel. Ut nec vitae auctor blandit. Risus arcu quis scelerisque mattis libero. Mattis ullamcorper elementum suspendisse fusce. Aenean tellus tortor nunc aliquet arcu morbi at semper urna.]</p>
      </div>
      <div class="cs-phones4" data-a aria-label="Four placeholder phones">{''.join(f'<div class="cs-phone-slot cs-phone-slot--row" data-screens="" data-row="{i}"><div class="cs-flat"><span class="cs-gray">Screen needed</span></div></div>' for i in range(4))}</div>''')

    lessons_ = [('Earn the habit before you teach a behavior.', 'We didn’t lead with a Calendar interface. We protected the our most retentive feature, the <b>Timer</b>, built the Now tab on top of it, and only then asked students to plan.'),
                ('Don’t conflate social with a feed', 'It’s a utility. Productizing free time with <b>Calendar Compare</b> made the concept of friending make sense on Saturn.'),
                ('Monetize through your own primitives.', 'The best ad unit feels like a feature, not an ad. <b>Drops</b> worked because they were our countdown, not someone else’s banner.'),
                ('Ship the disagreement.', 'After-school sat empty for a semester while we debated. Today I push to turn an unresolved argument into a two-week experiment.')]
    lessons = slide('lessons', 3, f'''
      <h2 class="t64 reg" data-a>What three years at Saturn taught me</h2>
      <div class="cs-cards cs-cards--lessons">{''.join(f'<div class="cs-card" data-a><h3>{E(h)}</h3><p>{p}</p></div>' for h, p in lessons_)}</div>''')

    lorem = '[Summary Lorem ipsum dolor sit amet consectetur. Adipiscing nisi pharetra pellentesque arcu erat elit donec leo donec. Nibh faucibus amet ultricies ut faucibus enim pharetra est. Curabitur ut tempus nisl vel. Ut nec vitae auctor blandit. Risus arcu quis scelerisque mattis libero. Mattis ullamcorper elementum suspendisse fusce. Aenean tellus tortor nunc aliquet arcu morbi at semper urna.'
    stats = [('Record DAU', '325,000 daily active users reached in the back-to-school season of 2023.'), ('150% app opens', lorem), ('#1 in the App Store', lorem)]
    results = slide('results', 3, f'''
      <h2 class="t64" data-a>Three years, three product bets, one acquisition.</h2>
      <div class="cs-stats">{''.join(f'<div data-a><h3>{E(h)}</h3><p>{E(p)}</p></div>' for h, p in stats)}</div>''')

    return [hero, context, before, problem, research, hunch, build, gallery, lessons, results]


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
      {hero_copy()}
      <div class="cs-video"><video src="{base}{ASSET}teaser.mp4" poster="{base}{ASSET}teaser-poster.jpg" muted loop playsinline autoplay preload="metadata"></video></div>
    </div>
  </section>'''
    return head('Saturn: A new home tab — Natalie Rose Taylor', base,
                'Saturn: A new home tab. How a beloved single-purpose class timer for high schoolers got a true home screen.') .replace(
        '</head>', f'<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@700&family=Plus+Jakarta+Sans:wght@700&display=swap" rel="stylesheet"><link rel="stylesheet" href="{base}css/cs.css"><meta name="robots" content="noindex"></head>') + f'''
<body class="cs-page is-scroll" data-base="{base}">
{nav(base, light=True)}
<div class="cs-bar">
  <a class="logo" href="{base}" aria-label="Natalie Rose Taylor, home"><img src="{base}assets/svg/flower-light.svg" alt=""><span>Natalie<br>Rose Taylor</span></a>
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
