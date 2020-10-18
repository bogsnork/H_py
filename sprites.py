#module: sprites

import pygame as pg
import os

# functions
vec = pg.math.Vector2  # 2 for two dimensional

# classes
class weapon(pg.sprite.Sprite):
    def __init__(self, orang, all_sprites, weapons, platforms, GRAV):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("knotspriteempty.png")
        self.surf = pg.image.load("knotspriteempty.png")
        
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
                self.surf = pg.image.load("knotspriteempty.png")
                self.going = False
                self.kill()