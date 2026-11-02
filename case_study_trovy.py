"""Trovy case study (/case-studies/trovy-design-engineer/): how Natalie went from Figma handoffs to shipping
production code at Trovy — the homepage redesign, then Renovate with Trovy.

Same deck as the Saturn page (case_study.py / cs.js / cs.css): slides on a 1728×1117 art board, Scroll or
Slides mode, stacked page on phones. Trovy-specific layouts use the `tv-` classes at the end of cs.css.

Sources: design projects/trovy/Trovy-writeup.txt, "About Trovy and Renovate" (Nov 2 2026), the Renovate
visual-QA screenshots and the coded homepage (site/proto/trovy-home/). [Bracketed] text is for Natalie to confirm.
"""
import html

E = html.escape
ASSET = 'assets/cs/trovy/'
CHAPTERS = ['Context', 'Homepage', 'Renovate', 'Takeaways']


def slide(key, chapter, inner, steps=1, cls=''):
    return (f'<section class="cs-slide cs-{key} {cls}" data-key="{key}" data-chapter="{chapter}" data-steps="{steps}" '
            f'aria-label="{key}"><div class="cs-fit">{inner}</div></section>')


def cards(items, cls=''):
    return (f'<div class="cs-cards {cls}">'
            + ''.join(f'<div class="cs-card" data-a><h3>{E(h)}</h3><p>{p}</p></div>' for h, p in items) + '</div>')


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
        <dl class="cs-meta">{''.join(f'<div{a}><dt>{x}</dt><dd>{y}</dd></div>' for x, y in META)}</dl>
      </div>'''


def slides():
    A = '{base}' + ASSET
    hero = slide('hero', 0, hero_copy(heading='h2'))

    context = slide('context', 0, f'''
      <div class="cs-col cs-col--text">
        <div class="cs-head"><h2 class="t64" data-a>Trovy puts home equity on a Mastercard.</h2></div>
        <div class="cs-body" data-a>
          <p>A HELOC is one of the cheapest ways to borrow, but it usually means weeks of paperwork and a draw request every time you need money. Trovy is a fully online HELOC, $25k to $250k, with the line on a card: swipe it, move cash to your bank, or lock a balance into a fixed-rate FixedPay plan. Approval in as little as 4 minutes, funding in as few as 4 business days.</p>
          <p>I joined as the founding designer and shipped the brand, the card, the application, the account dashboard, the marketing site and the ads.</p>
        </div>
      </div>
      <button type="button" class="tv-card3d" data-a data-glb="{ASSET}card.glb" aria-label="The gold Trovy Mastercard in 3D. Tap to spin it.">
        <img class="tv-card3d-flat" src="{A}card.webp" alt="" width="620" height="620">
        <i class="tv-card3d-shadow" aria-hidden="true"></i>
        <canvas aria-hidden="true"></canvas>
        <span class="tv-card3d-hint" aria-hidden="true">Tap to spin</span>
      </button>''')

    apply = slide('apply', 0, f'''
      <div class="cs-col cs-col--text tv-w780">
        <div class="cs-head"><h2 class="t64" data-a>Preapproved in 2 minutes</h2></div>
        <p class="cs-body" data-a>Trovy went from 0–100MM PMV in one year of operation, from relentlessly alleviating friction in the application flow.</p>
      </div>
      <div class="cs-proto" data-a>
        <div class="cs-proto-phone"><iframe data-src="{{base}}proto/trovy-apply/" title="Interactive prototype of the Trovy application" tabindex="-1"></iframe></div>
        <p class="cs-proto-hint">Live prototype · tap through it</p>
      </div>''')

    shift = slide('shift', 1, f'''
      <div class="cs-head"><h2 class="t56" data-a>One designer, one engineering team, one queue.</h2></div>
      <p class="cs-body cs-body--wide" data-a>Trovy’s engineers work on the lending product: application, underwriting, servicing, compliance. Everything else, the marketing site and new homeowner features, waited behind it. In [month] 2025 I started building those myself with AI coding agents and handing engineering working code instead of mockups.</p>
      {cards([('The deliverable changed.', 'Figma files became running code. The prototype is the spec; engineering reviews a build, not a redline.'),
              ('The loop got shorter.', 'Design, build and test happen in the browser in the same session. Motion and states are designed where they run.'),
              ('The split is deliberate.', 'I own the marketing site and the Homeowner Toolkit end to end. The core lending product stays with engineering.')], 'tv-cards3')}''')

    home_before = slide('home-before', 1, f'''
      <div class="cs-col cs-col--text tv-w520">
        <div class="cs-head"><span class="cs-pill">Project 1</span><h2 class="t64" data-a>The homepage</h2></div>
        <div class="cs-body" data-a>
          <p>The live homepage explains a HELOC: rates, speed, trust badges, a comparison table, an FAQ. It is a page about a loan.</p>
          <p>The card is what makes Trovy different, and on this page it is one image among many.</p>
        </div>
      </div>
      <figure class="tv-shot tv-shot--wide" data-a>
        <img src="{A}home-old.webp" alt="The live Trovy homepage: ‘The smart, flexible HELOC’ with a photo of a house at golden hour" width="1000" height="625">
        <figcaption>Before · live homepage, 2025</figcaption>
      </figure>''')

    frames = [('new-hero', 'Hero: the house lifts off'), ('new-wallet', 'The card comes out of the wallet'), ('new-tap', 'Tap it: no draw fees'),
              ('new-cash', 'Cash out at a fixed rate'), ('new-debt', 'Pay off debt'), ('new-plane', '“The best travel card is a HELOC”')]
    home_after = slide('home-after', 1, f'''
      <div class="cs-top">
        <div class="cs-head"><h2 class="t56" data-a>The redesign is a scroll-driven story about the card.</h2></div>
        <p class="cs-body cs-w570" data-a>One pinned stage, scrubbed by scroll: the house lifts off, the card comes out of the wallet, taps, pays for cash out and debt, then earns the perks. The page shows the product doing things instead of listing them. Process, reviews and FAQ follow as a normal page.</p>
      </div>
      <div class="tv-frames">{''.join(f'<figure data-a><img src="{A}{f}.webp" alt="" loading="lazy" width="520" height="325"><figcaption>{E(c)}</figcaption></figure>' for f, c in frames)}</div>''')

    home_live = slide('home-live', 1, f'''
      <div class="cs-col cs-col--text tv-w434">
        <div class="cs-head"><span class="cs-pill">Project 1</span><h2 class="t56" data-a>Ideate in Figma, polish in code.</h2></div>
        <div class="cs-body" data-a>
          <p>A designer’s superpower is the ability to describe visual ideas succinctly that humans innately understand. I always start in Figma, but 80% of my time is spent tweaking and reacting in Claude Code.</p>
        </div>
        <a class="tv-link" data-a href="{{base}}proto/trovy-home/" target="_blank" rel="noopener">Open the build full size ↗</a>
      </div>
      <div class="tv-browser" data-a>
        <div class="tv-browser-bar"><i></i><i></i><i></i><span>trovy.com</span></div>
        <iframe data-src="{{base}}proto/trovy-home/" title="The coded Trovy homepage, live" loading="lazy" tabindex="-1"></iframe>
        <p class="tv-browser-hint">Live build · scroll inside the frame</p>
      </div>''')

    brief = slide('brief', 2, f'''
      <div class="cs-col cs-col--text tv-w620">
        <div class="cs-head"><span class="cs-pill">Project 2</span><h2 class="t64" data-a>Renovate with Trovy</h2></div>
        <div class="cs-body" data-a>
          <p>Renovation is the biggest reason homeowners tap their equity, and the point where they are least sure what they want, what it costs and whom to hire.</p>
          <p>Renovate, part of Trovy’s Homeowner Toolkit, takes a homeowner from a photo of a room to an AI-generated plan, a rendered design, a cost estimate and a shopping list, with the Trovy line as the way to pay for it.</p>
          <p>It is live for cardholders behind a release flag. The redesign on these slides is in review.</p>
        </div>
      </div>
      <figure class="tv-shot tv-shot--wide" data-a>
        <img src="{A}d-projects-all.webp" alt="Renovate with Trovy: ‘Get a rendering, cost estimate, and shopping list for your renovation project’, with two projects listed" width="1000" height="694">
        <figcaption>Project list · desktop</figcaption>
      </figure>''')

    steps = [('m-upload-photo', 'Start with your room', 'Add a photo and say what should change.'),
             ('m-chat-intent', 'Plan it with Renault', 'A few quick questions: scope, style, budget.'),
             ('m-chat-plan-summary', 'Approve the plan', 'Renault writes a project plan. Edit it or generate now.'),
             ('m-design-ready', 'See your new room', 'Drawn on your own photo, with a before/after slider.'),
             ('m-ready-shop', 'Price it and shop it', 'Materials and labor, each product pinned and linked.')]
    flow = slide('flow', 2, f'''
      <div class="cs-head"><h2 class="t56" data-a>See the renovation of your dreams in minutes.</h2></div>
      <figure class="tv-shot tv-shot--hero" data-a>
        <img src="{A}d-design-ready.webp" alt="Renovate on desktop: a before/after slider over a bathroom redesign, a column of saved versions, Renault’s chat and a $24,900 estimate next to Take Out Cash" width="1600" height="1111">
      </figure>''')

    desktop = slide('desktop', 2, f'''
      <div class="cs-col cs-col--text tv-w434">
        <div class="cs-head"><h2 class="t56" data-a>The same build at 1440 and 390.</h2></div>
        <div class="cs-body" data-a>
          <p>Desktop gets three columns: project sections on the left, the design and its version stack in the middle, Renault on the right.</p>
          <p>The estimate sits next to <b>Take Out Cash</b>. That is where Trovy earns its place in the flow.</p>
          <p>On mobile the same components stack, and Renault becomes a sheet.</p>
        </div>
      </div>
      <figure class="tv-shot tv-shot--desk" data-a>
        <img src="{A}d-design-ready.webp" alt="Renovate on desktop: before/after slider over a bathroom, a column of versions, Renault’s chat and a $24,900 estimate next to Take Out Cash" width="1120" height="778">
      </figure>''')

    details = [('det-comment', 'Tap to change', 'Tap anywhere on the photo to pin a change. The pin goes to Renault as a comment, and the next version answers it.'),
               ('det-shop', 'Shop from the render', 'Every product in the design is numbered on the photo and listed with materials, installation cost and a store link.'),
               ('det-versions', 'Versions, kept', 'Every generation is saved. Older versions are marked outdated and can be restored or removed.')]
    detail = slide('detail', 2, f'''
      <div class="cs-head"><h2 class="t56" data-a>Details</h2></div>
      <div class="tv-details">{''.join(f'<div class="cs-card" data-a><img src="{A}{f}.webp" alt="" loading="lazy" width="440" height="275"><h3>{E(h)}</h3><p>{E(p)}</p></div>' for f, h, p in details)}</div>''')

    process = slide('process', 2, f'''
      <div class="cs-head"><h2 class="t56" data-a>How it was built</h2></div>
      {cards([('Code as the design tool', 'Layouts, states and motion were designed in the running app with AI coding agents, not in Figma first.'),
              ('Desktop and mobile together', 'Every change was checked at 1440 and 390 in the same pass, so neither size is a port of the other.'),
              ('A visual-QA rig', 'A test setup with a sample bathroom project renders every screen at both sizes after each change. The screenshots on this page come from it.'),
              ('Behind a release flag', 'Shipped to cardholders behind a flag, so Trovy controls rollout, and the redesign goes through review before it reaches everyone.')], 'cs-cards--lessons')}''')

    steps_ = [('Design', 'Figma', 'Layouts, type and the key screens start here.'),
              ('Build', 'Claude Code', 'I move into code early, working in VS Code, the Claude Code app and Claude in the terminal. Most design decisions after that get made in the running build.'),
              ('Assets', 'ChatGPT and Gemini', 'Where the photo and video assets come from.')]
    myprocess = slide('myprocess', 2, f'''
      <div class="cs-col cs-col--text tv-w520">
        <div class="cs-head"><h2 class="t56" data-a>My process</h2></div>
        <ol class="tv-process">{''.join(f'<li data-a><p class="tv-process-k">{E(k)}</p><h3>{E(t)}</h3><p>{E(p)}</p></li>' for k, t, p in steps_)}</ol>
      </div>
      <figure class="tv-shot tv-shot--process" data-a>
        <img src="{A}process-vscode.webp" alt="VS Code with Claude Code open on the Trovy frontend: the Homeowner Toolkit chat beside a Renovate visual-QA screenshot of Renault asking for a photo of the kitchen" width="1600" height="1003">
        <figcaption>Claude Code in VS Code, on the Renovate visual-QA captures</figcaption>
      </figure>''')

    takeaways_ = [('The prototype is the spec.', 'Engineering reviews a build. Fewer handoff questions, and the edge cases are already in the code.'),
                  ('Motion gets designed where it runs.', 'Scroll timelines and transitions were tuned in the browser, not described on a slide.'),
                  ('The queue is gone.', 'Marketing and Toolkit work no longer waits for engineering time. The lending product still does, and that is the right split.')]
    takeaways = slide('takeaways', 3, f'''
      <h2 class="t64" data-a>What changed in how I work</h2>
      <div class="cs-stats">{''.join(f'<div data-a><h3>{E(h)}</h3><p>{E(p)}</p></div>' for h, p in takeaways_)}</div>''')

    return [hero, context, apply, home_live, shift, brief, flow, process, myprocess, takeaways]


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
  <a class="logo cs-satlogo tv-barlogo" href="#top" aria-label="Trovy case study, back to the top"><img src="{base}{ASSET}trovy-icon.svg" alt="" width="74" height="67"><img src="{base}{ASSET}trovy-wordmark.svg" alt="Trovy" width="179" height="61"></a>
  <nav class="cs-outline" aria-label="Chapters">{outline}</nav>
  {toggle}
</div>
<main class="cs" id="top">
  {intro}
  <div class="cs-track">
    <div class="cs-deck">
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
