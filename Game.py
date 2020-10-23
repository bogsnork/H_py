import pygame as pg
import os
from ui import text_objects, button, text
from sprites import player, weapon, enemy, get_image




pg.init()

# helper functions and variables
clock = pg.time.Clock()
vec = pg.math.Vector2  # 2 for two dimensional
 
SCREENHEIGHT = 700
SCREENWIDTH = 1000
ACC = 0.5
FRIC = -0.12
GRAV = 1
FPS = 60
screen = pg.display.set_mode((SCREENWIDTH, SCREENHEIGHT)) 
pg.display.set_caption("Game so far")

all_sprites = pg.sprite.Group()
done = False

x = 30
y = 300
bgheight = 30
bgcolour = (251, 180, 92)
platcolour = bgcolour
pressed = pg.key.get_pressed()
working = "none yet"
playerparts = pg.sprite.Group()
enemies = pg.sprite.Group()
buttons = pg.sprite.Group()
platforms = pg.sprite.Group()
weapons = pg.sprite.Group()
loot = pg.sprite.Group()
titlefont = pg.font.Font(None, 115)
invfont = pg.font.Font(None,55)
invsprites = pg.sprite.Group()
pausesprites = pg.sprite.Group()
bones = 0


def end_intro():
    for i in all_sprites:
        i.kill()
    gameloopfirst()

def game_intro():
    for sprite in all_sprites:
        sprite.kill()
    
    but1 = button(screen, SCREENWIDTH, SCREENHEIGHT, all_sprites, buttons)
    but2 = button(screen, SCREENWIDTH, SCREENHEIGHT, all_sprites, buttons)
    but1.setloc(350,450)
    but1.setbut(" Start", end_intro)
    but2.setloc(550,450)
    but2.setbut(" Quit", quit)

    #global intro
    intro = True

    while intro:
        for event in pg.event.get():
            #print(event)
            if event.type == pg.QUIT:
                #pg.quit()
                quit()

        screen.fill((255, 255, 255))
        
        textSurf, textRect = text_objects("Title", titlefont)
        textRect.center = ((SCREENWIDTH/2),(SCREENHEIGHT/2))
        screen.blit(textSurf, textRect)

        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)
        for entity in buttons:
            screen.blit(entity.textSurf, entity.textRect)

        for i in all_sprites:
            i.update()

        
        #for i in buttons:
         #   screen.blit(i.textSurf, i.textRect)

        #pg.draw.rect(screen, (0, 0, 0),(350,450,100,50))
        #pg.draw.rect(screen, (0, 0, 0),(550,450,100,50))

        pg.display.update()

def reset():
    for sprite in all_sprites:
        sprite.kill()

    gameloopfirst()

def gameover():
    for sprite in all_sprites:
        sprite.kill()
    quitbut = button(screen, SCREENWIDTH, SCREENHEIGHT, all_sprites, buttons)
    rebut = button(screen, SCREENWIDTH, SCREENHEIGHT, all_sprites, buttons)
    titlebut = button(screen, SCREENWIDTH, SCREENHEIGHT, all_sprites, buttons)
    
    quitbut.setbut("Quit", quit)
    rebut.setbut("Retry", reset)
    titlebut.setbut("Return to title", game_intro)

    titlebut.setsize(255, 45)

    quitbut.setloc(SCREENWIDTH/2 - 50, 450)
    titlebut.setloc((SCREENWIDTH/2) - 125, 500)
    rebut.setloc((SCREENWIDTH/2) - 50, 550)

    dead = True

    while dead:
        for event in pg.event.get():
            #print(event)
            if event.type == pg.QUIT:
                pg.quit()
                quit()

        screen.fill((255, 255, 255))
        
        textSurf, textRect = text_objects("Game over", titlefont)
        textRect.center = ((SCREENWIDTH/2),(SCREENHEIGHT/2))
        screen.blit(textSurf, textRect)

        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)
        for entity in buttons:
            screen.blit(entity.textSurf, entity.textRect)


        for i in all_sprites:
            i.update()

        pg.display.update()

def resume():
    pause = False
    for i in pausesprites:
        i.kill() 
    gameloop()

def pause():
    pause= True
    pausetitle = text(SCREENWIDTH, all_sprites, titlefont)
    pausetitle.settext("Pause", (0, 0, 0))
    quitbut = button(screen, SCREENWIDTH, SCREENHEIGHT, all_sprites, buttons)
    rebut = button(screen, SCREENWIDTH, SCREENHEIGHT, all_sprites, buttons)
    titlebut = button(screen, SCREENWIDTH, SCREENHEIGHT, all_sprites, buttons)
    
    quitbut.setbut("Quit", quit)
    rebut.setbut("Resume", resume)
    titlebut.setbut("Return to title", game_intro)

    titlebut.setsize(255, 45)
    rebut.setsize(150, 45)

    pausetitle.setloc(SCREENWIDTH/2 - 115, SCREENHEIGHT/2)
    rebut.setloc((SCREENWIDTH/2) - 75, 450)
    titlebut.setloc((SCREENWIDTH/2) - 125, 500)
    quitbut.setloc(SCREENWIDTH/2 - 50, 550)

    pausesprites.add(pausetitle)
    pausesprites.add(quitbut)
    pausesprites.add(rebut)
    pausesprites.add(titlebut)

    while pause:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit()
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                pause = False
                for i in pausesprites:
                    i.kill() 


        for i in pausesprites:
            i.update()

        screen.fill((255, 255, 255))
        for i in pausesprites:
            screen.blit(i.surf, i.rect)
        for entity in buttons:
            screen.blit(entity.textSurf, entity.textRect)

        pg.display.update()

def openinv():
    inv = True
    invtitle = text(SCREENWIDTH, all_sprites, titlefont)
    invtitle.settext("Inventory", (255, 255, 255))
    invtitle.setloc(350, 100)
    invsprites.add(invtitle)

    bonecount = text(SCREENWIDTH, all_sprites, invfont)
    bonecount.settext(str(orang.bones), (255, 255, 255))
    bonecount.setloc(0, 150)
    invsprites.add(bonecount)

    while inv:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit()
            if event.type == pg.KEYDOWN and event.key == pg.K_e:
                inv = False
                for i in invsprites:
                    i.kill() 

        for i in invsprites:
            i.update()

        screen.fill((0, 0, 0))
        for i in invsprites:
            screen.blit(i.surf, i.rect)
        pg.display.update()



    
class platform(pg.sprite.Sprite):
    
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        
        self.surf = pg.Surface((SCREENWIDTH, bgheight))
        self.surf.fill((platcolour))
        self.rect = self.surf.get_rect(center = (SCREENWIDTH/2, bgheight/2))
        all_sprites.add(self)
        platforms.add(self)
    def setloc(self, x, y):
        
        self.rect.bottomleft = x,y
        
    def setsize(self, height, width):
        self.rect.height = height
        self.rect.width = width
        self.surf = pg.Surface((width, height))
        self.surf.fill((platcolour))

class background(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        
        self.surf = pg.Surface((SCREENWIDTH, bgheight))
        self.surf.fill((bgcolour))
        self.rect = self.surf.get_rect(center = (SCREENWIDTH/2, bgheight/2))
        all_sprites.add(self)
    def setloc(self, x, y):
        
        self.rect.bottomleft = x,y
        
    def setsize(self, height, width):
        self.rect.height = height
        self.rect.width = width
        self.surf = pg.Surface((width, height))
        self.surf.fill((bgcolour))

def gameloopfirst():
    floor = platform()
    plat1 = platform()
    floor.setloc(0, SCREENHEIGHT)
    bg1 = background()
    bg1.setloc(0, SCREENHEIGHT-bgheight)
    plat1.setloc(500, 500)
    plat1.setsize(30, 200)

    global orang
    orang = player(all_sprites, platforms, enemies, weapons, loot, GRAV, FRIC, ACC, SCREENWIDTH, bones)
    liz1 = enemy(orang, all_sprites, platforms, enemies, weapons, loot, GRAV, FRIC, ACC, SCREENWIDTH)
    global done
    while not done:
        #event loop
        for event in pg.event.get():
                
            if event.type == pg.QUIT:
                #done = True
                quit()
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                    #print(pg.font.get_fonts())
                #orang.kill()
                
                print(pausetitle.cont)
            if event.type == pg.KEYDOWN and event.key == pg.K_UP:
                orang.jump()
            if event.type == pg.KEYDOWN and event.key == pg.K_DOWN:
                orang.cancel_jump()
            if event.type == pg.KEYDOWN and event.key == pg.K_z:
                orang.attack()
            if event.type == pg.KEYDOWN and event.key == pg.K_e:   
                openinv()     
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                pause()

        #game logic

        
        for i in all_sprites:
            i.update()

        if not orang.alive():
            gameover()


        #drawing
        screen.fill((0, 0, 0))
        
        #pg.draw.rect(screen, platcolour, pg.Rect(0, (SCREENHEIGHT-60), SCREENWIDTH, bgheight))
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)
        if weapons.has():
            rope = pg.draw.line(screen,(120, 90, 22), orang.rect.center, knot.pos)
            screen.blit(rope)
        pg.display.update()
        pg.display.flip()
        clock.tick(FPS)

def gameloop():
    global done
    while not done:
        #event loop
        for event in pg.event.get():
                
            if event.type == pg.QUIT:
                #done = True
                quit()
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                    #print(pg.font.get_fonts())
                #orang.kill()
                
                print(pausetitle.cont)
            if event.type == pg.KEYDOWN and event.key == pg.K_UP:
                orang.jump()
            if event.type == pg.KEYDOWN and event.key == pg.K_DOWN:
                orang.cancel_jump()
            if event.type == pg.KEYDOWN and event.key == pg.K_z:
                orang.attack()
            if event.type == pg.KEYDOWN and event.key == pg.K_e:   
                openinv()     
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                pause()

        #game logic

        
        for i in all_sprites:
            i.update()

        if not orang.alive():
            gameover()


        #drawing
        screen.fill((0, 0, 0))
        
        #pg.draw.rect(screen, platcolour, pg.Rect(0, (SCREENHEIGHT-60), SCREENWIDTH, bgheight))
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)
        if weapons.has():
            rope = pg.draw.line(screen,(120, 90, 22), orang.rect.center, knot.pos)
            screen.blit(rope)
        pg.display.update()
        pg.display.flip()
        clock.tick(FPS)

game_intro()



print(working)


#small change