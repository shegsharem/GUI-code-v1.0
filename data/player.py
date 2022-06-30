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


ACCELERATION = 0.5
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
            # Scale the player relative to the screen size
            self.images[i] = pygame.transform.scale(self.images[i],(scaledWidth,scaledHeight))
            self.rect = self.images[i].get_rect()

        self.index = 3

        self.originalPos = (DISPLAY_W/2, DISPLAY_H/4)

        self.image = self.images[self.index]
        self.mask = pygame.mask.from_surface(self.image)

        self.pos = vec(self.originalPos)
        self.vel = vec(0,0)

        self.rect.center = self.pos

        self.direction = "right"
        self.pressingkeyx = False
        self.pressingkeyy = False

        print(self.pos)
    
    def outlineMask(self, surface):
        self.mask_outline = self.mask.outline()
        n = 0
        for point in self.mask_outline:
            self.mask_outline[n] = (point[0] + self.pos[0], point[1] + self.pos[1])
            n += 1
        pygame.draw.polygon(surface,(255,255,255),self.mask_outline,3)

    def update(self):
        #if the index is larger than the total images
        if self.index >= len(self.images):
            #we will make the index to 0 again
            self.index = 0
        
        #finally we will update the image that will be displayed
        if self.direction == 'right':
            # Keep original image orientation
            self.image = self.images[self.index]

        if self.direction == 'left':
            # Flip the image
            self.image = pygame.transform.flip(self.images[self.index], True, False)
   
    def move(self):
        top = -int(self.image.get_rect()[3]*0.25)
        bottom = DISPLAY_H-(DISPLAY_H/4 + int(self.images[1].get_rect()[3])*0.76)


        # Friction
        
        if self.cameraX != 0 and not self.pressingkeyx:
            if self.cameraX > 0:
                self.cameraX -= 1
            if self.cameraX < 0:
                self.cameraX += 1
            if -1 < self.cameraX < 1:
                self.cameraX = 0
        
        if self.cameraY != 0 and not self.pressingkeyy:
            if self.cameraY > 0:
                self.cameraY -= 1
            if self.cameraY < 0:
                self.cameraY += 1
            if -1 < self.cameraY < 1:
                self.cameraY = 0


        if self.pos.y < top:
            self.pos.y = top
    

        self.rect[0] = self.pos.x
        self.rect[1] = self.pos.y

    
    def moveLeft(self):
        self.direction = 'left'
        if self.pos.x < (DISPLAY_W/2)+(DISPLAY_W/8):
            self.pos.x += 5
            if self.cameraX != -10:
                self.cameraX = -10
        if self.pos.x >= (DISPLAY_W/2)+(DISPLAY_W/8):
            if self.cameraX != -5:
                self.cameraX = -5

        

    def moveRight(self):
        self.direction = 'right'
        if self.pos.x > (DISPLAY_W/2)-(DISPLAY_W/8):
            self.pos.x -= 5
            if self.cameraX != 10:
                self.cameraX = 10
        if self.pos.x <= (DISPLAY_W/2)-(DISPLAY_W/8):
            if self.cameraX != 5:
                self.cameraX = 5
        

    def moveUp(self):
        if self.cameraY != -20 and self.pos.y > 0:
            self.cameraY = 10


    
    def moveDown(self):
        if self.cameraY != 20 and self.pos.y < DISPLAY_H:
            self.cameraY = -10


