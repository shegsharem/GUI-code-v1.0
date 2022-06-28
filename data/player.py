import pygame
from pygame.locals import *
from fileget import Files

vec = pygame.math.Vector2  # 2 for two dimensional

# Game settings file(*.json) location
f = Files('data/settings/gamesettings.json')

# Load the game settings into a dictionary called loadedFile
loadedFile = f.readSettingsFile()


# Variables used to set window height, width, fullscreen(yes/no) from loadedFile
DISPLAY_W = int(loadedFile['settings']['window_w'])
DISPLAY_H = int(loadedFile['settings']['window_h'])


ACCELERATION = 0.5
FRICTION = -0.09


class Player(pygame.sprite.Sprite):
    def __init__(self, scaledWidth, scaledHeight):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for i in range(0,7):
            self.images.append(pygame.image.load('data/images/playerframes/player'+str(i)+'.png').convert_alpha())
            self.rect = self.images[i].get_rect()
            #self.rect = self.rect.
            # Scale the player relative to the screen size
            self.images[i] = pygame.transform.scale(self.images[i],(scaledWidth,scaledHeight))

        self.pos = vec((0, DISPLAY_H-(DISPLAY_H/4 + int(self.images[1].get_rect()[3])*0.76)))
        self.vel = vec(0,0)
        self.acc = vec(0,0)

        self.index = 0

        self.image = self.images[self.index]
        self.mask = pygame.mask.from_surface(self.image)
    
    def update(self):

        #if the index is larger than the total images
        if self.index >= len(self.images):
            #we will make the index to 0 again
            self.index = 0
        
        #finally we will update the image that will be displayed
        self.image = self.images[self.index]
   
    def move(self):
        top = -int(self.image.get_rect()[3]*0.25)
        # top = self.playerPosY = -int(self.playerList[1].get_rect()[3]*0.25)
        bottom = DISPLAY_H-(DISPLAY_H/4 + int(self.images[1].get_rect()[3])*0.76)
        self.acc = vec(0,0)
        
        # X-AXIS MOVEMENT
        self.acc.x += self.vel.x * FRICTION
    
        # Y-AXIS MOVEMENT
        self.acc.y =  -1.5
        if self.acc.y < 0:
            self.acc.y = 0

        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > DISPLAY_W:
            self.pos.x = 0

        if self.pos.x < 0:
            self.pos.x = DISPLAY_W

        if self.pos.y < top:
            self.pos.y = top
        
        #if self.pos.y > bottom:
        #    self.pos.y = bottom

        self.rect[0] = self.pos.x
        self.rect[1] = self.pos.y
    
    def moveLeft(self):
        self.acc = vec(0,0)
        self.acc.x = -ACCELERATION
        
        #self.acc.x += self.vel.x * FRICTION
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

    def moveRight(self):
        self.acc = vec(0,0)
        self.acc.x = ACCELERATION
        
        self.acc.x += self.vel.x * FRICTION
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

    def moveUp(self):
        self.acc = vec(0,0)
        self.acc.y = -4
        
        self.vel += self.acc
        self.pos += self.vel + 0.5 * -self.acc
    
    def moveDown(self):
        self.acc = vec(0,0)
        self.acc.y = ACCELERATION
        
        self.acc.y += self.vel.y * FRICTION
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
    
    def check_pos(self, sprite):
        return pygame.sprite.collide_mask(self, sprite)