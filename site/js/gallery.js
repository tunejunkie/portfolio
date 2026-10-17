// Screenshot gallery page: normal scrolling page. Screens taller than their frame scroll inside it
// while the cursor is on them (wheel / trackpad), or with a finger drag on touch screens.
// always open at the top (the browser/host otherwise carries over the previous scroll position)
if ('scrollRestoration' in history) history.scrollRestoration = 'manual';
const toTop = () => { if (!location.hash) window.scrollTo(0, 0); };
toTop(); addEventListener('load', toTop); addEventListener('pageshow', toTop);
const $ = (s, el = document) => el.querySelector(s), $$ = (s, el = document) => [...el.querySelectorAll(s)];

function makeScrollable(view) {
  const img = $('img', view);
  let y = 0;
  const max = () => Math.max(0, img.offsetHeight - view.clientHeight);
  const set = v => {
    y = Math.min(max(), Math.max(0, v));
    img.style.transform = `translateY(${-y}px)`;
    view.classList.toggle('scrolled', y > 1);
    view.classList.toggle('at-end', y >= max() - 1);
  };
  view.addEventListener('wheel', e => {
    const m = max();
    if (m <= 0 || Math.abs(e.deltaX) > Math.abs(e.deltaY)) return;
    // take the wheel only while there's more screen to see in that direction; then the page scrolls on
    if ((e.deltaY > 0 && y < m) || (e.deltaY < 0 && y > 0)) { e.preventDefault(); set(y + e.deltaY); }
  }, { passive: false });
  let ty = null;
  view.addEventListener('touchstart', e => { ty = e.touches[0].clientY; }, { passive: true });
  view.addEventListener('touchmove', e => {
    if (ty === null || max() <= 0) return;
    const dy = ty - e.touches[0].clientY; ty = e.touches[0].clientY;
    if ((dy > 0 && y < max()) || (dy < 0 && y > 0)) { e.preventDefault(); set(y + dy); }
  }, { passive: false });
  view.addEventListener('keydown', e => {
    if (e.key === 'ArrowDown' || e.key === 'ArrowUp') { e.preventDefault(); set(y + (e.key === 'ArrowDown' ? 120 : -120)); }
  });
  const check = () => {
    const can = max() > 4;
    view.classList.toggle('is-scrollable', can);
    view.tabIndex = can ? 0 : -1;
    if (can) view.setAttribute('aria-label', 'Long screen: scroll to see more');
  };
  img.complete ? check() : img.addEventListener('load', check, { once: true });
  addEventListener('resize', () => { check(); set(y); });
}
$$('.l3-view').forEach(makeScrollable);

// nav: white over the dark header and footer, dark over the light body
const nav = $('.nav'), top = $('.l3-top'), foot = $('.l3-foot');
const tone = () => {
  if (!foot) return;
  const overTop = false; // light header now: dark nav over it
  const overFoot = false; // light footer now too
  nav.classList.toggle('nav--light', overTop || overFoot);
};
addEventListener('scroll', tone, { passive: true }); tone();

// mobile menu
const sheet = $('.sheet');
$('.burger')?.addEventListener('click', () => sheet.classList.add('open'));
$('.sheet-close')?.addEventListener('click', () => sheet.classList.remove('open'));

// links to case studies that aren't written yet do nothing
document.addEventListener('click', e => { if (e.target.closest('a[data-dud]')) e.preventDefault(); });
