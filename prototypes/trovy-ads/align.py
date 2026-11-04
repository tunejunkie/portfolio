"""Place every exported layer of each ad so the stack matches Figma's full render, then rebuild the frame
background from the pixels no layer covers. Writes layout.json and a side-by-side check image per ad."""
import json, os, numpy as np, cv2
from PIL import Image

D = os.path.dirname(os.path.abspath(__file__))
ads = json.load(open(f'{D}/ads.json'))
SKIP = {'1532:114987'}  # an invisible 1px line
out = {}


def load(p):
    return np.asarray(Image.open(p).convert('RGBA')).astype(np.float32) / 255


def over(dst, src, x, y):
    """alpha-composite src onto dst (both float RGBA / RGB) at x, y, clipped to dst"""
    H, W = dst.shape[:2]; h, w = src.shape[:2]
    x0, y0, x1, y1 = max(0, x), max(0, y), min(W, x + w), min(H, y + h)
    if x0 >= x1 or y0 >= y1: return
    s = src[y0 - y:y1 - y, x0 - x:x1 - x]; a = s[..., 3:4]
    dst[y0:y1, x0:x1, :3] = s[..., :3] * a + dst[y0:y1, x0:x1, :3] * (1 - a)
    if dst.shape[2] == 4: dst[y0:y1, x0:x1, 3:4] = a + dst[y0:y1, x0:x1, 3:4] * (1 - a)


for ai, ad in enumerate(ads, 1):
    ref = load(f'{D}/ref/ad{ai:02d}.png')[..., :3]
    kids = [k for k in ad['kids'] if k['id'] not in SKIP]
    if not kids:  # a flat image in Figma: the whole render is its one layer
        import shutil; shutil.copy(f'{D}/ref/ad{ai:02d}.png', f"{D}/L/{ad['id'].replace(':', '_')}.png")
        kids = [dict(id=ad['id'], name='image', x=0, y=0, w=1080, h=1920)]
    layers = []
    for k in kids:
        im = load(f"{D}/L/{k['id'].replace(':', '_')}.png"); rh, rw = im.shape[:2]
        # first guess: the render is centred on the node (effects spread evenly), clipped to the frame
        x = round(k['x'] + k['w'] / 2 - rw / 2); y = round(k['y'] + k['h'] / 2 - rh / 2)
        if rw >= 1079: x = 0
        elif k['x'] < 0 and k['x'] + k['w'] > 0: x = 0
        elif k['x'] + k['w'] > 1080 and k['x'] < 1080: x = 1080 - rw
        if rh >= 1919: y = 0
        elif k['y'] < 0 and k['y'] + k['h'] > 0: y = 0
        elif k['y'] + k['h'] > 1920 and k['y'] < 1920: y = 1920 - rh
        # refine with masked template matching on the reference, where the layer is solid
        a = im[..., 3]
        if (a > 0.95).mean() > 0.01 and not (rw >= 1079 and rh >= 1919):
            m = ((a > 0.95) * 255).astype(np.uint8); tpl = (im[..., :3] * 255).astype(np.uint8)
            REF8 = (ref * 255).astype(np.uint8)
            def match(img, t, mk, x, y, R, sc):
                H, W = img.shape[:2]; h, w = t.shape[:2]
                X0, Y0 = max(-w + 8, x - R), max(-h + 8, y - R)
                # pad the reference so a layer can hang off the frame edges
                P = max(w, h) + R + 400; x = min(max(x, -w), W); y = min(max(y, -h), H)
                big = cv2.copyMakeBorder(img, P, P, P, P, cv2.BORDER_CONSTANT, value=(0, 0, 0))
                X0, Y0 = x - R, y - R
                win = big[P + Y0:P + y + h + R, P + X0:P + x + w + R]
                if sc != 1:
                    win = cv2.resize(win, None, fx=sc, fy=sc, interpolation=cv2.INTER_AREA)
                    t = cv2.resize(t, None, fx=sc, fy=sc, interpolation=cv2.INTER_AREA)
                    mk = cv2.resize(mk, None, fx=sc, fy=sc, interpolation=cv2.INTER_NEAREST)
                if win.shape[0] < t.shape[0] or win.shape[1] < t.shape[1] or mk.max() == 0: return x, y, np.inf
                res = cv2.matchTemplate(win, t, cv2.TM_SQDIFF, mask=mk); res[~np.isfinite(res)] = np.inf
                yy, xx = np.unravel_index(np.argmin(res), res.shape)
                return X0 + int(round(xx / sc)), Y0 + int(round(yy / sc)), float(res[yy, xx]) / max(1, (mk > 0).sum())
            cands = [(x, y)]
            cands.append(match(REF8, tpl, m, x, y, 8, 1)[:2])
            w0 = [(x, y), (round(k['x']), y), (round(k['x'] + k['w'] - rw), y)]
            best = min((match(REF8, tpl, m, cx, cy, 120, 0.25) for cx, cy in w0), key=lambda r: r[2])
            cands.append(match(REF8, tpl, m, best[0], best[1], 6, 1)[:2])
        else:
            cands = [(x, y)]
        k['_c'] = list(dict.fromkeys(cands))
        layers.append(dict(id=k['id'], name=k['name'], x=int(x), y=int(y), w=rw, h=rh))
        k['_im'] = im
    def background(pos):
        pm = np.zeros((1920, 1080, 4), np.float32)
        for (x, y), k in zip(pos, kids): over(pm, k['_im'], x, y)
        A = pm[..., 3:4]
        est = np.where(A < 0.85, (ref - pm[..., :3]) / np.maximum(1 - A, 1e-3), 0)
        known = (A[..., 0] < 0.85)
        est8 = np.clip(est * 255, 0, 255).astype(np.uint8)
        small = cv2.resize(est8, (270, 480), interpolation=cv2.INTER_AREA)
        kn = cv2.resize(known.astype(np.uint8), (270, 480), interpolation=cv2.INTER_AREA)
        filled = cv2.inpaint(small, (1 - kn).astype(np.uint8), 12, cv2.INPAINT_TELEA)
        filled = cv2.GaussianBlur(filled, (0, 0), 3)
        b = cv2.resize(filled, (1080, 1920), interpolation=cv2.INTER_CUBIC).astype(np.float32) / 255
        return np.where(known[..., None] & (A < 0.02), ref, b)

    def error(pos, bg):
        c = bg.copy()
        for (x, y), k in zip(pos, kids): over(c, k['_im'], x, y)
        return float(np.abs(c - ref).mean())

    pos = [k['_c'][0] for k in kids]
    for _ in range(2):
        bgimg = background(pos)
        for i, k in enumerate(kids):
            if len(k['_c']) > 1:
                pos[i] = min(k['_c'], key=lambda c: error(pos[:i] + [c] + pos[i + 1:], bgimg))
    bgimg = background(pos)
    for L, p in zip(layers, pos): L['x'], L['y'] = int(p[0]), int(p[1])
    comp = bgimg.copy()
    for L, k in zip(layers, kids): over(comp, k['_im'], L['x'], L['y'])
    err = np.abs(comp - ref).mean() * 255
    out[ad['id']] = dict(name=ad['name'], n=ai, err=round(float(err), 2), layers=layers,
                         )
    Image.fromarray((bgimg * 255).astype(np.uint8)).save(f'{D}/bg{ai:02d}.png')
    sbs = np.concatenate([ref, comp, np.clip(np.abs(comp - ref) * 4, 0, 1)], axis=1)
    Image.fromarray((sbs * 255).astype(np.uint8)).resize((810, 480)).save(f'{D}/chk{ai:02d}.png')
    print(ai, ad['name'][:30], 'err', round(float(err), 2), flush=True)
json.dump(out, open(f'{D}/layout.json', 'w'), indent=1)
