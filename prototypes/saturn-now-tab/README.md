# Saturn Now Tab prototype

Live, coded version of the Now tab from Figma (Saturn-Selects: Now Tab 2:66831, After school / dormant 2:80442, FTUX 2:81255).
17 states: 5 school-day, 6 dormant by time of day, 6 first-time setup. Timers count down, the class ring drains,
switching cross-fades. Drive it from a parent page with `postMessage({nowState: n})`; it posts back `nowReady` and `nowStateChanged`.

Pipeline (raw Figma assets are not committed; they live in the working folder):
1. `get_design_context` per frame -> `.tsx`; `tools/conv.py frame.tsx a/<dir> fN.html` inlines components and converts to HTML.
2. `build.py` stacks the layers (dormant variants are generated from one template), `npx tailwindcss -i in.css -o tw.css`.
3. `tools/pack.py site/proto/now-tab` dedupes and compresses assets (WebP) into the published copy.
Fonts are stand-ins for Moderat: DM Sans, Roboto Mono (timers), Inter (status bar).
