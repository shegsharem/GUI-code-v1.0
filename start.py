

import pygame
from pygame.locals import *
import pygame.freetype

import pygame_gui
from pygame_gui.core import ObjectID
from pygame_gui.elements import UIButton

import pygame_gui.data
import tkinter as tk

# Modules I wrote
from theme_edit import editThemeFile
import settings
import game
import sys





editTheme = editThemeFile()
g = game

global data
global manager


data = None

width = 400
height = 500


class Text:
    # Create text object
    def __init__(self, text, fontname=None, fontcolor=None, fontsize=None, pos=None):
        self.text = text
        self.pos = pos

        global width
        global height
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




class Start:
    def __init__(self):
        pygame.init()
        pygame.freetype.init()
        pygame.freetype.set_default_resolution(72)
        

        global width
        global height

        editTheme.themeFile = 'data/settings/theme.json'
        editTheme.openjson()

        self.data = data
        
        flags = NOFRAME


        Start.windowTitle = pygame.display.set_caption('game') # Window Title
        Start.screen = pygame.display.set_mode((width, height), flags, vsync=1)
        Start.manager = pygame_gui.UIManager((width, height), 'data/settings/theme.json',)
        Start.titleImage = pygame.image.load('data/images/image.png').convert()

        Start.background = pygame.Surface((width, height)) # Set to maximum possible resolution

        Start.title = Text("game", fontcolor=Color('white'), pos=(30,30), fontsize=48, fontname="Consolas")

        Start.settings_button = UIButton(relative_rect=pygame.Rect(((width/2)-100, 430), (100,50)), text='settings',
                manager=Start.manager, object_id=ObjectID(class_id='default'), 
                anchors={'left': 'left','right': 'right','top': 'top','bottom': 'bottom'})
        
        Start.play_button = UIButton(relative_rect=pygame.Rect((215, 380), (160,100)), text='play',
                manager=Start.manager, object_id=ObjectID(class_id='buttons'), 
                anchors={'left': 'left','right': 'right','top': 'top','bottom': 'bottom'})


        Start.exit_button = UIButton(relative_rect=pygame.Rect((30, 450), (60,30)), text='exit',
                manager=Start.manager, object_id=ObjectID(class_id='default'), 
                anchors={'left': 'left','right': 'right','top': 'top','bottom': 'bottom'})
        
        print (data)

        Start.running = True
    
    def titlePicture():
        Start.screen.blit(Start.titleImage, (50,125))


    
    def run(self):
        while Start.running:
            
            
            
            clock = pygame.time.Clock()
            time_delta = clock.tick(60)/1000.0 # Frame Cap at 60 FPS
            
            for event in pygame.event.get():
                Start.manager.process_events(event)
                #print(event)

                if event.type == pygame.QUIT:
                    Start.running = False

                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    
                    if event.ui_element == Start.exit_button:
                        Start.running = False
                        #GUI.quitConfirm_dialog.visible = 1
                        sys.exit()
                        
                        
                    if event.ui_element == Start.settings_button:
                        settings.main()

                    if event.ui_element == Start.play_button:
                        game.main()
                        Start.running = False
                        
            Start.manager.update(time_delta)

            Start.screen.fill(Color("#303030"))
            Start.manager.draw_ui(Start.screen)
            
            Start.titlePicture()
            Start.title.draw(Start.screen)
            pygame.display.update()
     
        pygame.quit()

    




        
# Only run if the program is run directly, not when imported as a module somewhere else
if __name__ == '__main__':
    #Settings().run()
    Start().run()
    
