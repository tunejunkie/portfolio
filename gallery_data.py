# Copy and settings for the L2 screenshot gallery pages.
# grad: the project's background gradient (top -> bottom), same as its thumbnail.
GAL = {
  'candle': dict(name='I Lit A Candle', grad=('#bd7d50', '#e15444'),
    sum='A tiny iPhone app I designed and vibe-coded: light a candle, and a Live Activity timer on your lock screen keeps reminding you it’s burning.',
    meta=[('Role', 'Designer & developer'), ('Designs circa', '2026'), ('Employment type', 'Personal project'), ('Type', 'Native iOS'), ('Launched', 'July 2026')]),
  'trovy': dict(name='Trovy', grad=('#f9d76b', '#ffb031'),
    sum='A HELOC that works like a credit card. As founding designer I designed the brand, the gold card, the marketing site, the application and the account dashboard.',
    meta=[('Role', 'Founding Designer'), ('Designs circa', '2025–Current'), ('Employment type', 'Full-time'), ('Type', 'Web & mobile web'), ('Growth', 'Seed → $100MM PMV')]),
  'wherei': dict(name='WhereI AI', grad=('#f5fca6', '#61b3ff'),
    sum='Remi, an AI biographer that interviews you about your life and pins each memory to the places it happened.',
    meta=[('Role', 'Founder'), ('Designs circa', '2026'), ('Employment type', 'Entrepreneurial'), ('Type', 'Native mobile'), ('Launched?', 'Not yet')]),
  'monstro': dict(name='Monstro', grad=('#d5faa1', '#ff9f9a'),
    sum='An AI money copilot for a seed-stage fintech, designed as a white-label product for banks. Bank names and logos are placeholders and don’t imply a partnership.',
    meta=[('Role', 'Sole designer'), ('Designs circa', '2024'), ('Employment type', 'Contract'), ('Type', 'Native mobile'), ('Stage', 'MVP')]),
  'saturn': dict(name='Saturn', grad=('#ffdb8b', '#789aff'),
    sum='The social calendar for high schoolers: classes, plans and friends on one screen. Three years of screens, from the Series A to the Snap acquisition, including concepts I pitched that never shipped.',
    meta=[('Role', 'Lead Product Designer'), ('Designs circa', '2022–2025'), ('Employment type', 'Full-time'), ('Type', 'Native mobile'), ('Installs', '68x')]),
  'kyn': dict(name='Kyn', grad=('#e6cbfb', '#7771ff'),
    sum='A personal CRM for staying close to the people you care about, designed for Pareto Holdings and taken from kickoff to the App Store in about six weeks.',
    meta=[('Role', 'Sole designer'), ('Designs circa', '2024'), ('Employment type', 'Contract'), ('Type', 'Native iOS'), ('Kickoff to App Store', '~6 weeks')]),
  'transforce': dict(name='TransForce', grad=('#b2cfff', '#b1e8c5'),
    sum='A job marketplace and driver app for CDL truck drivers: find a job, get verified, accept assignments and run your drives. Everything I designed shipped.',
    meta=[('Role', 'Sole designer'), ('Designs circa', '2024'), ('Employment type', 'Contract'), ('Type', 'Native mobile & web'), ('Shipped', 'All of it')]),
  'honored': dict(name='HonorEd', grad=('#fadda5', '#5c8fb3'),
    sum='Live, interactive online classes for college students. I was the first design hire and designed the MVP ahead of their $38M Series A.',
    meta=[('Role', 'Sole designer'), ('Designs circa', '2021'), ('Employment type', 'Contract'), ('Type', 'Native mobile & web'), ('Raised', '$38M Series A')]),
  'abbott': dict(name='Abbott', grad=('#6fd6fb', '#d6edfa'),
    sum='NeuroSphere MyPath: a patient app for tracking pain relief during a spinal cord stimulation trial, plus the physician portal. Designed at BCG Digital Ventures for Abbott.',
    meta=[('Role', 'Sole designer'), ('Designs circa', '2020'), ('Employment type', 'Consultancy (BCGDV)'), ('Type', 'Native mobile'), ('Status', 'Launched')]),
  'upclose': dict(name='UpClose', grad=('#bbb6fc', '#e5e4f0'),
    sum='My own startup: making plans in three questions instead of twenty texts, with a chatbot handling the back-and-forth for you.',
    meta=[('Role', 'Founder'), ('Designs circa', '2019–2021'), ('Employment type', 'Entrepreneurial'), ('Type', 'Native iOS'), ('Users', '~1,000')]),
  'adecco': dict(name='Adecco', grad=('#443bc0', '#d5605f'),
    sum='Adecco Direct, the staffing giant’s first self-serve tool: warehouse floor managers create job orders, schedules and shifts and see who’s checked in, without calling a recruiter.',
    meta=[('Role', 'Product designer'), ('Designs circa', '2020–2021'), ('Employment type', 'Contract'), ('Type', 'Web app'), ('First', 'Self-serve product')]),
  'monster': dict(name='Monster', grad=('#00788c', '#5f64af'),
    sum='Four years as Director of UX Engineering at Monster: the native apps, job search and apply, profiles and onboarding on the web.',
    meta=[('Role', 'Director of UX Engineering'), ('Designs circa', '2018–2022'), ('Employment type', 'Full-time'), ('Type', 'Native mobile & web')]),
  'gigmo': dict(name='Gigmo', grad=('#1f3b3a', '#4f8f86'),
    sum='An early concept for gig workers: find shifts, log hours, get rated and get paid, with savings and pay-advance tools built in. It didn’t launch.',
    meta=[('Role', 'Product designer'), ('Designs circa', '2020'), ('Employment type', 'Contract'), ('Type', 'Native mobile'), ('Launched?', 'No')]),
}

# Titles + captions for the galleries that had no caption sheet.
CAPTIONS = {
  'adecco': [
    ('Dashboard', 'Today at a glance: shifts filled, active job orders and schedules, and who has checked in.'),
    ('What do you want to create?', 'One entry point for everything a floor manager makes: job orders, schedules, roles, messages and events.'),
    ('Start From a Schedule', 'Reuse an existing schedule as a template instead of building a job order from scratch.'),
    ('Job Order - Describe It', 'Step one of three: title, role, description and dress code, with smart suggestions.'),
    ('Job Order - Shift Details', 'Pay, headcount, days and times for a shift, all on one long form.'),
    ('Job Order - Define a Schedule', 'Pick shifts against a calendar, with openings tracked per shift.'),
    ('Calendar', 'Month view with each day’s fill rate and the shifts that still need people.'),
    ('Job Orders', 'Every open order as a card: role, location, dates and how many openings are left.'),
    ('Shift Timeline', 'A day’s shifts on a timeline, with who’s confirmed and where there are gaps.'),
    ('Associates', 'The roster, with ratings and availability, ready to invite to a shift.'),
    ('Manage', 'Settings for the things that rarely change: roles, departments, locations, dress codes and users.'),
    ('Adecco Mobile App', 'The candidate side: search jobs near you and apply in a tap.'),
  ],
  'monster': [
    ('Monster Native App', 'The redesigned Monster app: job search, fit scores and one-tap apply.'),
    ('Referrals', 'Refer friends to jobs and track their progress from the app.'),
    ('Fit Score', 'How well you match a job, explained, so you know whether it’s worth applying.'),
    ('Search Results to Quick Apply', 'Swipe through matches and quick-apply without leaving the list.'),
    ('Ready to Apply?', 'Apply with your Monster profile in one step.'),
    ('Recruiter Chat and Fit Score', 'Answer a recruiter’s screening questions in chat, next to your fit score.'),
    ('Profile and Home', 'Your profile, saved jobs, applications and recommendations in one place.'),
    ('Sign Up or Log In', 'A single entry point with social sign-in.'),
    ('Apply on the Web', 'Apply with your profile or an uploaded resume, from any source.'),
    ('Career Advice Search', 'Search results that mix jobs and career-advice articles.'),
    ('Edit Profile', 'Build your profile section by section, with visibility controls for employers.'),
    ('Profile Overview', 'How employers see you, with profile strength and what to add next.'),
    ('My Activity', 'Every job you’ve applied to, its status, and what to do next.'),
    ('Onboarding - Welcome', '“It takes courage to discover something new”: the start of web onboarding.'),
    ('Onboarding - Where Do You Want to Work?', 'Pick locations on a map, or anywhere.'),
    ('Onboarding - Interests', 'Choose the fields you’re interested in.'),
    ('Onboarding - Education and Career Level', 'Two quick questions that shape your matches.'),
    ('Onboarding - What Resonates?', 'Pick the story that sounds like you, from work-life balance to pay.'),
    ('Onboarding - Matches Found', 'Show the payoff (226+ jobs) before asking for an email.'),
  ],
  'candle': [
    ('Lock Screen Timer Prompt', 'Explains the Live Activity and links straight to the settings to turn it on.'),
    ('Menu', 'Share with a friend, rate the app, and notification preferences.'),
    ('Candle Burning - 1 to 2 Hours', 'The timer keeps counting and the message shifts as time passes.'),
    ('Candle Burning - 3+ Hours', 'After three hours the timer turns red: “I’m scared.”'),
    ('Candle Burning - 3+ Hours (Alt)', 'Alternate copy for a long burn.'),
    ('Candle Burning - 2 to 3 Hours', '“Try ‘Siri, I blew out the candle’”: a Siri shortcut to stop the timer hands-free.'),
    ('Notifications Off Warning', 'A banner explains the lock-screen timer needs notifications, with a one-tap fix.'),
    ('Candle Burning - Under an Hour', 'Just lit: a calm message and the timer starting.'),
    ('No Candle Lit - Notifications Off', 'Inactive state with the notifications reminder.'),
    ('No Candle Lit', '“Try ‘Siri, I lit a candle’” to start the timer by voice.'),
    ('Candle Blown Out', '“Good job.” The timer stops and the flame goes dark.'),
    ('All Set', 'Onboarding confirmation before loading the home screen.'),
    ('Turn On Notifications', 'Onboarding shows the lock-screen timer before asking for permission.'),
    ('Splash', '“Never forget your candle again!”'),
  ],
  'gigmo': [
    ('Home to Video Interview', 'Review applicants and jump straight into a video interview.'),
    ('Calendar', 'Interviews and shifts on one calendar, with a call in progress.'),
    ('Discover Jobs', 'Browse nearby gigs, see details on a map, and schedule an interview.'),
    ('Approve Timecards', 'Employers approve hours, rate workers and extend contracts.'),
    ('Clock In and Out', 'Log hours with a slider, then rate the employer at the end of the contract.'),
    ('Next Gig', 'When a contract ends, a good rating unlocks better jobs.'),
    ('Savings', 'Put a percentage of every paycheck toward goals automatically.'),
    ('Balance', 'Weekly earnings and spending, with a payday advance a tap away.'),
    ('Loans', 'Borrow against upcoming pay and pay it back automatically.'),
    ('You Just Got Paid!', 'The payday notification that makes it all worth it.'),
  ],
}
# Which section each screen goes in. Flat phone screens -> "Mobile Selects", flat desktop screens -> "Desktop Selects",
# everything else (device mockups, marketing scenes, sketches, assets) -> "More Stuff".
def _r(spec):
    out = set()
    for part in spec.split():
        a, _, b = part.partition('-')
        out |= {f'{n:03d}' for n in range(int(a), int(b or a) + 1)}
    return out
DESKTOP = {k: _r(v) for k, v in {
    'trovy': '004-005 007-013 016-027 029-036', 'honored': '059-076', 'transforce': '021-029',
    'adecco': '001-011', 'monster': '008-019'}.items()}
# phone-shaped images that are really mockups / bordered artwork
NOT_MOBILE = {k: _r(v) for k, v in {'saturn': '027 038 039 052 057'}.items()}

def section(slug, num, kind):
    if num in DESKTOP.get(slug, ()): return 'desktop'
    if kind in ('phone', 'tall') and num not in NOT_MOBILE.get(slug, ()): return 'mobile'
    return 'other'

# ---- v3 template: sections grouped by feature; platform decides the layout ----
# (group name, 'm' mobile 3-up | 'd' desktop full-width, item numbers)
GROUPS = {
  'saturn': [
    ('Calendar', 'm', '004 011 012 019-024 030 056'),
    ('Calendar Compare', 'm', '013 018 026 059-061 064'),
    ('Reactions & Comments', 'm', '015-017 028 029'),
    ('Bubbles', 'm', '014 025'),
    ('Status', 'm', '008-010'),
    ('Chilling', 'm', '034-037'),
    ('DMs', 'm', '031-033'),
    ('Digest', 'm', '042-048'),
    ('Now Tab & Spotify', 'm', '040 041 053 058'),
    ('Superlatives', 'm', '001-003'),
    ('Explore & Brand Partnerships', 'm', '007 005 006 049-052 054 055 057 062 063'),
  ],
  'transforce': [
    ('Website, Mobile', 'm', '001-020'), ('Website, Desktop', 'd', '021-029'), ('Sign Up', 'm', '030-036'),
    ('Driver App', 'm', '037-058 060-066'), ('On the Road', 'm', '067-079'), ('Elite Profile', 'm', '080-091'),
    ('Copilot', 'm', '059 092-096'), ('Walmart Pitch', 'm', '097-104'),
  ],
  'honored': [('Planning Your Week', 'm', '009-032'), ('Live Class', 'm', '033-058'), ('Instructor Studio', 'd', '059-076')],
  'abbott': [('Onboarding & Baseline', 'm', '001-025'), ('Goals & Daily Check-ins', 'm', '026-047'),
             ('My Data & Stories', 'm', '048-058'), ('Care Team', 'm', '059-069')],
  'kyn': [('Onboarding', 'm', '002-018'), ('Reaching Out', 'm', '019-024'), ('Contacts & Tags', 'm', '025-050'),
          ('Goals & Reminders', 'm', '051-059'), ('Profile', 'm', '060-063')],
  'trovy': [('Marketing Site', 'd', '004 005'), ('Mobile', 'm', '006 028'), ('Application', 'd', '007-013 016 017'),
            ('Onboarding', 'd', '018-020'), ('Account', 'd', '021-027 029-036')],
  'monstro': [('Mobile', 'm', '001-030 032-034')], 'wherei': [('Mobile', 'm', '001-014')], 'candle': [('Mobile', 'm', '001-014')],
  'upclose': [('Mobile', 'm', '011-037')], 'adecco': [('Desktop', 'd', '001-011')], 'monster': [('Desktop', 'd', '008-019')],
  'gigmo': [],
}
# UI shown in context (device mockups, composites, store pages) -> the last section
IN_CONTEXT = {'trovy': '003 014 015', 'saturn': '027 038 039', 'honored': '008', 'kyn': '001', 'upclose': '001-010',
              'monster': '001-007', 'gigmo': '001-010', 'adecco': '012'}
# images with a baked-in white border (cropped in the frame)
BORDERED = {'saturn': _r('057')}

def _seq(spec):
    out = []
    for part in spec.split():
        a, _, b = part.partition('-')
        out += [f'{n:03d}' for n in range(int(a), int(b or a) + 1)]
    return out

def groups_for(slug, manifest_items):
    nums = {it['src'][:3] for it in manifest_items}
    out = [(name, plat, [n for n in _seq(spec) if n in nums]) for name, plat, spec in GROUPS[slug]]
    ctx = [n for n in _seq(IN_CONTEXT.get(slug, '')) if n in nums]
    return out, ctx
