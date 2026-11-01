# Saturn, before: schedule sheet up / down

Code recreation of the pre-redesign Saturn home screen (Figma 1479:31220), kept exactly as it shipped,
quirks included (e.g. the round arrow sitting over the sheet's header). Fonts: Poppins as designed;
Moderat isn't available, so DM Sans / Roboto Mono stand in.

- `index.html` + `anim.js`: the prototype. `setT(seconds)` drives a 5 s loop (rest → tap ↑ → sheet up → tap ↓ → sheet down).
- `rec.py`: records it frame by frame to `saturn-before-sheet.mp4` (750×1624, 60 fps).
  Serve this folder on :8777 first (`python3 -m http.server 8777`).
- Output used on the site: `site/assets/cs/saturn/proto/before-sheet.mp4`.
