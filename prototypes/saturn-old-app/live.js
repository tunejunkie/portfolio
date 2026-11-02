// Saturn before the redesign, tappable: tap the arrow to slide the schedule sheet up (the big timer shrinks into
// the nav) and down again; tap the people icon for the Directory. Same drawing code as the recorded video
// (prototypes/saturn-before-me-video-1-sheet-interaction/anim.js), driven by taps instead of a timeline.
const $ = s => document.querySelector(s), D = 394.56 - 74.88;   // sheet travel (Figma px)
const aDrawer = $('#A-drawer'), aContent = $('#A-drawer-content'), aTitle = $('#A-title');
const bSheet = [$('[data-node-id="1479:29583"]'), $('#Bbtn'), $('#Brect')];
const bPill = $('[data-node-id="1479:29575"]'), tap = $('#tap');
const big = $('#big'), mini = $('#mini'), morph = $('#morph'), phone = $('#phone');
const pillBox = $('[data-node-id="1479:29576"]');
const ringArt = [...document.querySelectorAll('#A > div:first-child > :not(:nth-child(3))')];
const hotSheet = $('#hot-sheet'), hotPeople = $('#hot-people'), dir = $('#dir');
const K = 375 / 270;
function centre(el) { const r = el.getBoundingClientRect(), p = phone.getBoundingClientRect(), k = p.width / 270;
  return { x: (r.left + r.width / 2 - p.left) / k, y: (r.top + r.height / 2 - p.top) / k }; }
let C0, C1;
const clamp = v => Math.max(0, Math.min(1, v));
const ease = x => x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;

function draw(m) {
  if (!C0) { C0 = centre(big); C1 = centre(mini); }
  aDrawer.style.transform = `translateY(${-D * m}px)`;
  aContent.style.opacity = clamp(1 - m * 2.2);
  aDrawer.style.visibility = m > 0.999 ? 'hidden' : 'visible';
  bSheet.forEach(el => { el.style.transform = `translateY(${D * (1 - m)}px)`; el.style.opacity = clamp((m - 0.25) * 2.2); });
  aTitle.style.opacity = clamp(1 - m * 2); bPill.style.opacity = clamp((m - 0.3) * 2);
  const moving = m > 0.001 && m < 0.999;
  big.style.opacity = moving || m >= 0.999 ? 0 : 1;
  mini.style.opacity = m >= 0.999 ? 1 : 0;
  morph.style.display = moving ? 'block' : 'none';
  if (moving) {
    const fs = 40.32 + (11.52 - 40.32) * m, ls = -0.72 * m;
    morph.style.fontSize = fs + 'px'; morph.style.lineHeight = fs + 'px'; morph.style.letterSpacing = ls + 'px';
    const x = C0.x + (C1.x - C0.x) * m, y = C0.y + (C1.y - C0.y) * m - Math.sin(Math.PI * m) * 6;
    morph.style.transform = `translate(${x}px,${y}px) translate(-50%,-50%)`;
  }
  pillBox.style.borderColor = `rgba(255,255,255,${0.2 * clamp((m - 0.7) / 0.3)})`;
  ringArt.forEach(el => { if (el._o == null) el._o = parseFloat(getComputedStyle(el).opacity); el.style.opacity = el._o * clamp(1 - m * 1.6); });
}

// time passes for real
let left = 15 * 60 + 27;
const tick = () => { const t = Math.floor(left / 60) + ':' + String(left % 60).padStart(2, '0'); big.textContent = mini.textContent = morph.textContent = t; };
tick(); setInterval(() => { left = left > 0 ? left - 1 : 50 * 60; tick(); }, 1000);

// sheet: animate the eased progress between 0 (timer) and 1 (schedule)
let p = 0, target = 0, from = 0, t0 = 0, raf = 0;
function animate(now) {
  const k = clamp((now - t0) / 500);
  p = from + (target - from) * ease(k); draw(p);
  if (k < 1) raf = requestAnimationFrame(animate); else placeHot();
}
function toggleSheet() {
  hint(false); cancelAnimationFrame(raf); from = p; target = p > 0.5 ? 0 : 1; t0 = performance.now(); raf = requestAnimationFrame(animate);
}
function placeHot() {   // the tappable arrow moves with the sheet
  const up = p > 0.5;
  Object.assign(hotSheet.style, up ? { left: (135.36 * K - 40) + 'px', top: (79.2 * K - 30) + 'px', width: '80px', height: '60px' }
                                   : { left: '0px', top: (394.56 * K - 40) + 'px', width: '375px', height: '80px' });
  hotSheet.setAttribute('aria-label', up ? 'Close your schedule' : 'Open your schedule');
}
hotSheet.addEventListener('click', toggleSheet);
hotPeople.addEventListener('click', () => { hint(false); dir.classList.add('open'); dir.setAttribute('aria-hidden', 'false'); });
$('#dir-back').addEventListener('click', () => { dir.classList.remove('open'); dir.setAttribute('aria-hidden', 'true'); });

// a soft pulsing finger hint on the arrow until the first tap
let hintOn = true, h0 = performance.now();
function hint(on) { hintOn = on; if (!on) tap.style.opacity = 0; }
(function pulse(now) {
  if (!hintOn) return;
  const k = ((now - h0) / 1600) % 1;
  tap.style.left = (135.36) + 'px'; tap.style.top = (394.56) + 'px';
  tap.style.transform = `scale(${0.7 + 0.5 * k})`; tap.style.opacity = (k < 0.2 ? k / 0.2 : 1 - (k - 0.2) / 0.8) * 0.9;
  requestAnimationFrame(pulse);
})(h0);

draw(0); placeHot();
