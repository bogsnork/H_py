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
 
SCREENHEIGHT = 500
SCREENWIDTH = 1000
ACC = 0.5
FRIC = -0.12
FPS = 60
screen = pg.display.set_mode((SCREENWIDTH, SCREENHEIGHT)) 
pg.display.set_caption("Game so far")

all_sprites = pg.sprite.Group()
done = False
is_blue = True
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
pressed = pg.key.get_pressed()
working = "none yet"

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

class player(pg.sprite.Sprite):
    x = 30
    y = 300
    
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        
        char = get_image(characterfile.format(looking,flap))
        
        self.image = char
        self.surf = pg.image.load("C:/Users/USER/Documents/Code/orang/orangphotofw1.png")
        self.rect = self.image.get_rect()
        
        self.pos = vec((10, 385))
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        
        all_sprites.add(self)
    def movecalc(self):
        #global x
        

        self.acc = vec(0,0)
        global working
        global looking
        working += "movecalc"
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
        if pressed[pg.K_RSHIFT]: 
            self.acc.x *= 2
            flapspeed = 5
        if pressed[pg.K_LSHIFT]: 
            flapspeed = 25
            self.acc.x *= 2
        

        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        #self.rect = (x, y)
        if self.pos.x > SCREENWIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = SCREENWIDTH
        working = str(self.pos)+str(self.acc)+str(self.vel)
        self.rect.midbottom = self.pos
class platform(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        
        self.surf = pg.Surface((SCREENWIDTH, bgheight))
        self.surf.fill((bgcolour))
        self.rect = self.surf.get_rect(center = (SCREENWIDTH/2, bgheight/2))
        all_sprites.add(self)
    #def setloc(x,y):




orang = player()
floor = platform()

print(working)
while not done:
        #event loop
        for event in pg.event.get():
                
                if event.type == pg.QUIT:
                    done = True
                if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                    print(working)
                    print(pressed)

                '''if event.type == pg.KEYDOWN and (event.key == pg.K_RIGHT):
                    print(working)
                    orang.movecalc()'''
                
        #game logic

        
        orang.movecalc()




        
        #drawing
        screen.fill((0, 0, 0))
        
        #pg.draw.rect(screen, bgcolour, pg.Rect(0, 470, SCREENWIDTH, bgheight))
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)
        
        pg.display.update()
        pg.display.flip()
        clock.tick(FPS)

#small change