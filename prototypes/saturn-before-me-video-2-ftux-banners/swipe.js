// Swiping through the onboarding banners. Deterministic: window.setT(seconds), 8 s loop.
const track = document.getElementById('track'), dotEls = [...document.querySelectorAll('#dots i')], finger = document.getElementById('swipe');
const PAGE = 335, N = 5, L = 8;
const cl = v => Math.max(0, Math.min(1, v));
const out = x => 1 - Math.pow(1 - x, 3), io = x => x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;
// sheet-space (375) point → phone (270) px: the block sits 103.68px into the drawer, which starts at 74.88
const toPhone = (x, y) => [x * 0.72, 74.88 + 103.68 + y * 0.72];
const SW = [0.7, 2.1, 3.5, 4.9];                 // forward swipes
const BACK = 6.4;                                // one long swipe back to the first banner
window.setT = t => {
  t = ((t % L) + L) % L;
  setBase(t);
  let pos = 0, fx = null, fy = 80, fo = 0;
  SW.forEach((s, i) => {
    const drag = cl((t - s) / 0.32);             // finger drags the card...
    const settle = cl((t - s - 0.32) / 0.38);    // ...then lets go and it snaps into place
    pos += drag * 0.35 + settle * 0.65;
    if (t >= s - 0.12 && t < s + 0.55) {
      const k = cl((t - s) / 0.32);
      fx = 300 - 190 * io(k);
      fo = t < s ? cl((t - s + 0.12) / 0.12) : t < s + 0.32 ? 1 : 1 - cl((t - s - 0.32) / 0.2);
    }
  });
  const b = cl((t - BACK) / 0.75);
  pos -= (N - 1) * out(b);
  if (t >= BACK - 0.12 && t < BACK + 0.6) {
    const k = cl((t - BACK) / 0.3);
    fx = 70 + 230 * io(k);
    fo = t < BACK ? cl((t - BACK + 0.12) / 0.12) : t < BACK + 0.3 ? 1 : 1 - cl((t - BACK - 0.3) / 0.25);
  }
  track.style.transform = `translateX(${(-pos * PAGE).toFixed(2)}px)`;
  dotEls.forEach((d, i) => d.style.opacity = (0.1 + 0.9 * cl(1 - Math.abs(pos - i))).toFixed(3));
  finger.style.opacity = fx == null ? 0 : fo;
  if (fx != null) { const [px, py] = toPhone(fx, fy); finger.style.left = px + 'px'; finger.style.top = py + 'px'; }
};
setT(0);
