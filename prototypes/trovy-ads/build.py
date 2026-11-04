"""Trovy Instagram-story ads, rebuilt as layered HTML with light motion (site/proto/trovy-ads/).

Source: Natalie's Figma, file xsFoIEpsO6xISuYx8oFAyU, section "Ads" (1528:113862): twelve 1080x1920 stories.
Each ad's top-level layers were rendered on their own from Figma (transparent PNGs), placed by matching them
against Figma's full render of the ad (align.py), and the frame background was recovered from the pixels
no layer covers. This script turns that into web assets plus a data file the player animates.

Run: python3 build.py <work dir with layout.json, L/, ref/, bgNN.png>
"""
import json, os, sys
from PIL import Image

W = sys.argv[1]
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', '..', 'site', 'proto', 'trovy-ads')
os.makedirs(os.path.join(OUT, 'a'), exist_ok=True)
layout = json.load(open(os.path.join(W, 'layout.json')))

# motion for each layer, in Figma layer order: (role, delay in s). Roles are animated in player.js.
#   bg: still   glow: fades in, breathes   kb: slow push-in (photos)   logo: drops in   rise: rises in
#   drop: the card falls in, then floats   pop: buttons pop in, then pulse   wipe: drawn left to right
#   zoom: grows in   foot: the legal footer, still   ghost: echo rows that cascade in
ROLES = {
    1:  [('drop', .35), ('foot', 0), ('rise', .95), ('logo', .1), ('pop', 1.35), ('rise', .6)],
    2:  [('glow', 0), ('foot', 0), ('pop', 1.45), ('rise', .2), ('rise', .38), ('logo', .05), ('rise', .65),
         ('wipe', .55), ('drop', .8)],
    3:  [('glow', 0), ('ghost', .35), ('bg', 0), ('rise', .2), ('rise', 1.0), ('rise', 1.15), ('drop', 0),
         ('zoom', 1.2), ('pop', 1.5), ('foot', 0)],
    4:  [('bg', 0), ('bg', 0), ('pop', 1.45), ('foot', 0), ('rise', 1.6), ('logo', .05), ('zoom', .95),
         ('rise', .2), ('rise', .35), ('zoom', 1.2), ('drop', .55)],
    5:  [('bg', 0), ('foot', 0), ('drop', .7), ('ghost', .4), ('ghost', .3), ('ghost', .2), ('ghost', .1),
         ('rise', .05), ('rise', .3), ('logo', 1.05), ('pop', 1.4), ('rise', 1.6)],
    6:  [('kb', 0)],
    7:  [('bg', 0), ('kb', 0), ('bg', 0), ('foot', 0), ('drop', .75), ('rise', .2), ('rise', 1.45)],
    8:  [('rise', .25), ('drop', .55), ('rise', 1.2), ('wipe', 1.35), ('wipe', 1.25), ('logo', .05)],
    9:  [('foot', 0), ('kb', 0), ('rise', .45), ('rise', .9), ('pop', 1.3), ('rise', 1.5), ('bg', 0),
         ('logo', .05)],
    10: [('glow', 0), ('foot', 0), ('drop', .55), ('zoom', 1.05), ('rise', .95), ('rise', .25), ('rise', .12),
         ('pop', 1.5), ('rise', 1.3), ('logo', .02)],
    11: [('foot', 0), ('rise', .95), ('pop', 1.35), ('logo', .1), ('drop', .35), ('rise', .6)],
    12: [('glow', 0), ('kb', 0), ('foot', 0), ('rise', 1.25), ('drop', .45), ('pop', 1.5), ('rise', .9)],
}
# what each ad is, for the screen reader and the case study (Figma frame names are internal)
ALT = {
    1: 'Trovy HELOC ad: Don’t own a home without it. Maintain, renovate, repair, furnish. Check your rate.',
    2: 'Trovy HELOC ad: Variable now, fixed later. Convert any balance or transaction over $100 into a fixed-rate payment plan, anytime.',
    3: 'Trovy HELOC ad: The world’s best HELOC, according to the cofounder’s mom. “Thanks sweetie, I love my new windows!”',
    4: 'Trovy HELOC ad: 3% cash back. Homeowners get up to 3% cash back when they spend with the Trovy HELOC Card.',
    5: 'Trovy HELOC ad: 3% Cash Back for homeowners: 3% top category, 1.5% on all purchases.',
    6: 'Trovy ad: No upfront draw required. Tap your home equity only when you need it, and spend and pay back like a credit card.',
    7: 'Trovy ad: Equity-rich, house-poor? Not anymore.',
    8: 'Trovy ad: a customer quote, “Super fast HELOC. It was easy. I’ve already used it to complete my next project!” over a hand holding the card.',
    9: 'Trovy HELOC ad: The essential tool for homeowners. Low rates, cash back rewards, fixed or variable.',
    10: 'Trovy ad: The only credit card you’ll ever need… is a HELOC.',
    11: 'Trovy HELOC ad: If you own a home, you need Trovy. Refi debt, lower APRs, lower payments.',
    12: 'Trovy ad: Your home = your safety net. The HELOC with no upfront draw requirement makes it possible.',
}


def webp(img, path, q=86):
    img.save(path, 'WEBP', quality=q, method=6)
    return os.path.basename(path)


ads = []
for fid, ad in sorted(layout.items(), key=lambda kv: kv[1]['n']):
    n = ad['n']; roles = ROLES[n]
    assert len(roles) == len(ad['layers']), (n, len(roles), len(ad['layers']))
    ref = Image.open(os.path.join(W, 'ref', f'ad{n:02d}.png')).convert('RGB')
    bg = Image.open(os.path.join(W, f'bg{n:02d}.png')).convert('RGB')
    layers = []
    for L, (role, delay) in zip(ad['layers'], roles):
        if role == 'foot':
            # the legal footer never moves: take it straight from Figma's render, background and all
            h = L['h']; x, y = 0, 1920 - h
            img = ref.crop((0, y, 1080, 1920))
            f = webp(img, os.path.join(OUT, 'a', f'{n:02d}-foot.webp'), 90)
            layers.append(dict(f=f, x=x, y=y, w=1080, h=h, role=role, d=delay))
            continue
        img = Image.open(os.path.join(W, 'L', L['id'].replace(':', '_') + '.png')).convert('RGBA')
        bbox = img.getchannel('A').getbbox()
        if not bbox: continue
        img = img.crop(bbox)  # trim transparent margins: smaller files, tighter transform origins
        x, y = L['x'] + bbox[0], L['y'] + bbox[1]
        f = webp(img, os.path.join(OUT, 'a', f"{n:02d}-{len(layers):02d}.webp"))
        layers.append(dict(f=f, x=x, y=y, w=img.width, h=img.height, role=role, d=delay))
    ads.append(dict(n=n, alt=ALT[n], bg=webp(bg, os.path.join(OUT, 'a', f'{n:02d}-bg.webp'), 88),
                    poster=webp(ref, os.path.join(OUT, 'a', f'{n:02d}-full.webp'), 84), layers=layers))
    print(n, len(layers), 'layers')

open(os.path.join(OUT, 'ads.js'), 'w').write('window.ADS = ' + json.dumps(ads, separators=(',', ':')) + ';\n')
tot = sum(os.path.getsize(os.path.join(OUT, 'a', f)) for f in os.listdir(os.path.join(OUT, 'a')))
print('assets', round(tot / 1e6, 2), 'MB')
