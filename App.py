from multiprocessing import Event
from matplotlib.font_manager import json_dump
import pygame
from tkinter.colorchooser import askcolor # used for color chooser
import pygame_gui
from pygame_gui.core import ObjectID
from pygame_gui.elements import UIButton
import json


pygame.init()


global default_background_color

default_background_color = ('#444444')

# Read json
f = open('theme.json', 'r')
data = json.load(f)
f.close()

width = 1000
height = 108

window_surface = pygame.display.set_mode((width, height),pygame.RESIZABLE) # Set Resolution
pygame.display.set_caption('Game')

background = pygame.Surface((width, height))
background.fill(pygame.Color("#252525"))

manager = pygame_gui.UIManager((width, height), 'theme.json')

chooseButtonBackgroundColor_button = UIButton(relative_rect=pygame.Rect((5, 40), (-1, -1)), text='Choose Button Background Color',
  manager=manager, object_id=ObjectID(class_id='default'))

chooseTextColor_button = UIButton(relative_rect=pygame.Rect((5, 5), (-1, -1)), text='Choose Text Color',
  manager=manager, object_id=ObjectID(class_id='default'))


clock = pygame.time.Clock()

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



running = True # Our main program state variable

while running:
  time_delta = clock.tick(60)/1000.0 # Frame Cap at 60 FPS
  for event in pygame.event.get():

    manager.process_events(event)

    #If window is closed
    if event.type == pygame.QUIT:
      running = False

    # If any pygame gui button is pressed
    if event.type == pygame_gui.UI_BUTTON_PRESSED:

      if event.ui_element == chooseButtonBackgroundColor_button:
        # Read theme file
        colorprompt('normal_bg')
      
      if event.ui_element == chooseTextColor_button:
        colorprompt('normal_text')

    

  manager.update(time_delta)
  
  window_surface.blit(background, (0,0))
  manager.draw_ui(window_surface)

  pygame.display.update()