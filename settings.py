
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
        self.width = 400
        self.height = 200
        # ----------------
        pygame.display.set_caption('Settings') # Window Title
        Settings.screen = pygame.display.set_mode((self.width, self.height), flags) # Set Resolution, set whatever flags is set to
        # For whatever reason, you must write text to the screen in order of position bottom right to top left
        Settings.t = Text("Settings", 'Consolas', pos=(20, 20))
        Settings.t1 = Text("Hello World", pos=(0,1))

        Settings.running = True

    def run(self):
        while Settings.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    Settings.running = False
            Settings.screen.fill(Color('gray'))
            Settings.t.draw()
            
            Settings.t1.draw()
            pygame.display.flip()
            pygame.display.update()
        pygame.quit()



        
        
# Only run if the program is run directly, not when imported as a module somewhere else
if __name__ == '__main__':
    Settings().run()
