
from multiprocessing.synchronize import Event
#from turtle import width
import pygame
from pygame.locals import *
import pygame.freetype

from tkinter.colorchooser import askcolor # used for color chooser

import pygame_gui
from pygame_gui.core import ObjectID
from pygame_gui.core.drawable_shapes import DrawableShape
from pygame_gui.elements import UIButton
from pygame_gui.windows import UIColourPickerDialog, UIConfirmationDialog
from pygame_gui.elements.ui_text_box import UITextBox
from pygame_gui import UI_TEXT_BOX_LINK_CLICKED, UI_TEXT_EFFECT_FINISHED
import pygame_gui.data
from pygame_gui.elements.ui_text_box import UITextBox

import json


global width
global height
global data
global manager

width = 400
height = 200
data = None




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
        self.rect.topleft = self.pos
        
    
    def draw(self):
        # Draw the text image to the screen
        self.font.render_to(Settings.screen, self.rect.center, self.text, self.fontcolor)
        Settings.screen.blit(Settings.screen, self.rect)

class Settings:
    # Create a single window app

    def __init__(self):
        # Initialize pygame and the application
        pygame.init()
        
        flags = RESIZABLE # Window is resizeable
        # Resolution -----
        self.width = width
        self.height = height
        # ----------------
        Settings.windowTitle = pygame.display.set_caption('Settings') # Window Title
        #GUI.manager = pygame_gui.UIManager((self.width, self.height), 'theme.json')
        Settings.screen = pygame.display.set_mode((self.width, self.height), flags) # Set Resolution, set whatever flags is set to
        # For whatever reason, you must write text to the screen in order of position bottom right to top left
        Settings.t = Text("Settings", 'Consolas', pos=(20, 20))
        Settings.t1 = Text("Hello World", pos=(0,10))

        Settings.running = True

    def run(self):
        while Settings.running:
            

            for event in pygame.event.get():
                if event.type == QUIT:
                    Settings.running = False
                    #GUI.running = True
            Settings.screen.fill(Color('gray'))
            
            Settings.t.draw()
            Settings.t1.draw()
            
            pygame.display.flip()
            pygame.display.update()
           

        pygame.quit()


class GUI:
    def __init__(self):
        pygame.init()


        self.width = width
        self.height = height
        self.data = data
        
        flags = RESIZABLE

        GUI.windowTitle = pygame.display.set_caption('GUI') # Window Title
        GUI.screen = pygame.display.set_mode((self.width, self.height), flags)
        GUI.manager = pygame_gui.UIManager((self.width, self.height), 'theme.json')

        GUI.background = pygame.Surface((1920, 1080)) # Set to maximum possible resolution
        GUI.background.fill(pygame.Color("#252525"))
        
        print (data)
        GUI.running = True

    def openjson(self):
    # Read json
        self.f = open('theme.json', 'r')
        self.data = json.load(self.f)
        self.f.close()

    def colorprompt(self, yes):
        self.f = open('theme.json', 'r')
        self.data = json.load(self.f)
        self.f.close()
        self.originalcolor = self.data['default']['colours'][yes]

        self.colorChoice = askcolor(color=(self.data['default']['colours'][yes]), title="Choose Color")
        if self.colorChoice[1] == None:
            self.data['default']['colours'][yes] = self.originalcolor
        else:
            self.data['default']['colours'][yes] = self.colorChoice[1]

        self.f = open('theme.json', 'w')
        print(self.data['default']['colours'][yes])
        json.dump(self.data, self.f, indent=4)
        self.f.close()
    
    def run(self):
        while GUI.running:
            chooseButtonBackgroundColor_button = UIButton(relative_rect=pygame.Rect((10, 50), (-1,-1)), text='Button Background Color',
                manager=GUI.manager, object_id=ObjectID(class_id='default'), anchors={'left': 'left','right': 'right','top': 'top','bottom': 'bottom'})
            
            clock = pygame.time.Clock()
            time_delta = clock.tick(60)/1000.0 # Frame Cap at 60 FPS
            
            for event in pygame.event.get():
                GUI.manager.process_events(event)

                if event.type == pygame.QUIT:
                    GUI.running = False

                if event.type == pygame_gui.UI_BUTTON_PRESSED:

                    if event.ui_element == chooseButtonBackgroundColor_button:
                        # Read theme file
                        GUI.colorprompt('normal_bg')
                

            GUI.manager.update(time_delta)
            GUI.screen.blit(GUI.background, (0,0))
            GUI.manager.draw_ui(GUI.screen)
            pygame.display.update()

                
        pygame.quit()

    



        
        
# Only run if the program is run directly, not when imported as a module somewhere else
if __name__ == '__main__':
    GUI().run()
    Settings().run()
