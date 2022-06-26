import pygame, os
import pygame.freetype
from fileget import Files
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
global FULLSCREEN
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

# Player-defined button variables to values stored in the loadedFile dictionary
user_ESCAPEKEY = loadedFile['settings']['button_esc']
user_UPKEY = loadedFile['settings']['button_up']
user_DOWNKEY = loadedFile['settings']['button_down']
user_LEFTKEY = loadedFile['settings']['button_left']
user_RIGHTKEY = loadedFile['settings']['button_right']
user_SELECTKEY = loadedFile['settings']['button_select']

# Narrow down the loadedFile dictionary to values nested under settings
narrowedDownDict = loadedFile['settings']

# Event Logic
PRESSED_ESCAPEKEY = False
PRESSED_UPKEY  = False
PRESSED_DOWNKEY  = False
PRESSED_RIGHTKEY  = False
PRESSED_LEFTKEY  = False
PRESSED_SELECTKEY = False


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.playerList = []
        for i in range(0,7):
            self.playerList.append(pygame.image.load('data/images/pixilart-frames/pixil-frame-'+str(i)+'.png').convert_alpha())
            self.playerRect = self.playerList[i].get_rect()
            self.playerRect = self.playerRect.bottom
            # Scale the player relative to the screen size
            self.playerList[i] = pygame.transform.scale(self.playerList[i],(DISPLAY_W/10,DISPLAY_W/10))
        print (self.playerList)
    
    #def update(self):
    #    newpos = self.calcNewPos(self.playerRect, self.vector)
    #    self.playerRect = newpos
    #
    #def calcNewPos(self, rect, vector):
    #    (angle,z) = vector
    #    (dx,dy) = (z*math.cos(angle),z*math.sin(angle))
    #    return rect.move(dx,dy)

class Line(pygame.sprite.Sprite):
    def __init__(self, color, startPos, endPos):
        super().__init__()
        width = DISPLAY_W
        height = DISPLAY_H
        self.image = pygame.Surface([width,height])
        pygame.draw.line(self.image,color, startPos, endPos)
        self.rect = self.image.get_rect()


class Game():
    def __init__(self):
        # Start pygame
        pygame.init()

        # Center the window on the display
        os.environ['SDL_VIDEO_CENTERED'] = '1'

        

        # Main clock used to keep track of frames and other time-based events
        self.mainClock =  pygame.time.Clock()

        # Set the window to window variables defined earlier
        self.screen = pygame.display.set_mode(((DISPLAY_W, DISPLAY_H)), pygame.SCALED, vsync=1)
        self.screenRect = self.screen.get_rect()

        # Sprite Initiation

        self.allSprites = pygame.sprite.Group()
        self.ground = Line(('#FFFFFF'), (0,DISPLAY_H - DISPLAY_H/4),(DISPLAY_W,DISPLAY_H - DISPLAY_H/4))
        self.allSprites.add(self.ground)

        # Event logic variables to control game loops
        self.running, self.playing = True, True

        # Useful variables to be reused later
        self.font = 'data/fonts/orange kid.ttf'
        self.FPSLOOPCOUNT = 0
        self.gravity = 4.8
        
        self.BLACK, self.WHITE = (0,0,0), (255,255,255)
        self.BLUE = '#4fadf5'

        ## Sprite xy coordinate variables
        #self.playerPosX = self.DISPLAY_W/5
        #self.playerPosY = 300

        # red square change in dx
        #self.playerDX = 1
        #self.playerDY = 5

        # [location, velocity, timer]
        self.particles = []
        self.pixels = []

        # get starting time
        self.last_time = time.time()
        
        self.averageFPS = ''

    def checkFullscreen(self): 
        if FULLSCREEN == 1:
            self.screen = pygame.display.set_mode(((DISPLAY_W, DISPLAY_H)), pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWACCEL)
        else:
            self.screen = pygame.display.set_mode(((DISPLAY_W, DISPLAY_H)),pygame.NOFRAME | pygame.DOUBLEBUF | pygame.HWACCEL)
    
    def renderBackground(self):
        self.screen.fill(self.BLACK)

    def renderFPS(self):
        self.delta_t = time.time() - self.last_time
        self.delta_t *= FPS
        self.last_time = time.time()
        takeaverage = 0
        takeaverage = int(FPS/self.delta_t)
        # Update framerate string every second
        if self.FPSLOOPCOUNT == 60:
            self.averageFPS = takeaverage
            self.FPSLOOPCOUNT = 0
            takeaverage = 0
        self.FPSLOOPCOUNT+=1

        # Show FPS count
        Game.draw_text(self,text=str(self.averageFPS),font=pygame.font.Font(self.font, 20),color=self.WHITE, surface=self.screen, x=15,y=15)

    
    def circle_surf(self, radius, color):
        serf = pygame.Surface((radius * 2, radius * 2))
        pygame.draw.circle(serf, color, (radius, radius), radius)
        serf.set_colorkey((0,0,0))
        return serf

    def drawParticles(self, posx, posy, color, initial_x_velocity, initial_y_velocity, radius):
        self.particles.append([[posx, posy], [initial_x_velocity*-1, initial_y_velocity*-1], radius])
        # draw a circle where the mouse is
        #[0] = postition (x,y)
        #[1] = velocity (x,y)
        for particle in self.particles:
            particle[0][0] += particle[1][0]
            particle[0][1] += particle[1][1]
            particle[2] -= 0.4
            particle[1][1] += randint(0,10)/10
            pygame.draw.circle(self.screen, (color), [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
        
            radius = particle[2] * 2
            self.screen.blit(Game.circle_surf(self,radius, ('#0d0d0d')),
                (int(particle[0][0] - radius), int(particle[0][1] - radius)), special_flags=pygame.BLEND_RGB_ADD)

            if particle[2] <= 0:
                self.particles.remove(particle)

    # Function to draw text on screen. 
    # Arguments: text, font, text color, surface to render on, x position, y position
    def draw_text(self, text, font, color, surface, x, y):
        textObj = font.render(text, True, color) # Set boolean (True/False) for antialiasing
        textRect = textObj.get_rect() # Get text's occupied space size
        textRect.topleft = (x-1,y-8) # Set the text's position to the x and y position
        surface.blit(textObj, textRect) # Render the text to the surface
    
    def gravity(self):
        self.playerPosY -= self.gravity
        self.gravity -= 0.3


    def controlBinding(self):
        # Get mouse coordinates
        self.Mouse_x, self.Mouse_y = pygame.mouse.get_pos()
        # end the program when running is = False
        if self.running == False:
            pygame.quit()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
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
            if event.type == pygame.KEYUP:
                # If key is released
                if event.key == pygame.key.key_code(str(user_ESCAPEKEY)):
                    PRESSED_ESCAPEKEY = False
                    self.running = False
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

    def drawSprites(self):
#        
#        self.playerRect = (self.playerPosX,self.playerPosY)
#        ground = self.DISPLAY_H-(self.DISPLAY_H/4 + int(self.playerList[1].get_rect()[3])*0.76)
#
#        if self.i > 6:
#            self.i = 5
#
#        # if touching top
#        if self.playerRect[1] <= -int(self.playerList[1].get_rect()[3]*0.25):
#            self.playerPosY = -int(self.playerList[1].get_rect()[3]*0.25)
#            if self.i>1:
#                self.i-=1
#
#        # if touching ground
#        if self.playerRect[1] >= ground:
#            # Snap to the ground, not past
#            self.playerPosY = ground
#            self.i = 3
#            
#        if self.playerRect[0]<= 0:
#            self.playerPosX = 0
#        
#        if self.playerRect[0] >= self.DISPLAY_W:
#            self.playerPosX = self.DISPLAY_W
#
#        # If not touching the ground, apply the effects of gravity
#        if self.playerPosY != ground:
#            Game.gravity(self)
#
#        if self.PRESSED_UPKEY:
#            # Move
#            self.gravity = 4.8
#            if self.playerPosY == ground:
#                self.playerPosY -= 10
#            if self.i != 6:
#                self.i +=1
#
#        if self.PRESSED_LEFTKEY:
#            self.playerPosX -= 10
#
#        if self.PRESSED_RIGHTKEY:
#            self.playerPosX += 10
#  
#        if self.PRESSED_DOWNKEY:
#            # if not already touching the ground
#            if self.playerPosY != ground:
#                self.playerPosY += 10
#            if self.i != 2 and self.i >0:
#                self.i -= 1
#        
#               
        # Copy image to display
        self.allSprites.update()
        self.allSprites.draw(self.screen)    
        #self.screen.blit(self.playerList[self.i],self.playerRect)
        
    def clockTick(self):
        # Delta t to be used for framerate independence
        # Wait for next frame render time
        self.delta_t = time.time() - self.last_time
        self.delta_t *= FPS
        self.last_time = time.time()
        pygame.display.flip()
        self.mainClock.tick(FPS)

        
        
    def mainGameLoop(self):
        # Go through this initial logic to set window up
        Game.checkFullscreen(self) # determine if window should be fullscreened or not, based on the loadedFile's parameters

        # Hide mouse
        pygame.mouse.set_visible(False)

        self.running = True # Set control logic variable to True
        # Loop to run while control logic variable is set to True
        PRESSED_ESCAPEKEY = False
        PRESSED_UPKEY  = False
        PRESSED_DOWNKEY  = False
        PRESSED_RIGHTKEY  = False
        PRESSED_LEFTKEY  = False
        PRESSED_SELECTKEY = False
        
        # ------------------------------------------------------------------------------------------
        # MAIN GAME LOOP (Should be function calls only, keep as clean as possible)
        while self.running:
            # Draw background
            Game.renderBackground(self)
            
            # Check for key input
            Game.controlBinding(self)
            
            # Draw Sprites
            Game.drawSprites(self)

            # Display current FPS in top left corner
            Game.renderFPS(self)

            # Run limitor to lock in set frame rate (loop will only iterate whatever FPS is set to)
            Game.clockTick(self)

            # Update to next frame
            pygame.display.flip()
        # ------------------------------------------------------------------------------------------

if __name__ == '__main__':
    g = Game()
    g.mainGameLoop()