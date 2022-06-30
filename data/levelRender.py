import pygame
from fileget import Files
from terrain import Dirt, WhiteSquare

# Game settings file(*.json) location
f = Files('data/settings/gamesettings.json')

# Load the game settings into a dictionary called loadedFile
loadedFile = f.readSettingsFile()

# Variables used to set window height, width, fullscreen(yes/no) from loadedFile
DISPLAY_W = int(loadedFile['settings']['window_w'])
DISPLAY_H = int(loadedFile['settings']['window_h'])

class Level:
    def __init__(self, levelMap):
        self.levelMap = levelMap
        self.mapTerrain = pygame.sprite.Group()
        self.worldShift = 0

        for row_index,row in enumerate(self.levelMap):
            for col_index,cell in enumerate(row):
                x = col_index * DISPLAY_W/30
                y = row_index * DISPLAY_W/30

                if cell == "X":
                    self.terrain = Dirt('dirt', (x,y), DISPLAY_W/20)
                    self.rect = self.terrain.image.get_rect()
                    self.image = self.terrain.image
                    self.mask = pygame.mask.from_surface(self.image)
                    self.mapTerrain.add(self.terrain)
                    
                if cell == "Y":
                    self.terrain = WhiteSquare('whitesquare', (x,y),DISPLAY_W/20, DISPLAY_W/50)
                    self.rect = self.terrain.image.get_rect()
                    self.image = self.terrain.image
                    self.mask = pygame.mask.from_surface(self.image)
                    self.mapTerrain.add(self.terrain)

    def collisionCheck(self, playerSprite):
        for sprite in self.mapTerrain.sprites():
            if pygame.sprite.collide_mask(sprite, playerSprite):
                return True

    def cameraMove(self, xShift, yShift):
        for sprite in self.mapTerrain.sprites():
            sprite.rect.x -= xShift
            sprite.rect.y += yShift
        


        
