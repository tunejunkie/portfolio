// Case study deck. Two ways to read it (toggle at the top, remembered per browser):
//  • Scroll mode — scrolling steps through the slides with transitions (snaps to each step); the footer follows.
//  • Slide mode  — a presentation: ←/→, space, PageUp/PageDown, Home/End, the on-screen buttons, or one
//                  trackpad/wheel gesture per step. The page itself doesn't scroll.
// A slide can have several steps: it stays on screen and the 3D phone spins to the next screen.
// Phones / narrow windows get a plain stacked page instead (.is-stack).
import { Stage } from './phone.js';
import * as THREE from 'three';

const $ = (s, el = document) => el.querySelector(s), $$ = (s, el = document) => [...el.querySelectorAll(s)];
const body = document.body, base = body.dataset.base || '';
const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
const D = reduced ? 0.01 : 1;                                     // duration multiplier
const BW = 1728, BH = 1117;                                       // art board (Figma frame)

const deck = $('.cs-deck'), track = $('.cs-track'), board = $('.cs-board');
const slides = $$('.cs-slide');
const intro = $('.cs-intro'), introBoard = $('.cs-intro-board');
// steps = [slideIndex, sub]. Scroll mode opens with the normal-scrolling intro, so the title slide is slides-mode only.
let steps = [], N = 0;
function buildSteps() {
  steps = [];
  slides.forEach((s, i) => {
    if (s.dataset.key === 'hero' && mode === 'scroll') return;
    for (let k = 0; k < +s.dataset.steps; k++) steps.push([i, k]);
  });
  N = steps.length;
}
const firstStep = i => steps.findIndex(([s]) => s === i);

let mode = 'scroll', stack = false, cur = -1, S = 1, U = innerHeight, lenis = null;
try { mode = localStorage.getItem('cs-mode') === 'slides' ? 'slides' : 'scroll'; } catch (e) {}
const qp = new URLSearchParams(location.search).get('mode'); if (qp === 'slides' || qp === 'scroll') mode = qp;

/* ---------------- background ---------------- */
// background: one gradient pinned to the viewport (css), the same behind every slide

/* ---------------- 3D phones ---------------- */
let stage = null;
{ const glc = $('.cs-gl'); if (glc && $('.cs-phone-slot')) { try { stage = new Stage(glc); } catch (e) { body.classList.add('no-gl'); } } }   // only pages/slides that ask for the 3D phone get one
const texCache = {};
function grayTex(label) {
  const c = document.createElement('canvas'); c.width = 375 * 2; c.height = 812 * 2;
  const g = c.getContext('2d'); g.fillStyle = '#b9b9bd'; g.fillRect(0, 0, c.width, c.height);
  g.fillStyle = '#5a5a63'; g.font = '600 44px "Plus Jakarta Sans", sans-serif'; g.textAlign = 'center';
  g.fillText(label, c.width / 2, c.height / 2);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t;
}
async function tex(src, i = 0) {
  const key = src || 'gray' + i;
  if (!texCache[key]) texCache[key] = src ? stage.load(base + src) : Promise.resolve(grayTex(`Screen ${i + 1} needed`));
  return texCache[key];
}
// one hero phone (hunch/build slides) + four for the gallery row
const REST = { rx: 6, ry: -24, rz: 3 };
const ph = { main: null, row: [] };
const st = { main: { x: 0, y: 0, h: 600, rx: 0, ry: 0, rz: 0, o: 0 }, row: [0, 1, 2, 3].map(() => ({ x: 0, y: 0, h: 600, rx: 0, ry: 0, rz: 0, o: 0 })) };
let glDirty = true;
if (stage) {
  ph.main = stage.add(null); ph.main.o = 0;
  for (let i = 0; i < 4; i++) { const p = stage.add(null); p.o = 0; ph.row.push(p); tex(null, i).then(t => p.setTexture(t)); }
}
function slotPose(slot, scale = 0.94) {
  const r = slot.getBoundingClientRect(), d = deck.getBoundingClientRect();
  return { x: r.left - d.left + r.width / 2 - d.width / 2, y: d.height / 2 - (r.top - d.top + r.height / 2), h: r.height * scale };
}
function syncGL() {
  if (!stage || stack) return;
  const apply = (p, s) => Object.assign(p, s, { sh: 0.9 });
  apply(ph.main, st.main); ph.row.forEach((p, i) => apply(p, st.row[i]));
  stage.render(); glDirty = false;
}
gsap.ticker.add(() => { if (glDirty) syncGL(); });
const tw = (o, v) => gsap.to(o, { ...v, onUpdate: () => { glDirty = true; } });

let mainSlide = -1, mainSub = -1;
async function phoneTo(si, sub, dir, instant) {
  if (!stage) return;
  const slide = slides[si], slot = $('.cs-phone-slot:not(.cs-phone-slot--row)', slide);
  const m = st.main;
  if (!slot) {                                                    // leave: tip back and shrink away
    if (mainSlide >= 0) { gsap.killTweensOf(m); tw(m, { o: 0, h: m.h * 0.7, ry: REST.ry + 50 * dir, y: m.y - 80 * dir, duration: 0.5 * D, ease: 'power2.in' }); }
    mainSlide = -1; mainSub = -1; return;
  }
  const screens = slot.dataset.screens.split(',');
  const t = await tex(screens[sub] || null, sub);
  const pose = slotPose(slot);
  gsap.killTweensOf(m);
  if (instant || mainSlide < 0) {                                 // arrive: rise in with a quarter turn
    ph.main.setTexture(t);
    Object.assign(m, { ...pose, ...REST, ry: REST.ry - 70 * dir, y: pose.y - 140 * dir, o: 0, h: pose.h * 0.9 });
    tw(m, { ...pose, ...REST, o: 1, duration: (instant ? 0.01 : 1.1) * D, delay: instant ? 0 : 0.25 * D, ease: 'power3.out' });
  } else {                                                        // same phone, new screen: spin 360 and swap at edge-on
    const from = REST.ry, to = REST.ry - 360 * dir; let swapped = false;
    m.ry = from;
    gsap.to(m, { ...pose, rx: REST.rx, rz: REST.rz, o: 1, duration: 1.0 * D, ease: 'power2.inOut', overwrite: 'auto',
      onUpdate() { glDirty = true; m.ry = from + (to - from) * this.ratio; if (!swapped && this.ratio > 0.5) { ph.main.setTexture(t); swapped = true; } },
      onComplete() { m.ry = REST.ry; glDirty = true; } });
    const hop = { v: 0 }; gsap.to(hop, { v: 1, duration: 1.0 * D, ease: 'none', onUpdate() { m.y = pose.y + Math.sin(Math.PI * hop.v) * 36; glDirty = true; } });
  }
  mainSlide = si; mainSub = sub;
}
let rowOn = false;
function rowTo(si, dir, instant) {
  if (!stage) return;
  const slots = $$('.cs-phone-slot--row', slides[si]);
  if (!slots.length) {
    if (rowOn) st.row.forEach((s, i) => { gsap.killTweensOf(s); tw(s, { o: 0, y: s.y - 80 * dir, h: s.h * 0.8, duration: 0.45 * D, delay: i * 0.04 * D, ease: 'power2.in' }); });
    rowOn = false; return;
  }
  slots.forEach((slot, i) => {
    const pose = slotPose(slot, 0.9), s = st.row[i];
    gsap.killTweensOf(s);
    Object.assign(s, { ...pose, rx: 4, ry: -18, rz: 2, y: pose.y - 160 * dir, o: 0, h: pose.h * 0.9 });
    tw(s, { ...pose, o: 1, duration: (instant ? 0.01 : 1.0) * D, delay: instant ? 0 : (0.3 + i * 0.09) * D, ease: 'power3.out' });
  });
  rowOn = true;
}
function placePhones() {                                          // after a resize: snap phones to their slots
  if (!stage || stack) return;
  if (mainSlide >= 0) { const slot = $('.cs-phone-slot:not(.cs-phone-slot--row)', slides[mainSlide]); Object.assign(st.main, slotPose(slot)); }
  if (rowOn) $$('.cs-phone-slot--row', slides[steps[cur][0]]).forEach((slot, i) => Object.assign(st.row[i], slotPose(slot, 0.9)));
  glDirty = true;
}

/* ---------------- layout ---------------- */
function layout() {
  stack = innerWidth <= 820 || (innerWidth < 1000 && innerHeight > innerWidth);
  body.classList.toggle('is-stack', stack);
  body.classList.toggle('is-slides', !stack && mode === 'slides');
  body.classList.toggle('is-scroll', stack || mode === 'scroll');
  if (stack) { document.documentElement.style.setProperty('--ps-stack', Math.min(1, (innerWidth - 32) / 399).toFixed(4)); stackLayout(); return; }
  const vw = deck.clientWidth || innerWidth, vh = deck.clientHeight || innerHeight;
  S = Math.min(vw / BW, vh / BH);
  const tx = (vw - BW * S) / 2, ty = Math.max(0, (vh - BH * S) / 2);
  board.style.transform = `translate(${tx}px,${ty}px) scale(${S})`;
  // while reading, the slim case-study bar (logo · chapters · Scroll/Slides) replaces the site nav; slides start under it
  const barH = $('.cs-bar').offsetHeight || 81;
  const top = Math.max(60, (barH + 36 - ty) / S), h = BH - top - (mode === 'slides' ? 128 : 60);
  board.style.setProperty('--top', top + 'px'); board.style.setProperty('--h', h + 'px');
  board.style.setProperty('--ps', Math.min(1.15, (h - 40) / 836).toFixed(4));   // live Now-tab prototype phone
  // intro (scroll mode): same scale and margins as the slides, but in the normal page flow
  if (intro) {
    introBoard.style.transform = `translate(${tx}px,0) scale(${S})`;
    introBoard.style.paddingTop = Math.max(60, (20 + 96 + 28 - ty) / S) + 80 + 'px';   // under the full site nav, plus breathing room above the logo + summary
    intro.style.height = mode === 'scroll' ? Math.ceil(introBoard.offsetHeight * S) + 'px' : '0px';
  }
  // shrink any slide whose content is taller than the space under the HUD
  slides.forEach(s => {
    const f = $('.cs-fit', s); f.style.setProperty('--k', 1);
    const k = Math.min(1, h / f.offsetHeight); f.style.setProperty('--k', k.toFixed(4));
  });
  U = innerHeight;
  track.style.height = mode === 'scroll' ? ((N - 1) * U + innerHeight) + 'px' : innerHeight + 'px';
  if (stage) stage.resize();
}

/* ---------------- slide lifecycle: scenes listen for cs:enter / cs:leave ---------------- */
const fire = (s, t) => { if (s) s.dispatchEvent(new CustomEvent('cs:' + t)); };

/* ---------------- problems slide: the Trojan horse ----------------
   Tap the horse: students climb down its ladder and march off to the right, six of them saying a complaint
   (the bubble rides along above them, then fades). As their numbers grow the horse rolls back to the left,
   and when the last one is out it rolls after them, back to where it started. */
const army = (() => {
  const el = $('.cs-army--men'), btn = $('.cs-horse-btn'), hint = $('.cs-horse-hint'), horse = $('.cs-trojan .cs-horse');
  if (!el) return;
  const slide = el.closest('.cs-slide');
  const src = el.dataset.student, quotes = el.dataset.quotes.split('|');
  const SPEED = 118, GAP = 0.34, COUNT = 22, W = 1760, FEET = 376, LADDER = 868, ROLL = -300;
  const SPEAKERS = [1, 4, 7, 10, 13, 16];
  const LIFT = [0, 80, 160, 40, 120, 20];
  let running = false, raf = 0, men = [], says = [], t0 = 0, last = 0, spawned = 0, shift = 0, vel = 0;
  const spawn = i => {
    const img = new Image(); img.src = src; img.alt = ''; img.style.animationDelay = (-Math.random() * 0.5).toFixed(2) + 's';
    el.appendChild(img); const m = { img, x: LADDER + shift - 14, i, born: performance.now() };
    img.style.opacity = 0; img.style.transform = `translateX(${m.x}px)`; men.push(m); return m;
  };
  const place = s => { s.b.style.left = (s.m.x - 14) + 'px'; s.b.style.top = (FEET - s.b.offsetHeight - 14 - s.lift) + 'px'; };
  function say(m, text) {
    const k = SPEAKERS.indexOf(m.i), lift = LIFT[k % LIFT.length];
    const b = document.createElement('p'); b.className = 'cs-say'; b.textContent = text; b.style.setProperty('--lift', lift + 'px');
    el.appendChild(b); const s = { m, b, lift }; m.said = true; says.push(s); place(s);
    gsap.fromTo(b, { autoAlpha: 0, scale: 0.6, transformOrigin: '29px 100%' }, { autoAlpha: 1, scale: 1, duration: 0.45, ease: 'back.out(2.2)' });
    gsap.to(b, { autoAlpha: 0, y: -16, duration: 0.7, delay: 2.8, ease: 'power1.in', onComplete() { b.remove(); says = says.filter(x => x !== s); } });
  }
  function frame(now) {
    if (!running) return;
    const t = (now - t0) / 1000, dt = Math.min(0.05, (now - (last || now)) / 1000); last = now;
    if (t > 0 && spawned < COUNT && t > spawned * GAP) spawn(spawned++);
    // the horse rolls back as the line grows; once the last student is out, it follows them back to where it started
    const out = spawned === COUNT && t > COUNT * GAP + 0.7;
    if (out) {  // walk after them: ease up to marching speed, ease in to a stop at the start
      vel = Math.min(SPEED, vel + SPEED * 1.5 * dt);
      shift = Math.min(0, shift + Math.min(vel, Math.max(30, -shift * 2.2)) * dt);
    } else {
      const target = ROLL * Math.min(1, spawned / COUNT);
      shift += (target - shift) * Math.min(1, dt * 2.2);
    }
    horse.style.transform = `translateX(${shift.toFixed(1)}px)`;
    for (const m of men) {
      m.x += SPEED * dt; m.img.style.transform = `translateX(${m.x.toFixed(1)}px)`;
      m.img.style.opacity = Math.min(1, (now - m.born) / 260);
      const k = SPEAKERS.indexOf(m.i);
      if (k >= 0 && !m.said && m.x > LADDER + shift + 70) say(m, quotes[k % quotes.length]);
    }
    men = men.filter(m => (m.x < W) || (m.img.remove(), false));
    says.forEach(place);
    if (spawned === COUNT && !men.length && !says.length) { finish(); return; }
    raf = requestAnimationFrame(frame);
  }
  function finish() { running = false; gsap.to(horse, { x: 0, duration: 1.4, ease: 'power2.inOut', onUpdate() { shift = gsap.getProperty(horse, 'x'); } }); hint.classList.remove('off'); horse.classList.add('nudge'); }
  function go() {
    if (running) return;
    stop(); running = true; hint.classList.add('off'); horse.classList.remove('nudge');
    if (reduced) { for (let i = 0; i < 10; i++) { const m = spawn(i); m.x += 40 + i * 70; m.img.style.opacity = 1; m.img.style.transform = `translateX(${m.x}px)`; } running = false; return; }
    t0 = performance.now() + 250; last = 0; spawned = 0; vel = 0;
    raf = requestAnimationFrame(frame);
  }
  function stop() {
    running = false; cancelAnimationFrame(raf);
    gsap.killTweensOf(horse); shift = 0; gsap.set(horse, { x: 0, clearProps: 'transform' });
    says.forEach(s => { gsap.killTweensOf(s.b); s.b.remove(); }); says = [];
    men.forEach(m => m.img.remove()); men = [];
  }
  btn.addEventListener('click', go);
  slide.addEventListener('cs:enter', () => { stop(); hint.classList.remove('off'); horse.classList.add('nudge'); });
  slide.addEventListener('cs:leave', () => { stop(); horse.classList.remove('nudge'); });
})();

/* ---------------- media: videos play only while their slide is up; prototypes load when first needed ---------------- */
slides.forEach((s, i) => {
  const vids = $$('video[data-src]', s), frames = $$('iframe[data-src]', s);
  if (!vids.length && !frames.length) return;
  const load = () => { vids.forEach(v => { if (!v.src) v.src = v.canPlayType('video/mp4; codecs="avc1.42E01E"') ? v.dataset.src : v.dataset.src.replace(/\.mp4$/, '.webm'); }); frames.forEach(f => { if (!f.src) f.src = f.dataset.src; }); };
  s.addEventListener('cs:enter', () => { load(); vids.forEach(v => { v.currentTime = 0; v.play().catch(() => {}); }); });
  s.addEventListener('cs:leave', () => vids.forEach(v => v.pause()));
  s.addEventListener('cs:near', load);
});
// warm up the next slide's media so it's ready when you arrive
const near = i => { if (slides[i]) fire(slides[i], 'near'); };

/* ---------------- prototypes with a row of state chips beside them ---------------- */
$$('.cs-proto2').forEach(box => {
  const frame = $('iframe', box), btns = $$('.cs-chip', box);
  let ready = false, pending = null;
  const mark = n => btns.forEach(b => { const on = +b.dataset.state === n; b.classList.toggle('is-on', on); b.setAttribute('aria-pressed', on); });
  const send = n => frame.contentWindow.postMessage({ nowState: n }, '*');
  btns.forEach(b => b.addEventListener('click', () => {
    const n = +b.dataset.state; mark(n);
    if (ready) send(n); else { pending = n; if (!frame.src) frame.src = frame.dataset.src; }
  }));
  addEventListener('message', e => {
    if (e.source !== frame.contentWindow || !e.data) return;
    if (e.data.nowReady) { ready = true; if (pending) { send(pending); pending = null; } }
    else if (e.data.nowStateChanged && !pending) mark(e.data.nowStateChanged);
  });
});

/* ---------------- sticky stacks: tap a stack and its notes burst out into a row ---------------- */
(() => {
  const box = $('.cs-sticky'); if (!box) return;
  const slide = box.closest('.cs-slide'), stacks = $$('.cs-stack', box), tabs = $$('.cs-stab', box);
  const sets = Object.fromEntries($$('.cs-notes', box).map(n => [n.dataset.set, n]));
  let cur = null;
  const centre = el => { const r = el.getBoundingClientRect(), b = box.getBoundingClientRect(), k = b.width / box.offsetWidth; return { x: (r.left - b.left + r.width / 2) / k, y: (r.top - b.top + r.height / 2) / k }; };
  function show(k, from) {
    if (stack) return;
    box.classList.add('open'); tabs.forEach(t => t.classList.toggle('on', t.dataset.set === k));
    Object.entries(sets).forEach(([kk, n]) => { if (kk !== k) gsap.to($$('.cs-note', n), { autoAlpha: 0, y: 20, duration: 0.25, stagger: 0.02, overwrite: true }); });
    const notes = $$('.cs-note', sets[k]), o = centre(from);
    gsap.set(notes, { x: 0, y: 0, rotation: 0, autoAlpha: 0 });
    notes.forEach((n, i) => {
      const c = centre(n);
      gsap.fromTo(n, { x: o.x - c.x, y: o.y - c.y, rotation: (i % 2 ? 7 : -7) * (1 + i * 0.2), scale: 0.6, autoAlpha: 1 },
        { x: 0, y: 0, rotation: (i % 2 ? 1.2 : -1.2), scale: 1, duration: 0.75, delay: 0.05 + i * 0.06, ease: 'back.out(1.3)', overwrite: true });
    });
    cur = k;
  }
  stacks.forEach(s => s.addEventListener('click', () => show(s.dataset.set, s)));
  tabs.forEach(t => t.addEventListener('click', () => { if (t.dataset.set !== cur) show(t.dataset.set, t); }));
  slide.addEventListener('cs:enter', () => { if (stack) return; box.classList.remove('open'); gsap.set($$('.cs-note', box), { autoAlpha: 0 }); cur = null; });
})();

// embedded live builds (iframe[data-src]) load the first time their slide is shown
function loadFrames(sl) { $$('iframe[data-src]', sl).forEach(f => { if (!f.src) f.src = f.dataset.src; }); }

/* ---------------- stepping ---------------- */
const outlineBtns = $$('.cs-outline button');
function setSub(slide, sub, dir, instant) {
  const key = slide.dataset.key, d = instant ? 0.01 : D;
  $$('[data-sub]', slide).forEach(c => {
    const on = +c.dataset.sub === sub;
    gsap.to(c, { autoAlpha: on ? 1 : 0, y: on ? 0 : (+c.dataset.sub < sub ? -24 : 24), duration: 0.5 * d, delay: on ? 0.25 * d : 0, ease: on ? 'power3.out' : 'power2.in' });
  });
}
function goTo(i, instant = false) {
  i = Math.max(0, Math.min(N - 1, i));
  if (i === cur) return;
  const dir = i > cur ? 1 : -1, [si, sub] = steps[i], prev = cur >= 0 ? steps[cur] : null;
  const changeSlide = !prev || prev[0] !== si;
  const sl = slides[si];
  if (changeSlide) {
    if (prev) {
      const old = slides[prev[0]];
      gsap.killTweensOf(old);
      gsap.to(old, { autoAlpha: 0, y: -50 * dir, duration: (instant ? 0.01 : 0.45) * D, ease: 'power2.in', onComplete: () => old.classList.remove('on') });
      fire(old, 'leave');
    }
    sl.classList.add('on'); gsap.killTweensOf(sl); fire(sl, 'enter'); near(si + 1);
    gsap.set(sl, { autoAlpha: 1, y: 0 });
    loadFrames(sl);
    const parts = $$('[data-a], .cs-pill', sl);
    gsap.fromTo(parts, { autoAlpha: 0, y: 56 * dir }, { autoAlpha: 1, y: 0, duration: (instant ? 0.01 : 0.85) * D, delay: instant ? 0 : 0.3 * D, stagger: instant ? 0 : 0.06 * D, ease: 'power3.out', overwrite: true });
    // jump this slide's own sub-state into place, then animate to the target sub
    setSub(sl, dir > 0 ? 0 : sub, dir, true);
    if (sub && dir > 0) setSub(sl, sub, dir, instant); else if (dir < 0) setSub(sl, sub, dir, true);
  } else setSub(sl, sub, dir, instant);
  phoneTo(si, sub, dir, instant);
  if (changeSlide) rowTo(si, dir, instant);
  cur = i;
  updateBar();
  outlineBtns.forEach(b => b.classList.toggle('on', +b.dataset.chapter === +sl.dataset.chapter));
  $('.cs-count').textContent = `${i + 1} / ${N}`;
  $('.cs-prev').disabled = i === 0; $('.cs-next').disabled = i === N - 1;
  $('.cs-progress i').style.width = (i / (N - 1) * 100) + '%';
  $('.cs-hint').classList.toggle('off', i > 0);
}

/* ---------------- scroll mode ---------------- */
let snapT = 0, programmatic = false;
const trackTop = () => track.offsetTop;
function hideAll() { slides.forEach(s => { gsap.killTweensOf(s); gsap.set(s, { autoAlpha: 0 }); if (s.classList.contains('on')) fire(s, 'leave'); s.classList.remove('on'); }); phoneTo(0, 0, -1, true); rowTo(0, -1, true); cur = -1; }
function scrollToStep(i, immediate) {
  i = Math.min(N - 1, i);
  const y = i < 0 ? 0 : trackTop() + i * U;
  if (lenis) lenis.scrollTo(y, { immediate, duration: 0.9, lock: false });
  else window.scrollTo({ top: y, behavior: immediate ? 'auto' : 'smooth' });
}
let lastY = 0, lastDir = 1;
function onScroll() {
  if (stack || mode !== 'scroll') return;
  if (scrollY !== lastY) { lastDir = scrollY > lastY ? 1 : -1; lastY = scrollY; }
  const pos = (scrollY - trackTop()) / U;
  // the first slide plays in as the deck arrives from under the intro, and resets if you scroll back up
  if (pos > -0.45 && pos <= N - 1 + 0.01) goTo(Math.max(0, Math.round(pos)));
  else if (pos < -0.7 && cur === 0) hideAll();
  clearTimeout(snapT);
  snapT = setTimeout(() => {                                       // settle onto the nearest step
    // a small nudge past the current step is enough to move on (one wheel notch shouldn't bounce back)
    const p = (scrollY - trackTop()) / U;
    if (p <= -0.3 || p >= N - 1 || Math.abs(p - Math.round(p)) <= 0.02) return;
    scrollToStep(Math.max(0, lastDir > 0 ? Math.ceil(p - 0.04) : Math.floor(p + 0.04)));
  }, 160);
}
if (window.Lenis && !reduced) {
  lenis = new window.Lenis({ lerp: 0.1, wheelMultiplier: 0.9 });
  gsap.ticker.add(t => lenis.raf(t * 1000)); gsap.ticker.lagSmoothing(0);
  lenis.on('scroll', onScroll);
} else addEventListener('scroll', onScroll, { passive: true });

/* ---------------- slide mode ---------------- */
let wheelLock = 0;
addEventListener('wheel', e => {
  if (stack || mode !== 'slides') return;
  e.preventDefault();
  const now = performance.now();
  if (now < wheelLock || Math.abs(e.deltaY) + Math.abs(e.deltaX) < 8) return;
  wheelLock = now + 900;
  goTo(cur + ((e.deltaY || e.deltaX) > 0 ? 1 : -1));
}, { passive: false });
let tx0 = null, ty0 = null;
addEventListener('touchstart', e => { tx0 = e.touches[0].clientX; ty0 = e.touches[0].clientY; }, { passive: true });
addEventListener('touchend', e => {
  if (stack || mode !== 'slides' || tx0 === null) return;
  const dx = e.changedTouches[0].clientX - tx0, dy = e.changedTouches[0].clientY - ty0;
  if (Math.max(Math.abs(dx), Math.abs(dy)) > 40) goTo(cur + ((Math.abs(dx) > Math.abs(dy) ? -dx : -dy) > 0 ? 1 : -1));
  tx0 = null;
});
addEventListener('keydown', e => {
  if (stack || e.metaKey || e.ctrlKey || e.altKey) return;
  if (e.target.closest('input,textarea,select,[contenteditable]')) return;
  const next = ['ArrowRight', 'ArrowDown', 'PageDown', ' ', 'Enter'].includes(e.key) && !(e.key === ' ' && e.shiftKey);
  const prev = ['ArrowLeft', 'ArrowUp', 'PageUp'].includes(e.key) || (e.key === ' ' && e.shiftKey);
  if (e.key === 'Escape' && mode === 'slides') { setMode('scroll'); return; }
  let to = null;
  if (next) to = cur + 1; else if (prev) to = cur - 1; else if (e.key === 'Home') to = 0; else if (e.key === 'End') to = N - 1;
  if (to === null) return;
  if ((e.key === 'Enter' || e.key === ' ') && e.target.closest('a,button:not(.cs-mode button)')) return;
  if (mode === 'scroll') {
    const pos = (scrollY - trackTop()) / U;
    if (pos > N - 1 + 0.01 || (pos < -0.5 && to < 0)) return;      // in the footer / intro: let the page scroll
    if (pos < -0.5 && prev) return;
    e.preventDefault(); scrollToStep(to);
  } else { e.preventDefault(); goTo(to); }
});
$('.cs-prev').addEventListener('click', () => goTo(cur - 1));
$('.cs-next').addEventListener('click', () => goTo(cur + 1));
outlineBtns.forEach(b => b.addEventListener('click', () => {
  const k = +b.dataset.chapter;
  const to = steps.findIndex(([si]) => +slides[si].dataset.chapter === k);
  mode === 'scroll' ? scrollToStep(to) : goTo(to);
}));

/* ---------------- mode toggle ---------------- */
const modeBtns = $$('.cs-mode button');
function setMode(m) {
  mode = m;
  try { localStorage.setItem('cs-mode', m); } catch (e) {}
  modeBtns.forEach(b => b.setAttribute('aria-checked', String(b.dataset.mode === m)));
  const pair = cur >= 0 ? steps[cur] : null;
  buildSteps(); hideAll(); layout();
  let to = pair ? steps.findIndex(([a, b]) => a === pair[0] && b === pair[1]) : (m === 'slides' ? 0 : -1);
  if (m === 'slides') { lenis && lenis.stop(); window.scrollTo(0, 0); goTo(Math.max(0, to), true); }
  else { lenis && lenis.start(); scrollToStep(to, true); requestAnimationFrame(onScroll); }
  requestAnimationFrame(placePhones);
}
modeBtns.forEach(b => b.addEventListener('click', () => setMode(b.dataset.mode)));

/* ---------------- phones: stacked page ---------------- */
let io = null;
function stackLayout() {
  track.style.height = '';
  slides.forEach(s => { gsap.set(s, { clearProps: 'all' }); $$('[data-a],[data-sub],.cs-pill,[data-pop]', s).forEach(el => gsap.set(el, { clearProps: 'all' })); });
  const tro = $('.cs-trojanbox'); if (tro) tro.style.setProperty('--tz', (tro.clientWidth / 1728).toFixed(4));
  if (!io) {
    io = new IntersectionObserver(es => es.forEach(en => {
      if (!stack) return;
      if (en.isIntersecting && !en.target.classList.contains('in')) { en.target.classList.add('in'); loadFrames(en.target); fire(en.target, 'enter'); }
      else if (!en.isIntersecting && en.target.classList.contains('in')) { en.target.classList.remove('in'); fire(en.target, 'leave'); }
    }), { threshold: 0.12 });
    slides.forEach(s => io.observe(s));
  }
}

/* ---------------- site nav at the very top; the slim case-study bar everywhere else ---------------- */
function updateBar() {
  const compact = !stack && (mode === 'slides' ? cur > 0 : scrollY > 60);
  body.classList.toggle('cs-compact', compact);
}
addEventListener('scroll', updateBar, { passive: true });

/* ---------------- nav (mobile sheet) ---------------- */
const sheet = $('.sheet');
$('.burger')?.addEventListener('click', () => sheet.classList.add('open'));
$('.sheet-close')?.addEventListener('click', () => sheet.classList.remove('open'));
document.addEventListener('click', e => { if (e.target.closest('a[data-dud]')) e.preventDefault(); });

/* ---------------- boot ---------------- */
if ('scrollRestoration' in history) history.scrollRestoration = 'manual';
modeBtns.forEach(b => b.setAttribute('aria-checked', String(b.dataset.mode === mode)));
gsap.set(slides, { autoAlpha: 0 });
$$('[data-sub]').forEach(c => gsap.set(c, { autoAlpha: 0 }));
buildSteps();
layout();
window.scrollTo(0, 0);
if (!stack && mode === 'slides') goTo(0, true);
let rT = 0;
addEventListener('resize', () => {
  clearTimeout(rT);
  rT = setTimeout(() => {
    const keep = cur, was = stack; layout();
    if (stack) return;
    if (was) { cur = -1; if (keep >= 0 || mode === 'slides') goTo(Math.max(0, keep), true); }
    if (mode === 'scroll' && cur >= 0) scrollToStep(cur, true);
    if (cur >= 0) setSub(slides[steps[cur][0]], steps[cur][1], 1, true);
    placePhones();
  }, 120);
});
document.fonts && document.fonts.ready.then(() => { if (!stack) { layout(); placePhones(); } });
window.__cs = { goTo, get steps() { return steps; }, setMode, get cur() { return cur; } };

/* ---------------- build slide: live Now-tab prototype + state picker ---------------- */
(() => {
  const frame = $('.cs-proto iframe'), btns = $$('.cs-state');
  if (!frame || !btns.length) return;
  // load it once the page has settled (it's ~1 MB of screens), or right away if someone reaches for it
  let pending = null, ready = false;
  const load = () => { if (!frame.src) frame.src = frame.dataset.src; };
  if (document.readyState === 'complete') setTimeout(load, 1200); else addEventListener('load', () => setTimeout(load, 1200));
  const mark = n => btns.forEach(b => { const on = +b.dataset.state === n; b.classList.toggle('is-on', on); b.setAttribute('aria-pressed', on); });
  const send = n => frame.contentWindow.postMessage({ nowState: n }, '*');
  btns.forEach(b => b.addEventListener('click', () => {
    const n = +b.dataset.state; mark(n);
    if (ready) send(n); else { pending = n; load(); }
  }));
  addEventListener('message', e => {
    if (e.source !== frame.contentWindow || !e.data) return;
    if (e.data.nowReady) { ready = true; if (pending) { send(pending); pending = null; } }
    else if (e.data.nowStateChanged && !pending) mark(e.data.nowStateChanged);
  });
})();
