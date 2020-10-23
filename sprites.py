#module: sprites

import pygame as pg
import os

# functions
vec = pg.math.Vector2  # 2 for two dimensional
_image_library = {}

def get_image(path):
        global _image_library
        image = _image_library.get(path)
        if image == None:
                canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
                image = pg.image.load(canonicalized_path)
                _image_library[path] = image
        return image
# classes

class player(pg.sprite.Sprite):
    x = 30
    y = 300
    
    def __init__(self, all_sprites, platforms, enemies, weapons, loot, GRAV, FRIC, ACC, SCREENWIDTH, bones):
        pg.sprite.Sprite.__init__(self)
        
        self.characterfile = "sprites/orangphotofw{}.png"
        self.flap = 1
        self.looking = "fw"

        char = get_image(self.characterfile.format(self.flap))
        
        self.image = char
        self.surf = pg.image.load("sprites/orangphotofw1.png")
        self.rect = self.image.get_rect()
        
        self.all_sprites = all_sprites
        self.platforms = platforms
        self.enemies = enemies
        self.weapons = weapons
        self.loot = loot
        self.bones = bones
        self.GRAV = GRAV
        self.FRIC = FRIC
        self.ACC = ACC
        self.SCREENWIDTH = SCREENWIDTH


        self.pos = vec((100, 960))
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
        hits = pg.sprite.spritecollide(self, self.platforms, False)
        if hits and not self.jumping:
           self.jumping = True
           self.vel.y = -self.jumpower
 
    def cancel_jump(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3

    def attack(self):
        if not self.weapons.has():
            knot = weapon(self, self.all_sprites, self.weapons, self.platforms, self.GRAV)
            knot.attack(self)
    
    def update(self):
        self.acc = vec(0,self.GRAV*self.weight)
        hits = pg.sprite.spritecollide(self , self.platforms, False)
        if self.vel.y > 0:
            if hits:
                if self.pos.y < hits[0].rect.bottom:               
                    self.pos.y = hits[0].rect.top +1
                    self.vel.y = 0
                    self.jumping = False
            
        hit = pg.sprite.spritecollide(self , self.loot, True)
        if hit:
            
            self.bones += 1

        if self.hp == 0:
            self.kill()

        
        pressed = pg.key.get_pressed()


        
        
        if pressed[pg.K_LEFT]:
            self.looking = "bw"
            self.acc.x = -self.ACC

        elif pressed[pg.K_RIGHT]:
            self.acc.x = self.ACC
            
            self.looking = "fw"

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

        self.acc.x += self.vel.x * self.FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        

        if self.pos.x > self.SCREENWIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = self.SCREENWIDTH

        if self.looking == "bw":
            self.surf = pg.transform.flip(get_image(self.characterfile.format(self.flap)), True, False)
        else:
            self.surf = get_image(self.characterfile.format(self.flap))
        
        self.rect.midbottom = self.pos
    def collidecheck(self):
        hit = pg.sprite.spritecollide(self, self.enemies, False)
        if hit and self.iframe <= 0:
            for enemy in self.enemies:
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
    

class weapon(pg.sprite.Sprite):
    def __init__(self, orang, all_sprites, weapons, platforms, GRAV):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("sprites/knotspriteempty.png")
        self.surf = pg.image.load("sprites/knotspriteempty.png")
        
        self.rect = self.image.get_rect()
        
        self.going = True
        self.peak = False
        self.weight = 5
        self.acc = int(orang.throwstrength)
        
        self.orang = orang
        self.platforms = platforms
        self.GRAV = GRAV

        all_sprites.add(self)
        weapons.add(self)
        
    def attack(self,player):
        
        
        self.surf = pg.image.load("sprites/knotsprite.png")
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
        self.movecalc(self.orang)
    def movecalc(self, player):
        
        global working
        
        playerloc = vec(player.rect.center)
        attackspeed = player.attackspeed
        hits = pg.sprite.spritecollide(self, self.platforms, False)
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
                    self.pos.y += self.GRAV*self.weight*1.5


            self.pos.y += self.GRAV*self.weight
            self.rect.center = self.pos
                
            if player.rect.contains(self.rect):
                self.peak = False
                self.surf = pg.image.load("sprites/knotspriteempty.png")
                self.going = False
                self.kill()



class enemy(pg.sprite.Sprite):
    def __init__(self, orang, all_sprites, platforms, enemies, weapons, loot, GRAV, FRIC, ACC, SCREENWIDTH):
        pg.sprite.Sprite.__init__(self)
        
        self.orang = orang
        self.all_sprites = all_sprites
        self.platforms = platforms
        self.enemies = enemies
        self.weapons = weapons
        self.loot = loot
        self.GRAV = GRAV
        self.FRIC = FRIC
        self.ACC = ACC
        self.SCREENWIDTH = SCREENWIDTH

        self.imageroot = "sprites/lizard{}.png"
        
        self.image = pg.image.load("sprites/lizard1.png")
        self.surf = pg.image.load("sprites/lizard1.png")
        
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
        self.acc = vec(0, self.GRAV*self.weight)

        hits = pg.sprite.spritecollide(self , self.platforms, False)
        if self.vel.y > 0:
            if hits:
                if self.pos.y < hits[0].rect.bottom:               
                    self.pos.y = hits[0].rect.top +1
                    self.vel.y = 0
                    self.jumping = False
        
        hit = pg.sprite.spritecollide(self , self.weapons, False)
        if hit and self.iframe <= 0:
            self.hp -= 1
            self.iframe = 50
            self.aggro = True
            print(self.aggro)
        


        if self.hp <= 0:
            print(self.pos)
            self.kill()
            bone = loot(self.orang, self.all_sprites, self.platforms, self.loot, self, self.GRAV)
            self.all_sprites.add(bone)
            print(bone.pos)

        if self.rect.right > self.SCREENWIDTH :
            
            
            self.surf = pg.transform.flip(self.surf, True, False)
            self.forward = False
            self.pos.x -= 5

        if self.rect.left < 0:
            
            self.surf = pg.transform.flip(self.surf, True, False)
            self.forward = True
            self.pos.x += 5

        if not self.aggro and self.moving:    
            if self.forward:
                self.acc.x = self.ACC
            elif not self.forward:
                self.acc.x = -self.ACC
        else:
            if self.pos.x < self.orang.pos.x:
                if self.forward:
                    self.surf = pg.transform.flip(self.surf, True, False)
                    self.forward = False
                    self.acc.x = -self.ACC
                elif not self.forward:
                    self.acc.x = -self.ACC
            if self.pos.x > self.orang.pos.x:
                if self.forward:
                    self.acc.x = self.ACC
                elif not self.forward:
                    self.surf = pg.transform.flip(self.surf, True, False)
                    self.forward = True
                    self.acc.x = self.ACC
            if self.rect.right > self.SCREENWIDTH:
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
            self.acc.x += self.vel.x * self.FRIC
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


class loot(pg.sprite.Sprite):
    def __init__(self, orang, all_sprites, platforms, loot, spawner, GRAV):  #, enemies, weapons, FRIC, ACC, SCREENWIDTH):
        pg.sprite.Sprite.__init__(self)
        self.orang = orang
        self.all_sprites = all_sprites
        self.platforms = platforms
        self.loot = loot
        self.GRAV = GRAV

        self.imageroot = ("sprites/bonesprite.png")
        self.image = pg.image.load("sprites/bonesprite.png")
        self.surf = pg.image.load("sprites/bonesprite.png")

        self.pos = vec(spawner.rect.center)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.weight = 1

        self.rect = self.image.get_rect()
        
        self.rect.midbottom = self.pos

        self.loot.add(self)
        self.all_sprites.add(self)
    def update(self):
        self.acc = vec(0, self.GRAV*self.weight)
        hits = pg.sprite.spritecollide(self , self.platforms, False)
        if self.vel.y > 0:
            if hits:
                if self.pos.y < hits[0].rect.bottom:               
                    self.pos.y = hits[0].rect.top +1
                    self.vel.y = 0

        self.acc.x += self.vel.x
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        self.rect.midbottom = self.pos
