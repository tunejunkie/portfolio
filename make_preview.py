"""Copy ./site into a preview folder for the claude.ai artifact preview.
The artifact host doesn't resolve folder URLs, so relative links like "screenshots/saturn/" get "index.html" appended.
Prints the files map (JSON) for the publish call."""
import os, re, shutil, json, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, 'site')
DST = sys.argv[1]
shutil.rmtree(DST, ignore_errors=True)
shutil.copytree(SRC, DST, ignore=shutil.ignore_patterns('_test.html'))
link = re.compile(r'href="(?!https?:|mailto:|#)([^"]*/)"')
for dp, _, fs in os.walk(DST):
    for f in fs:
        if f.endswith('.html'):
            p = os.path.join(dp, f); s = open(p).read()
            s = link.sub(lambda m: f'href="{m.group(1)}index.html"', s)
            s = s.replace('href=""', 'href="_preview.html"').replace('href="../../"', 'href="../../_preview.html"').replace('href="../../index.html"', 'href="../../_preview.html"').replace('href="../../#about"', 'href="../../_preview.html#about"').replace('href="../#about"', 'href="../_preview.html#about"').replace('href="../../#anecdotes"', 'href="../../_preview.html#anecdotes"').replace('href="../#anecdotes"', 'href="../_preview.html#anecdotes"').replace('href="../"', 'href="../_preview.html"').replace('href="../index.html"', 'href="../_preview.html"')
            open(p, 'w').write(s)
# gallery images that don't fit in the artifact's file limit live in its asset store
BM = '/tmp/claude-0/-home-claude/f712a811-cb0a-5b2d-a170-5aef756c78a1/scratchpad/blobmap.txt'
if os.path.exists(BM):
    blob = dict(l.split() for l in open(BM) if l.strip())
    pat = re.compile(r'(?:\.\./)*assets/galleries/([a-z]+)/(\d{3})\.webp')
    for dp, _, fs in os.walk(DST):
        for f in fs:
            if f.endswith('.html'):
                p = os.path.join(dp, f); s = open(p).read()
                s2 = pat.sub(lambda m: '/_blob/' + blob[f'{m.group(1)}-{m.group(2)}'] if f'{m.group(1)}-{m.group(2)}' in blob else m.group(0), s)
                if s2 != s: open(p, 'w').write(s2)
only = sys.argv[2].split(',') if len(sys.argv) > 2 else None
files = {}
for dp, _, fs in os.walk(DST):
    for f in fs:
        rel = os.path.relpath(os.path.join(dp, f), DST)
        if rel == '_preview.html' or rel == 'index.html': continue
        if only and not any(rel.startswith(o) for o in only): continue
        files[rel] = rel
print(json.dumps(files))
