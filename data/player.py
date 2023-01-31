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
        self.image = self.images[self.index]

        #self.rect.x = self.boundingRect.x
        #self.rect.y = self.boundingRect.y
        
        self.boundingRect.center = (self.rect.x+DISPLAY_W/24, self.rect.y+((DISPLAY_W/24)+6))

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

    def checkCollision(self, mapTiles):
        collisionTypes = {'top': False, 'bottom': False, 'right': False, 'left': False}

        collisionList = Player.collisionTest(self, self.boundingRect, mapTiles)

        for tile in collisionList:
            print("Tile= ",tile.rect)
            print("Rect= ", self.boundingRect)

            if self.boundingRect.top - tile.rect.top <= self.boundingRect.height:
                collisionTypes['bottom'] = True

            if self.boundingRect.bottom >=  self.boundingRect.bottom - tile.rect.bottom:
                collisionTypes['top'] = True

            #if tile.rect.left != self.boundingRect.right - tile.rect.left:
            #    collisionTypes['right'] = True
#
#
            #if tile.rect.right != self.boundingRect.left - tile.rect.right:
            #    collisionTypes['left'] = True
            #
            #
            #if tile.rect.top <= self.boundingRect.bottom:
            #    collisionTypes['bottom'] = True
        #
#
            #if tile.rect.bottom >= self.boundingRect.top:
            #    collisionTypes['top'] = True
#
        return collisionTypes



    def move(self, movement, mapTiles):
        top = -int(self.image.get_rect()[3]*0.25)
        bottom = DISPLAY_H-(DISPLAY_H/4 + int(self.images[1].get_rect()[3])*0.76)

    
        self.rect.x = movement[0]
        self.rect.y = movement[1]

        
        
        return self.rect #collisionTypes