import random
from pygame import Color
from math import sin

dim = 500
k = 22
k = 12
time = 0

ticks = 1
frms = 13

sweeps = []

maxpal = 256
numpal = 0
colors = []

def setup():
    size(480,120)
    takecolor("pollockShimmering.gif")
    background((255,255,255,255))
    clear((255,255,255))
    
    g = int(HEIGHT/float(k))

    for y in range(k):
        sweeps.append(Sweep(0,random.randrange(HEIGHT),g*10))

def draw():
    global time
    
    time += 1
    for sweep in sweeps:
        sweep.render()
        
def takecolor(fn):
    global colors
    import Image
    
    img = Image.open(fn)
    img = img.convert('RGB')
    icolors = [p[1] for p in img.getcolors()]
    print "Img: %s, colors: %s" % (img, len(icolors))

    colors = icolors
    colors.sort()
    print "First color: %s, last color: %s" % (colors[0],
                                               colors[-1])
    

class Sweep:
    def __init__(self, x, y, gage):
        self.ox = 0.0
        self.oy = 0.0
        self.x = 0.0
        self.y = 0.0
        self.vx = 0.0
        self.ogage = 0.0
        self.gage = 0.0
        self.color = None
        self.time  = 0.0
        self.sc = 0.0
        self.sg = 0.0

        self.ox = self.x = x
        self.oy = self.y = y
        self.ogage = self.gage = gage

        self.selfinit()

    def selfinit(self):
        self.myc = Color(*random.choice(colors))
        self.sg = random.uniform(0.01,0.1)
        self.x = self.ox
        self.y = self.oy
        self.gage = self.ogage
        self.vx = 1.0

    def render(self):
        global colors
        
        self.x += self.vx
        if (self.x > WIDTH): self.selfinit()

        tpoint(int(self.x), int(self.y), self.myc, 0.07)

        self.sg += random.uniform(-0.042,0.042)

        if self.sg < -0.3:
            self.sg = -0.3
        elif self.sg > 0.3:
            self.sg = 0.3
        elif -0.01 < self.sg < 0.01:
            if random.uniform(0.0,1.0) < 0.99:
                self.myc = Color(*random.choice(colors))

        wd = 200.0
        w = self.sg / wd

        for i in range(int(wd)):
            dy = self.gage*sin(i*w)
            a = 0.1 - i/(wd*10+10)
            tpoint(int(self.x),int(self.y + dy), self.myc, a)
            tpoint(int(self.x),int(self.y - dy), self.myc, a)

def tpoint(x, y, src, a):
    if not (0 < x < WIDTH): return
    if not (0 < y < HEIGHT): return
    
    dst = get_pixel(int(x), int(y))
    PIXELS[x,y] = map_rgb(blend_pixels(src, dst, a))
    

def blend_pixels(src, dst, a=1.0):
    a1 = a
    a2 = 1.0 - a
    
    np = (int(src.r * a1 + dst.r * a2),
          int(src.g * a1 + dst.g * a2),
          int(src.b * a1 + dst.b * a2),
          255)
    
    return np

                
