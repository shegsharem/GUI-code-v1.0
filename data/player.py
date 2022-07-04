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

        self.movingRight = False
        self.movingLeft = False

        self.pressingkeyx = False
        self.pressingkeyy = False

        self.airTimer = 0

        self.momentumY = 0

        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.boundingRects = []

        for i in range(0,7):
            self.images.append(pygame.image.load('data/images/playerframes/player'+str(i)+'.png').convert_alpha())
            # Scale the player relative to the screen size
            self.images[i] = pygame.transform.scale(self.images[i],(scaledWidth,scaledHeight))
            self.boundingRects.append(self.images[i].get_bounding_rect())
            self.rect = self.images[i].get_rect()
            
        self.index = 3

        self.originalPos = (DISPLAY_W/4-(self.rect[2]/2), DISPLAY_H/4+(self.rect[3]/2))

        self.image = self.images[self.index]
        self.boundingRect = self.boundingRects[self.index]
        
        self.pos = vec(self.originalPos)
        self.vel = vec(0,0)

        self.rect.center = self.pos

    def update(self):
        self.boundingRect = self.boundingRects[self.index]
        self.boundingRect.center = (self.rect.x+36, self.rect.y+40)

        #if the index is larger than the total images
        if self.index >= len(self.images):
            #we will make the index to 0 again
            self.index = 0
        
        #finally we will update the image that will be displayed
        if self.movingRight:
            # Keep original image orientation
            self.image = self.images[self.index]

        if self.movingLeft:
            # Flip the image
            self.image = pygame.transform.flip(self.images[self.index], True, False)

    def collisionTest(self, playerBoundingRect, mapTiles):
        hit_list = []
        for tile in mapTiles():
            collide = pygame.rect.Rect.colliderect(playerBoundingRect, tile.rect)
            if collide:
                hit_list.append(tile)
        return hit_list

    def move(self, movement, mapTiles):
        top = -int(self.image.get_rect()[3]*0.25)
        bottom = DISPLAY_H-(DISPLAY_H/4 + int(self.images[1].get_rect()[3])*0.76)

        collisionTypes = {'top': False, 'bottom': False, 'right': False, 'left': False}
        
        self.rect.x += movement[0]
        self.boundingRect.x += movement[0]
        
        hit_list = Player.collisionTest(self, self.boundingRect, mapTiles)
        for tile in hit_list:
            if movement[0] > 0:
                self.boundingRect.right = tile.rect.left
                collisionTypes['right'] = True
            elif movement[0] < 0:
                self.boundingRect.left = tile.rect.right
                collisionTypes['left'] = True
        
        self.rect.y += movement[1]
        self.boundingRect.y += movement[1]
        hit_list = Player.collisionTest(self, self.boundingRect, mapTiles)
        for tile in hit_list:
            if movement[1] > 0:
                self.boundingRect.bottom = tile.rect.top
                collisionTypes['bottom'] = True
            elif movement[0] < 0:
                self.boundingRect.top = tile.rect.bottom
                collisionTypes['top'] = True


        #if self.pos.x <= (DISPLAY_W/2)-(DISPLAY_W/8):
        #    #self.pos.x += 5
        #    if self.cameraX != -3:
        #        self.cameraX = -3
        #
        #if self.pos.x <= (DISPLAY_W/2)-(DISPLAY_W/8):
        #    if self.cameraX != 3:
        #        self.cameraX = 3
        
        else:
            self.cameraX =0
        
        return self.rect, collisionTypes

        # Friction
        if self.cameraX != 0 and not self.pressingkeyx:
            self.cameraX = 0
            #if self.cameraX > 0:
            #    self.cameraX -= 0.2
            #if self.cameraX < 0:
            #    self.cameraX += 0.2
            #if -0.2 < self.cameraX < 0.2:
            #    self.cameraX = 0
        
        if self.cameraY != 0 and not self.pressingkeyy:
            self.cameraY = 0
            #if self.cameraY > 0:
            #    self.cameraY -= 0.2
            #if self.cameraY < 0:
            #    self.cameraY += 0.2
            #if -0.2 < self.cameraY < 0.2:
            #    self.cameraY = 0


        if self.pos.y < top:
            self.pos.y = top
    
    def moveLeft(self):
        self.movingLeft = True
        if self.pos.x < (DISPLAY_W/2)-(DISPLAY_W/8):
            #self.pos.x += 5
            if self.cameraX != -3:
                self.cameraX = -3
        else:
            self.pos.x -= 3
            self.cameraX = 0
        

    def moveRight(self):
        self.movingRight = True
        if self.pos.x <= (DISPLAY_W/2)-(DISPLAY_W/8):
            if self.cameraX != 3:
                self.cameraX = 3
        else:
            self.pos.x += 3
            self.cameraX = 0
        

    def jump(self):
        if self.cameraY != 10 and self.pos.y > DISPLAY_H/4:
            self.pos.y -= 10
        if self.pos.y <= DISPLAY_H/4:
            self.cameraY = 10

    def gravity(self):
        self.vel.y = self.vel.y + ACCELERATION
        self.pos.y = self.pos.y + self.vel.y

    
    def moveDown(self):
        if self.cameraY != 20 and self.pos.y < DISPLAY_H:
            self.cameraY = -10

