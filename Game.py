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
GRAV = 0.5
FPS = 60
screen = pg.display.set_mode((SCREENWIDTH, SCREENHEIGHT)) 
pg.display.set_caption("Game so far")

all_sprites = pg.sprite.Group()
done = False

x = 30
y = 300
bgheight = 30
bgcolour = (135,150,74)
looking = "fw"
flap = 1
flapcount = 1
characterfile = "C:/Users/USER/Documents/Code/orang/orangphoto{}{}.png"
speed = 3
flapspeed = 25
platforms = pg.sprite.Group()
pressed = pg.key.get_pressed()
working = "none yet"
attackspeed = 5
attackdist = 100
peak = False
weapons = pg.sprite.Group()
totalmove = 0

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

class weapon(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("C:/Users/USER/Documents/Code/orang/knotspriteempty.png")
        self.surf = pg.image.load("C:/Users/USER/Documents/Code/orang/knotspriteempty.png")
        
        self.rect = self.image.get_rect()
        all_sprites.add(self)
        weapons.add(self)
    def attack(self,player):
        
        
        self.surf = pg.image.load("C:/Users/USER/Documents/Code/orang/knotsprite.png")
        self.pos = vec(player.pos)
        self.pos.y -= player.rect.height/2
        if looking == "fw":
            self.pos.x += 60
        if looking == "bw":
            self.pos.x -= 60
        global totalmove
        totalmove = 0
        #while not self.pos.x - playerloc.x >= 100:# or not player.rect.contains(self.rect):
        #    self.pos.x += 1
        #    self.rect.center = self.pos
    def update(self):
        self.movecalc(orang)
    def movecalc(self, player):
        global peak
        global going
        global totalmove
        playerloc = vec(player.rect.center)
        if going == True:
            if totalmove < 100 and not peak:
                if looking == "fw":
                    self.pos.x += attackspeed
                if looking == "bw":
                    self.pos.x -= attackspeed
                
                if self.pos.x > playerloc.x:
                    self.pos.x += attackspeed
                if self.pos.x < playerloc.x:
                    self.pos.x -= attackspeed
                
                totalmove += 10
                
                self.rect.center = self.pos
            elif  totalmove >= attackdist or peak:
                peak = True
                if self.pos.x > playerloc.x:
                    self.pos.x -= attackspeed
                if self.pos.x < playerloc.x:
                    self.pos.x += attackspeed
                if self.pos.y > playerloc.y:
                    self.pos.y -= attackspeed
                if self.pos.y < playerloc.y:
                    self.pos.y += attackspeed
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
        
        self.jumping = False

        all_sprites.add(self)
    def jump(self): 
        hits = pg.sprite.spritecollide(self, platforms, False)
        if hits and not self.jumping:
           self.jumping = True
           self.vel.y = -15
 
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

        self.acc = vec(0,GRAV)
        hits = pg.sprite.spritecollide(self , platforms, False)
        if self.vel.y > 0:
            if hits:
                if self.pos.y < hits[0].rect.bottom:               
                    self.pos.y = hits[0].rect.top +1
                    self.vel.y = 0
                    self.jumping = False
            
        
        
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
        
        

        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        

        if self.pos.x > SCREENWIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = SCREENWIDTH

        self.surf = get_image(characterfile.format(looking,flap))
        
        self.rect.midbottom = self.pos


    
class platform(pg.sprite.Sprite):
    
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        
        self.surf = pg.Surface((SCREENWIDTH, bgheight))
        self.surf.fill((bgcolour))
        self.rect = self.surf.get_rect(center = (SCREENWIDTH/2, bgheight/2))
        all_sprites.add(self)
        platforms.add(self)
    def setloc(self, x, y):
        global working
        self.rect.bottomleft = x,y
        #working = self.rect
    def setsize(self, height, width):
        self.rect.height = height
        self.rect.width = width
        self.surf = pg.Surface((width, height))
        self.surf.fill((bgcolour))

floor = platform()
orang = player()

plat1 = platform()
floor.setloc(0, SCREENHEIGHT)
plat1.setloc(500, 500)
plat1.setsize(30, 200)

print(working)
while not done:
        #event loop
        for event in pg.event.get():
                
                if event.type == pg.QUIT:
                    done = True
                if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                    print(working)
                if event.type == pg.KEYDOWN and event.key == pg.K_UP:
                    orang.jump()
                if event.type == pg.KEYDOWN and event.key == pg.K_DOWN:
                    orang.cancel_jump()
                if event.type == pg.KEYDOWN and event.key == pg.K_z:
                    orang.attack()
                    going = True


        #game logic

        
        for i in all_sprites:
            i.update()



        
        #drawing
        screen.fill((0, 0, 0))
        
        pg.draw.rect(screen, bgcolour, pg.Rect(0, (SCREENHEIGHT-60), SCREENWIDTH, bgheight))
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)
        if weapons.has():
            rope = pg.draw.line(screen,(120, 90, 22), orang.rect.center, knot.pos)
            screen.blit(rope)
        pg.display.update()
        pg.display.flip()
        clock.tick(FPS)

#small change