"""Record the stories prototype frame by frame (render(t) is deterministic) and encode it."""
import subprocess, sys
from playwright.sync_api import sync_playwright
OUT = sys.argv[1]; FPS = 30
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 375, 'height': 812}, device_scale_factor=2)
    pg.goto('http://localhost:8765/proto/trovy-ads/?still'); pg.evaluate('preload()'); pg.wait_for_timeout(1200)
    total = pg.evaluate('TOTAL'); n = int(total * FPS)
    ff = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'image2pipe', '-framerate', str(FPS), '-i', '-',
                           '-c:v', 'libx264', '-preset', 'slow', '-crf', '21', '-pix_fmt', 'yuv420p', '-movflags', '+faststart',
                           OUT + '.mp4'], stdin=subprocess.PIPE)
    for i in range(n):
        pg.evaluate(f'render({i / FPS})')
        ff.stdin.write(pg.screenshot(type='jpeg', quality=95))
        if i % 300 == 0: print(i, '/', n, flush=True)
    ff.stdin.close(); ff.wait()
    pg.evaluate('render(1.4)'); pg.screenshot(path=OUT + '-poster.jpg', type='jpeg', quality=88)
