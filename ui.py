#module: user interface 

class button(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        
        self.surf = pg.Surface((100, 45))
        self.surf.fill((0, 0, 0))
        self.rect = self.surf.get_rect(center = (SCREENWIDTH/2, bgheight/2))
        self.textcont = " Start"
        self.textSurf = pg.font.Font.render(buttontext, self.textcont, False, (255, 255, 255))
        self.textRect = self.rect
        #self.textoff = self.rect.topright + vec(20, 10)

        self.action = end_intro

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
        screen.blit(self.textSurf, self.textRect)
        
        if self.rect.right > mouse[0] > self.rect.left and self.rect.bottom > mouse[1] > self.rect.top:
            self.surf.fill((0, 0, 0))
            if click[0] == 1 and self.action != None:
                self.action()  
        else:
            self.surf.fill((56, 56, 56))
    def setbut(self, text, action):
        self.textcont = (text)    
        self.action = action