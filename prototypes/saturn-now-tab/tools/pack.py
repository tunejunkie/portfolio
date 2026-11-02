import hashlib, os, re, shutil, sys
from PIL import Image
SRC='/tmp/claude-0/now'; OUT=sys.argv[1]
os.makedirs(OUT+'/a',exist_ok=True); os.makedirs(OUT+'/fonts',exist_ok=True)
h=open(SRC+'/index.html').read()
refs=sorted(set(re.findall(r'(?:src="|url\(&quot;)(a/[^"&]+)',h)))
m={}; total=0
for r in refs:
    p=os.path.join(SRC,r)
    data=open(p,'rb').read(); dig=hashlib.sha1(data).hexdigest()[:12]
    ext=r.rsplit('.',1)[1]
    head=data[:4]
    if head.startswith(b'\x89PNG') or head.startswith(b'\xff\xd8'):
        name=f'a/{dig}.webp'
        if not os.path.exists(OUT+'/'+name):
            im=Image.open(p); im.save(OUT+'/'+name,'WEBP',quality=86,method=6)
    else:
        name=f'a/{dig}.{ext}'
        if not os.path.exists(OUT+'/'+name): shutil.copy(p,OUT+'/'+name)
    m[r]=name
for r,n in m.items(): h=h.replace(r,n)
open(OUT+'/index.html','w').write(h)
for f in ['tw.css','now.css','now.js']: shutil.copy(SRC+'/'+f,OUT+'/'+f)
for f in os.listdir(SRC+'/fonts'): shutil.copy(SRC+'/fonts/'+f,OUT+'/fonts/'+f)
sz=sum(os.path.getsize(os.path.join(OUT,'a',f)) for f in os.listdir(OUT+'/a'))
print(len(refs),'refs ->',len(set(m.values())),'files',round(sz/1e6,2),'MB')
