// "Legal to work in" line that loops across the screen riding a wave.
// Each item (flag or label) is placed along a sine curve and tilted to its slope.
export function initMarquee(root) {
  const track = root.querySelector('.wave-track');
  const unit = [...track.children];                 // one set: label, flag, label, flag, label, flag
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  let items = [], setW = 0, gap = 0, amp = 0, lambda = 0, offset = 0, last = 0, running = false;

  function build() {
    const vw = window.innerWidth, mob = vw <= 820;
    gap = mob ? 28 : 48; amp = mob ? 22 : 46; lambda = mob ? 640 : 1400;
    track.innerHTML = ''; unit.forEach(n => track.appendChild(n));
    // measure one set
    const widths = unit.map(n => n.getBoundingClientRect().width);
    setW = widths.reduce((a, b) => a + b + gap, 0);
    // clone sets until the screen is covered twice over
    const copies = Math.ceil((vw * 2) / setW) + 1;
    items = [];
    for (let c = 0; c < copies; c++) {
      unit.forEach((n, i) => {
        const el = c === 0 ? n : n.cloneNode(true);
        if (c) { el.setAttribute('aria-hidden', 'true'); track.appendChild(el); }
        items.push({ el, w: widths[i], x0: c * setW + widths.slice(0, i).reduce((a, b) => a + b + gap, 0) });
      });
    }
    place();
  }
  const waveY = x => amp * Math.sin((2 * Math.PI * x) / lambda);
  const slope = x => amp * (2 * Math.PI / lambda) * Math.cos((2 * Math.PI * x) / lambda);
  function place() {
    const total = setW * Math.max(1, Math.round(items.length / unit.length));
    for (const it of items) {
      let x = it.x0 - offset; x = ((x % total) + total) % total - setW;   // wrap seamlessly
      const cx = x + it.w / 2;
      const ang = Math.atan(slope(cx)) * 180 / Math.PI;
      it.el.style.transform = `translate3d(${x}px, ${waveY(cx)}px, 0) rotate(${ang.toFixed(2)}deg)`;
    }
  }
  function frame(t) {
    if (!running) return;
    const dt = Math.min(64, t - (last || t)); last = t;
    offset += dt * (window.innerWidth <= 820 ? 0.05 : 0.08);   // px per ms
    place();
    requestAnimationFrame(frame);
  }
  const start = () => { if (running || reduced) return; running = true; last = 0; requestAnimationFrame(frame); };
  const stop = () => { running = false; };
  new IntersectionObserver(([e]) => e.isIntersecting ? start() : stop()).observe(root);
  let rt; window.addEventListener('resize', () => { clearTimeout(rt); rt = setTimeout(build, 150); });
  (document.fonts ? document.fonts.ready : Promise.resolve()).then(build);
}
