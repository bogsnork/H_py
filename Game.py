import pygame as pg
import os
from ui import button, text

_image_library = {}
def get_image(path):
        global _image_library
        image = _image_library.get(path)
        if image == None:
                canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
                image = pg.image.load(canonicalized_path)
                _image_library[path] = image
        return image





pg.init()
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
titlefont = pg.font.Font(None, 115)
#buttontext = pg.font.Font(None,55)
invsprites = pg.sprite.Group()
pausesprites = pg.sprite.Group()

def text_objects(text, font):
    textSurface = font.render(text, True, (0, 0, 0))
    return textSurface, textSurface.get_rect()

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
    invsprites.add(invtitle)

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

""" class text(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        
        self.col = (0, 0, 0)
        self.cont = " Start"
        self.surf = pg.font.Font.render(titlefont, self.cont, False, self.col)
        self.rect = self.surf.get_rect(center = (SCREENWIDTH/2, bgheight/2))
        
        all_sprites.add(self)
        

    def setloc(self, x, y):
        
        self.rect.bottomleft = x,y
        
    def setsize(self, width, height):
        self.rect.height = height
        self.rect.width = width
        self.surf = pg.Surface((width, height))
        self.surf.fill((0, 0, 0))
    def settext(self, text, col):
        self.cont = (text)
        self.col = col
    def update(self):


        self.surf = pg.font.Font.render(titlefont, self.cont, False, self.col)

         """



class weapon(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("knotspriteempty.png")
        self.surf = pg.image.load("knotspriteempty.png")
        
        self.rect = self.image.get_rect()
        
        self.going = True
        self.peak = False
        self.weight = 5
        self.acc = int(orang.throwstrength)
        
        all_sprites.add(self)
        weapons.add(self)
    def attack(self,player):
        
        
        self.surf = pg.image.load("knotsprite.png")
        self.pos = vec(player.rect.topright)
        #self.pos.y -= player.rect.centery
        
        
        
        if player.looking == "fw":
            self.pos.x -= 10
        
        if player.looking == "bw":
            self.pos.x -= 120
        
        
        #while not self.pos.x - playerloc.x >= 100:# or not player.rect.contains(self.rect):
        #    self.pos.x += 1
        #    self.rect.center = self.pos
    def update(self):
        self.movecalc(orang)
    def movecalc(self, player):
        
        global working
        
        

        playerloc = vec(player.rect.center)
        attackspeed = player.attackspeed
        hits = pg.sprite.spritecollide(self, platforms, False)
        returnspeed = player.returnspeed

        if self.going == True:
            if self.acc > 0:
                if player.looking == "fw":
                    self.pos.x += attackspeed
                    
                if player.looking == "bw":
                    self.pos.x -= attackspeed
                
                if self.pos.x > playerloc.x:
                    self.pos.x += attackspeed
                if self.pos.x < playerloc.x:
                    self.pos.x -= attackspeed
                self.acc -= 10
                
                
                
            elif self.peak:
                self.peak = True
                if self.pos.x > playerloc.x:
                    self.pos.x -= returnspeed
                if self.pos.x < playerloc.x:
                    self.pos.x += returnspeed
                if self.pos.y > playerloc.y:
                    self.pos.y -= returnspeed
                if self.pos.y < playerloc.y:
                    self.pos.y += returnspeed
            
            if not self.peak:
                if hits:
                    if self.pos.y < hits[0].rect.bottom:  
                        self.peak = True
                if self.acc == 0 and not self.peak:
                    self.pos.y += GRAV*self.weight*1.5


            self.pos.y += GRAV*self.weight
            self.rect.center = self.pos
                
            if player.rect.contains(self.rect):
                self.peak = False
                self.surf = pg.image.load("knotspriteempty.png")
                self.going = False
                self.kill()
class player(pg.sprite.Sprite):
    x = 30
    y = 300
    
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        
        self.characterfile = "orangphoto{}{}.png"
        self.flap = 1
        self.looking = "fw"

        char = get_image(self.characterfile.format(self.looking,self.flap))
        
        self.image = char
        self.surf = pg.image.load("orangphotofw1.png")
        self.rect = self.image.get_rect()
        
        self.pos = vec((10, 490))
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        
        self.weight = 1
        self.iframe = 0

        self.hp = 3
        self.attackspeed = 4
        self.returnspeed = 9
        self.throwstrength = 150
        self.jumpower = 23
        self.flapcount = 1
        
        self.flapspeed = 25

        self.jumping = False

        
        all_sprites.add(self)
    def jump(self): 
        hits = pg.sprite.spritecollide(self, platforms, False)
        if hits and not self.jumping:
           self.jumping = True
           self.vel.y = -self.jumpower
 
    def cancel_jump(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3

    def attack(self):
        if not weapons.has():
            knot = weapon()
            knot.attack(self)
    
    def update(self):
        self.acc = vec(0,GRAV*self.weight)
        hits = pg.sprite.spritecollide(self , platforms, False)
        if self.vel.y > 0:
            if hits:
                if self.pos.y < hits[0].rect.bottom:               
                    self.pos.y = hits[0].rect.top +1
                    self.vel.y = 0
                    self.jumping = False
            
        if self.hp == 0:
            self.kill()
            gameover()
        
        pressed = pg.key.get_pressed()


        
        
        if pressed[pg.K_LEFT]:
            self.looking = "bw"
            #x -= speed
            self.acc.x = -ACC
            #self.flapspeed = 15
            #self.flapcalc()
            
        elif pressed[pg.K_RIGHT]:
            self.acc.x = ACC
            
            self.looking = "fw"
            #x += speed
            #self.flapspeed = 15
            #self.flapcalc()
        #else:
            #self.flapspeed = 25
            #self.flapcalc()
        if pressed[pg.K_RSHIFT]: 
            self.acc.x *= 2
            #self.flapspeed = 5
        if pressed[pg.K_LSHIFT]: 
            #self.flapspeed = 5
            self.acc.x *= 2
        

        self.flapspeed = 25/((self.vel.x**2 + self.vel.y**2)**0.5 + 0.5)
        self.flapcalc()

        self.collidecheck()
        self.iframe -= 1

        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        

        if self.pos.x > SCREENWIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = SCREENWIDTH

        self.surf = get_image(self.characterfile.format(self.looking,self.flap))
        
        self.rect.midbottom = self.pos
    def collidecheck(self):
        hit = pg.sprite.spritecollide(self, enemies, False)
        if hit and self.iframe <= 0:
            for enemy in enemies:
                if enemy.aggro:    
                    self.hp -= 1
                    print(self.hp)
                    print(enemy.hp)
                    self.iframe = 120
    def flapcalc(self):
    
        if self.flapcount >= self.flapspeed:
            
            if self.flap < 4:
                self.flap += 1
            else:
                self.flap= 1
            self.flapcount = 1
        elif self.flapcount < self.flapspeed:
            self.flapcount += 1
    


class enemy(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        
        self.imageroot = "lizard{}.png"
        
        self.image = pg.image.load("lizard1.png")
        self.surf = pg.image.load("lizard1.png")
        
        self.pos = vec((500, 600))#SCREENHEIGHT-bgheight))
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.weight = 1
        
        self.hp = 3
        self.attackspeed = 4
        self.returnspeed = 9
        self.throwstrength = 150
        self.jumpower = 23
        
        self.moving = True
        self.aggro = False
        self.iframe = 0
        self.step = 0
        self.stepcount = 10
        self.forward = True
        self.jumping = False

        #self.surf = pg.transform.scale(self.surf, (200,100))
        self.rect = self.image.get_rect()
        all_sprites.add(self)
        enemies.add(self)
    def update(self):
        self.acc = vec(0,GRAV*self.weight)

        hits = pg.sprite.spritecollide(self , platforms, False)
        if self.vel.y > 0:
            if hits:
                if self.pos.y < hits[0].rect.bottom:               
                    self.pos.y = hits[0].rect.top +1
                    self.vel.y = 0
                    self.jumping = False
        
        hit = pg.sprite.spritecollide(self , weapons, False)
        if hit and self.iframe <= 0:
            self.hp -= 1
            self.iframe = 50
            self.aggro = True
            print(self.aggro)
        


        if self.hp <= 0:
            self.kill()

        if self.rect.right > SCREENWIDTH :
            
            
            self.surf = pg.transform.flip(self.surf, True, False)
            self.forward = False
            self.pos.x -= 5

        if self.rect.left < 0:
            
            self.surf = pg.transform.flip(self.surf, True, False)
            self.forward = True
            self.pos.x += 5

        if not self.aggro and self.moving:    
            if self.forward:
                self.acc.x = ACC
            elif not self.forward:
                self.acc.x = -ACC
        else:
            if self.pos.x < orang.pos.x:
                if self.forward:
                    self.surf = pg.transform.flip(self.surf, True, False)
                    self.forward = False
                    self.acc.x = -ACC
                elif not self.forward:
                    self.acc.x = -ACC
            if self.pos.x > orang.pos.x:
                if self.forward:
                    self.acc.x = ACC
                elif not self.forward:
                    self.surf = pg.transform.flip(self.surf, True, False)
                    self.forward = True
                    self.acc.x = ACC
            if self.rect.right > SCREENWIDTH:
                self.moving = False

            if self.rect.left < 0:
                self.moving = False


        if self.stepcount > 10 and self.moving:
            self.step = not self.step
            self.stepcount = 0
            self.surf = get_image(self.imageroot.format(int(self.step)))
            if not self.forward:
                self.surf = pg.transform.flip(self.surf, True, False)

        if self.moving:
            self.acc.x += self.vel.x * FRIC
            self.vel += self.acc
            self.pos += self.vel + 0.5 * self.acc
        else:
            self.surf = get_image(self.imageroot.format(2))
            if not self.forward:
                self.surf = pg.transform.flip(self.surf, True, False)

        self.stepcount += 1 
        self.iframe -= 1

        global working
        working = int(self.step)

        
        
        self.rect.midbottom = self.pos
        

    
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

    liz1 = enemy()
    global orang
    orang = player()
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