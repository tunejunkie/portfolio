"""Career Anecdotes (homepage). Copy is Natalie's, from the anecdotes carousel on natalierose.works."""
import html

ANECDOTES = [
    ('nike', 'Saturn partners with Nike; gets acquired by Snap',
     'As lead product designer at Saturn from 2022 until the acquisition by Snap in 2025, I designed the work that awarded Saturn its first sponsored partnership, with Nike.'),
    ('honored', 'HonorEd raises 35MM Series A',
     'As the first design hire (contract), I designed the MVP for Honor Education’s pilot program and their initial product concepts – making remote education just as engaging and equitable as in-person learning. Congrats to the team!'),
    ('transforce', 'TransForce lands partnership with Walmart',
     'As a contracted designer, I designed the mockups for the pitch deck that won truck driver recruitment startup Transforce a partnership with Walmart to post and fill CDL-A jobs. Congrats to the team!'),
    ('card', 'I designed a credit card',
     'I had fun designing Trovy’s HELOC Card. A subdued engraved design, in keeping with its substantial metal fabrication, has a repeating icon pattern evoking textiles from luxury brands – while the fun yellow color is made to stand out in your wallet and on the market.'),
    ('candle', 'Adventures in vibe-coding',
     'I Lit A Candle App is my first foray into shipping an app without an engineering partner. Like most “vibe-coded” projects, it solves a highly personal problem: forgetting about a candle you’ve lit in your home! Try it out.'),
    ('kyn', 'Kyn Contacts MVP is live',
     'I designed the MVP for Pareto Holding’s supercharged contact book app, Kyn. It allows you to organize your contacts in intuitive and useful ways, and set reminders and recurring goals for making time to connect with those who matter to you.'),
    ('upclose', 'UpClose hits the App Store',
     'I created, designed, PM’d, deployed, marketed my own app, UpClose. UpClose is the friendly way to make plans! The app was ultimately retired after this project caught the attention of Saturn, the social calendar company, where I became the design lead.'),
    ('yc', 'I interviewed for Y-Combinator',
     'In 2019, I got as far as the in-person interview stage for Y Combinator for my IRL dating app, Radar. Based on the advice from the panel, I pivoted the app into what I later renamed UpClose. Both apps shipped to the App Store and had their own organic user base.'),
    ('pitch', 'I won a pitch night competition',
     'In 2017, I won 1st place at PitchForce in SF pitching my startup, Radar. PitchForce is a fast-paced startup pitch forum and competition hosted by Ecosystem Venture Group, connecting early-stage founders seeking seed funding with a panel of angel investors and venture capitalists.'),
    ('sofi', 'We won the 2017 SoFi Hackathon',
     '4 engineers and I won the internal SoFi Hackathon with our idea for an app that helps rejected SoFi applicants improve their credit profile, and invite them to reapply when they are more likely to get approved.'),
    ('figma', 'You’ll love my Figma files',
     'Meant for cross functional human eyes as well as AI MCP servers, my Figma files are well organized and beautiful. My components are componentized, my color and font styles are assigned, my layouts are Auto, and my decisions are documented.'),
]
# crop focus inside the 566×488 frame
POS = {'yc': 'center 30%', 'sofi': 'center 40%', 'pitch': 'center 20%', 'upclose': 'top', 'candle': 'top', 'figma': 'top left'}


def anecdotes_section(base=''):
    e = html.escape; a = f'{base}assets/anecdotes/'
    cards = []
    for k, title, body in ANECDOTES:
        pos = f' style="object-position:{POS[k]}"' if k in POS else ''
        if k == 'nike':
            media = (f'<video src="{a}nike.mp4" poster="{a}nike-poster.webp" muted loop playsinline preload="none" '
                     f'aria-label="{e(title)}" data-autoplay></video>')
        else:
            media = f'<img src="{a}{k}.webp" alt="{e(title)}" loading="lazy"{pos}>'
        cards.append(f'<article class="an-card"><div class="an-media">{media}</div>'
                     f'<h3>{e(title)}</h3><p>{e(body)}</p></article>')
    return f'''<section class="anecdotes" id="anecdotes" aria-labelledby="an-title">
    <div class="an-head"><h2 id="an-title">Career<br>Anecdotes</h2><p>Noteworthy moments in my career that I’d like to share with you.</p></div>
    <div class="an-grid">{''.join(cards)}</div>
  </section>'''
