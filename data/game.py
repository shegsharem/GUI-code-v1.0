import pygame, os
from pygame.locals import *
import pygame.freetype
from fileget import Files
from terrain import Dirt, WhiteSquare
from player import Player
from levelRender import Level
from random import randint
import time
import math

# Game settings file(*.json) location
f = Files('data/settings/gamesettings.json')

# Load the game settings into a dictionary called loadedFile
loadedFile = f.readSettingsFile()

# "Global" variables, usable in any part of the program
# ---------------------
global DISPLAY_W
global DISPLAY_H
global FPS
global user_DOWNKEY
global user_UPKEY
global user_ESCAPEKEY
global user_LEFTKEY
global user_RIGHTKE
global user_SELECTKEY
global narrowedDownDict
global PRESSED_DOWNKEY
global PRESSED_UPKEY
global PRESSED_ESCAPEKEY
global PRESSED_LEFTKEY
global PRESSED_RIGHTKEY
global PRESSED_SELECTKEY
# -----------------------

# Variables used to set window height, width, fullscreen(yes/no) from loadedFile
DISPLAY_W = int(loadedFile['settings']['window_w'])
DISPLAY_H = int(loadedFile['settings']['window_h'])
FULLSCREEN = int(loadedFile['settings']['fullscreen'])

# Frame Rate Cap
FPS = 60

# Clock used to handle time-based events
mainClock =  pygame.time.Clock()

# Player-defined button variables to values stored in the loadedFile dictionary
user_ESCAPEKEY = loadedFile['settings']['button_esc']
user_UPKEY = loadedFile['settings']['button_up']
user_DOWNKEY = loadedFile['settings']['button_down']
user_LEFTKEY = loadedFile['settings']['button_left']
user_RIGHTKEY = loadedFile['settings']['button_right']
user_SELECTKEY = loadedFile['settings']['button_select']

# Narrow down the loadedFile dictionary to values nested under settings

narrowedDownDict = loadedFile['settings']

# Colors
BLACK, WHITE = (0,0,0), (255,255,255)
BLUE = '#4fadf5'

# [location, velocity, timer]
particles = []
pixels = []

# Useful variables to be reused later
font = 'data/fonts/orange kid.ttf'
gravity = 4.8
FPSLOOPCOUNT = 0
last_time = time.time()
averageFPS = ''

DEBUGMODE = True



def checkFullscreen(): 
    if FULLSCREEN == 1:
        screen = pygame.display.set_mode(((DISPLAY_W, DISPLAY_H)), pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWACCEL)
    else:
        screen = pygame.display.set_mode(((DISPLAY_W, DISPLAY_H)),pygame.NOFRAME | pygame.DOUBLEBUF | pygame.HWACCEL)
    return screen
    
def renderBackground(surface):
    surface.fill(BLACK)

def renderText(surface, FPS, x, y):
    # Show FPS count
    draw_text(text=str(FPS),font=pygame.font.Font(font, 20),color=WHITE, surface=surface, x=x ,y=y)

    
def circle_surf(radius, color):
    serf = pygame.Surface((radius * 2, radius * 2))
    pygame.draw.circle(serf, color, (radius, radius), radius)
    serf.set_colorkey((0,0,0))
    return serf

def drawParticles(surface, posx, posy, color, initial_x_velocity, initial_y_velocity, radius):
    particles.append([[posx, posy], [initial_x_velocity*-1, initial_y_velocity*-1], radius])
    # draw a circle where the mouse is
    #[0] = postition (x,y)
    #[1] = velocity (x,y)
    for particle in particles:
        particle[0][0] += particle[1][0]
        particle[0][1] += particle[1][1]
        particle[2] -= 0.4
        particle[1][1] += randint(0,10)/10
        pygame.draw.circle(surface, (color), [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
    
        radius = particle[2] * 2
        surface.blit(circle_surf(radius, ('#0d0d0d')),
            (int(particle[0][0] - radius), int(particle[0][1] - radius)), special_flags=pygame.BLEND_RGB_ADD)
        if particle[2] <= 0:
            particles.remove(particle)

    # Function to draw text on screen. 
    # Arguments: text, font, text color, surface to render on, x position, y position
def draw_text(text, font, color, surface, x, y):
    textObj = font.render(text, True, color) # Set boolean (True/False) for antialiasing
    textRect = textObj.get_rect() # Get text's occupied space size
    textRect.topleft = (x-1,y-8) # Set the text's position to the x and y position
    surface.blit(textObj, textRect) # Render the text to the surface 
  
def clockTick():
    last_time = time.time()
    # Delta t to be used for framerate independence
    # Wait for next frame render time
    delta_t = time.time() - last_time
    delta_t *= FPS
    pygame.display.flip()
    mainClock.tick(FPS)

def mainGameLoop():
    # Start pygame
    pygame.init()

    # Center the window on the display
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    # Go through this initial logic to set window up
    # ----------------------------------------------
    # Main game window variable
    screen = checkFullscreen()

    # Get space occupied by the screen
    screenRect = screen.get_rect()
    # ----------------------------------------------
    level_map = [
    '                                                                  ',
    '                                                                        ',
    '                                                                        ',
    '                                                                  ',
    'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
    '                                                                        ',
    '                                                                        ',
    '                                                                        ',
    '     XXXXX                                                              ',
    'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
    '',
    '                                                                        ',
    '                                                                        ',
    'XXXXXXXXXXXXXXXXXXXXXXXX                                                ',
    '                                                                        ',
    '                                                                        ',
    '                                                                        ',
    '                                                                        ',
    '                                                                        ',
    '                                                                        ',
    '                                                                        ',
    'XXXXXX                                                                  ',
    'XX                                                                      ',
    '                                                                        ',
    'XX                                                                      ',
    'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
    'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
    'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
    'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
    'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
    ]

    # Sprite Initiation
    playerSprite = pygame.sprite.Group()
    player = Player(DISPLAY_W/15,DISPLAY_W/15)
    levelmap = Level(level_map)

    playerSprite.add(player)

    # Hide mouse
    pygame.mouse.set_visible(False)

    FPSLOOPCOUNT = 0
    averageFPS = FPS

    # Event Logic
    PRESSED_ESCAPEKEY = False
    PRESSED_UPKEY  = False
    PRESSED_DOWNKEY  = False
    PRESSED_RIGHTKEY  = False
    PRESSED_LEFTKEY  = False
    PRESSED_SELECTKEY = False

    

    # MAIN GAME LOOP (keep as clean as possible)
    while True:
        last_time = time.time()

        # Camera movement
        cameraX = player.cameraX
        cameraY = player.cameraY

        # Draw background
        renderBackground(screen)

        # Draw level map
        levelmap.cameraMove(cameraX,cameraY)
        levelmap.mapTerrain.draw(screen)

        # Draw player
        player.update()
        playerSprite.draw(screen)

        

        # This function call will return True if colliding with mapTerrain
        player_collide = levelmap.collisionCheck(player)

        if player_collide:
            print("YEYEYE")
            player.pos.y = player.pos.y

        
        
        
        # Get mouse coordinates
        Mouse_x, Mouse_y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYUP:
                # If key is released
                if event.key == pygame.key.key_code(str(user_ESCAPEKEY)):
                    PRESSED_ESCAPEKEY = False
                    pygame.quit()
                if event.key == pygame.key.key_code(str(user_SELECTKEY)):
                    PRESSED_SELECTKEY = False
                if event.key == pygame.key.key_code(str(user_RIGHTKEY)):
                    PRESSED_RIGHTKEY = False
                if event.key == pygame.key.key_code(str(user_LEFTKEY)):
                    PRESSED_LEFTKEY = False
                if event.key == pygame.key.key_code(str(user_DOWNKEY)):
                    PRESSED_DOWNKEY = False
                if event.key == pygame.key.key_code(str(user_UPKEY)):
                    PRESSED_UPKEY = False
            
            if event.type == pygame.KEYDOWN:
                # IF KEY IS PRESSED DOWN
                if event.key == pygame.key.key_code(str(user_ESCAPEKEY)):
                    PRESSED_ESCAPEKEY = True
                if event.key == pygame.key.key_code(str(user_SELECTKEY)):
                    PRESSED_SELECTKEY = True
                if event.key == pygame.key.key_code(str(user_RIGHTKEY)):
                    PRESSED_RIGHTKEY = True
                if event.key == pygame.key.key_code(str(user_LEFTKEY)):
                    PRESSED_LEFTKEY = True
                if event.key == pygame.key.key_code(str(user_DOWNKEY)):
                    PRESSED_DOWNKEY = True
                if event.key == pygame.key.key_code(str(user_UPKEY)):
                    PRESSED_UPKEY = True

        if PRESSED_RIGHTKEY:
            if player.index < 6:
                player.index += 1
            if player.index == 6:
                player.index = 6
            player.moveRight()
        
        if PRESSED_LEFTKEY:
            if player.index > 2:
                player.index -= 1
            if player.index == 2:
                player.index = 2
            player.moveLeft()

        if PRESSED_UPKEY:
            player.moveUp()

        if PRESSED_DOWNKEY:
            player.moveDown()

        player.move()

        

        if DEBUGMODE:
            # Display current FPS in top left corner
            renderText(screen, str(averageFPS)+' FPS', 15,15)
            renderText(screen, ("Player Position: ("+str(int(player.pos.x))+", "+str(int(player.pos.y))+')'),15,30)
            renderText(screen, ("Player Velocity: ("+str(int(player.vel.x))+", "+str(int(player.vel.y))+')'),15,45)
            renderText(screen, ("Player Acceleration: ("+str(int(player.acc.x))+", "+str(int(player.acc.y))+')'),15,60)
            renderText(screen, ("Camera Acceleration: ("+str(int(player.cameraX))+", "+str(int(player.cameraY))+')'),15,75)
            renderText(screen, ("Touching Terrain = "+ str(player_collide)), 15,90)

        # Run limitor to lock in set frame rate (loop will only iterate whatever FPS is set to)
        clockTick()

        delta_t = time.time() - last_time
        delta_t *= FPS
        takeaverage = int(FPS/delta_t)
  
        # Update framerate string every second
        if FPSLOOPCOUNT == 60:
            averageFPS = takeaverage
            FPSLOOPCOUNT = 0
            takeaverage = 0
        FPSLOOPCOUNT+=1

        # Update to next frame
        pygame.display.flip()


if __name__ == '__main__':
    mainGameLoop()