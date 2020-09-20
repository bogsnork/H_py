import pygame
import os

_image_library = {}
def get_image(path):
        global _image_library
        image = _image_library.get(path)
        if image == None:
                canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
                image = pygame.image.load(canonicalized_path)
                _image_library[path] = image
        return image

screenheight = 500
screenwidth = 1000



pygame.init()
clock = pygame.time.Clock()
vec = pygame.math.Vector2  # 2 for two dimensional
 
HEIGHT = 500
WIDTH = 1000
ACC = 0.5
FRIC = -0.12
FPS = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT)) 
pygame.display.set_caption("Game so far")


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


while not done:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    is_blue = not is_blue
        
        pressed = pygame.key.get_pressed()
        #if pressed[pygame.K_UP]: y -= 3
        #if pressed[pygame.K_DOWN]: y += 3
        
        if pressed[pygame.K_RSHIFT]: #or pressed[pygame.K_LSHIFT]:
            speed = 6
            flapspeed = 5
        if not pressed[pygame.K_RSHIFT]: #or pressed[pygame.K_LSHIFT]:
            flapspeed = 25
            speed = 3

        #    flapspeed = 25
        if pressed[pygame.K_LEFT]:
            
            looking = "bw"
            x -= speed
            flapspeed = 15
            flapcalc()
        elif pressed[pygame.K_RIGHT]:

            looking = "fw"
            x += speed
            flapspeed = 15
            flapcalc()
        elif flapspeed != 5:
            flapspeed = 25
            flapcalc()



        
        
        screen.fill((0, 0, 0))
        #flapcalc()
        pygame.draw.rect(screen, bgcolour, pygame.Rect(0, 470, screenwidth, bgheight))
        character = (characterfile.format(looking,flap))
        screen.blit(get_image(character), (x, y))
        pygame.display.flip()
        clock.tick(FPS)

#small change