from PIL import Image, ImageDraw, ImageFilter
import subprocess, glob, math
W,H=750,1624; FPS=30
fs=sorted(glob.glob('0*.png'))
ims=[Image.open(f).convert('RGB').resize((W,H),Image.LANCZOS) for f in fs]
# where the finger taps on each screen before moving on (375-space)
taps=[(188,742),(300,420),(300,420),(300,420),(300,420),(247,262),(300,420),(300,420),None]
HOLD,TR=2.1,0.38
def ease(x): return 1-(1-x)**3
def tap(img,x,y,k):
    if k<=0 or k>=1: return img
    a=(k/0.25 if k<0.25 else 1-(k-0.25)/0.75)
    r=int(36*(0.75+0.35*min(1,k*3)))
    ov=Image.new('RGBA',img.size,(0,0,0,0)); d=ImageDraw.Draw(ov)
    d.ellipse((x*2-r,y*2-r,x*2+r,y*2+r),fill=(255,255,255,int(150*a)),outline=(0,0,0,int(30*a)),width=3)
    return Image.alpha_composite(img.convert('RGBA'),ov).convert('RGB')
p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-',
                    '-c:v','libx264','-preset','slow','-crf','20','-pix_fmt','yuv420p','-movflags','+faststart','digest.mp4'],stdin=subprocess.PIPE)
n=len(ims)
for i in range(n):
    nxt=ims[(i+1)%n]
    for f in range(int(HOLD*FPS)):
        t=f/FPS; img=ims[i]
        if taps[i] and t>HOLD-0.55: img=tap(img,*taps[i],(t-(HOLD-0.55))/0.45)
        p.stdin.write(img.tobytes())
    for f in range(int(TR*FPS)):
        k=ease((f+1)/(TR*FPS)); off=int(W*k)
        fr=Image.new('RGB',(W,H)); fr.paste(ims[i].crop((off,0,W,H)),(0,0)); fr.paste(nxt.crop((0,0,off,H)),(W-off,0))
        p.stdin.write(fr.tobytes())
p.stdin.close(); p.wait()
ims[0].save('poster.jpg',quality=85)
