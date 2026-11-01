// Deterministic timeline so it can be recorded frame by frame: window.setT(seconds)
const $ = s => document.querySelector(s), D = 394.56 - 74.88;   // sheet travel (Figma px)
const aDrawer = $('#A-drawer'), aContent = $('#A-drawer-content'), aTitle = $('#A-title');
const bSheet = [$('[data-node-id="1479:29583"]'), $('#Bbtn'), $('#Brect')];
const bPill = $('[data-node-id="1479:29575"]'), tap = $('#tap');
const LOOP = 8.0;
const big = $('#big'), mini = $('#mini'), morph = $('#morph'), phone = $('#phone');
const pillBox = $('[data-node-id="1479:29576"]');
const ringArt = [...document.querySelectorAll('#A > div:first-child > :not(:nth-child(3))')];   // ring, beaker, share (not the digits)
// centre of an element in phone (Figma) px
function centre(el) { const r = el.getBoundingClientRect(), p = phone.getBoundingClientRect(), k = p.width / 270;
  return { x: (r.left + r.width / 2 - p.left) / k, y: (r.top + r.height / 2 - p.top) / k }; }
let C0, C1;
const clamp = v => Math.max(0, Math.min(1, v));
const ease = x => x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;   // easeInOutCubic
const seg = (t, a, b) => ease(clamp((t - a) / (b - a)));
function tapAt(t, t0, x, y) {                     // finger tap: press in, then fade
  const k = (t - t0) / 0.45;
  if (k < 0 || k > 1) return 0;
  tap.style.left = x + 'px'; tap.style.top = y + 'px';
  tap.style.transform = `scale(${0.7 + 0.3 * Math.min(1, k * 3)})`;
  return k < 0.25 ? k / 0.25 : 1 - (k - 0.25) / 0.75;
}
window.setT = t => {
  t = ((t % LOOP) + LOOP) % LOOP;
  if (!C0) { C0 = centre(big); C1 = centre(mini); }
  // twice per loop: up, hold, down, rest
  let p = 0;
  for (const o of [0, 4]) p += seg(t, o + 0.85, o + 1.35) - seg(t, o + 2.55, o + 3.05);
  aDrawer.style.transform = `translateY(${-D * p}px)`;
  aContent.style.opacity = clamp(1 - p * 2.2);
  aDrawer.style.visibility = p > 0.999 ? 'hidden' : 'visible';
  bSheet.forEach(el => { el.style.transform = `translateY(${D * (1 - p)}px)`; el.style.opacity = clamp((p - 0.25) * 2.2); });
  aTitle.style.opacity = clamp(1 - p * 2); bPill.style.opacity = clamp((p - 0.3) * 2);
  // the big countdown shrinks up into the nav as the mini timer (and grows back down)
  const m = p;                                                  // same eased progress as the sheet
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
  // time passes: the countdown ticks down a second at a time. The loop's 8-second rewind is hidden in the
  // middle of the second downward morph (t = 6.8 s), when the digits are small and moving.
  const left = 15 * 60 + 27 - Math.floor(((t - 6.8) % LOOP + LOOP) % LOOP);
  const txt = Math.floor(left / 60) + ':' + String(left % 60).padStart(2, '0');
  if (big.textContent !== txt) { big.textContent = mini.textContent = morph.textContent = txt; }
  // taps: the up arrow on the collapsed sheet, then the down arrow on the open one
  const o = Math.max(...[0, 4].flatMap(k => [tapAt(t, k + 0.55, 135.36, 394.56), tapAt(t, k + 2.25, 135.36, 79.2)]));
  tap.style.opacity = o;
};
setT(0);
