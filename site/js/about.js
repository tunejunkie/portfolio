// About Me — pinned, scroll-scrubbed sequence on a fixed "art board" (Figma frame coordinates),
// scaled to fit the viewport. Desktop board 1728×1117, mobile board 430×932.
const $ = (s, el = document) => el.querySelector(s), $$ = (s, el = document) => [...el.querySelectorAll(s)];
const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));
const io = t => t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
const backOut = t => { const c1 = 1.9, c3 = c1 + 1; return 1 + c3 * Math.pow(t - 1, 3) + c1 * Math.pow(t - 1, 2); };
// keyframes: [[q, v], ...] eased between neighbours, held outside
function kf(q, keys) {
  if (q <= keys[0][0]) return keys[0][1];
  for (let i = 1; i < keys.length; i++) {
    const [q1, v1] = keys[i], [q0, v0] = keys[i - 1];
    if (q <= q1) {
      const t = io(clamp((q - q0) / (q1 - q0)));
      return Array.isArray(v0) ? v0.map((a, j) => a + (v1[j] - a) * t) : v0 + (v1 - v0) * t;
    }
  }
  return keys[keys.length - 1][1];
}
const fade = (q, a, b, c, d) => d === undefined ? kf(q, [[a, 0], [b, 1]]) : kf(q, [[a, 0], [b, 1], [c, 1], [d, 0]]);

export const TITLES = ['Cellist', 'Fine Artist', 'Wife', 'Mom', 'Traveler', 'Karaoke-er', 'Boater', 'Dog mom', 'Skater'];
// The pin ends once the Slash scene has assembled; from there the page scrolls normally and the
// ring auto-advances on a timer (tap a photo to jump to it).
export const QT = 7.2;
const DWELL = 1000, SPIN = 520;      // ms per title, ms per rotation

const PORTRAIT_AR = 1302 / 1208;
// outline svgs: native size and where their dot sits inside them
const OUT = { wa: { w: 136.6, h: 92.9, dx: 38, dy: 28.6 }, ny: { w: 157.06, h: 157.06, dx: 119.14, dy: 127.55 }, ca: { w: 310, h: 310, dx: 50.12, dy: 129.93 } };

const L = {
  desk: {
    W: 1728, H: 1117,
    circle: [[1, [864, 864, 862]], [2, [864, 1298, 1177]], [5.9, [864, 1298, 1177]], [6.8, [864, 1004, 2902]]],
    portrait: [[1, [349, 398, 887]], [2, [161, 662, 1211]], [5.9, [161, 662, 1211]], [6.8, [424, 533, 757]]],
    dots: { sea: [280, 361.5], ny: [1451, 440.5], sf: [272, 652] }, outScale: 1,
    labels: { sea: [-130, -25], ny: [33, -25], sf: [-114, -20] },
    lines: ['M280,361 C560,170 1150,170 1451,440', 'M1451,440 C1250,640 700,650 272,652', 'M272,652 C600,760 1250,700 1451,440'],
    ring: { cx: 872, cy: 996, r: 578, d: 220 },
  },
  mob: {
    W: 430, H: 932,
    circle: [[1, [215, 610, 380]], [2, [215, 930, 560]], [5.9, [215, 930, 560]], [6.8, [215, 720, 1900]]],
    portrait: [[1, [20, 400, 390]], [2, [-45, 660, 520]], [5.9, [-45, 660, 520]], [6.8, [-20, 491, 425]]],
    dots: { sea: [74, 360], ny: [356, 400], sf: [70, 560] }, outScale: 0.42,
    labels: { sea: [-56, -12], ny: [14, -12], sf: [14, -12] },
    lines: ['M74,360 C140,270 300,270 356,400', 'M356,400 C330,500 200,560 70,560', 'M70,560 C180,630 350,560 356,400'],
    ring: { cx: 226, cy: 750, r: 330, d: 114 },
  },
};

export function initAbout() {
  const sec = $('.about'), board = $('.ab-board');
  const el = {
    circle: $('.ab-circle'), portrait: $('.ab-portrait'), pink: $('.ab-pink'),
    hello: $('.ab-hello'), tb: $('.ab-t1'), tsf: $('.ab-t2'), slash: $('.ab-slash'), work: $('.ab-work'), workHead: $('.ab-work-head'), rows: $$('.ab-logos'), title: $('.ab-title'),
    ring: $('.ab-ring'), photos: $$('.ab-photo'), map: $('.ab-map'),
    out: { sea: $('.ab-out-wa'), ny: $('.ab-out-ny'), sf: $('.ab-out-ca') },
    lab: { sea: $('.ab-lab-sea'), ny: $('.ab-lab-ny'), sf: $('.ab-lab-sf') },
    lines: $$('.ab-line'), dots: $$('.ab-dots'),
  };
  let mode = null, S = 1, drop = 0;
  function fit() {
    const vw = window.innerWidth, vh = window.innerHeight;
    const m = vw <= 820 && vh > vw ? 'mob' : 'desk';
    const B = L[m];
    S = Math.min(vw / B.W, vh / B.H);
    board.style.width = B.W + 'px'; board.style.height = B.H + 'px';
    // pin text/map to the top of the screen and the circle, portrait and ring to the bottom,
    // so taller-than-designed windows don't leave an empty band above the content
    board.style.transform = `translate(${(vw - B.W * S) / 2}px, 0px) scale(${S})`;
    drop = Math.max(0, vh - B.H * S) / S;
    if (m !== mode) {
      mode = m; sec.dataset.mode = m;
      // dotted lines: lay dots along each curve so they can be revealed one by one as you scroll
      el.lines.forEach((p, i) => {
        p.setAttribute('d', B.lines[i]);
        const len = p.getTotalLength(), gap = m === 'mob' ? 9 : 17.4, n = Math.floor(len / gap), g = el.dots[i];
        g.innerHTML = '';
        for (let k = 0; k <= n; k++) {
          const pt = p.getPointAtLength(k * gap), c = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
          c.setAttribute('cx', pt.x.toFixed(1)); c.setAttribute('cy', pt.y.toFixed(1)); c.setAttribute('r', m === 'mob' ? 1.1 : 1.6);
          g.appendChild(c);
        }
        g._n = -1;
      });
      el.map.setAttribute('viewBox', `0 0 ${B.W} ${B.H}`);
      for (const k of ['sea', 'ny', 'sf']) {
        const o = OUT[{ sea: 'wa', ny: 'ny', sf: 'ca' }[k]], [x, y] = B.dots[k], sc = B.outScale;
        Object.assign(el.out[k].style, { left: x - o.dx * sc + 'px', top: y - o.dy * sc + 'px', width: o.w * sc + 'px', height: o.h * sc + 'px' });
        const [lx, ly] = B.labels[k];
        Object.assign(el.lab[k].style, { left: x + lx + 'px', top: y + ly + 'px' });
      }
    }
  }
  fit(); window.addEventListener('resize', fit);

  let lastTitle = -1;
  let update = function (q) {
    const B = L[mode];
    const [cx, cy, d] = kf(q, B.circle);
    Object.assign(el.circle.style, { left: cx - d / 2 + 'px', top: cy + drop - d / 2 + 'px', width: d + 'px', height: d + 'px' });
    const [px, py, pw] = kf(q, B.portrait);
    Object.assign(el.portrait.style, { left: px + 'px', top: py + drop + 'px', width: pw + 'px', height: pw * PORTRAIT_AR + 'px' });
    el.pink.style.opacity = fade(q, 6.3, 6.8);

    // work-history teaser: heading + button, then one row of logos from each side
    const wIn = fade(q, 4.5, 4.9, 5.8, 6.2);
    el.work.style.opacity = wIn; el.work.style.visibility = wIn > 0.01 ? 'visible' : 'hidden';
    el.workHead.style.transform = `translateY(${(1 - fade(q, 4.5, 4.9)) * 30}px)`;
    const W = L[mode].W, r1 = fade(q, 4.6, 5.25), r2 = fade(q, 4.75, 5.4), out = fade(q, 5.8, 6.2);
    el.rows[0].style.transform = `translateX(${-(1 - r1) * W * 1.1 + out * -60}px)`;
    el.rows[1].style.transform = `translateX(${(1 - r2) * W * 1.1 + out * 60}px)`;
    el.work.style.pointerEvents = wIn > 0.9 ? 'auto' : 'none';

    const h = 1 - fade(q, 0.9, 1.5);
    el.hello.style.opacity = h; el.hello.style.transform = `translateY(${(1 - h) * -40}px)`;
    el.hello.style.visibility = h > 0.02 ? 'visible' : 'hidden';

    const a1 = fade(q, 1.4, 2.0, 4.2, 4.6), a2 = fade(q, 2.8, 3.2, 4.2, 4.6);
    el.tb.style.opacity = a1; el.tb.style.transform = `translateY(${(1 - fade(q, 1.4, 2.0)) * 30}px)`;
    el.tsf.style.opacity = a2; el.tsf.style.transform = `translateY(${(1 - fade(q, 2.8, 3.2)) * 20}px)`;
    for (const k of ['sea', 'ny']) { el.out[k].style.opacity = a1; el.lab[k].style.opacity = a1; }
    el.out.sf.style.opacity = a2; el.lab.sf.style.opacity = a2;
    const draw = [fade(q, 1.7, 2.5), fade(q, 3.0, 3.6), fade(q, 3.5, 4.1)];
    const lo = 1 - fade(q, 4.2, 4.6);
    el.dots.forEach((g, i) => {
      const cs = g.children, n = Math.round(draw[i] * cs.length);
      if (n !== g._n) { for (let k = 0; k < cs.length; k++) cs[k].style.display = k < n ? '' : 'none'; g._n = n; }
      g.style.opacity = lo;
    });

    // ring of photos
    const rIn = fade(q, 6.4, 7.0);
    el.ring.style.opacity = rIn; el.ring.style.visibility = rIn > 0.01 ? 'visible' : 'hidden';
    const sIn = fade(q, 6.6, 7.0);
    el.slash.style.opacity = sIn; el.slash.style.transform = `translateY(${(1 - sIn) * 24}px)`;
    lastRIn = rIn;
    renderRing();
  }

  // ---- Slash ring: time-based, independent of scroll ----
  let lastRIn = 0, step = 0, target = 0, from = 0, t0 = 0, spinning = false, timer = null, visible = false, hovering = false;
  const N = TITLES.length, mod = (a, n) => ((a % n) + n) % n;
  function renderRing() {
    const B = L[mode], rIn = lastRIn;
    const active = mod(Math.round(target), N);
    const { cx: rx, r, d: pd } = B.ring, ry = B.ring.cy + drop;
    const R = r * (0.75 + 0.25 * rIn);
    Object.assign(el.ring.style, { left: rx - R + 'px', top: ry - R + 'px', width: R * 2 + 'px', height: R * 2 + 'px' });
    el.photos.forEach((ph, i) => {
      const ang = (-90 + (i - step) * (360 / N)) * Math.PI / 180;
      const x = rx + Math.cos(ang) * R, y = ry + Math.sin(ang) * R;
      const isA = i === active;
      const pop = clamp((rIn - i * 0.04) / 0.6);
      Object.assign(ph.style, { left: x - pd / 2 + 'px', top: y - pd / 2 + 'px', width: pd + 'px', height: pd + 'px', opacity: pop });
      // closeness to the top slot (1 = selected) drives size and scrim continuously, so nothing jumps
      let dd = ((i - step) % N + N) % N; if (dd > N / 2) dd = N - dd;
      const near = clamp(1 - dd);
      ph.style.transform = `scale(${(0.6 + 0.4 * backOut(pop)) * (0.9 + 0.22 * near)})`;
      ph.style.setProperty('--scrim', (1 - near).toFixed(3));
      ph.style.zIndex = near > 0.5 ? 2 : 1;
      ph.classList.toggle('is-active', isA);
      ph.style.pointerEvents = rIn > 0.9 ? 'auto' : 'none';
    });
    if (active !== lastTitle) {
      lastTitle = active;
      el.title.textContent = TITLES[active];
      if (rIn > 0.5) el.title.animate([{ transform: 'translateY(40%)', opacity: 0 }, { transform: 'none', opacity: 1 }], { duration: 420, easing: 'cubic-bezier(.2,1.4,.4,1)' });
    }
  }
  function spinTo(idx) {
    let delta = mod(idx - mod(target, N), N); if (delta > N / 2) delta -= N;
    if (!delta) return;
    from = step; target = Math.round(target) + delta; t0 = performance.now();
    if (!spinning) { spinning = true; requestAnimationFrame(tick); }
    renderRing();
  }
  function tick(now) {
    const t = clamp((now - t0) / SPIN);
    step = from + (target - from) * io(t);
    renderRing();
    if (t < 1) requestAnimationFrame(tick); else { step = target; spinning = false; renderRing(); }
  }
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  function schedule() {
    clearTimeout(timer);
    if (reduced || !visible || lastRIn < 0.99 || hovering) return;
    timer = setTimeout(() => { spinTo(mod(Math.round(target), N) + 1); schedule(); }, DWELL);
  }
  // only run while the ring is on screen
  new IntersectionObserver(([e]) => { visible = e.isIntersecting; schedule(); }, { threshold: 0.25 }).observe(sec);
  el.photos.forEach((ph, i) => {
    ph.setAttribute('role', 'button'); ph.setAttribute('tabindex', '0'); ph.setAttribute('aria-label', TITLES[i]);
    const go = () => { spinTo(i); schedule(); };
    ph.addEventListener('click', go);
    ph.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); go(); } });
  });
  // pause the auto-advance while someone is looking closely at a photo
  el.ring.parentElement.addEventListener('pointerover', e => { if (e.target.closest('.ab-photo')) { hovering = true; clearTimeout(timer); } });
  el.ring.parentElement.addEventListener('pointerout', e => { if (e.target.closest('.ab-photo')) { hovering = false; schedule(); } });
  let wasReady = false;
  const _update = update;
  update = q => { _update(q); const ready = lastRIn >= 0.99; if (ready !== wasReady) { wasReady = ready; schedule(); } };

  return { update, fit, light: q => q < 6.55, end: QT };
}
