"""Work History page (/work-history/). Content is Natalie's own, from natalierose.works/work-history."""
import html

ROLES = [
    dict(co='Trovy', title='Senior Director of Product Design', dates='May 2025–Current', loc='New York, NY', logo='trovy',
         link=('screenshots/trovy/', 'Trovy screenshots'),
         body=['Founding / sole product designer, shipping digital experiences that took Trovy from Seed to $100MM PMV in one year.',
               'Designing all product experiences (application, dashboard), as well as initial brand look/feel, design system, physical credit card, marketing site, ads, creative direction, product and marketing strategy.'],
         about='Trovy is a fintech platform launching products for homeowners – providing fast, flexible, and affordable credit options.',
         stats=[('Seed → $100MM', 'PMV in one year')]),
    dict(co='Saturn', title='Lead Product Designer', dates='April 2022–May 2025', loc='New York, NY', logo='saturn',
         link=('screenshots/saturn/', 'Saturn screenshots'),
         body=['Lead product designer at Saturn from 2022 (Series A) until acquisition by Snap in May 2025. During my tenure, app installs went up 68x, sharing behavior went up 13x, K-factor went up 47%. Player/coach role.'],
         about='About: “At Saturn, we’re on a mission to build community around the calendar. We’re starting in high schools – and helping students across hundreds of campuses manage their time and stay better connected with friends. More than half of our users are active daily. We are funded by General Catalyst, Coatue, Ashton Kutcher’s Sound Ventures, Inspired Capital, as well as other top venture investors.”',
         stats=[('68x', 'app installs'), ('13x', 'sharing'), ('+47%', 'K-factor')]),
    dict(co='Monster', title='Director of UX Engineering', dates='April 2018–April 2022', loc='Remote', logo='monster',
         link=('screenshots/monster/', 'Monster screenshots'),
         body=['Legacy job search platform. Became part of the Monster team through their acquisition of startup Jobr. Rose to become Director of UX Engineering, leading consumer product design and innovation strategies in player-coach role.',
               'Achievements include overhauling UI/UX for GDPR compliance, developing and maintaining a multi-brand design system for both designers and engineers to deploy cross-platform and cross-business; being primary individual contributor for interfaces across web, iOS and Android platforms serving millions of users, with a high level of compliance and supportive of 10+ languages and regions. Manager of a team of 5.'],
         stats=[('5', 'person team managed'), ('10+', 'languages & regions')]),
    dict(co='SoFi', title='Product Designer', dates='April 2017–April 2018', loc='San Francisco, CA', logo='sofi',
         body=['Product design for fintech products including banking, investing, and innovative social networking products, for web and native mobile. Winner of 2017 internal Hackathon.']),
    dict(co='Elephant', title='Interaction Designer', dates='November 2015–February 2017', loc='San Francisco, CA', logo='elephant-and-apple',
         body=['I worked onsite in Sunnyvale on the Apple account as an agency designer, working on large-scale web marketing projects. Elephant is a spinoff agency to agency Huge Inc., serving conflict-of-interest clients.']),
    dict(co='Huge, Inc.', title='UX Designer', dates='June 2014–October 2015', loc='Brooklyn, NY', logo='huge',
         body=['I kicked off my design career as a 2015 graduate of Huge’s famed UX Design School. During the prior year, I was on the Business Development team, in executive support role.']),
]

# (name, what it was, gallery slug or None, thumb or None)
CONTRACTS = [
    ('Monstro', 'AI money copilot', 'monstro', 't04'),
    ('TransForce', 'Job marketplace & driver app', 'transforce', 't07'),
    ('BCG Digital Ventures', 'Abbott NeuroSphere MyPath', 'abbott', 't09'),
    ('Prophet', None, None, None),
    ('Pareto', 'Kyn, a personal CRM', 'kyn', 't06'),
    ('Adecco', 'Adecco Direct', 'adecco', 't11'),
    ('HonorEd', 'Live online classes', 'honored', 't08'),
    ('DesignMap', None, None, None),
    ('Gigmo', 'Gig-work concept', 'gigmo', None),
]
PERSONAL = [
    ('WhereI', 'Remi, an AI biographer', 'wherei', 't03'),
    ('UpClose', 'Plans in three questions', 'upclose', 't10'),
    ('Radar', None, None, None),
    ('I Lit A Candle', 'iPhone app, designed & vibe-coded', 'candle', 't01'),
]
SKILLS = ['Digital Product Design', 'Native Mobile Design', 'Figma', 'Leveraging AI', 'Design Systems', 'Prototyping', 'Design Strategy', 'Design Team Building']
INDUSTRIES = ['Fintech', 'Social', 'Job Search', 'Healthcare', 'Education', 'Consumer Mobile']

_ARROW_UNUSED = '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M7 17L17 7M9 7h8v8" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'


def work_history():
    from build import head, nav, LINKEDIN
    base = '../'; e = html.escape
    def co_link(r):
        return (f'<a href="{base}{r["link"][0]}">{e(r["co"])}</a>' if r.get('link') else e(r['co']))
    def role(r):
        about = f'<p>{e(r["about"])}</p>' if r.get('about') else ''
        return f'''<article class="rv-role">
        <h2>{co_link(r)} • {e(r["title"])}</h2>
        <p class="rv-when">{e(r["dates"])} • {e(r["loc"])}</p>
        {''.join(f'<p>{e(t)}</p>' for t in r["body"])}{about}
      </article>'''
    def lst(items):
        return ''.join(f'<li><a href="{base}screenshots/{slug}/">{e(n)}</a></li>' if slug else f'<li>{e(n)}</li>' for n, _, slug, _ in items)
    plain = lambda xs: ''.join(f'<li>{e(x)}</li>' for x in xs)
    return head('Work History — Natalie Rose Taylor', base, 'Natalie Rose Taylor’s work history: Trovy, Saturn, Monster, SoFi, Elephant (Apple) and Huge, plus contracts and personal projects.') + f'''
<body class="gallery rv-page" data-base="{base}">
{nav(base)}
<main class="rv">
  <div class="rv-cols">
    <section class="rv-main" aria-labelledby="rv-ft">
      <h1 id="rv-ft">Full time positions</h1>
      {''.join(role(r) for r in ROLES)}
    </section>
    <aside class="rv-side">
      <section><h2>Contracts</h2><ul>{lst(CONTRACTS)}</ul></section>
      <section><h2>Personal Projects</h2><ul>{lst(PERSONAL)}</ul></section>
      <section><h2>Top Skillset</h2><ul>{plain(SKILLS)}</ul></section>
      <section><h2>Industries</h2><ul>{plain(INDUSTRIES)}</ul></section>
    </aside>
  </div>
</main>
<script type="module" src="{base}js/gallery.js"></script>
</body></html>'''
