/* Trovy story ads in an Instagram Stories frame.
   Everything is a pure function of one clock, render(t), so the page can play live or be stepped frame by
   frame for the recording (?still, then window.render(t)). Each ad is its own sponsored story: it plays, then
   the deck turns like a cube to the next one, either by itself, or under a finger swipe or tap (recording).
   Live: tap the right half for the next ad, the left half for the previous one.  ?ad=N starts on ad N. */
(() => {
  const ADS = window.ADS, deck = document.getElementById('deck'), touch = document.getElementById('touch');
  const live = document.getElementById('live');
  const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));
  const outCubic = x => 1 - Math.pow(1 - x, 3);
  const inOut = x => x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;
  const outBack = x => { const c1 = 1.5, c3 = c1 + 1; return 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2); };

  const SVG_MORE = '<svg width="24" height="24" viewBox="0 0 24 24" fill="#fff"><circle cx="5" cy="12" r="1.7"/><circle cx="12" cy="12" r="1.7"/><circle cx="19" cy="12" r="1.7"/></svg>';
  const SVG_X = '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round"><path d="M6 6l12 12M18 6L6 18"/></svg>';

  // ---- build the stories ----
  const stories = ADS.map(ad => {
    const el = document.createElement('div'); el.className = 'story';
    el.setAttribute('role', 'img'); el.setAttribute('aria-label', ad.alt);
    const imgs = ad.layers.map(L => `<img src="a/${L.f}" alt="" style="left:${L.x}px;top:${L.y}px;width:${L.w}px;height:${L.h}px;transform-origin:${L.w / 2}px ${L.h / 2}px" draggable="false">`).join('');
    el.innerHTML = `<div class="ad"><img src="a/${ad.bg}" alt="" style="left:0;top:0;width:1080px;height:1920px" draggable="false">${imgs}</div>
      <div class="shade"></div><div class="bar"><i></i></div>
      <div class="hd"><img src="a/avatar.webp" alt=""><div class="who"><b>trovy</b><span>Sponsored</span></div>${SVG_MORE}${SVG_X}</div><div class="dim"></div>`;
    deck.appendChild(el);
    const layerEls = [...el.querySelectorAll('.ad img')].slice(1);
    return { el, ad, layers: ad.layers.map((L, i) => ({ L, img: layerEls[i] })), fill: el.querySelector('.bar i'), dim: el.querySelector('.dim') };
  });

  // ---- each layer's motion at its local time l (seconds after its cue) ----
  function pose(role, l) {
    let o = 1, x = 0, y = 0, s = 1, r = 0, clip = null;
    switch (role) {
      case 'glow': o = clamp(l / .9); s = 1 + .035 * Math.sin(l * 1.7); break;
      case 'kb': s = 1.09 - .09 * outCubic(clamp(l / 5.5)); break;
      case 'logo': { const e = outCubic(clamp(l / .55)); o = clamp(l / .4); y = -26 * (1 - e); break; }
      case 'rise': { const e = outCubic(clamp(l / .7)); o = clamp(l / .45); y = 48 * (1 - e); break; }
      case 'ghost': { const e = outCubic(clamp(l / .8)); o = e; y = 34 * (1 - e); break; }
      case 'zoom': { const e = clamp(l / .65); o = clamp(l / .3); s = .84 + .16 * outBack(e); break; }
      case 'drop': {
        const e = clamp(l / .9); o = clamp(l / .3);
        y = -170 * (1 - outBack(e)); r = -9 * (1 - outCubic(e));
        if (l > .9) { const f = (l - .9) * 2 * Math.PI / 3.4; y += -11 * Math.sin(f); r += 1.1 * Math.sin(f * .5 + .6); }
        break;
      }
      case 'pop': {
        const e = clamp(l / .5); o = clamp(l / .25); s = .72 + .28 * outBack(e);
        if (l > .8) { const k = Math.sin((l - .8) * 2 * Math.PI / 1.5); s *= 1 + .028 * Math.max(0, k) * Math.max(0, k); }
        break;
      }
      case 'wipe': { const p = outCubic(clamp(l / .95)); o = l > 0 ? 1 : 0; clip = `inset(-20px ${((1 - p) * 100).toFixed(2)}% -20px -20px)`; break; }
    }
    return { o, x, y, s, r, clip };
  }

  function paintAd(st, lt, dur) {
    for (const { L, img } of st.layers) {
      if (L.role === 'bg' || L.role === 'foot') continue;
      const p = pose(L.role, lt - L.d);
      img.style.opacity = p.o.toFixed(3);
      img.style.transform = `translate(${p.x.toFixed(1)}px,${p.y.toFixed(1)}px) rotate(${p.r.toFixed(2)}deg) scale(${p.s.toFixed(4)})`;
      if (L.role === 'wipe') img.style.clipPath = p.clip;
    }
    st.fill.style.transform = `scaleX(${clamp(lt / dur).toFixed(4)})`;
  }

  // ---- the timeline: how long each ad plays and how we leave it ----
  const q = new URLSearchParams(location.search);
  const DUR = ADS.map(a => a.n === 6 ? 4.2 : 3.7), TR = .55;
  // exits for the recording: mostly finger swipes, a couple of taps, a couple left to run out on their own
  const EXIT = ['swipe', 'swipe', 'tap', 'swipe', 'auto', 'swipe', 'swipe', 'tap', 'swipe', 'auto', 'swipe', 'swipe'];
  const segs = []; let acc = 0;
  ADS.forEach((a, i) => { segs.push({ i, t0: acc, dur: DUR[i], exit: EXIT[i % EXIT.length] }); acc += DUR[i] + (EXIT[i % EXIT.length] === 'tap' ? .12 : TR); });
  const TOTAL = acc;

  let shown = [];
  function show(list) {   // list of [story, {transform, dim}]
    const on = new Set(list.map(x => x[0]));
    stories.forEach(st => { const v = on.has(st); if (v !== st._on) { st.el.classList.toggle('on', v); st._on = v; } });
    list.forEach(([st, tf, dim]) => { st.el.style.transform = tf; st.dim.style.opacity = dim.toFixed(3); });
  }

  // the cube: the outgoing story hinges on its right edge, the incoming one on its left
  function cube(a, b, p) {
    const W = 375, ang = 90 * p;
    a.el.style.transformOrigin = '100% 50%'; b.el.style.transformOrigin = '0% 50%';
    show([[a, `translateX(${-W * p}px) rotateY(${-ang}deg)`, .55 * p], [b, `translateX(${W * (1 - p)}px) rotateY(${90 - ang}deg)`, .55 * (1 - p)]]);
  }

  function setTouch(x, y, o, s = 1) {
    touch.style.left = x + 'px'; touch.style.top = y + 'px';
    touch.style.opacity = o.toFixed(3); touch.style.transform = `scale(${s.toFixed(3)})`;
  }

  function render(t) {
    t = ((t % TOTAL) + TOTAL) % TOTAL;
    let k = segs.findIndex((s, j) => t < (segs[j + 1] ? segs[j + 1].t0 : TOTAL)); if (k < 0) k = segs.length - 1;
    const sg = segs[k], cur = stories[sg.i], nxt = stories[segs[(k + 1) % segs.length].i];
    const lt = t - sg.t0;
    setTouch(0, 0, 0);
    if (lt <= sg.dur) {
      paintAd(cur, lt, sg.dur);
      cur.el.style.transformOrigin = '50% 50%';
      show([[cur, 'none', 0]]);
      // the finger comes down a moment before a swipe
      if (sg.exit === 'swipe') { const a = clamp((lt - (sg.dur - .35)) / .2); if (a > 0) setTouch(300, 430, a * .95, 1.15 - .15 * a); }
      if (sg.exit === 'tap') { const a = clamp((lt - (sg.dur - .3)) / .18); if (a > 0) setTouch(318, 380, a, 1.2 - .2 * a); }
      announce(sg.i);
      return;
    }
    // between two stories
    const u = lt - sg.dur;
    paintAd(cur, lt, sg.dur); paintAd(nxt, u, segs[(k + 1) % segs.length].dur);
    if (sg.exit === 'tap') {        // a tap on the right cuts straight to the next one
      cur.el.style.transformOrigin = nxt.el.style.transformOrigin = '50% 50%';
      show([[nxt, 'none', 0]]);
      const f = clamp(u / .12); setTouch(318, 380, 1 - f, 1 + .25 * f);
      return;
    }
    const p = inOut(clamp(u / TR));
    cube(cur, nxt, p);
    if (sg.exit === 'swipe') setTouch(300 - 230 * outCubic(clamp(u / (TR * .85))), 430 - 14 * p, .95 * (1 - clamp((u - TR * .7) / (TR * .3))));
  }
  let said = -1;
  function announce(i) { if (i !== said) { said = i; live.textContent = `Ad ${i + 1} of ${ADS.length}`; } }

  window.render = render; window.TOTAL = TOTAL; window.SEGS = segs;
  window.preload = () => Promise.all([...document.images].map(im => im.complete ? 0 : new Promise(r => { im.onload = im.onerror = r; })));

  // ---- live: plays on its own clock; taps jump between ads ----
  if (q.has('still')) { render(+(q.get('t') || 0)); return; }
  let start = performance.now() / 1000 - (q.has('ad') ? segs[clamp(+q.get('ad') - 1, 0, segs.length - 1)].t0 : 0);
  const now = () => performance.now() / 1000 - start;
  const jump = d => {
    const t = ((now() % TOTAL) + TOTAL) % TOTAL;
    let k = segs.findIndex((s, j) => t < (segs[j + 1] ? segs[j + 1].t0 : TOTAL)); if (k < 0) k = segs.length - 1;
    const to = segs[(k + d + segs.length) % segs.length].t0;
    start = performance.now() / 1000 - to - (d < 0 && to > t ? 0 : 0);
  };
  document.querySelector('.hit--r').addEventListener('click', () => jump(1));
  document.querySelector('.hit--l').addEventListener('click', () => jump(-1));
  document.querySelector('.cta').addEventListener('click', e => e.preventDefault());
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduced) {   // no motion: each ad shown settled; taps still step through them
    let k = 0; const still = () => { render(segs[k].t0 + 3); touch.style.opacity = 0; };
    document.querySelector('.hit--r').addEventListener('click', () => { k = (k + 1) % segs.length; still(); });
    document.querySelector('.hit--l').addEventListener('click', () => { k = (k - 1 + segs.length) % segs.length; still(); });
    still(); return;
  }
  (function loop() {
    render(now());
    touch.style.opacity = 0;   // the finger is only for the recording
    requestAnimationFrame(loop);
  })();
})();
