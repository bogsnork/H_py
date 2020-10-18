#module: user interface 
import pygame as pg
import os

pg.font.init()
buttontext = pg.font.Font(None,55)
titlefont = pg.font.Font(None, 115)


# functions
def text_objects(text, font):
    textSurface = font.render(text, True, (0, 0, 0))
    return textSurface, textSurface.get_rect()

# classes
class button(pg.sprite.Sprite):
    def __init__(self, screen, SCREENWIDTH, SCREENHEIGHT, all_sprites, buttons):

        pg.sprite.Sprite.__init__(self)

        
        self.surf = pg.Surface((100, 45))
        self.surf.fill((0, 0, 0))
        self.rect = self.surf.get_rect(center = (SCREENWIDTH/2, 15))
        self.textcont = " Start"
        self.textSurf = pg.font.Font.render(buttontext, self.textcont, False, (255, 255, 255))
        self.textRect = self.rect
        

        self.action = None

        all_sprites.add(self)
        buttons.add(self)

    def setloc(self, x, y):
        
        self.rect.bottomleft = x,y
        
    def setsize(self, width, height):
        self.rect.height = height
        self.rect.width = width
        self.surf = pg.Surface((width, height))
        self.surf.fill((0, 0, 0))
    def update(self):
        mouse = pg.mouse.get_pos()
        click = pg.mouse.get_pressed()

        #print(mouse)
        
        self.textRect.center = (self.rect.center)
        self.textSurf = pg.font.Font.render(buttontext, self.textcont, False, (255, 255, 255))
        #screen.blit(self.textSurf, self.textRect)
        
        if self.rect.right > mouse[0] > self.rect.left and self.rect.bottom > mouse[1] > self.rect.top:
            self.surf.fill((0, 0, 0))
            if click[0] == 1 and self.action != None:
                self.action()  
        else:
            self.surf.fill((56, 56, 56))
    def setbut(self, text, action):
        self.textcont = (text)    
        self.action = action


class text(pg.sprite.Sprite):
    def __init__(self, SCREENWIDTH, all_sprites, titlefont):
        pg.sprite.Sprite.__init__(self)
        
        self.col = (0, 0, 0)
        self.cont = " Start"
        self.surf = pg.font.Font.render(titlefont, self.cont, False, self.col)
        self.rect = self.surf.get_rect(center = (SCREENWIDTH/2, 15))
        
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

        