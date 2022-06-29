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
    
        
        self.cameraX = self.vel.x
        self.cameraY = self.vel.y

        # Friction
        if self.vel.x != 0:
            if self.vel.x > 0:
                self.vel.x -= 1
            if self.vel.x < 0:
                self.vel.x += 1

        if self.vel.y != 0:
            if self.vel.y > 0:
                self.vel.y -= 1
            if self.vel.y < 0:
                self.vel.y += 1
        


        if self.cameraX != 0:
            if self.cameraX > 0:
                self.cameraX -= 0.1
            if self.cameraX < 0:
                self.cameraX += 0.1
        
        if self.cameraY != 0:
            if self.cameraY > 0:
                self.cameraY -= 0.1
            if self.cameraY < 0:
                self.cameraY += 0.1

        if self.pos.y < top:
            self.pos.y = top
    

        self.rect[0] = self.pos.x
        self.rect[1] = self.pos.y

        #self.pos.x += self.vel.x
        #if self.vel.y > 0:
        #    self.pos.y += self.vel.y
    
    def moveLeft(self):
        self.vel.x += -ACCELERATION


    def moveRight(self):
        self.vel.x += ACCELERATION


    def moveUp(self):
        self.vel.y += ACCELERATION

    
    def moveDown(self):
        self.vel.y -= ACCELERATION


