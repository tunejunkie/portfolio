# Saturn Before Me - Video 1, Sheet Interaction

Code recreation of the pre-redesign Saturn home screen (Figma 1479:31220), kept exactly as it shipped,
quirks included (e.g. the round arrow sitting over the sheet's header). Fonts: Poppins as designed;
Moderat isn't available, so DM Sans / Roboto Mono stand in.

- `index.html` + `anim.js`: the prototype. `setT(seconds)` drives an 8 s loop (sheet up and down twice; the countdown rewinds once per loop).
- `rec.py`: records it frame by frame to `saturn-before-sheet.mp4` (750×1624, 60 fps).
  Serve this folder on :8777 first (`python3 -m http.server 8777`).
- Output used on the site: `site/assets/cs/saturn/proto/before-me-video-1-sheet-interaction.mp4`.
