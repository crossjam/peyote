import numpy as np
from noise import pnoise3 as noise

from random import randrange, random
from math import pi, cos, sin

num = 100
pos = np.zeros((num, 2), dtype='int')
vel = np.zeros((num, 2), dtype='int')
acc = np.zeros((num, 2), dtype='int')

R1 = random()
R2 = random()
G1 = random()
G2 = random()
B1 = random()
B2 = random()
noisy = 0.007

def setup():
    size(400,400)
    background((255,255,255,255))
    clear((255,255,255))

    for i in range(num):
        pos[i] = [randrange(0,WIDTH), randrange(0,HEIGHT)]

    print "C1: %s, %s, %s" % (R1,G1,B1)
    print "C2: %s, %s, %s" % (R2,G2,B2)


def dist(x1, y1, x2, y2):
    return sqrt( (x1 - x2) ** 2 + (y1 - y2) ** 2 )

def draw():
    global noisy, WIDTH, HEIGHT
    set_line_width(1.0)

    set_source_rgba(1.0,1.0,1.0,0.2)
    rectangle(0,0,WIDTH,HEIGHT)
    fill()
    
    for i in range(num):
        x, y = pos[i]

        # print "Drawing circle at: %s, %s" % (x, y)
        
        set_source_rgba(R1,G1,B1)
        arc(x, y, 4, 0, 2 * pi)
        stroke()
        
        set_source_rgba(R2,G2,B2,100/255.0)
        arc(x, y, 4.5, 0, 2 * pi)
        stroke()

        set_source_rgba(100/255.0,100/255.0,100/255.0,1.0)
        vel[i][0] = 10 * noise(200+x*0.007, 200+y*0.007, noisy*2)*cos(4*pi*noise(x*0.003,y*0.003, noisy))
        vel[i][1] = 10 * noise(200+x*0.007, 200+y*0.007, noisy*2)*sin(4*pi*noise(x*0.003,y*0.003, noisy))

        '''
        # If you want to adjust the acceleration of the circles
        for j in range(num):
            if j != i:
                jx, jy = pos[j]
                den1, den2 = dist(x, y, jx, jy), (5+dist(x, y, jx, jy)) ** 2

                acc[i][0] += (x-jy)/den1/den2
                acc[i][1] += (y-jy)/den1/den2
        '''
        
        pos[i] += vel[i]
        if not (0 < pos[i][0] < WIDTH) or not (0 < pos[i][1] < HEIGHT):
            pos[i][0], pos[i][1] = randrange(0, WIDTH), randrange(0, HEIGHT)
            vel[i] = 0

        # acc[i] = 0
        
    noisy += 0.007
            
                
        
        
        
    
