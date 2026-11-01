import asyncio, subprocess
from playwright.async_api import async_playwright
FPS=60; LOOP=5.0
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':375,'height':812},device_scale_factor=2)
        await pg.goto('http://localhost:8777/index.html'); await pg.wait_for_timeout(1500)
        ff=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','image2pipe','-framerate',str(FPS),'-c:v','png','-i','-',
          '-c:v','libx264','-preset','slow','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart','saturn-before-sheet.mp4'],stdin=subprocess.PIPE)
        for i in range(int(LOOP*FPS)):
            await pg.evaluate(f"setT({i/FPS})")
            ff.stdin.write(await pg.screenshot(type='png'))
        ff.stdin.close(); ff.wait(); await b.close()
asyncio.run(main())
