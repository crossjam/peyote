import random, math, pygame
from math import cos, sin, pi
from pprint import pprint

import Image
import numpy as np
from pygame import Color
import pygame.surfarray

# Repository for global state
class Substrate:
    pass

def setup():
    global Substrate

    # size(256,256)
    # size(400,120)
    size(512,512)

    background((255,255,255,255))
    clear((255,255,255,0))

    # Substrate.maxnum = 100
    Substrate.maxnum = 50
    Substrate.maxpal = 512
    
    Substrate.cgrid = np.empty((HEIGHT,WIDTH),'int')
    Substrate.cgrid[:,:] = 10001
    Substrate.seeds =[]
    Substrate.cracks = []
    Substrate.goodcolor = []

    takecolor("pollockShimmering.gif")

    for k in range(16):
        x = random.randrange(WIDTH)
        y = random.randrange(HEIGHT)
        print "Crack seed location: %d,%d" % (y,x)
        Substrate.cgrid[y,x] = int(random.randrange(360))
        Substrate.seeds.append((y,x))
        
    for k in range(3):
        makeCrack()

def draw():
    global Substrate
    
    for crack in Substrate.cracks:
        crack.move()

def blend_pixels(src, dst, a=1.0):
    a1 = a
    a2 = 1.0 - a
    
    np = (int(src.r * a1 + dst.r * a2),
          int(src.g * a1 + dst.g * a2),
          int(src.b * a1 + dst.b * a2),
          255)
    
    return np

def makeCrack():
    global Substrate
    if len(Substrate.cracks) < Substrate.maxnum:
        # print "Making crack: %s" % len(Substrate.cracks)
        Substrate.cracks.append(Crack())

def takecolor(fn):
    global Substrate
    img = Image.open(fn)
    img = img.convert('RGB')
    icolors = [p[1] for p in img.getcolors()]
    print "Img: %s, colors: %s" % (img, len(icolors))

    Substrate.goodcolor = icolors
    Substrate.goodcolor.sort()
    print "First color: %s, last color: %s" % (Substrate.goodcolor[0],
                                               Substrate.goodcolor[-1])

class Crack:

    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.t = 0.0 
        
        self.findStart()
        # print "New crack: %d,%d" % (self.x, self.y)
        self.sp = SandPainter()
        
    def findStart(self):
        global Substrate
        
        px, py = 0,0
        found = False
        timeout = 0
        seed = None
        
        for i in xrange(100000):
            rx = random.randrange(WIDTH)
            ry = random.randrange(HEIGHT)
            if Substrate.cgrid[ry,rx] < 10000:
                seed = (ry, rx)
                break
        
        if not seed: return
        
        a = Substrate.cgrid[seed]
        
        if random.randrange(100) < 50:
            a = a - (90 + int(random.uniform(-2.0,2.1)))
        else:
            a = a + (90 + int(random.uniform(-2.0,2.1)))
        self.startCrack(seed[1],seed[0],a)
            
    def startCrack(self, x, y, t):
        # print "Starting crack at: %d,%d,%s" % (x, y, t)
        self.x = x
        self.y = y
        self.t = t
        self.x += 0.61 * cos(t*pi/180.0)
        self.y += 0.61 * sin(t*pi/180.0)
        
    def move(self):
        global Substrate
        # print "Moving crack at: %d,%d,%s" % (self.x, self.y, self.t)
        cgrid = Substrate.cgrid
        
        self.x += 0.42*cos(self.t*pi/180.0)
        self.y += 0.42*sin(self.t*pi/180.0)
        z = 0.33
        cx = int(self.x+random.uniform(-z,z))
        cy = int(self.y+random.uniform(-z,z))
        
        self.regionColor()
                
        if (0 <= cx < WIDTH) and (0 <= cy < HEIGHT):
            if (cgrid[cy,cx] > 10000) or (abs(cgrid[cy,cx]-self.t)) < 5:
                cgrid[cy,cx] = int(self.t)

                a = 85 / 255.0
                src = Color(0,0,0)
                dst = get_pixel(cx,cy)
                PIXELS[cx,cy] = map_rgb(blend_pixels(src, dst, a))
                
            elif abs(cgrid[cy,cx]-self.t) > 2:
                self.findStart()
                makeCrack()
        else:
            self.findStart()
            makeCrack()

    def regionColor(self):
        rx = float(self.x)
        ry = float(self.y)

        dx = 0.81*sin(self.t*pi/180.0)
        dy = -0.81*cos(self.t*pi/180.0)
        while True:
            # rx += 0.81*sin(self.t*pi/180.0)
            # ry += -0.81*cos(self.t*pi/180.0)
            rx += dx
            ry += dy
            cx, cy = int(rx), int(ry)
            if not (0 <= cx < WIDTH): break
            if not (0 <= cy < HEIGHT): break
            if Substrate.cgrid[cy,cx] <= 10000: break

        self.sp.render(rx, ry, self.x, self.y)
    
class SandPainter:
    def __init__(self):
        global Substrate
        
        self.c = pygame.Color(*random.choice(Substrate.goodcolor))
        self.c_int = map_rgb(self.c)
        self.g = random.uniform(0.01,0.1)
        
    def render(self, x, y, ox, oy):
        global Substrate
        
        self.g += random.uniform(-0.050,0.050)
        maxg = 1.0
        if self.g < 0: self.g = 0.0
        if self.g > maxg: self.g = maxg
        
        grains = 64
        w = self.g / (grains - 1.0)
        
        dx, dy = x-ox, y-oy

        alpha_factor = 1 / 10.0
        sa, da = alpha_factor, alpha_factor / grains 

        for i in xrange(grains):
            a = sa - da * i
            ssw = sin(sin(i*w))
            sx = ox + int(dx*ssw)
            sy = oy + int(dy*ssw)

            if not (0 <= int(sx) < WIDTH): break
            if not (0 <= int(sy) < HEIGHT): break

            c1 = get_pixel(int(sx), int(sy))
            c2 = self.c
            
            PIXELS[sx,sy] = map_rgb(blend_pixels(c2, c1, a))

            '''
            a1 = 1.0 - a
            a2 = a
            
            c1 = get_pixel(int(sx), int(sy))
            c2 = self.c

            nc = (int(c1.r * a1 + c2.r * a2),
                  int(c1.g * a1 + c2.g * a2),
                  int(c1.b * a1 + c2.b * a2),
                  255)

            
            PIXELS[sx, sy] = map_rgb(nc)
            '''
            
    
