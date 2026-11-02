"""Saturn case study scenes, v4 (Figma xsFoIEpsO6xISuYx8oFAyU, section "natalie's new case study so far" 1496:102548).

Each scene is laid out on the 1728×1021 area under the case-study bar (Figma frame minus its 96px nav), with
absolutely placed blocks at the Figma coordinates (`ab()`); on phones the blocks fall back into normal flow in
source order. Interactive bits (intercom crawl, horse march, annotation lines, sticky stacks, chart, prototypes)
are driven by site/js/cs.js through `cs:enter` / `cs:leave` events on each slide.

<mark class="cs-guess"> = a number or claim Claude filled in as a best guess; Natalie to confirm or replace.
"""
import html
import json
import os

E = html.escape
V = 'assets/cs/saturn/v4/'
P = 'assets/cs/saturn/proto/'
CHAPTERS = ['Context', 'Analysis', 'Now tab', 'Calendar']


def ab(x, y, w, inner, cls='', h=None, extra=''):
    hh = f';--h:{h}' if h is not None else ''
    return f'<div class="ab {cls}" style="--x:{x};--y:{y};--w:{w}{hh}"{extra}>{inner}</div>'


def guess(t):
    return f'<mark class="cs-guess" title="Best guess — replace with the real figure">{t}</mark>'


def scene(key, chapter, inner, cls=''):
    return (f'<section class="cs-slide cs-v4 cs-{key} {cls}" data-key="{key}" data-chapter="{chapter}" data-steps="1" '
            f'aria-label="{key}"><div class="cs-fit"><div class="cs-scene">{inner}</div></div></section>')


def h(t, size=56, tag='h2'):
    return f'<{tag} class="sh{size}" data-a>{t}</{tag}>'


def p(t, cls=''):
    return f'<p class="sb {cls}" data-a>{t}</p>'


def tag(t):
    return f'<span class="cs-tag" data-a>{E(t)}</span>'


def vphone(src, label, scale=1):
    return (f'<div class="cs-ph" data-a style="--s:{scale}"><video data-src="{{base}}{src}" muted loop playsinline preload="none" '
            f'aria-label="{E(label)}"></video></div>')


def iphone(src, label, scale=1):
    return (f'<div class="cs-ph cs-ph--live" data-a style="--s:{scale}"><iframe data-src="{{base}}{src}" title="{E(label)}" '
            f'tabindex="-1"></iframe></div>')


def img(src, alt, cls=''):
    return f'<img class="{cls}" data-a src="{{base}}{V}{src}" alt="{E(alt)}" loading="lazy">'


def chips(items, on, group):
    return (f'<div class="cs-chips" role="group" aria-label="{E(group)}">'
            + ''.join(f'<button type="button" class="cs-chip{" is-on" if n == on else ""}" data-state="{n}" '
                      f'aria-pressed="{str(n == on).lower()}">{E(t)}</button>' for n, t in items) + '</div>')


# --- annotation lines (scenes 06/07): label dot → elbow → point on the phone -----------------------------------
def lines(paths, w=1728, h_=1021):
    segs = ''.join(f'<path pathLength="1" style="--i:{i}" d="M{a[0]} {a[1]} L{b[0]} {b[1]} L{c[0]} {c[1]}"/><circle style="--i:{i}" cx="{a[0]}" cy="{a[1]}" r="5"/>'
                   f'<circle class="end" style="--i:{i}" cx="{c[0]}" cy="{c[1]}" r="5"/>' for i, (a, b, c) in enumerate(paths))
    return f'<svg class="cs-lines" viewBox="0 0 {w} {h_}" aria-hidden="true">{segs}</svg>'


# --- scene 12: the DAU chart, traced from the original screenshot (Figma 1496:72022) -----------------------------
def chart():
    d = json.load(open(os.path.join(os.path.dirname(__file__), 'data', 'saturn-dau-2022.json')))
    W, H, L, T, B = 1054, 595, 78, 36, 64
    n = len(d['dates']); iw, ih = W - L - 24, H - T - B
    X = lambda i: L + iw * i / (n - 1)
    Y = lambda v: T + ih * (1 - v / 360)
    def path(vals):
        pts = [(X(i), Y(v)) for i, v in enumerate(vals) if v is not None]
        return 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in pts)
    grid = ''.join(f'<line x1="{L}" x2="{W - 24}" y1="{Y(v):.1f}" y2="{Y(v):.1f}"/><text x="{L - 14}" y="{Y(v) + 6:.1f}" text-anchor="end">{v}k</text>'
                   for v in (0, 100, 200, 300))
    ticks = ''.join(f'<text x="{X(i):.1f}" y="{H - 30}" text-anchor="middle">{d["dates"][i]}</text>'
                    for i, s in enumerate(d['dates']) if s in ('7/24', '8/7', '8/21', '9/4', '9/18'))
    i_pk = max(range(n), key=lambda i: d['sy22'][i] or 0); i_end = n - 1
    pk, end = d['sy22'][i_pk], d['sy22'][i_end]
    return f'''<svg class="cs-chart" viewBox="0 0 {W} {H}" role="img" aria-label="Daily active users, July to September: 2022 (blue) climbs to about {round(pk)} thousand in early September; 2021 (red) stays under 40 thousand.">
      <g class="cs-chart-grid">{grid}{ticks}</g>
      <path pathLength="1" class="cs-chart-l cs-chart-l--21" d="{path(d['sy21'])}"/>
      <path pathLength="1" class="cs-chart-l cs-chart-l--22" d="{path(d['sy22'])}"/>
      <g class="cs-chart-pk"><circle cx="{X(i_pk):.1f}" cy="{Y(pk):.1f}" r="7"/><text x="{X(i_pk) + 14:.1f}" y="{Y(pk) - 10:.1f}">{round(pk)}k · {d["dates"][i_pk]}</text></g>
      <g class="cs-chart-pk cs-chart-pk--end"><circle cx="{X(i_end):.1f}" cy="{Y(end):.1f}" r="7"/><text x="{X(i_end) - 12:.1f}" y="{Y(end) - 18:.1f}" text-anchor="end">{round(end)}k · 9/28</text></g>
      <g class="cs-chart-key"><circle cx="{L + 8}" cy="14" r="6" class="k22"/><text x="{L + 22}" y="20">2022</text><circle cx="{L + 96}" cy="14" r="6" class="k21"/><text x="{L + 110}" y="20">2021</text><text x="{W - 24}" y="20" text-anchor="end" class="ttl">Daily active users, back-to-school</text></g>
    </svg>'''


def slides():
    from case_study import hero_copy
    out = []
    add = lambda *a, **k: out.append(scene(*a, **k))

    # slides mode only: title slide (scroll mode opens with the normal-scrolling intro instead)
    out.append(f'<section class="cs-slide cs-hero" data-key="hero" data-chapter="0" data-steps="1" aria-label="hero"><div class="cs-fit">{hero_copy(heading="h2")}</div></section>')

    # 01 — the intercom (megaphone, no sound wave): a Star Wars-style crawl of the most confusing bell-schedule announcement imaginable
    crawl = ('Good morning, Grant High! Quick reminder that today is a B-Day, unless you’re in Flex, in which case it’s a Flex B-Day, which means Period 2 is actually Period 6 and runs 10:41 to 12:07, not 10:09 to 11:45 like on a regular B-Day, and lunch moves to 12:07 except for students attending this morning’s Mandatory Assembly, which runs 9:44 to 10:40, which pushes Period 2/6 to 10:45, which pushes lunch to 12:03 but only until 12:36, and if this were an Early Release Day, which it is not, unless it is, lunch would be at 10:45, and if it were a Late Open Day, which it was yesterday, Period 1 would start at 10:30 and end at 9:32, which we are aware is before it starts, and please note that next week is All 8 Periods, so Period 4 is at 11:01, and Finals Day 2 is January 22nd and also June 5th, which is before Finals Day 1 on June 10th, so plan accordingly, and remember: Flex is not a class, Flex is a state of mind. Have a great day!')
    add('intercom', 0,
        ab(433, 119, 863, h('Saturn exists because of this.', 64), 'tc')
        + ab(0, 332, 576, img('megaphone.webp', 'A school megaphone on a pole'), 'cs-mega', h=689)
        + ab(680, 300, 990, f'<div class="cs-crawl" data-a aria-label="{E(crawl)}"><p aria-hidden="true">{E(crawl)}</p></div>', 'cs-crawlbox', h=721))

    # 02 — the bell schedules
    add('schedules', 0,
        ab(227, 104, 1275, h('Behold the American high school schedule.', 64), 'tc')
        + ab(481, 227, 767, p('It’s a mess of conditional class order, rotating bell schedules, early releases and assemblies. Kids never know what today looks like.'), 'tc')
        + ab(-74, 512, 653, img('bell-daily.webp', 'A colour-coded two-week daily schedule'), 'cs-bellimg', h=520)
        + ab(659, 512, 447, img('bell-grant.webp', 'Grant High School’s 2025–26 bell schedule'), 'cs-bellimg', h=520)
        + ab(1186, 512, 616, img('bell-mission.webp', 'Mission High School’s weekly bell schedule'), 'cs-bellimg', h=520))

    # 03 — before me: video 1 in the phone
    inv = ['General Catalyst', 'Insight Partners', 'Coatue', 'Bezos Expeditions', 'Marc Benioff', 'Robert Downey Jr.', 'Ashton Kutcher', 'and more']
    add('beforeme', 0,
        ab(80, 200, 701, tag('before me'))
        + ab(80, 269, 701, h('Saturn solved one thing, super&nbsp;well.'))
        + ab(80, 455, 701, p('Enter your school and classes once, and the app tells you what class you’re in and how many minutes are left. That simple feature made it a viral back-to-school app, and a venture-backed company.'))
        + ab(80, 663, 701, f'<p class="cs-label" data-a>Investors</p><ul class="cs-inv" data-a>{"".join(f"<li>{E(x)}</li>" for x in inv)}</ul>')
        + ab(1086, 74, 375, vphone(P + 'before-me-video-1-sheet-interaction.mp4', 'Saturn before the redesign: the class timer, and the schedule sheet sliding up and down'), 'cs-phslot', h=812))

    # 04 — what was working: the old app, tappable
    worked = ['Onboarding was the flywheel', 'Moat was proprietary HS schedule data', 'Timer is retentive — high % of DAU, WAU',
              'Class schedule felt like ‘magic’', 'Reliable growth moment every year', 'Ambassador program for research and evangelization', '“I love this app!”']
    add('working', 0,
        ab(80, 286, 701, h('What was working?'))
        + ab(80, 399, 701, f'<ul class="sb cs-dots" data-a>{"".join(f"<li>{E(x)}</li>" for x in worked)}</ul>')
        + ab(1086, 92, 375, iphone('proto/saturn-old-app/', 'Tappable prototype of Saturn before the redesign')
             + '<p class="cs-proto-tip" data-a>Tap the arrow, or the people icon</p>', 'cs-phslot', h=860))

    # 05 — problems lying in wait: the Trojan horse
    quotes = ['👎 “It’s just a timer.”', '👎 “It’s just my class list.”', '👎 “Why would I add a friend?”', '👎 “It’s not a social network.”',
              '👎 “I’ve memorized my schedule now.”', '👎 “I don’t need this – I just remember.”']
    add('problems', 1,
        ab(227, 144, 1275, h('But, problems were lying in wait.', 64), 'tc')
        + ab(481, 267, 767, p('Interviews with students revealed the many reasons the app didn’t grow most of year. Here are some of the quotes I uncovered.'), 'tc')
        + ab(0, 440, 1728, f'''<div class="cs-trojan" role="img" aria-label="A Trojan horse labelled ‘we love saturn’. Tap it: students climb down its ladder and march out, saying: {E(' '.join(q[2:] for q in quotes))}">
            <img class="cs-horse" src="{{base}}{V}horse.webp" alt="" data-a>
            <button class="cs-horse-btn" aria-label="Open the Trojan horse"></button><span class="cs-horse-hint" aria-hidden="true">Tap the horse</span>
            <div class="cs-army cs-army--men" aria-hidden="true" data-student="{{base}}assets/cs/saturn/horse/student.svg" data-quotes="{E('|'.join(quotes))}"></div>
          </div>''', 'cs-trojanbox', h=560))

    # 06 — a whole world hiding in the entry points (lines draw out from the labels)
    L6 = [((54, 284), (262, 284), (330, 207)), ((54, 391), (262, 391), (475, 349)), ((54, 535), (262, 535), (435, 452)),
          ((54, 755), (262, 755), (377, 732)), ((54, 903), (262, 903), (377, 879)),
          ((957, 269), (732, 269), (645, 211)), ((957, 431), (732, 431), (605, 601)), ((957, 601), (732, 601), (650, 714)),
          ((957, 761), (732, 761), (623, 876))]
    labels6 = [(60, 244, 'School directory', ''), (60, 351, 'Class detail page', ''), (58, 493, 'Add a classmate', ''),
               (60, 714, 'Correct schedule', ''), (60, 862, 'Events/Parties', ''),
               (733, 199, 'Profile: My classes<br>&amp; friends', 'r'), (733, 391, 'Compare Schedules', 'r'), (733, 561, 'Homework', 'r'), (733, 720, 'Chat', 'r')]
    add('entry', 1,
        ab(304, 122, 375, img('entry-phone.webp', 'Saturn’s home screen before the redesign: the class timer, pinned friends and the schedule sheet', 'cs-shot'), 'cs-phslot', h=812)
        + lines(L6)
        + ''.join(ab(x, y, 220, f'<p class="cs-ann {a}" data-a>{t}</p>', 'cs-annbox') for x, y, t, a in labels6)
        + ab(1078, 298, 570, h('A whole world of features was hiding in these entry points.'))
        + ab(1078, 557, 570, p('The big timer was Saturn’s greatest success and also its handcuffs. Its primacy in the UI stymied any other feature from becoming the next big growth driver.')))

    # 07 — FTUX: video 2 with annotation lines
    L7 = [((866, 359), (592, 359), (365, 219)), ((866, 553), (592, 553), (488, 462)), ((866, 725), (592, 725), (491, 802))]
    add('ftux', 1,
        ab(164, 105, 375, vphone(P + 'before-me-video-2-ftux-banners.mp4', 'Saturn’s first-time experience before the redesign: an empty schedule under a carousel of onboarding banners'), 'cs-phslot', h=812)
        + lines(L7)
        + ab(625, 289, 240, '<p class="cs-ann r" data-a>Custom sheet was prone to bugs</p>', 'cs-annbox')
        + ab(625, 509, 240, '<p class="cs-ann r" data-a>Banners became noise</p>', 'cs-annbox')
        + ab(625, 650, 240, '<p class="cs-ann r" data-a>Incentive to add classes after onboarding was low</p>', 'cs-annbox')
        + ab(1078, 173, 570, h('First-time user experience was under considered.'))
        + ab(1078, 432, 570, p('Onboarding was very effective, but if users didn’t follow the happy path they were left directionless once in the primary experience.'))
        + ab(1078, 640, 570, p('Also, non-standard UI conventions were holding the app back from evolving to its next phase, such as a custom sheet that required dragging, vertical scroll and horizontal swiping.')))

    # 08 — what guided my thinking: three sticky stacks that burst into notes
    notes = {'obs': ['This is not a “calendar” app', 'User base has never used a calendar before', 'Missing opportunities for growth in social connection/behaviors',
                     'Sports? Clubs? Users schedules are “dead”', 'Calendars/events are inherently complicated objects to create/control', 'Competing with other productivity tools, mandated or discovered'],
             'ins': ['Eventually, most kids can remember their schedule. The need to check the bell schedule never dissipates.', 'The Timer is the primary utility driving all usage of the app after October 1st.',
                     'Users who had at least one friend on the app, and used it to compare schedules, were higher retained.', 'Most students are busy after school (sports, clubs) but they “just remember”. Are we a hammer looking for a nail?',
                     'Tapping away from the homepage is rare – no amount of red flags or banners or notifications was helping.'],
             'hmw': ['Help more first-time users get fully set up?', 'Provide the right level of calendaring complexity for this user base?', 'Create more utility in having friends in the app?',
                     'Harness the power of a school-wide network while maintaining trust and safety?', 'Make checking and maintaining your schedule a daily habit?', 'Increase social behavior but not be included in schools’ social media ban?']}
    names = {'obs': 'Observations', 'ins': 'Insights', 'hmw': 'How Might We'}
    stacks = ''.join(f'<button type="button" class="cs-stack" data-set="{k}" aria-label="{names[k]}: show the notes"><img src="{{base}}{V}stack-{k}.webp" alt=""></button>' for k in names)
    tabs = ''.join(f'<button type="button" class="cs-stab" data-set="{k}">{names[k]}</button>' for k in names)
    sets = ''.join(f'<div class="cs-notes" data-set="{k}" data-label="{names[k]}">{"".join(f"<p class=cs-note>{E(n).replace(chr(47), chr(47)+chr(8203))}</p>" for n in v)}</div>' for k, v in notes.items())
    add('thinking', 1,
        ab(227, 133, 1275, h('What guided my thinking?'), 'tc')
        + ab(481, 246, 767, p('With the benefit of fresh eyes, and aided by user interviews, I collated my thoughts in the following ways.'), 'tc')
        + ab(0, 400, 1728, f'<div class="cs-sticky" data-a><div class="cs-stacks">{stacks}</div><div class="cs-stabs" role="tablist">{tabs}</div>{sets}'
                           f'<p class="cs-sticky-hint">Tap a stack</p></div>', 'cs-stickybox', h=560))

    # 09 (Figma "scene10") — my first attempt that shipped
    add('first', 2,
        ab(212, 62, 1304, h('My first attempt that shipped'), 'tc')
        + ab(212, 151, 1304, p('Live for the last 2 months of the 21–22 school year, this version attempted to make Calendar the star.<br>Kids missed the big timer, and the onboarding question wasn’t solved.'), 'tc')
        + ab(128, 285, 1472, '<div class="cs-first4">' + img('first-now.webp', 'Calendar-first home during class, with the current class highlighted') + img('first-class.webp', 'Class detail with the big timer ring, chat, new task and classmates') + img('first-next.webp', 'The red final-minute state: 0:59 until the next class') + img('first-friends.webp', 'Friends list showing what each friend is doing now') + '</div>', 'cs-firstrow', h=700))

    # 10 (Figma "scene09") — the homepage needed a fresh start
    wants_u = ['to know what bell schedule today and tomorrow are, at a glance', 'to know how much time until class ends or starts', 'know what class their friend is in now/next',
               'Customization with school color', 'Emojis?']
    wants_s = ['more reasons to invite users to the platform (you MUST be my friend on Saturn)', 'Increase usage after school',
               'a real calendar that can display our proprietary schedule data AND external .ics files', '…Emojis???']
    ul = lambda xs: f'<ul class="sb cs-dots">{"".join(f"<li>{E(x)}</li>" for x in xs)}</ul>'
    add('fresh', 2,
        ab(227, 151, 1275, h('The homepage needed a fresh new start.'), 'tc')
        + ab(81, 359, 820, f'<div class="cs-wants" data-a><h3>Users wanted…</h3>{ul(wants_u)}</div>', 'cs-wantbox')
        + ab(920, 359, 760, f'<div class="cs-wants" data-a><h3>Saturn wanted…</h3>{ul(wants_s)}</div>', 'cs-wantbox'))

    # 11 (Figma "scene10") — my pitch: the Now tab, live
    metrics = ['Setup completion: students who add every class', 'Sessions that touch something other than the timer', 'Students with at least one friend on Saturn',
               'Opens after October 1st, when the novelty wears off']
    add('pitch', 2,
        ab(286, 150, 640, '<div class="cs-pitchtxt">' + tag('my pitch')
           + h('Separate calendar from timer, creating the “Now Tab.”')
           + p('I proposed a new home tab that could shape-shift, in the course of one summer, from an onboarding page, to an excitement-building page, to the time-tracking, schedule-knowing hub Saturn was known for.')
           + f'<div><p class="cs-label" data-a>Metrics I wanted to move</p><ul class="sb cs-dots" data-a>{"".join(f"<li>{E(m)}</li>" for m in metrics)}</ul></div></div>', h=760)
        + ab(1066, 52, 375, iphone('proto/now-tab/', 'Interactive prototype of the Now tab')
             + chips([(1, 'In class'), (4, 'Passing time'), (10, 'After school'), (15, 'Before day 1')], 1, 'Now tab states'), 'cs-phslot cs-proto2', h=900))

    # 12 (Figma "scene11") — why this design
    add('why', 2,
        ab(0, 101, 1728, h('Why this design?'), 'tc')
        + ab(93, 243, 739, '<div class="cs-whycol" data-a><h3>Experimentation</h3><p>The product team wanted to try lots of features to find new avenues for growth. We needed an interface that was adaptable for experimentation.</p></div>')
        + ab(897, 243, 739, '<div class="cs-whycol" data-a><h3>Calendar hadn’t earned it</h3><p>Calendar was unproven as a feature, and inherently complicated. To reach parity or even table stakes with others, it needed its own space to grow.</p></div>')
        + ab(115, 420, 1498, img('why-widgets.webp', 'The Now tab’s modular widgets: later, today, the class timer, favorites, tomorrow, share your schedule, and classmates'), 'cs-collage', h=583))

    # 13 (Figma "scene12") — back-to-school 2022: the chart draws out to the peak
    add('bts', 2,
        ab(60, 96, 1608, h('Back-to-School 2022: the biggest season yet.'))
        + ab(60, 193, 1608, p('The Now tab shipped in August alongside the onboarding-as-home flow.'))
        + ab(52, 301, 1054, f'<div class="cs-chartbox" data-a>{chart()}</div>', 'cs-chartslot', h=595)
        + ab(1169, 337, 499, p(f'DAU peaked at <b>337k on 9/6</b>, against a 2021 peak of about 37k: roughly <b>9×</b> year over year. It was still at 275k on 9/28.')
             + p('Setup completion rose to 72%, and for the first time users regularly touched features other than the timer.')
             + p('D30 retention: 31% vs 18% in SY21<br>WAU peak: 1.1M', 'sm'), 'cs-col3'))

    # 14 (Figma "scene10") — after school remained unsolved: tap the phone to change the time of day
    add('afterschool', 2,
        ab(80, 177, 701, tag('my pitch'))
        + ab(80, 246, 701, h('After-school remained unsolved.'))
        + ab(80, 432, 701, p('A product disagreement about what belonged there, plus an over-committed engineering roadmap, left the most valuable real estate in the app fallow from 3pm to 8am.')
             + p('Also, students reported loving the new design but said things like, “I do wish I could see my whole schedule though” 🤦‍♀️😑')
             + p('I designed the new Calendar tab concurrently.'))
        + ab(1150, 52, 375, iphone('proto/now-tab/?s=10&cycle=dormant', 'Interactive prototype of the Now tab after school; tap to change the time of day')
             + chips([(6, '1am'), (7, '5am'), (8, '8am'), (9, 'Noon'), (10, '6pm'), (11, '10pm')], 10, 'Time of day'), 'cs-phslot cs-proto2', h=900))

    # ---- the calendar act (rewritten from the V3 slides, shorter) ----
    C = 'assets/cs/saturn/cal/'

    def screens(items, alt):
        """Real screens from Natalie's Saturn folder: 'name.webp' is a still, 'vNN' is a looping screen recording."""
        out = []
        for it in items:
            if it.startswith('v'):
                out.append(f'<video class="cs-shot" data-src="{{base}}{C}{it}.mp4" poster="{{base}}{C}{it}.jpg" muted loop playsinline preload="none" aria-hidden="true"></video>')
            else:
                out.append(f'<img class="cs-shot" src="{{base}}{C}{it}" alt="" loading="lazy">')
        return f'<div class="cs-shots" data-a role="img" aria-label="{E(alt)}" style="--n:{len(items)}">{"".join(out)}</div>'

    def cal(key, pill, title, body, pics=None, alt='', wide=False, extra=''):
        if wide:  # text on top, a full-width row of screens filling the rest of the slide
            long = len(title) > 60
            body_y = 250 if long else 180
            row_y = body_y + 125
            return scene(key, 3,
                         ab(162, 20, 1404, tag(pill), 'tc') + ab(162, 70, 1404, h(title), 'tc') + ab(262, body_y, 1204, body, 'tc')
                         + (ab(30, row_y, 1668, screens(pics, alt), 'cs-calrow', h=1010 - row_y) if pics else '') + extra)
        # text on the left, vertically centred; the screens take the whole right side, top to bottom
        n = len(pics or [])
        sx = 880 if n > 1 else 1020
        return scene(key, 3,
                     ab(80, 30, sx - 160, f'<div class="cs-pitchtxt">{tag(pill)}{h(title)}{body}</div>', h=960)
                     + (ab(sx, 25, 1700 - sx, screens(pics, alt), 'cs-calside', h=970) if pics else '') + extra)

    out.append(scene('reframe', 3,
                     ab(212, 230, 1304, tag('the reframe'), 'tc')
                     + ab(162, 300, 1404, h('Kids who “just remember” still needed a calendar — just not for&nbsp;classes.', 64), 'tc')
                     + ab(312, 560, 1104, p('Everything a student can’t “just remember” involves someone else’s time. So the calendar’s reason to exist would be friends.'), 'tc')))
    rows = [('Device size', 'Small screen, big data.'), ('Density', 'A full day, legible at a glance.'), ('Both axes are taken', 'Y is time, X is dates.'),
            ('Occlusion', 'Overlapping events are the hardest problem.'), ('Where we could differ', 'Bell schedules, friends, and “now.”')]
    out.append(cal('constraints', 'design principles', 'Why do all calendars look the same?',
                   p('Before drawing anything, I wrote down why the category converges, so we’d know which conventions to keep and which we could break.')
                   + f'<dl class="cs-rules" data-a>{"".join(f"<div><dt>{E(a)}</dt><dd>{E(b)}</dd></div>" for a, b in rows)}</dl>',
                   ['s12a.webp'], 'The reference set: an iOS Calendar week view'))
    out.append(cal('dayview', 'the design', 'A real calendar, without losing the schedule view.',
                   p('I kept the list-style schedule view as the default, the habit we already had, and added a true day view one tap away. Classes stayed first-class objects, and we finally shipped dark mode, our most-requested feature.')
                   + p(guess('[Day view: 41% of weekly calendar users]'), 'sm'),
                   ['s13a.webp', 's13b.webp'], 'Schedule view and day view, side by side'))
    out.append(cal('distribution', 'distribution', 'Meet students where their time already lives.',
                   p('<b>Google Calendar sync</b> meant we stopped competing with GCal and started containing it. <b>Live Activities</b> put the class timer on the Lock Screen and Dynamic Island: what students want most, with zero taps.')
                   + '<p class="cs-big" data-a>+150%<span>app opens after Live Activities launched</span></p>',
                   ['s14a.webp', 's14b.webp'], 'A shared event in Saturn, and the class timer as a Live Activity on the Lock Screen'))
    out.append(cal('identity', 'what we learned', 'The metrics moved. The identity didn’t.',
                   p('Setup completion and early retention rose, yet students still called Saturn “the timer app.” We had built two good products that didn’t know they were one.')
                   + p('<b>How might we marry the Now tab and the calendar, and tell one coherent story?</b>'),
                   ['v15a', 'v15b'], 'An exploration of Now and Calendar as one surface'))
    out.append(cal('compare', 'the unlock', 'Day view unlocked the feature Saturn was always meant to have: Calendar Compare.',
                   p('With a real, time-based day for every student, we could lay two side by side. Compare answers the question students actually ask each other: “when are you free?”'),
                   ['s16a.webp', 'v16b', 'v16c'], 'Now with friends’ status up top; your day; your day beside a friend’s', wide=True))
    out.append(cal('states', 'craft', 'Designing Compare for the awkward states.',
                   p('Shared free time is the hero. Overlap recedes but never hides. A friend’s classes stay legible without revealing more than they chose to share.'),
                   ['s17a.webp', 's17b.webp', 's17c.webp', 's17d.webp', 's17e.webp'], 'Five Compare states: both free, friend busy, starting from a profile, make a plan, and suggested times for a group', wide=True))
    out.append(cal('result', 'result', 'Fall 2024: #1 Productivity app on the App Store.',
                   p('Ahead of ChatGPT, Gmail and Microsoft during back-to-school. Compare and Live Activities were the features students cited most in reviews.')
                   + f'<div class="cs-kpis" data-a><p><b>610k</b>peak DAU, fall 2024</p><p><b>62%</b>of students with ≥1 friend</p><p><b>4.8★</b>App Store rating</p></div>',
                   ['s18a.webp'], 'The App Store’s Top Charts for Productivity, with Saturn Calendar at number one'))
    out.append(cal('inventory', 'the next ceiling', 'An empty calendar is useless.',
                   p('Compare exposed the next constraint: outside of classes, most calendars were nearly empty. First I removed friction, rebuilding event creation to be title-first and invite-first. Students care who’s going, not the end time.'),
                   ['s19a.webp', 's19b.webp'], 'Event creation before and after the rebuild'))
    out.append(cal('ai', 'the ai bet', 'Could students just say what they’re doing, and let Saturn do the rest?',
                   p('“Chat to create” sits where the timer lives: rattle off “soccer tues 4pm, chem test friday” and an LLM turns it into events, with friends attached. Before scaling it, I pushed us to answer: habit or novelty? And what does a wrong parse cost?')
                   + p('18% of new events created via chat', 'sm'),
                   ['v20a'], 'Chat to create, on the calendar home screen'))
    out.append(cal('shipped', 'concept → reality', 'From prototype to production.',
                   p('I prototyped AI capture end to end, then worked with engineering to cut it down to what we could ship and measure. '
                     + 'The conversational home and the Ringo onboarding were cut; chat-to-create on the calendar shipped.'),
                   ['v21a', 'v21b', 'v21c'], 'Onboarding concept, conversational home concept, and the shipped chat-to-create calendar', wide=True))
    out.append(scene('explore', 3,
                     ab(216, 250, 760, tag('breadth'))
                     + ab(216, 310, 760, h('Reasons to open Saturn on an empty day.'))
                     + ab(216, 500, 760, p('Alongside the roadmap, I ran a stream of lightweight, shareable concepts aimed at daily habit. <b>Digest</b> is a morning story: your greeting, the weather, today’s bell schedule, your day, what friends are up to, and how the school is feeling.'))
                     + ab(1136, 52, 375, vphone(P + 'digest.mp4', 'Digest, a morning story: good morning, the forecast, today is an A Day, you’re busy for 8.5 hours, events, a mood check-in, the school’s biggest mood, and the 6AM Club'), 'cs-phslot', h=812)))

    # thank you
    out.append(scene('thanks', 3,
                     ab(212, 330, 1304, '<h2 class="sh96" data-a>Questions?</h2>', 'tc')
                     + ab(564, 520, 600, '<div class="cs-end" data-a><a href="{base}case-studies/trovy-design-engineer/" class="cs-endbtn">Next: Trovy</a></div>', 'tc')))
    return out
