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


(width, height) = (800, 600)

window_surface = pygame.display.set_mode((width, height)) # Set Resolution
pygame.display.set_caption('Game')

background = pygame.Surface((width, height))
background.fill(pygame.Color("#DDDDDD"))

manager = pygame_gui.UIManager((width, height), 'theme.json')

chooseColor_button = UIButton(relative_rect=pygame.Rect((350, 280), (-1, -1)), text='Choose Color',
  manager=manager, object_id=ObjectID(class_id='default'))


clock = pygame.time.Clock()


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

      if event.ui_element == chooseColor_button:
        # Read theme file
          f = open('theme.json', 'r')
          data = json.load(f)
          f.close()

          
          colorChoice = askcolor(color=(data['default']['colours']['normal_bg']), title="Choose Color")
          print(colorChoice)
          if colorChoice[1] == None:
            data['default']['colours']['normal_bg'] = default_background_color
          else:
            data['default']['colours']['normal_bg'] = colorChoice[1]

          f = open('theme.json', 'w')
          print(data['default']['colours']['normal_bg'])
          json.dump(data, f, indent=4)
          f.close()


        

          
          #data["default":"colours"]
            
            #json.dump(colorChoice[1], f)
        

        #print(colorChoice)

    

  manager.update(time_delta)
  
  window_surface.blit(background, (0,0))
  manager.draw_ui(window_surface)

  pygame.display.update()