
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
from pygame_gui.windows import UIConfirmationDialog
from pygame_gui.elements.ui_text_box import UITextBox
from pygame_gui import UI_TEXT_BOX_LINK_CLICKED, UI_TEXT_EFFECT_FINISHED
import pygame_gui.data
from pygame_gui.elements.ui_text_box import UITextBox

import json



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

class Settings:
    # Create a single window app

    def __init__(self):
        # Initialize pygame and the application
        pygame.init()
        global width
        global height
        
        flags = RESIZABLE # Window is resizeable
        # Resolution -----
        self.width = width
        self.height = height
        # ----------------
        Settings.windowTitle = pygame.display.set_caption('Settings') # Window Title
        #GUI.manager = pygame_gui.UIManager((self.width, self.height), 'theme.json')
        Settings.screen = pygame.display.set_mode((width, height))#, #flags) # Set Resolution, set whatever flags is set to
        # For whatever reason, you must write text to the screen in order of position bottom right to top left
        Settings.t = Text("Settings", 'Consolas', pos=(0, 0), fontsize=24)
        Settings.t1 = Text("Hello World", pos=(40,10), fontsize=24, fontcolor=Color('red'))

        Settings.running = True

    def run(self):
        while Settings.running:
            

            for event in pygame.event.get():
                if event.type == QUIT:
                    Settings.running = False

                '''
                if event.type == pygame.VIDEORESIZE:
                    # Make sure that if user resizes another screen, that we maintain the change when switching
                    
                    width = event.w
                    height = event.h
                    Settings.screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
                    ''' # Set the window size to new resized resolution

            Settings.screen.fill(Color('gray'))
            
            Settings.t.draw(Settings.screen)
            Settings.t1.draw(Settings.screen)
            
            #pygame.display.flip()
            pygame.display.update()
           

        pygame.quit()


class GUI:
    def __init__(self):
        pygame.init()
        pygame.freetype.init()
        pygame.freetype.set_default_resolution(72)
        GUI.titleImage = pygame.image.load('image.png')

        global width
        global height


        #self.width = width
        #self.height = height
        self.data = data
        
        flags = NOFRAME




        GUI.windowTitle = pygame.display.set_caption('game') # Window Title
        GUI.screen = pygame.display.set_mode((width, height), flags, vsync=1)
        GUI.manager = pygame_gui.UIManager((width, height), 'theme.json',)

        GUI.background = pygame.Surface((width, height)) # Set to maximum possible resolution

        GUI.title = Text("game", fontcolor=Color('white'), pos=(30,30), fontsize=48, fontname="Consolas")

        GUI.settings_button = UIButton(relative_rect=pygame.Rect(((width/2)-100, 430), (100,50)), text='settings',
                manager=GUI.manager, object_id=ObjectID(class_id='default'), 
                anchors={'left': 'left','right': 'right','top': 'top','bottom': 'bottom'})
        
        GUI.settings_button = UIButton(relative_rect=pygame.Rect((215, 380), (160,100)), text='play',
                manager=GUI.manager, object_id=ObjectID(class_id='buttons'), 
                anchors={'left': 'left','right': 'right','top': 'top','bottom': 'bottom'})


        GUI.exit_button = UIButton(relative_rect=pygame.Rect((30, 450), (60,30)), text='exit',
                manager=GUI.manager, object_id=ObjectID(class_id='default'), 
                anchors={'left': 'left','right': 'right','top': 'top','bottom': 'bottom'})
        
        print (data)

        GUI.running = True
    
    def titlePicture():
        GUI.screen.blit(GUI.titleImage, (50,125))

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
            
            
            
            clock = pygame.time.Clock()
            time_delta = clock.tick(60)/1000.0 # Frame Cap at 60 FPS
            
            for event in pygame.event.get():
                GUI.manager.process_events(event)
                print(event)

                if event.type == pygame.QUIT:
                    GUI.running = False
                    #Settings.running = True
                    #Settings().run()

                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    
                    if event.ui_element == GUI.exit_button:
                        GUI.running = False
                        #GUI.quitConfirm_dialog.visible = 1
                        
                        
                        
                        # Read theme file
                        #GUI.colorprompt(self,'normal_bg')
                        #GUI.running = False

                '''''
                if event.type == pygame.VIDEORESIZE:
                    print(event.size)
                    width = event.w
                    height = event.h
                    GUI.screen = pygame.display.set_mode(event.size, pygame.RESIZABLE) # Set the window size to new resized resolution
                    print(height)
                    print(width)
                    GUI.title.draw(GUI.screen)
                    pygame.display.update()
                '''

            
        

            GUI.manager.update(time_delta)


                
            
            
            
            
            GUI.screen.fill(Color("#252525"))
            GUI.manager.draw_ui(GUI.screen)
            GUI.title.draw(GUI.screen)
            GUI.titlePicture()
            pygame.display.update()
     
        pygame.quit()

    




        
# Only run if the program is run directly, not when imported as a module somewhere else
if __name__ == '__main__':
    #Settings().run()
    GUI().run()
    
