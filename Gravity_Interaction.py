import pygame
from pygame.locals import *
import time
import math
import numpy as np
import copy

windowW = 1200
windowH = 800
Divfac = 2.8e8
movfac = 50



timefac =  1
running = True
 
Masses = [1.9891e30 , 5.9722e24 ] 
planet1pos = [0 , 0]
planet2pos = [1.47e11 , 0]


planet1v0 = [0,  1 , 1]
planet2v0 = [ 30e3 , 0, 1]

sizes = [6.96e9 , 12e8 ]

G = 6.67e-11

class point2d:
    def __init__(self,x=0,y=0):
        self.x = x
        self.y = y
    def __add__(self,point):

        self.x += point.x
        self.y += point.y
        return self
    def __mul__(self,num):
        self.x *= num
        self.y *= num
        return self
    def print(self):
        print(self.x , self.y)
    def __add__(self,vec):
        self.x += vec.magi
        self.y += vec.magj
        return self

def discal(pnt1 , pnt2) :
    dis = math.sqrt(math.pow(pnt2.x- pnt1.x , 2) + math.pow(pnt2.y - pnt1.y  , 2))

    return dis

class vec2d : 
    def __init__(self,mag = 1 , I = 0 ,J = 0):
        self.I = I
        self.J = J
        self.mag = mag
        self.magi = mag * I
        self.magj = mag * J
    def __add__(self,vec) :
        self.magi += vec.magi
        self.magj += vec.magj
        return self
    def __mul__(self , num):
        v = copy.deepcopy(self)
        v.magi *= num
        v.magj *= num
        return v
    def __truediv__(self , num):
        v = copy.deepcopy(self)
        v.magi /= num
        v.magj /= num
        return v 
    def len(self) :
       return discal(point2d(0,0) , point2d (self.magi , self.magj))
    def print(self):
        print(self.magi ,self.magj )
    def norm(self):
        R = discal(point2d(0 , 0)  , point2d (self.I , self.J))
        self.I /= R
        self.J /= R
        self.magi = self.mag * self.I
        self.magj = self.mag * self.J
    def p2v(self , mag , point1 , point2) :
        self.mag = mag
        self.I =((point2.x - point1.x))
        self.J =((point2.y - point1.y))
        self.magi = mag * self.I
        self.magj = mag * self.J

class color : 
    def __init__(self, R ,G ,B , A = 1) :
        self.R = R
        self.G = G
        self.B = B
        self.A = A
class topixel :
    def __init__(self, Divfac , movfac  ):
        self.Divfac = Divfac
        self.movfac = movfac
        self.movR = 0
        self.movU = 0
    def Dis(self ,Dis) :
        return Dis / self.Divfac 
    def movup(self ,pix):
        self.movU += pix * self.movfac
    def movri(self ,pix):
        self.movR += pix * self.movfac
    def movori(self):
        self.movR = 0
        self.movU = 0
    def zomein( self , fac ) :
        self.Divfac /= fac
    def coorx (self , x): 
        return windowW / 2 + x / self.Divfac + self.movR
    def coory (self , y): 
       return windowH / 2 - y / self.Divfac + self.movU
    def drawaxis(self , pg):
       pg.draw.line(window, (165, 201, 204), (self.coorx(0), self.coory(10)),
                    (self.coorx(0), self.coory(-10)))
       pg.draw.line(window, (165, 201, 204), (self.coorx(-10), self.coory(0)),
                   (self.coorx(10), self.coory(0)))
    def renderdis(self , pygame , window):
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render('1pixel =  : ' + str(f'{self.Divfac:.0f}'  ) + " m",
                                      True, (107, 176, 194) ,)
        window.blit(text , ( windowW - 400 ,windowH - 150))


class tme :

    def __init__(self , t0  ,  timefac ,dt = 0 ):
        self.paused = False
        self.meth = 1
        self.t = t0
        self.dt = dt
        self.timefac = timefac
        self.startt = time.time() 
        self.endt = 0
        if dt == 0 : meth = 1 
        else : meth = 2
    def update(self) :
        if self.meth == 1 :

            self.endt = time.time()
            self.dt = (self.endt - self.startt) * self.timefac 
            self.startt = time.time()
        else : 
                self.dt = 0.1

        if self.paused : 
            self.dt = 0
        self.t +=  self.dt 

    def Pause(self) :
        self.paused = not self.paused

    def print(self) :
        print (t , dt)
    def render(self , pygame , window) :
        font = pygame.font.Font('freesansbold.ttf', 32)
        if self.t < 1e-15  :
              text = font.render('time : ' + str(f'{tm.t * 1e15:.9f}' ) + " ns",
                                      True, (107, 176, 194) ,)

        elif self.t >= 60 and self.t <= 86400 :
              text = font.render('time : ' + str(f'{tm.t/ 60:.5f}'  ) + " min",
                                      True, (107, 176, 194) ,)
        elif self.t >= 86400 and self.t <= 31536000:
              text = font.render('time : ' + str(f'{tm.t/ (86400):.5f}'  ) + " days",
                                      True, (107, 176, 194) ,)
        elif self.t >= 31536000 :
              text = font.render('time : ' + str(f'{tm.t/ (31536000 ) :.5f}' ) + " years",
                                      True, (107, 176, 194) ,)
        else : 
              text = font.render('time : ' + str(f'{tm.t:.9f}'  ) + " sec",
                                      True, (107, 176, 194) ,)
        window.blit(text , ( 20 ,windowH - 150))

class trace :
    def __init__(self,) :
        self.px = topixel
        self.a = []
    def addpoint(self , point2d ) :
        if len(self.a) < 1e4 :
            self.a.append((point2d.x, point2d.y))
    def render(self,topixel , pygame , window ,color,width = 1) :
        if len(self.a) > 1 :
            b = [(px.coorx(tup[0]) , px.coory(tup[1])) for tup in self.a]
            pygame.draw.lines(window , (color.R , color.G , color.B) ,False , b ,width  )

class planet :

    def __init__(self , pos = point2d(0 , 0)  ,
                 mass = 1 , size = 1,color = color(0 , 255 , 0)) :
        self.clr = color
        self.pos = pos
        self.mass = mass
        self.size = size
        self.vel = vec2d(0,0 , 0)
        self.acc = vec2d(0,0 , 0)
    def addfrc(self , vecfrc):
        #self.acc.print()
        self.acc = vecfrc / self.mass

        #self.acc.print()
    def addvel(self , vecvel) :
        self.vel += vecvel
    def update(self , dt):

        #print(dt)
        #self.acc *= dt
        #self.acc.print()
        self.vel += self.acc * dt
        #self.vel.print()
        #self.pos = self.pos.addvec(self.vel * dt)
        self.pos += self.vel *dt 
        #self.pos.print()
    def render(self,topixel ,pygame , window) :
        D1 = px.Dis(self.size)
        pygame.draw.circle(window, (self.clr.R , self.clr.G , self.clr.B),
          [px.coorx(pln1.pos.x) , px.coory(pln1.pos.y)],D1 , 0)

def gravforce( pln1 = planet , pln2 = planet) :
        v = vec2d()
        dis = discal(pln1.pos , pln2.pos)
        v.p2v( (G *  pln1.mass * pln2.mass) /   (dis * dis) , pln1.pos , pln2.pos )
        v.norm()
        return v
                     
               
px = topixel(Divfac ,movfac )
pygame.init()
window = pygame.display.set_mode((windowW , windowH))
window.fill((37, 41, 41))

tm = tme(0 , timefac , 0)

pln1 = planet(point2d(planet1pos[0] , planet1pos[1]) ,Masses[0] ,sizes[0] ,color(201, 46, 40))
pln2 = planet(point2d(planet2pos[0] , planet2pos[1]) ,Masses[1],sizes[1] , color(42, 161, 191))
pln1.addvel(vec2d( planet1v0[0] ,planet1v0[1] , planet1v0[2]))
pln2.addvel(vec2d( planet2v0[0] ,planet2v0[1] , planet2v0[2]))
tr = trace()
while running:

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_2:
                tm.timefac *= 10
            if event.key == pygame.K_1:
                tm.timefac *= 0.1
            if event.key == pygame.K_KP_PLUS:
                px.zomein(1.1)
            if event.key == pygame.K_KP_MINUS:
                px.zomein(0.9)
            if event.key == pygame.K_w:
                px.movup(1) 
            if event.key == pygame.K_s:
                px.movup(-1) 
            if event.key == pygame.K_a:
                px.movri(1) 
            if event.key == pygame.K_d:
                px.movri(-1) 
            if event.key == pygame.K_r:
                px.movori()
            if event.key == pygame.K_SPACE:
                tm.Pause()
    window.fill((37, 41, 41))
    #px.drawaxis(pygame)
    tm.update()
    if not tm.paused :
        gforce = gravforce(pln1 , pln2)
        #print(gforce.len())
        #pln1.applyfrc(gforce)
        pln2.addfrc(gforce * -1)
        pln2.vel.print()
        pln2.acc.print()
        #pln2.acc = vec2d(1,0 , 2)
        pln1.update(tm.dt)
        tr.addpoint(pln2.pos)
        pln2.update(tm.dt)
    pln1.render(px, pygame ,window)
    tr.render(px,pygame,window , color(103, 166, 120) , 5)
    px.renderdis(pygame , window)        
    tm.render(pygame , window)
    pygame.display.update()

    


