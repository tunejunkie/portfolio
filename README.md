# natalierose.works

Natalie Rose Taylor's portfolio. A static site: `python3 build.py` writes every page into `site/`, and Netlify publishes `site/` as-is (see `netlify.toml`).

- `build.py` – page templates (homepage, screenshot galleries)
- `gallery_data.py` – gallery copy, grouping and captions
- `anecdotes.py`, `work_history.py`, `loader_svg.py` – homepage anecdotes, Work History page, loader flower
- `site/css`, `site/js` – styles and interactions (three.js phone, GSAP scroll scenes)
- `site/assets` – images, logos, screenshots

To change copy: edit the Python file, run `python3 build.py`, commit and push. Netlify redeploys automatically.
