import { Stage } from './phone.js';
import { initAbout } from './about.js';
import { initMarquee } from './marquee.js';
initMarquee(document.querySelector('.wave'));
const gsap = window.gsap, ScrollTrigger = window.ScrollTrigger;
gsap.registerPlugin(ScrollTrigger);

const $ = (s, el = document) => el.querySelector(s), $$ = (s, el = document) => [...el.querySelectorAll(s)];
const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));
const lerp = (a, b, t) => a + (b - a) * t;
const ease = t => t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;      // easeInOutCubic
const seg = (p, a, b) => ease(clamp((p - a) / (b - a)));                         // eased 0..1 inside [a,b]
const lin = (p, a, b) => clamp((p - a) / (b - a));
const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;

/* ---------------- screens ---------------- */
const S = 'assets/screens/';
const HERO_DEFAULT = 'wherei-001';
const HOVER = ['saturn-009', 'kyn-019', 'candle-003', 'upclose-012', 'monstro-010', 'honored-020', 'saturn-052', 'abbott-015',
  'transforce-069', 'wherei-009', 'kyn-003', 'saturn-031', 'candle-013', 'honored-018', 'abbott-001', 'trovy-006', 'wherei-001'];
// procession order: phone 0 is the hero phone, last phone becomes the Saturn teaser phone
const PROC = ['wherei-001', 'kyn-019', 'candle-003', 'monstro-010', 'honored-020', 'abbott-015', 'transforce-069', 'saturn-052', 'upclose-012', 'saturn-009'];
// teaser easter egg: tap the phone to flip through that project's screens (first = the teaser's default screen)
const TAP = { saturn: 10, trovy: 3, upclose: 10 };
const SLUGS = ['saturn', 'trovy', 'upclose'];
const tapName = (slug, i) => `tap/${slug}-${String(i + 1).padStart(2, '0')}`;
const tapIdx = [0, 0, 0];
const TEASERS = SLUGS.map(s => tapName(s, 0));

/* ---------------- layout scale ---------------- */
let vw, vh, s, mobile;
function measure() {
  vw = window.innerWidth; vh = window.innerHeight; mobile = vw <= 820;
  s = mobile ? Math.min(vw / 430, vh / 860) : Math.min(vw / 1728, vh / 1117);
  document.documentElement.style.setProperty('--s', Math.max(0.55, s).toFixed(4));
}
measure();

/* ---------------- loader ---------------- */
const loader = $('.loader');
// the flower opens and closes on its own (SVG animation); hold the loader for one full bloom
const loaderTl = gsap.timeline({ paused: true }).to({}, { duration: 1.6 });

/* ---------------- hero letters ---------------- */
$$('.hero-copy .w').forEach(w => {
  w.innerHTML = [...w.textContent].map(c => c === ' ' ? ' ' : `<span class="ch">${c}</span>`).join('');
});

/* ---------------- 3D ---------------- */
const canvas = $('#phones');
let stage, phones = [], tex = {}, ready = false;
try { stage = new Stage(canvas); } catch (e) { console.warn('WebGL unavailable', e); }

async function loadTextures() {
  if (!stage) return;
  const names = [...new Set([HERO_DEFAULT, ...HOVER, ...PROC, ...TEASERS])];
  // load the hero screen first so the page can open fast; rest in parallel
  tex[HERO_DEFAULT] = await stage.load(S + HERO_DEFAULT + '.webp');
  await Promise.all(names.filter(n => !tex[n]).map(async n => { tex[n] = await stage.load(S + n + '.webp'); }));
}

/* ---------------- choreography ----------------
   p runs 0 → T over the pinned stage.
   0–1   hero: phone stands up and rises, words slide away
   1–2   fan: more phones fan out from behind the first
   2–6.5 procession moves left; last phone stops at the teaser slot
   6–6.6 Saturn teaser in    7.4–8.2 → Trovy    9–9.8 → UpClose    10.6+ hold, then page scrolls on */
const T = 11.2, N = PROC.length;
let P = 0, Q = 0, stageLight = false, enter = 0, mouseX = 0, mouseY = 0, hoverTex = null;

function heroPose(ph) {
  if (mobile) return { x: 0, y: -vh * 0.3, z: vh * 0.5, h: vh * 0.5, rx: -50, ry: 0, rz: 0 };
  return { x: 0, y: -vh * 0.27, z: vh * 0.75, h: 860 * s, rx: -56, ry: 0, rz: 0 };
}
function standPose() {
  if (mobile) return { x: 0, y: -vh * 0.04, h: vh * 0.56, rx: 0, ry: 0, rz: 0 };
  return { x: 0, y: (558 - 455) * s, h: 640 * s, rx: 0, ry: 0, rz: 0 };
}
function teaserPose() {
  if (mobile) return { x: 0, y: -vh * 0.31, h: vh * 0.42, rx: 6, ry: -16, rz: 3 };
  return { x: (1256 - 864) * s, y: (558 - 600) * s, h: 680 * s, rx: 6, ry: -20, rz: 4 };
}
const gap = () => mobile ? vw * 0.62 : 460 * s;

function layout(p) {
  const st = standPose(), hp = heroPose(), tp = teaserPose(), G = gap();
  const ph = phones;
  // --- line geometry ---
  const lineX0 = mobile ? -G * 0.9 : -534 * s;                   // where phone 0 sits when the line forms
  const lastStart = lineX0 + (N - 1) * G;
  const stopShift = lastStart - tp.x;                            // shift at which the last phone reaches its slot
  const totalShift = stopShift + (mobile ? vw * 1.4 : 1250 * s); // keep going until the rest exit left
  const shift = totalShift * lin(p, 2.6, 6.4);
  const tUp = seg(p, 0, 1), tFan = seg(p, 1, 1.9), tLine = seg(p, 1.9, 2.7);

  for (let i = 0; i < N; i++) {
    const f = ph[i]; if (!f) continue;
    // fan pose: stacked to the right, receding
    const fx = st.x + i * (mobile ? 18 : 62 * s) * (i < 5 ? 1 : 0.6), fz = -i * 60, fry = -6 - i * 0.5;
    let x, y, h, rx, ry, rz, z = 0, o = 1;
    if (i === 0) {
      x = lerp(hp.x, st.x, tUp); y = lerp(hp.y, st.y, tUp); h = lerp(hp.h, st.h, tUp); rx = lerp(hp.rx, st.rx, tUp); ry = 0; rz = 0;
      z = lerp(hp.z, 0, tUp);
      if (p < 0.05 && !reduced) { ry += mouseX * 6; rx += mouseY * -3; }       // subtle parallax in hero
      // entrance from below
      y -= (1 - enter) * vh * 0.6;
    } else {
      x = st.x; y = st.y; h = st.h; rx = 0; ry = 0; rz = 0; z = -40 - i * 2;
      o = p > 1 ? 1 : 0;
    }
    // fan out
    if (i > 0) { x = lerp(x, fx, tFan); z = lerp(z, fz, tFan); ry = lerp(0, fry, tFan); }
    else { ry = lerp(ry, -4, tFan); }
    // into the line
    const lx = lineX0 + i * G;
    x = lerp(x, lx, tLine); z = lerp(z, 0, tLine); ry = lerp(ry, 0, tLine);
    y = lerp(y, mobile ? -vh * 0.08 : (558 - 668) * s, tLine);   // the procession sits lower, under its headline
    // procession
    if (p > 2.6) {
      let nx = lx - shift;
      if (i === N - 1) nx = Math.max(tp.x, nx);
      x = nx;
    }
    // the last phone becomes the teaser phone
    if (i === N - 1) {
      const t = seg(p, 5.9, 6.6);
      y = lerp(y, tp.y, t); h = lerp(h, tp.h, t); rx = lerp(rx, tp.rx, t); ry = lerp(ry, tp.ry, t); rz = lerp(rz, tp.rz, t);
      if (p > 6.6) {
        // spins between teasers
        const s1 = seg(p, 7.4, 8.2), s2 = seg(p, 9, 9.8);
        ry = tp.ry - 360 * (s1 + s2);
        y = tp.y + Math.sin(Math.PI * s1) * 30 * s + Math.sin(Math.PI * s2) * 30 * s;
        const want = s2 > 0.5 ? 2 : s1 > 0.5 ? 1 : 0;
        showTeaserTex(f, want);
      } else showTeaserTex(f, 0);
      // little "tap" flick when someone taps through screens
      const tk = clamp((performance.now() - tapT) / 420), bump = tk < 1 ? Math.sin(tk * Math.PI) : 0;
      ry -= 9 * bump; h *= 1 - 0.025 * bump;
    }
    // hide off-screen phones
    if (x < -vw / 2 - h) o = 0;
    // drop shadows only on a lone phone: the hero phone until the fan starts, and the teaser phone.
    // Overlapping shadows in the fan/procession stack into a muddy cloud.
    let shd = 0;
    if (i === 0) shd = 1 - seg(p, 1, 1.25);
    if (i === N - 1) shd = seg(p, 6.0, 6.6);
    Object.assign(f, { x, y, z, h, rx, ry, rz, o, sh: shd });
  }

  // --- hero words ---
  const w = seg(p, 0.05, 0.9);
  lines[0].style.transform = `translate3d(${-w * vw * 0.75}px,0,0)`;
  lines[1].style.transform = `translate3d(${w * vw * 0.75}px,0,0)`;
  lines[2].style.transform = `translate3d(${-w * vw * 0.55}px,0,0)`;
  heroCopy.style.opacity = 1 - seg(p, 0.5, 1.1);
  const pc = seg(p, 2.1, 2.7) * (1 - seg(p, 5.4, 5.85));
  procCopy.style.opacity = pc; procCopy.style.transform = `translate3d(0,${(1 - seg(p, 2.1, 2.7)) * 30 - seg(p, 5.4, 5.85) * 30}px,0)`;
  hint.style.opacity = 0.6 * (1 - lin(p, T - 0.35, T));            // stays through the whole pinned sequence

  // --- backgrounds + teasers ---
  const a1 = seg(p, 5.8, 6.5), a2 = seg(p, 7.5, 8.1), a3 = seg(p, 9.1, 9.7);
  const cx = mobile ? '50% 70%' : '73% 52%';
  [[bgs.saturn, a1], [bgs.trovy, a2], [bgs.upclose, a3]].forEach(([el, a]) => {
    el.style.opacity = a > 0 ? 1 : 0; el.style.clipPath = `circle(${(a * 130).toFixed(2)}% at ${cx})`;
  });
  const ts = [seg(p, 6.1, 6.7) * (1 - seg(p, 7.3, 7.7)), seg(p, 7.9, 8.4) * (1 - seg(p, 8.9, 9.3)), seg(p, 9.5, 10)];
  if (phones[N - 1]) placeTap(ts);
  teasers.forEach((t, i) => {
    t.style.opacity = ts[i];
    t.style.transform = `translate3d(0,${(1 - ts[i]) * 40}px,0)`;
    t.style.visibility = ts[i] > 0.02 ? 'visible' : 'hidden';
  });
  // nav colour: light on Saturn + UpClose, dark on hero + Trovy
  const light = (a1 > 0.5 && a2 < 0.5) || a3 > 0.5;
  hint.classList.toggle('is-light', light);
  stageLight = light;
}

function showTeaserTex(f, want) {
  const name = tapName(SLUGS[want], tapIdx[want]), key = want + ':' + tapIdx[want];
  if (f._t !== key && tex[name]) { f.setTexture(tex[name]); f._t = key; }
}

/* ---------------- teaser tap-through ---------------- */
let tapT = -1e9, activeTeaser = -1;
const tapzone = $('.tapzone'), tapHint = $('.tap-hint');
const noHover = matchMedia('(hover: none)').matches;
async function ensureTex(name) { if (!tex[name] && stage) tex[name] = await stage.load(S + name + '.webp'); return tex[name]; }
function preloadNext(i) { const n = TAP[SLUGS[i]]; for (let k = 1; k <= 2; k++) ensureTex(tapName(SLUGS[i], (tapIdx[i] + k) % n)); }
function hintText(i) {
  const n = TAP[SLUGS[i]];
  return tapIdx[i] === 0 && !tapzone._used ? 'Tap for screenshots' : `${tapIdx[i] + 1} / ${n} · tap for next`;
}
tapzone.addEventListener('pointerenter', () => { if (activeTeaser < 0) return; tapHint.classList.add('show'); preloadNext(activeTeaser); });
tapzone.addEventListener('pointerleave', () => { if (!noHover) tapHint.classList.remove('show'); });
tapzone.addEventListener('click', async () => {
  const i = activeTeaser; if (i < 0) return;
  const n = TAP[SLUGS[i]];
  tapIdx[i] = (tapIdx[i] + 1) % n; tapzone._used = true;
  await ensureTex(tapName(SLUGS[i], tapIdx[i]));
  tapT = performance.now(); kick = 30;
  tapHint.textContent = hintText(i); tapHint.classList.add('show');
  preloadNext(i);
});
// place the invisible tap target + hint over the teaser phone each frame
function placeTap(ts) {
  const i = ts.findIndex(v => v > 0.9);
  if (i !== activeTeaser) {
    activeTeaser = i;
    if (i >= 0) { tapHint.textContent = hintText(i); tapHint.classList.toggle('is-dark', i === 1); }
    tapHint.classList.toggle('show', i >= 0 && noHover);
  }
  tapzone.style.display = i >= 0 && stage ? 'block' : 'none';
  if (i < 0 || !stage) { tapHint.classList.remove('show'); return; }
  const r = stage.screenRect(phones[N - 1]);
  Object.assign(tapzone.style, { left: r.x + 'px', top: r.y + 'px', width: r.w + 'px', height: r.h + 'px' });
  Object.assign(tapHint.style, { left: r.x + r.w / 2 + 'px', top: r.y + r.h + (mobile ? 10 : 28) + 'px' });
}

/* ---------------- DOM refs ---------------- */
const nav = $('.nav'), procCopy = $('.proc-copy'), heroCopy = $('.hero-copy'), lines = $$('.hero-copy .line'), hint = $('.scroll-hint');
const teasers = $$('.teaser'), bgs = { saturn: $('.bg--saturn'), trovy: $('.bg--trovy'), upclose: $('.bg--upclose') };

/* ---------------- hover swaps the hero phone screen ---------------- */
$$('.hero-copy .ch').forEach((c, i) => c.addEventListener('mouseenter', () => {
  if (P > 0.15 || !phones[0]) return;
  const t = tex[HOVER[i % HOVER.length]]; if (!t) return;
  phones[0].setTexture(t); hoverTex = t; kick = 3;
  gsap.fromTo(phones[0], { h: phones[0].h * 0.97 }, { h: phones[0].h, duration: .35, ease: 'back.out(3)' });
}));
window.addEventListener('pointermove', e => { mouseX = e.clientX / vw - 0.5; mouseY = e.clientY / vh - 0.5; }, { passive: true });

/* ---------------- headshot pop-in ---------------- */
function heroIntro() {
  const hs = $('.hs'), img = $('.hs img');
  const full = getComputedStyle(hs).width;
  gsap.set(hs, { width: 0 }); gsap.set(img, { scale: 0 });
  gsap.timeline({ delay: .15 })
    .to(hs, { width: full, duration: .7, ease: 'back.out(1.6)', clearProps: 'width' })
    .to(img, { scale: 1, duration: .6, ease: 'back.out(2.2)' }, '-=.55')
    .to({ v: 0 }, { v: 1, duration: 1.1, ease: 'power3.out', onUpdate() { enter = this.targets()[0].v; } }, .1);
}

/* ---------------- scroll ---------------- */
let lenis, stageST, aboutST;
const about = initAbout();
const abHint = document.querySelector('.ab-hint');
function setupScroll() {
  if (window.Lenis && !reduced) {
    lenis = new window.Lenis({ lerp: 0.1, wheelMultiplier: 0.9 });
    lenis.on('scroll', ScrollTrigger.update);
    gsap.ticker.add(t => lenis.raf(t * 1000)); gsap.ticker.lagSmoothing(0);
  }
  stageST = ScrollTrigger.create({
    trigger: '.stage', start: 'top top', end: () => '+=' + Math.round(T * vh * 0.85), pin: true, scrub: true,
    onUpdate: self => { P = self.progress * T; },
  });
  aboutST = ScrollTrigger.create({
    trigger: '.about', start: 'top top', end: () => '+=' + Math.round(about.end * vh * 0.8), pin: true, scrub: true,
    onUpdate: self => { Q = self.progress * about.end; },
  });
  window.__aboutST = aboutST;
  // "About Me" button jumps to the hometown chapter of the sequence
  document.querySelector('.ab-btn').addEventListener('click', e => {
    e.preventDefault();
    const y = aboutST.start + (aboutST.end - aboutST.start) * (2.3 / about.end);
    lenis ? lenis.scrollTo(y, { duration: 1.6 }) : window.scrollTo({ top: y, behavior: 'smooth' });
  });
  // nav "About me" (and /#about from other pages) lands on the start of the About section
  const toAbout = (instant) => {
    const y = aboutST.start + 2;
    lenis && lenis.resize && lenis.resize();
    if (instant) { lenis ? lenis.scrollTo(y, { immediate: true }) : window.scrollTo(0, y); }
    else lenis ? lenis.scrollTo(y, { duration: 1.6 }) : window.scrollTo({ top: y, behavior: 'smooth' });
  };
  document.querySelectorAll('a[data-about]').forEach(a => a.addEventListener('click', e => {
    e.preventDefault(); document.querySelector('.sheet')?.classList.remove('open'); toAbout(false);
  }));
  window.__toAbout = toAbout;
  // other in-page jumps (Anecdotes)
  const toSection = (id, instant) => {
    const el = document.getElementById(id); if (!el) return;
    lenis && lenis.resize && lenis.resize();
    const y = el.getBoundingClientRect().top + window.scrollY;
    if (instant) { lenis ? lenis.scrollTo(y, { immediate: true }) : window.scrollTo(0, y); }
    else lenis ? lenis.scrollTo(y, { duration: 1.6 }) : window.scrollTo({ top: y, behavior: 'smooth' });
  };
  window.__toSection = toSection;
  document.querySelectorAll('a[data-jump]').forEach(a => a.addEventListener('click', e => {
    e.preventDefault(); document.querySelector('.sheet')?.classList.remove('open'); toSection(a.dataset.jump, false);
  }));
}

/* ---------------- loop ---------------- */
// only re-render when something moved (keeps laptops cool when the page is idle)
let lastKey = '', kick = 0, lastQ = -1;
export const invalidate = () => { kick = 3; };
function frame() {
  const k = [P.toFixed(4), performance.now() - tapT < 500 ? performance.now() : 0, enter.toFixed(3), P < 0.05 ? mouseX.toFixed(3) + mouseY.toFixed(3) : '', phones[0] && phones[0].h.toFixed(1), vw, vh].join();
  if (k !== lastKey || kick > 0) { layout(P); if (stage) stage.render(); lastKey = k; kick = Math.max(0, kick - 1); }
  if (Q !== lastQ) { about.update(Q); lastQ = Q; abHint.style.opacity = 0.6 * (1 - Math.min(1, Math.max(0, (Q - about.end + 0.4) / 0.4))); }
  // nav colour: whichever pinned section owns the screen decides
  const ap = aboutST ? aboutST.progress : 0;
  const light = ap >= 1 ? false : (ap > 0 ? about.light(Q) : stageLight);
  nav.classList.toggle('nav--light', light);
  requestAnimationFrame(frame);
}

window.addEventListener('resize', () => { kick = 3; lastQ = -1; measure(); ScrollTrigger.refresh(); stage && stage.resize(); });

/* ---------------- boot ---------------- */
(async function boot() {
  window.scrollTo(0, 0);
  loaderTl.play();
  const minTime = new Promise(r => setTimeout(r, reduced ? 200 : 1500));
  const fonts = document.fonts ? document.fonts.ready : Promise.resolve();
  await Promise.all([loadTextures(), fonts, minTime]);
  if (stage) {
    for (let i = 0; i < N; i++) phones.push(stage.add(tex[PROC[i]]));
    phones[0].setTexture(tex[HERO_DEFAULT]);
  } else {
    document.body.classList.add('no-webgl');
  }
  ready = true;
  setupScroll();
  layout(0); stage && stage.render();
  if (loaderTl.progress() < 1) await new Promise(r => loaderTl.eventCallback('onComplete', r));
  loader.classList.add('done');
  heroIntro();
  if (location.hash === '#about' || location.hash === '#anecdotes') {
    const id = location.hash.slice(1);
    history.replaceState(null, '', location.pathname + location.search);
    ScrollTrigger.refresh();
    requestAnimationFrame(() => id === 'about' ? window.__toAbout(true) : window.__toSection(id, true));
  }
  requestAnimationFrame(frame);
})();

/* ---------------- anecdote videos: play only while on screen ---------------- */
document.querySelectorAll('video[data-autoplay]').forEach(v => {
  if (reduced) return;
  new IntersectionObserver(([en]) => {
    if (en.isIntersecting) { if (v.preload === 'none') v.preload = 'auto'; v.play().catch(() => {}); } else v.pause();
  }, { threshold: 0.25 }).observe(v);
});

/* links to case studies that aren't written yet do nothing */
document.addEventListener('click', e => { if (e.target.closest('a[data-dud]')) e.preventDefault(); });

/* ---------------- mobile menu ---------------- */
const sheet = $('.sheet');
$('.burger')?.addEventListener('click', () => sheet.classList.add('open'));
$('.sheet-close')?.addEventListener('click', () => sheet.classList.remove('open'));
