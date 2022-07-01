import pygame
from pygame.locals import *
import pygame.freetype

import pygame_gui
from pygame_gui.core import ObjectID
from pygame_gui.elements import UIButton

import pygame_gui.data
import tkinter as tk

# Modules I wrote

import settings
from fileget import Files

import sys
import os

f = Files('data/settings/gamesettings.json')
loadedFile = f.readSettingsFile()
settings.getScreenData()



class Text:
    # Create text object
    def __init__(self, text, fontname=None, fontcolor=None, fontsize=None, pos=None):
        self.text = text
        self.pos = pos

        self.fontname = fontname
        self.fontsize = fontsize
        self.fontcolor = fontcolor

        # Revert to defaults if parameters (fontsize, fontname, etc) are not specified
        # DEFAULTS -------------------------
        if self.fontname == None:
            self.fontname = "Consolas"

        if self.fontcolor == None:
            self.fontcolor = Color("black")
        
        if self.pos == None:
            self.pos = (0,0)
        
        if self.fontsize == None:
            self.fontsize = 24
        # ---------------------------------

        self.set_font()
        self.render()

    def set_font(self):
        # Set the font from its name and size.
        # pygame.freetype.SysFont('Consolas', 24, True)
        self.font = pygame.freetype.SysFont(self.fontname, self.fontsize, True) #antialiasing = True
    
    def render(self):
        # Render the text into an image
        self.rect = self.font.get_rect(self.text) # Get the image for the string of text
        self.rect.center = self.pos
        
    
    def draw(self, screen):
        # Draw the text image to the screen
        self.font.render_to(screen, self.rect.center, self.text, self.fontcolor)
        #screen.blit(screen, (width/2,height/2))


pygame.quit()

pygame.init()
pygame.freetype.init()
pygame.freetype.set_default_resolution(72)

width = 400
height = 500

flags = NOFRAME

windowTitle = pygame.display.set_caption('bloot') # Window Title
screen = pygame.display.set_mode((width, height), flags, vsync=1)
manager = pygame_gui.UIManager((width, height), 'data/settings/theme.json',)
titleImage = pygame.image.load('data/images/playerframes/player0.png').convert_alpha()
titleImageRect = titleImage.get_rect()
titleImageRect = titleImageRect.center
titleImage = pygame.transform.scale(titleImage, (width*0.9, width*0.9))
background = pygame.Surface((width, height)) # Set to maximum possible resolution

title = Text("bloot", fontcolor=Color('white'), pos=(30,30), fontsize=48, fontname="Consolas")

settings_button = UIButton(relative_rect=pygame.Rect(((width/2)+50, 400), (125,75)), text='settings',
            manager=manager, object_id=ObjectID(class_id='default'), 
            anchors={'left': 'left','right': 'right','top': 'top','bottom': 'bottom'})
    
play_button = UIButton(relative_rect=pygame.Rect((25, 380), (200,100)), text='play',
            manager=manager, object_id=ObjectID(class_id='buttons'), 
            anchors={'left': 'left','right': 'right','top': 'top','bottom': 'bottom'})

exit_button = UIButton(relative_rect=pygame.Rect((350, 10), (40,40)), text='X',
            manager=manager, object_id=ObjectID(class_id='default'), 
            anchors={'left': 'left','right': 'right','top': 'top','bottom': 'bottom'})



def titlePicture():
    screen.blit(titleImage, (14,30))

    
def run():
    running = True
    while running:
        clock = pygame.time.Clock()
        time_delta = clock.tick(60)/1000.0 # Frame Cap at 60 FPS
            
        for event in pygame.event.get():
            manager.process_events(event)

            if event.type == pygame.QUIT:
                    running = False

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    
                if event.ui_element == exit_button:
                    running = False
                    sys.exit()
                        
                        
                if event.ui_element == settings_button:
                    settings.main()

                if event.ui_element == play_button:
                    running = False
                    pygame.quit()
                    import game
                    game.mainGameLoop()
                        
                        
            manager.update(time_delta)

            screen.fill(Color("#303030"))
            manager.draw_ui(screen)
            
            titlePicture()
            title.draw(screen)
            pygame.display.update()
     
    pygame.quit()

    




        
# Only run if the program is run directly, not when imported as a module somewhere else
if __name__ == '__main__':
    run()
    
