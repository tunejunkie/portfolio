import re
# 1-5 school day, 6-11 dormant (time of day), 12-17 first-time setup
DORM=[  # time, greeting, sub, later-sub, background
 ('1:24am','🌙 Good night, Alex!','Tomorrow is a B-Day','tomorrow','linear-gradient(180deg,rgb(30,32,112) 0%,rgb(9,91,108) 100%)'),
 ('5:43am','☀️ Good morning, Alex!','You’re free until 8am','at 8:00am','linear-gradient(180deg,rgb(94,110,213) 0%,rgb(198,152,236) 50.11%,rgb(251,201,179) 86.46%)'),
 ('8:14am','☀️ Good morning, Alex!','You’re free until 12pm','tomorrow','linear-gradient(180deg,rgb(33,136,255) 13.54%,rgb(228,226,159) 100%)'),
 ('12:29pm','🌥️ Good afternoon, Alex!','Tomorrow is a B-Day','tomorrow','radial-gradient(3229px 3055px at 260px 349px,rgb(51,168,255) 0%,rgb(0,82,254) 63.54%)'),
 ('6:27pm','✨ Good evening, Alex!','Tomorrow is a B-Day','tomorrow','linear-gradient(180deg,rgb(63,61,222) 0%,rgb(238,168,81) 149.74%)'),
 ('10:51pm','🌙 Good night, Alex!','Tomorrow is a B-Day','tomorrow','linear-gradient(180deg,rgb(28,34,93) 0%,rgb(63,61,222) 149.74%)'),
]
NAV=['2:66846','2:66884','2:67000','2:66923','2:66962','2:80509','2:81433','2:81509','2:81574','2:81312','2:81357','2:81591']
TAB=['2:66337']
HERO=['2:66843','2:66881','2:66997','2:66920','2:66959','2:66402','2:81367','2:81442','2:81518','2:81269','2:81320','2:81589']
HERO2=['2:66845','2:66883','2:66999','2:66922','2:66961','2:80503','2:81586']
src=[open(f'f{i}.html').read() for i in range(1,6)]
D=open('fD.html').read()
for t,g,s,l,bg in DORM:
    h=D.replace('<div class="bg-gradient-to-b from-[#3f3dde] relative size-full to-[#eea851] to-[149.74%]" data-node-id="2:80499"',
                f'<div class="relative size-full" style="background:{bg}" data-node-id="2:80499"')
    h=h.replace('>6:27pm<',f' class="dclock">{t}<'.replace(' class="dclock">','>',1) if False else f'>{t}<')
    h=h.replace('✨ Good evening, Alex!',g).replace('Tomorrow is a B-Day',s).replace('>tomorrow</p>',f'>{l}</p>')
    src.append(h)
src+= [open(f'f{i}.html').read() for i in range(7,13)]

def light_options(h):
    """First-time setup screens: Figma had two of the four option buttons in the dark style by accident. Make them all light."""
    for t in ('Invite friends to Saturn<', 'Edit school schedule<'):
        i = h.find(t)
        if i < 0: continue
        j = h.rfind('bg-[rgba(0,0,0,0.2)]', 0, i)
        if j < 0 or i - j > 600: continue
        h = h[:j] + 'bg-[rgba(129,166,255,0.2)]' + h[j + len('bg-[rgba(0,0,0,0.2)]'):]
    return h
layers=[]
for i,h in enumerate(src,1):
    h=re.sub(r'<div class="', f'<div id="L{i}" class="layer ', h, count=1)
    for n in NAV: h=h.replace(f'data-node-id="{n}"', f'data-node-id="{n}" data-fix="nav"')
    for n in TAB: h=h.replace(f'data-node-id="{n}"', f'data-node-id="{n}" data-fix="tab"')
    for n in HERO: h=h.replace(f'data-node-id="{n}"', f'data-node-id="{n}" data-hero="1"')
    for n in HERO2: h=h.replace(f'data-node-id="{n}"', f'data-node-id="{n}" data-hero="2"')
    h=re.sub(r'<img([^>]*?)src="(a/[^"]*imgCountdownRingTimer\.svg)"', r'<img data-ring="1"\1src="\2"', h)
    h=re.sub(r'<img([^>]*?)src="(a/[^"]*imgNotch\.svg)"', r'<img data-notch="1"\1src="\2"', h)
    if i >= 12: h = light_options(h)
    layers.append(h)
page=f'''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=375">
<title>Saturn Now Tab</title>
<link rel="stylesheet" href="tw.css"><link rel="stylesheet" href="now.css">
</head><body><div id="stage">
{''.join(layers)}
</div><script src="now.js"></script></body></html>'''
open('index.html','w').write(page); print(len(layers),'layers')
