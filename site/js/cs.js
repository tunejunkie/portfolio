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
const steps = [];                                                 // [slideIndex, sub]
slides.forEach((s, i) => { for (let k = 0; k < +s.dataset.steps; k++) steps.push([i, k]); });
const N = steps.length;
const firstStep = i => steps.findIndex(([s]) => s === i);

let mode = 'scroll', stack = false, cur = -1, S = 1, U = innerHeight, lenis = null;
try { mode = localStorage.getItem('cs-mode') === 'slides' ? 'slides' : 'scroll'; } catch (e) {}
const qp = new URLSearchParams(location.search).get('mode'); if (qp === 'slides' || qp === 'scroll') mode = qp;

/* ---------------- background ---------------- */
const paint = c => { gsap.to([document.documentElement, body], { backgroundColor: c, duration: 0.9 * D, ease: 'power1.out', overwrite: 'auto' }); };

/* ---------------- 3D phones ---------------- */
let stage = null;
try { stage = new Stage($('.cs-gl')); } catch (e) { body.classList.add('no-gl'); }
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
  if (stack) { stackLayout(); return; }
  const vw = deck.clientWidth || innerWidth, vh = deck.clientHeight || innerHeight;
  S = Math.min(vw / BW, vh / BH);
  const tx = (vw - BW * S) / 2, ty = Math.max(0, (vh - BH * S) / 2);
  board.style.transform = `translate(${tx}px,${ty}px) scale(${S})`;
  // keep the HUD clear of the site nav (96px tall in screen px, whatever the scale)
  const hud = Math.max(132, (96 + 16 - ty) / S), top = hud + 92, h = BH - top - (mode === 'slides' ? 128 : 60);
  Object.assign(board.style, { '--hud': hud + 'px', '--top': top + 'px', '--h': h + 'px' });
  board.style.setProperty('--hud', hud + 'px'); board.style.setProperty('--top', top + 'px'); board.style.setProperty('--h', h + 'px');
  const hudEl = $('.cs-hud'); Object.assign(hudEl.style, { left: '60px', right: '60px', top: hud + 'px', width: 'auto' });
  // shrink any slide whose content is taller than the space under the HUD
  slides.forEach(s => {
    if (s.classList.contains('cs-hero')) return;
    const f = $('.cs-fit', s); f.style.setProperty('--k', 1);
    const k = Math.min(1, h / f.offsetHeight); f.style.setProperty('--k', k.toFixed(4));
  });
  U = innerHeight;
  track.style.height = mode === 'scroll' ? ((N - 1) * U + innerHeight) + 'px' : innerHeight + 'px';
  if (stage) stage.resize();
}

/* ---------------- stepping ---------------- */
const outlineBtns = $$('.cs-outline button');
function setSub(slide, sub, dir, instant) {
  const key = slide.dataset.key, d = instant ? 0.01 : D;
  if (key === 'hero') {
    const copy = $('.cs-hero-copy', slide), vid = $('.cs-video', slide), v = $('video', slide);
    const h = parseFloat(getComputedStyle(board).getPropertyValue('--h'));
    const k = Math.min(1, h / 900, 1608 / 1600) * 0.98;
    // distance from the slide's top to the video, in art-board px (measured on the untransformed wrapper)
    const top0 = (vid.parentElement.getBoundingClientRect().top - slide.getBoundingClientRect().top) / S;
    const target = (h - 900 * k) / 2 - top0;
    gsap.to(copy, { autoAlpha: sub ? 0 : 1, y: sub ? -90 : 0, duration: 0.7 * d, ease: 'power3.inOut' });
    gsap.to(vid, { y: sub ? target : 0, scale: sub ? k : 1, duration: 0.9 * d, ease: 'power3.inOut' });
    if (v) { v.muted = true; v.play().catch(() => {}); }
  }
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
      if (old.dataset.key === 'hero') { const v = $('video', old); v && v.pause(); }
    }
    sl.classList.add('on'); gsap.killTweensOf(sl);
    gsap.set(sl, { autoAlpha: 1, y: 0 });
    const parts = $$('[data-a], .cs-pill', sl);
    gsap.fromTo(parts, { autoAlpha: 0, y: 56 * dir }, { autoAlpha: 1, y: 0, duration: (instant ? 0.01 : 0.85) * D, delay: instant ? 0 : 0.3 * D, stagger: instant ? 0 : 0.06 * D, ease: 'power3.out', overwrite: true });
    if (sl.dataset.key === 'problem') {
      gsap.fromTo($$('[data-pop]', sl), { autoAlpha: 0, scale: 0.6, transformOrigin: '20% 100%' },
        { autoAlpha: 1, scale: 1, duration: 0.55 * D, delay: (instant ? 0 : 0.9) * D, stagger: 0.32 * D, ease: 'back.out(2)' });
    }
    paint(sl.dataset.bg);
    // jump this slide's own sub-state into place, then animate to the target sub
    setSub(sl, dir > 0 ? 0 : sub, dir, true);
    if (sub && dir > 0) setSub(sl, sub, dir, instant); else if (dir < 0) setSub(sl, sub, dir, true);
  } else setSub(sl, sub, dir, instant);
  phoneTo(si, sub, dir, instant);
  if (changeSlide) rowTo(si, dir, instant);
  cur = i;
  outlineBtns.forEach((b, k) => b.classList.toggle('on', k === +sl.dataset.chapter));
  $('.cs-count').textContent = `${i + 1} / ${N}`;
  $('.cs-prev').disabled = i === 0; $('.cs-next').disabled = i === N - 1;
  $('.cs-progress i').style.width = (i / (N - 1) * 100) + '%';
  $('.cs-hint').classList.toggle('off', i > 0);
}

/* ---------------- scroll mode ---------------- */
let snapT = 0, programmatic = false;
function scrollToStep(i, immediate) {
  i = Math.max(0, Math.min(N - 1, i));
  const y = i * U;
  if (lenis) lenis.scrollTo(y, { immediate, duration: 0.9, lock: false });
  else window.scrollTo({ top: y, behavior: immediate ? 'auto' : 'smooth' });
}
function onScroll() {
  if (stack || mode !== 'scroll') return;
  const pos = scrollY / U;
  if (pos <= N - 1 + 0.01) goTo(Math.round(pos));
  clearTimeout(snapT);
  snapT = setTimeout(() => {                                       // settle onto the nearest step
    const p = scrollY / U;
    if (p < N - 1 && Math.abs(p - Math.round(p)) > 0.02) scrollToStep(Math.round(p));
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
  if (e.key === 'Enter' && e.target.closest('a,button')) return;
  if (mode === 'scroll') {
    if (scrollY > (N - 1) * U + 4 && to < N) return;               // down in the footer: let the page scroll
    e.preventDefault(); scrollToStep(to);
  } else { e.preventDefault(); goTo(to); }
});
$('.cs-prev').addEventListener('click', () => goTo(cur - 1));
$('.cs-next').addEventListener('click', () => goTo(cur + 1));
outlineBtns.forEach((b, k) => b.addEventListener('click', () => {
  const to = firstStep(slides.findIndex(s => +s.dataset.chapter === k));
  mode === 'scroll' ? scrollToStep(to) : goTo(to);
}));

/* ---------------- mode toggle ---------------- */
const modeBtns = $$('.cs-mode button');
function setMode(m) {
  mode = m;
  try { localStorage.setItem('cs-mode', m); } catch (e) {}
  modeBtns.forEach(b => b.setAttribute('aria-checked', String(b.dataset.mode === m)));
  const keep = Math.max(0, cur);
  layout();
  if (m === 'slides') { lenis && lenis.stop(); window.scrollTo(0, 0); }
  else { lenis && lenis.start(); scrollToStep(keep, true); }
  requestAnimationFrame(placePhones);
}
modeBtns.forEach(b => b.addEventListener('click', () => setMode(b.dataset.mode)));

/* ---------------- phones: stacked page ---------------- */
let io = null;
function stackLayout() {
  track.style.height = '';
  slides.forEach(s => { s.style.setProperty('--sbg', s.dataset.bg); gsap.set(s, { clearProps: 'all' }); $$('[data-a],[data-sub],.cs-pill,[data-pop]', s).forEach(el => gsap.set(el, { clearProps: 'all' })); });
  const tro = $('.cs-trojan'); if (tro) { tro.style.zoom = ''; tro.style.width = '1595px'; tro.style.height = '426px'; tro.style.aspectRatio = 'auto'; tro.style.zoom = (tro.parentElement.clientWidth / 1595).toFixed(4); }
  const vid = $('.cs-hero video'); vid && vid.play().catch(() => {});
  if (!io) {
    io = new IntersectionObserver(es => es.forEach(en => { if (en.isIntersecting) en.target.classList.add('in'); }), { threshold: 0.12 });
    slides.forEach(s => io.observe(s));
  }
}

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
layout();
window.scrollTo(0, 0);
if (!stack) goTo(0, true);
let rT = 0;
addEventListener('resize', () => {
  clearTimeout(rT);
  rT = setTimeout(() => {
    const keep = cur, was = stack; layout();
    if (stack) return;
    if (was) { cur = -1; goTo(Math.max(0, keep), true); }
    if (mode === 'scroll') scrollToStep(Math.max(0, cur), true);
    setSub(slides[steps[cur][0]], steps[cur][1], 1, true); placePhones();
  }, 120);
});
document.fonts && document.fonts.ready.then(() => { if (!stack) { layout(); placePhones(); } });
window.__cs = { goTo, steps, setMode, get cur() { return cur; } };
