// Deterministic timeline so it can be recorded frame by frame: window.setT(seconds)
const $ = s => document.querySelector(s), D = 394.56 - 74.88;   // sheet travel (Figma px)
const aDrawer = $('#A-drawer'), aContent = $('#A-drawer-content'), aTitle = $('#A-title');
const bSheet = [$('[data-node-id="1479:29583"]'), $('#Bbtn'), $('#Brect')];
const bPill = $('[data-node-id="1479:29575"]'), tap = $('#tap');
const LOOP = 5.0;
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
  const p = seg(t, 1.25, 1.75) - seg(t, 3.55, 4.05);      // 0 collapsed → 1 expanded → 0
  aDrawer.style.transform = `translateY(${-D * p}px)`;
  aContent.style.opacity = clamp(1 - p * 2.2);
  aDrawer.style.visibility = p > 0.999 ? 'hidden' : 'visible';
  bSheet.forEach(el => { el.style.transform = `translateY(${D * (1 - p)}px)`; el.style.opacity = clamp((p - 0.25) * 2.2); });
  aTitle.style.opacity = clamp(1 - p * 2); bPill.style.opacity = clamp((p - 0.3) * 2);
  // taps: the up arrow on the collapsed sheet, then the down arrow on the open one
  const o = Math.max(tapAt(t, 0.95, 135.36, 394.56), tapAt(t, 3.25, 135.36, 79.2));
  tap.style.opacity = o;
};
setT(0);
