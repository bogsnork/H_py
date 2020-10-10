import pygame as pg
import os

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
looking = "fw"
flap = 1
flapcount = 1
characterfile = "C:/Users/USER/Documents/Code/orang/orangphoto{}{}.png"
speed = 3
flapspeed = 25
platforms = pg.sprite.Group()
pressed = pg.key.get_pressed()
working = "none yet"
peak = False
weapons = pg.sprite.Group()
totalmove = 0
going = False
playerparts = pg.sprite.Group()
enemies = pg.sprite.Group()
buttons = pg.sprite.Group()
titlefont = pg.font.Font(None, 115)
smallText = pg.font.Font(None,20)

def text_objects(text, font):
    textSurface = font.render(text, True, (0, 0, 0))
    return textSurface, textSurface.get_rect()



def gameover():
    for sprite in all_sprites:
        sprite.kill()

def flapcalc():
    global flapcount
    if flapcount == flapspeed:
        global flap
        if flap < 4:
            flap += 1
        else:
            flap = 1
        flapcount = 1
    elif flapcount < flapspeed:
        flapcount += 1

def game_intro():
    global intro
    intro = True

    while intro:
        for event in pg.event.get():
            #print(event)
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                
                intro = False
        screen.fill((255, 255, 255))
        
        textSurf, textRect = text_objects("Title", titlefont)
        textRect.center = ((SCREENWIDTH/2),(SCREENHEIGHT/2))
        screen.blit(textSurf, textRect)

        for i in all_sprites:
            i.update()

        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)


        #pg.draw.rect(screen, (0, 0, 0),(350,450,100,50))
        #pg.draw.rect(screen, (0, 0, 0),(550,450,100,50))

        pg.display.update()

class button(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        
        self.surf = pg.Surface((100, 50))
        self.surf.fill((0, 0, 0))
        self.rect = self.surf.get_rect(center = (SCREENWIDTH/2, bgheight/2))
        self.textSurf, self.textRect = text_objects("GO!", smallText)
        self.textRect.center = ( self.rect.center )
        self.surf.blit(self.textSurf, self.textRect)
        
        all_sprites.add(self)
        buttons.add(self)

    def setloc(self, x, y):
        
        self.rect.bottomleft = x,y
        
    def setsize(self, height, width):
        self.rect.height = height
        self.rect.width = width
        self.surf = pg.Surface((width, height))
        self.surf.fill((0, 0, 0))
    def update(self):
        mouse = pg.mouse.get_pos()

        #print(mouse)

        if self.rect.right > mouse[0] > self.rect.left and self.rect.bottom > mouse[1] > self.rect.top:
            self.surf.fill((0, 0, 0))
        else:
            self.surf.fill((56, 56, 56))
        self.surf.blit(self.textSurf, self.textRect)

class weapon(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("C:/Users/USER/Documents/Code/orang/knotspriteempty.png")
        self.surf = pg.image.load("C:/Users/USER/Documents/Code/orang/knotspriteempty.png")
        
        self.rect = self.image.get_rect()

        self.weight = 5
        self.acc = int(orang.throwstrength)
        
        all_sprites.add(self)
        weapons.add(self)
    def attack(self,player):
        
        
        self.surf = pg.image.load("C:/Users/USER/Documents/Code/orang/knotsprite.png")
        self.pos = vec(player.rect.topright)
        #self.pos.y -= player.rect.centery
        
        
        
        if looking == "fw":
            self.pos.x -= 10
        
        if looking == "bw":
            self.pos.x -= 120
        
        
        #while not self.pos.x - playerloc.x >= 100:# or not player.rect.contains(self.rect):
        #    self.pos.x += 1
        #    self.rect.center = self.pos
    def update(self):
        self.movecalc(orang)
    def movecalc(self, player):
        global peak
        global going
        global working
        global totalmove
        playerloc = vec(player.rect.center)
        attackspeed = player.attackspeed
        hits = pg.sprite.spritecollide(self, platforms, False)
        returnspeed = player.returnspeed

        if going == True:
            if self.acc > 0:
                if looking == "fw":
                    self.pos.x += attackspeed
                    
                if looking == "bw":
                    self.pos.x -= attackspeed
                
                if self.pos.x > playerloc.x:
                    self.pos.x += attackspeed
                if self.pos.x < playerloc.x:
                    self.pos.x -= attackspeed
                self.acc -= 10
                
                
                
            elif peak:
                peak = True
                if self.pos.x > playerloc.x:
                    self.pos.x -= returnspeed
                if self.pos.x < playerloc.x:
                    self.pos.x += returnspeed
                if self.pos.y > playerloc.y:
                    self.pos.y -= returnspeed
                if self.pos.y < playerloc.y:
                    self.pos.y += returnspeed
            
            if not peak:
                if hits:
                    if self.pos.y < hits[0].rect.bottom:  
                        peak = True
                if self.acc == 0 and not peak:
                    self.pos.y += GRAV*self.weight*1.5


            self.pos.y += GRAV*self.weight
            self.rect.center = self.pos
                
            if player.rect.contains(self.rect):
                peak = False
                self.surf = pg.image.load("C:/Users/USER/Documents/Code/orang/knotspriteempty.png")
                going = False
                self.kill()
class player(pg.sprite.Sprite):
    x = 30
    y = 300
    
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        
        char = get_image(characterfile.format(looking,flap))
        
        self.image = char
        self.surf = pg.image.load("C:/Users/USER/Documents/Code/orang/orangphotofw1.png")
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
        
        self.jumping = False

        playerparts.add(self)
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
            knot =  weapon()
        
        
        knot.attack(self)
    
    def update(self):
        global flapspeed
        global working
        global looking

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
        
        pressed = pg.key.get_pressed()


        
        
        if pressed[pg.K_LEFT]:
            looking = "bw"
            #x -= speed
            self.acc.x = -ACC
            flapspeed = 15
            flapcalc()
            
        elif pressed[pg.K_RIGHT]:
            self.acc.x = ACC
            
            looking = "fw"
            #x += speed
            flapspeed = 15
            flapcalc()
        else:
            flapspeed = 25
            flapcalc()
        if pressed[pg.K_RSHIFT]: 
            self.acc.x *= 2
            flapspeed = 5
        if pressed[pg.K_LSHIFT]: 
            flapspeed = 5
            self.acc.x *= 2
        
        self.collidecheck()
        self.iframe -= 1

        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        

        if self.pos.x > SCREENWIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = SCREENWIDTH

        self.surf = get_image(characterfile.format(looking,flap))
        
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
    
    


class enemy(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        
        self.imageroot = "C:/Users/USER/Documents/Code/lizard{}.png"
        
        self.image = pg.image.load("C:/Users/USER/Documents/Code/lizard1.png")
        self.surf = pg.image.load("C:/Users/USER/Documents/Code/lizard1.png")
        
        self.pos = vec((500, 600))#SCREENHEIGHT-bgheight))
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.weight = 1
        
        self.hp = 3
        self.attackspeed = 4
        self.returnspeed = 9
        self.throwstrength = 150
        self.jumpower = 23
        
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

        if self.rect.right > SCREENWIDTH:
            
            
            self.surf = pg.transform.flip(self.surf, True, False)
            self.forward = False
            self.pos.x -= 5

        if self.rect.left < 0:
            
            self.surf = pg.transform.flip(self.surf, True, False)
            self.forward = True
            self.pos.x += 5
            
        if self.forward:
            self.acc.x = ACC
        elif not self.forward:
            self.acc.x = -ACC

        if self.stepcount > 10:
            self.step = not self.step
            self.stepcount = 0
            self.surf = get_image(self.imageroot.format(int(self.step)))
            if not self.forward:
                self.surf = pg.transform.flip(self.surf, True, False)


        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        
        self.stepcount += 1 
        self.iframe -= 1

        global working
        working = int(self.step)

        

        self.rect.midbottom = self.pos
        #if self.looking = "fw":

    
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

but1 = button()
but2 = button()
but1.setloc(350,450)
but2.setloc(550,450)

game_intro()

floor = platform()
plat1 = platform()
floor.setloc(0, SCREENHEIGHT)
bg1 = background()
bg1.setloc(0, SCREENHEIGHT-bgheight)
plat1.setloc(500, 500)
plat1.setsize(30, 200)

liz1 = enemy()
orang = player()

print(working)
while not done:
        #event loop
        for event in pg.event.get():
                
                if event.type == pg.QUIT:
                    done = True
                if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                    print(pg.font.get_fonts)
                    #orang.kill()
                    game_intro()
                if event.type == pg.KEYDOWN and event.key == pg.K_UP:
                    orang.jump()
                if event.type == pg.KEYDOWN and event.key == pg.K_DOWN:
                    orang.cancel_jump()
                if event.type == pg.KEYDOWN and event.key == pg.K_z:
                    if going == False:
                        orang.attack()
                        going = True


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

#small change