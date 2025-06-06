import pygame as pg
import time
import datetime
import math

pg.init()
RES = WIDTH ,HEIGHT = 1000,1000
midle = WIDTH//2 , HEIGHT//2
RADIUS = 1000

screen = pg.display.set_mode((RES))
clock = pg.time.Clock()

pg.display.set_caption("Mickey Clock")

sec = pg.image.load("pict/leftarm.png").convert_alpha()
minute = pg.image.load("pict/rightarm.png").convert_alpha()
rectsec = sec.get_rect()
rectmin = minute.get_rect()
rectmin.center = rectsec.center = midle

background = pg.image.load("pict/mainclock.png")
run =True

angle1 = 0
angle2 = 0
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
    #system time
    time = datetime.datetime.now()
    minuteTime = time.minute
    secondTime = time.second

    #minute
    angle1 = -minuteTime*6 #6 is degree
    leg1 = pg.transform.rotate(minute, angle1)
    rect1 = leg1.get_rect()
    rect1.center = rectmin.center

    #second
    angle2 = -secondTime*6 #6 is degree
    leg2 = pg.transform.rotate(sec, angle2)
    rect2 = leg2.get_rect()
    rect2.center = rectsec.center

    #output
    screen.blit(background, (-200, -20))
    screen.blit(leg1, rect1)
    screen.blit(leg2, rect2)
    

    pg.display.flip()
    clock.tick(60)