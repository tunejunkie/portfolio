// Saturn Now Tab prototype: 12 states (6 school-day, 6 first-time setup), live timers, cross-faded switches.
// Drive from outside with postMessage({nowState: n}) or window.setNowState(n) (n = 1..12).
(() => {
  const NAMES = ['In class', 'In class, final minute', 'Missing period', 'Passing time', 'Passing time, final minute',
    'Midnight–4am', '4am–8am', '8am–noon', 'Noon–4pm', '4pm–8pm', '8pm–midnight',
    'School not built, no contacts', 'School on the waitlist', 'School not built, has contacts', 'No classes added', 'Classes partly added', 'Schedule not shared'];
  const GROUPS = [['School day', 1, 5], ['No class for an hour+', 6, 11], ['First-time setup', 12, 17]];
  const COUNT = NAMES.length;
  const P = 'rgba(66,42,212,.93)', D = 'rgba(15,22,39,.93)';
  const TINT = ['', P, P, P, D, D, 'rgba(30,32,112,.93)', 'rgba(94,110,213,.93)', 'rgba(33,136,255,.93)', 'rgba(20,120,255,.93)', 'rgba(63,61,222,.93)', 'rgba(28,34,93,.93)', D, D, D, D, D, D];
  const stage = document.getElementById('stage');
  const H = {};
  // Figma frames clip their overflow, so measure each state's real content height.
  function measure() {
    for (let n = 1; n <= COUNT; n++) {
      const L = document.getElementById('L' + n), top = L.getBoundingClientRect().top;
      let max = 0;
      L.querySelectorAll('*').forEach(el => {
        if (el.closest('[data-fix]')) return;
        const r = el.getBoundingClientRect();
        if (r.height && r.bottom - top > max) max = r.bottom - top;
      });
      H[n] = Math.max(812, Math.ceil(max + 95));
    }
    if (cur) stage.style.height = H[cur] + 'px';
  }

  // ---- timers -------------------------------------------------------------
  // Each layer keeps its own clock, so returning to a state finds it where it left off.
  const fmt = {
    mmss: s => [String(Math.floor(s / 60)), String(s % 60).padStart(2, '0')],
    ss: s => [String(s % 60).padStart(2, '0')],
  };
  const T = {
    1: { left: 24 * 60 + 49, total: 75 * 60, f: 'mmss', ring: true },
    2: { left: 49, total: 60, f: 'ss', wrap: 59 },
    3: { left: 24 * 60 + 49, total: 75 * 60, f: 'mmss', ring: true },
    4: { left: 4 * 60 + 49, total: 5 * 60, f: 'mmss' },
    5: { left: 49, total: 60, f: 'ss', wrap: 59 },
    15: { left: 22 * 60 + 48, total: 45 * 60, f: 'joined' },
    16: { left: 22 * 60 + 48, total: 45 * 60, f: 'joined' },
  };
  const R = 105.6, C = 2 * Math.PI * R;
  for (const [n, t] of Object.entries(T)) {
    const L = document.getElementById('L' + n);
    const ps = [...L.querySelectorAll('.f-moderat-mono_black > p')].filter(p => /^[\d:]+$/.test(p.textContent.trim()) && p.textContent.trim() !== '5');
    t.ps = ps.filter(p => p.textContent.trim() !== ':');
    if (t.ring) {
      // swap the static progress arc for a drawable one with the same geometry
      const img = L.querySelector('img[data-ring]');
      const ringBox = img.closest('.size-\\[220px\\]');
      const holder = img.parentElement.children.length === 1 && img.parentElement !== ringBox ? img.parentElement : img;
      const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
      svg.setAttribute('viewBox', '0 0 220 220');
      svg.style.cssText = 'position:absolute;left:0;top:0;width:220px;height:220px;overflow:visible';
      svg.innerHTML = `<circle cx="110" cy="110" r="${R - 0.0}" fill="none" stroke="#fff" stroke-width="8.8" stroke-linecap="round" transform="rotate(-90 110 110)" stroke-dasharray="${C} ${C}"/>`;
      holder.replaceWith(svg);
      t.arc = svg.firstChild;
    }
    paint(t);
  }
  function paint(t) {
    if (t.f === 'joined') { t.ps[0].textContent = fmt.mmss(t.left).join(':'); }
    else { const v = fmt[t.f](t.left); t.ps.forEach((p, i) => { if (v[i] != null) p.textContent = v[i]; }); }
    if (t.arc) t.arc.setAttribute('stroke-dashoffset', String(C * (1 - t.left / t.total)));
  }
  const q = new URLSearchParams(location.search);
  if (!q.has('still')) setInterval(() => {
    for (const t of Object.values(T)) {
      t.left = t.left > 0 ? t.left - 1 : (t.wrap ?? t.total);
      paint(t);
    }
  }, 1000);

  // dormant clocks: advance a minute every 60 s
  const clocks = [...document.querySelectorAll('[data-hero="1"][data-node-id="2:66402"] p')];
  if (!q.has('still')) setInterval(() => clocks.forEach(p => {
    const m = p.textContent.match(/^(\d+):(\d\d)(am|pm)$/); if (!m) return;
    let h = +m[1], mi = +m[2] + 1, ap = m[3];
    if (mi === 60) { mi = 0; h = h === 12 ? 1 : h + 1; if (h === 12) ap = ap === 'am' ? 'pm' : 'am'; }
    p.textContent = `${h}:${String(mi).padStart(2, '0')}${ap}`;
  }), 60000);

  // ---- state switching ----------------------------------------------------
  let cur = 0;
  function setNowState(n, instant) {
    n = Math.max(1, Math.min(COUNT, +n || 1));
    if (n === cur) return;
    const prev = cur && document.getElementById('L' + cur);
    const next = document.getElementById('L' + n);
    const grp = k => GROUPS.findIndex(g => k >= g[1] && k <= g[2]);
    const reset = !cur || grp(cur) !== grp(n) || n > 11; // different layouts: start from the top
    if (H[n]) stage.style.height = H[n] + 'px';
    stage.classList.toggle('instant', !!instant);
    if (prev) { prev.classList.remove('on'); prev.classList.add('out'); setTimeout(() => prev.classList.remove('out'), 700); }
    next.classList.remove('enter'); void next.offsetWidth;
    next.classList.add('on');
    if (!instant) next.classList.add('enter');
    cur = n;
    document.documentElement.style.setProperty('--tint', TINT[n]);
    if (reset) window.scrollTo({ top: 0, behavior: instant ? 'auto' : 'smooth' });
    onScroll();
    if (parent !== window) parent.postMessage({ nowStateChanged: n, name: NAMES[n - 1], group: GROUPS[grp(n)][0] }, '*');
  }
  function onScroll() { document.body.classList.toggle('scrolled', scrollY > 6); }
  addEventListener('scroll', onScroll, { passive: true });
  addEventListener('message', e => { if (e.data && e.data.nowState) setNowState(e.data.nowState); });
  window.setNowState = setNowState;
  window.NOW_STATES = NAMES;
  window.NOW_GROUPS = GROUPS;

  // scrolling classmates: duplicate the row so the marquee loops seamlessly
  const row = document.querySelector('[data-node-id="2:81744"]');
  if (row) { const w = row.scrollWidth; row.innerHTML += row.innerHTML; row.style.setProperty('--loop', -(w + 8) + 'px'); }

  measure();
  setNowState(+(q.get('s') || 1), true);
  (document.fonts ? document.fonts.ready : Promise.resolve()).then(measure);
  addEventListener('load', measure);
  if (parent !== window) parent.postMessage({ nowReady: true, states: NAMES, groups: GROUPS }, '*');
})();
