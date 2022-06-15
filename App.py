from multiprocessing import Event
import pygame
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


pygame.init()

# ---------------------- Variables ----------------------------
global default_background_color
global width
global height
global running
global window_surface
global background
global manager

width = 400 #278
height = 200 #78

running = True

white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)

default_background_color = ('#252525')
window_surface = pygame.display.set_mode((width, height), pygame.RESIZABLE) # Set Resolution, is resizeable
menufont = pygame.freetype.SysFont('Consolas', 24, True)
# ------------------------------------------------------------


pygame.display.set_caption('Game')

background = pygame.Surface((1920, 1080)) # Set to maximum possible resolution
background.fill(pygame.Color("#252525"))

manager = pygame_gui.UIManager((width, height), 'theme.json')

# ------------------------------------------------------ Buttons ---------------------------------------------------------------------

chooseButtonBackgroundColor_button = UIButton(relative_rect=pygame.Rect((10, 50), (-1,-1)), text='Button Background Color',
  manager=manager, object_id=ObjectID(class_id='default'), anchors={'left': 'left','right': 'right','top': 'top','bottom': 'bottom'})

chooseTextColor_button = UIButton(relative_rect=pygame.Rect((10, 90), (-1, -1)), text='Button Text Color',
  manager=manager, object_id=ObjectID(class_id='default'), anchors={'left': 'left','right': 'right','top': 'top','bottom': 'bottom'})

# ------------------------------------------------------------------------------------------------------------------------------------


class Game():
  def openjson():
    # Read json
    f = open('theme.json', 'r')
    data = json.load(f)
    f.close()

  def MenuTextString(menuStr, color=None):
    if color == None:
      color = white
    menuTextRect = menufont.get_rect(menuStr)
    menuTextRect.topleft = ((width*0.01)+10, (height*0.01)+15)
    menufont.render_to(window_surface, menuTextRect.topleft, menuStr, color)
  
  def colorprompt(yes):
    f = open('theme.json', 'r')
    data = json.load(f)
    f.close()
    originalcolor = data['default']['colours'][yes]

    colorChoice = askcolor(color=(data['default']['colours'][yes]), title="Choose Color")
    if colorChoice[1] == None:
      data['default']['colours'][yes] = originalcolor
    else:
      data['default']['colours'][yes] = colorChoice[1]

    f = open('theme.json', 'w')
    print(data['default']['colours'][yes])
    json.dump(data, f, indent=4)
    f.close()

  def SettingsMenu(width=width, height=height):
    window_surface = pygame.display.set_mode((width, height), pygame.RESIZABLE) # Set Resolution, is resizeable

    running = True
    while running:
      time_delta = clock.tick(60)/1000.0 # Frame Cap at 60 FPS
      for event in pygame.event.get():

        manager.process_events(event)

        #If window is closed
        if event.type == pygame.QUIT:
          running = False
        
        if event.type == pygame.VIDEORESIZE:
          print(event.size)
          width = event.w
          height = event.h
          window_surface = pygame.display.set_mode(event.size,pygame.RESIZABLE)

        # If any pygame gui button is pressed
        if event.type == pygame_gui.UI_BUTTON_PRESSED:

          if event.ui_element == chooseButtonBackgroundColor_button:
            # Read theme file
            Game.colorprompt('normal_bg')
          
          if event.ui_element == chooseTextColor_button:
            Game.colorprompt('normal_text')

        if event.type == pygame_gui.UI_COLOUR_PICKER_COLOUR_PICKED:
          print(event.colour)

        

      manager.update(time_delta)
      
      window_surface.blit(background, (0,0))
      Game.MenuTextString("Settings", white)
      manager.draw_ui(window_surface)

      pygame.display.update()



clock = pygame.time.Clock()

Game.openjson()
Game.SettingsMenu()





    




