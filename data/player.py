import pygame
from pygame.locals import *
from fileget import Files
from physicsengine import accelerate, deaccelerate

vec = pygame.math.Vector2  # 2 for two dimensional

# Game settings file(*.json) location
f = Files('data/settings/gamesettings.json')

# Load the game settings into a dictionary called loadedFile
loadedFile = f.readSettingsFile()


# Variables used to set window height, width, fullscreen(yes/no) from loadedFile
DISPLAY_W = int(loadedFile['settings']['window_w'])
DISPLAY_H = int(loadedFile['settings']['window_h'])


ACCELERATION = 2
FRICTION = 0.5


class Player(pygame.sprite.Sprite):
    def __init__(self, scaledWidth, scaledHeight):
        # Empty space from edges of image
        self.leftalpha = -3
        self.rightalpha = 2 + DISPLAY_W
        self.topalpha = -7
        self.bottomalpha = 7 + DISPLAY_H

        self.minxpos = self.leftalpha
        self.maxxpos = self.rightalpha 
        self.minypos = self.topalpha
        self.maxypos = self.bottomalpha

        self.cameraX = 0
        self.cameraY = 0

        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for i in range(0,7):
            self.images.append(pygame.image.load('data/images/playerframes/player'+str(i)+'.png').convert_alpha())
            self.rect = self.images[i].get_rect()
            #self.rect = self.rect.
            # Scale the player relative to the screen size
            self.images[i] = pygame.transform.scale(self.images[i],(scaledWidth,scaledHeight))

        self.index = 0

        self.originalPos = (DISPLAY_W/7, DISPLAY_H-(DISPLAY_H/4 + int(self.images[1].get_rect()[3])*0.76))

        self.image = self.images[self.index]
        self.mask = pygame.mask.from_surface(self.image)

        self.pos = vec(self.originalPos)
        self.vel = vec(0,0)
        self.acc = vec(0,0)

        print(self.pos)
    
    def update(self):

        #if the index is larger than the total images
        if self.index >= len(self.images):
            #we will make the index to 0 again
            self.index = 0
        
        #finally we will update the image that will be displayed
        self.image = self.images[self.index]
   
    def move(self):
        top = -int(self.image.get_rect()[3]*0.25)
        bottom = DISPLAY_H-(DISPLAY_H/4 + int(self.images[1].get_rect()[3])*0.76)
    
        self.pos.x += self.vel.x * 0.5 * self.acc.x
        self.pos.y += self.vel.y * 0.5 * self.acc.y
        
        # Y-AXIS MOVEMENT
        if self.pos.y > bottom:
            self.pos.y = bottom
        
        self.vel += self.acc

        if self.pos.x == self.originalPos[0]:
            if self.cameraX != 0:
                self.cameraX = deaccelerate(self.cameraX, FRICTION)

        # Friction
        if self.acc.x != 0:
            self.acc.x = 0


        if self.cameraX != 0:
            if self.cameraX > 0:
                self.cameraX -= 0.5
            if self.cameraX < 0:
                self.cameraX += 0.5
            

        if self.pos.y < top:
            self.pos.y = top
        
        #if self.pos.y > bottom:
        #    self.pos.y = bottom

        self.rect[0] = self.pos.x
        self.rect[1] = self.pos.y
    
    def moveLeft(self):
        if self.pos.x < self.originalPos[0] + 10:
            if self.cameraX != self.vel.x:
                self.cameraX = accelerate(self.cameraX, -FRICTION, self.vel.x)
        self.acc.x = ACCELERATION

    def moveRight(self):
        # WORKS
        if self.pos.x > self.originalPos[0] - 10:
            if self.cameraX != self.vel.x:
                self.cameraX = accelerate(self.cameraX, FRICTION, self.vel.x)
        self.acc.x = -ACCELERATION


    def moveUp(self):
        self.acc.y = -ACCELERATION

    
    def moveDown(self):
        self.acc.y = ACCELERATION


