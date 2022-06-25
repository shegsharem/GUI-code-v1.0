from tkinter import CENTER
import pygame, os
import pygame.freetype
from fileget import Files
from time import sleep
from random import randint, random
import time

import pygame.gfxdraw


# Game settings file(*.json) location
f = Files('data/settings/gamesettings.json')

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.img = pygame.Surface((50,50))
        self.img.fill((255,0,0))
        self.rect = self.img.get_rect()
        self.rect.left = 0
        self.rect.centery = g.DISPLAY_H / 2
        self.vx = 2
    


class Game():
    def __init__(self):
        # Start pygame
        pygame.init()

        # Center the window on the display
        os.environ['SDL_VIDEO_CENTERED'] = '1'

        # Load the game settings into a dictionary called loadedFile
        loadedFile = f.readSettingsFile()

        # Main clock used to keep track of frames and other time-based events
        self.mainClock =  pygame.time.Clock()

        # Frame Rate Cap
        self.FPS = 20

        # Variables used to set window height, width, fullscreen(yes/no) from loadedFile
        self.DISPLAY_W = int(loadedFile['settings']['window_w'])
        self.DISPLAY_H = int(loadedFile['settings']['window_h'])
        self.FULLSCREEN = int(loadedFile['settings']['fullscreen'])

        # Narrow down the loadedFile dictionary to values nested under settings
        self.narrowedDownDict = loadedFile['settings']

        # Player-defined button variables to values stored in the loadedFile dictionary
        self.user_ESCAPEKEY = loadedFile['settings']['button_esc']
        self.user_UPKEY = loadedFile['settings']['button_up']
        self.user_DOWNKEY = loadedFile['settings']['button_down']
        self.user_LEFTKEY = loadedFile['settings']['button_left']
        self.user_RIGHTKEY = loadedFile['settings']['button_right']
        self.user_SELECTKEY = loadedFile['settings']['button_select']

        self.PRESSED_ESCAPEKEY = False  # Pressed key logic
        self.PRESSED_UPKEY  = False# Pressed key logic
        self.PRESSED_DOWNKEY  = False# Pressed key logic
        self.PRESSED_RIGHTKEY  = False# Pressed key logic
        self.PRESSED_LEFTKEY  = False# Pressed key logic
        self.PRESSED_SELECTKEY = False# Pressed key logic

        # Set the window to window variables defined earlier
        self.screen = pygame.display.set_mode(((self.DISPLAY_W, self.DISPLAY_H)), pygame.SCALED, vsync=1)
        self.screen = pygame.transform.scale(self.screen,(120,120))
        self.screenRect = self.screen.get_rect()
        #print(self.screenRect)

        
        # Event logic variables to control game loops
        self.running, self.playing = True, True

        # Useful variables to be reused later
        self.font = 'data/fonts/orange kid.ttf'
        
        self.BLACK, self.WHITE = (0,0,0), (255,255,255)
        self.BLUE = '#4fadf5'

        # Sprite xy coordinate variables
        self.redSquarePosX = 300
        self.redSquarePosY = 300

        # red square change in dx
        self.redSquareDX = 1
        self.redSquareDY = 5


        # [location, velocity, timer]
        self.particles = []
        self.pixels = []

        # get starting time
        self.last_time = time.time()
        
        self.averageFPS = ''
        self.redList = []
        for i in range(0,7):
            self.redList.append(pygame.image.load('data/images/pixilart-frames/pixil-frame-'+str(i)+'.png').convert_alpha())
            self.redRect = self.redList[i].get_rect()
            self.redList[i] = pygame.transform.scale(self.redList[i],(100,100))
        print (self.redList)
        #self.red = pygame.transform.scale(self.redList,(400,400))
        self.red = pygame.image.load('data/images/pixilart-frames/pixil-frame-0.png').convert_alpha()
        self.rect = self.red.get_rect()
        self.screen.blit(self.red,self.rect)
        self.i = 0
        
        
        
        

    def checkFullscreen(self): 
        if self.FULLSCREEN == 1:
            self.screen = pygame.display.set_mode(((self.DISPLAY_W, self.DISPLAY_H)), pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWACCEL)
        else:
            self.screen = pygame.display.set_mode(((self.DISPLAY_W, self.DISPLAY_H)),pygame.NOFRAME | pygame.DOUBLEBUF | pygame.HWACCEL)
    
    def renderBackground(self):
        self.screen.fill(self.BLUE)
        # Show FPS count
        Game.draw_text(self,text=str(self.averageFPS),font=pygame.font.Font(self.font, 20),color=self.WHITE, surface=self.screen, x=0,y=0)
        #self.screen.blit(self.cloud1,self.cloud1rect)

    def writeKEYSTRING(self):
        Game.draw_text(self,text='Select Key Pressed',font=pygame.font.Font(self.font, 500),color=self.WHITE, surface=self.screen, x=5,y=5)
        pygame.display.flip()
    
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
    
    def drawPixels(self, color, posx, posy, width, height):
        self.pixels = [[posx,posy],[width,height]]
        shapeW = self.pixels[1][0]
        shapeH = self.pixels[1][1]
        xpos = self.pixels[0][0]
        ypos = self.pixels[0][1]
        
        rect = [int(self.pixels[0][0]), int(self.pixels[0][1]), int(self.pixels[1][0]), int(self.pixels[1][1])]
        pygame.draw.rect(self.screen, color, rect)
        
        return rect

    # Function to draw text on screen. 
    # Arguments: text, font, text color, surface to render on, x position, y position
    def draw_text(self, text, font, color, surface, x, y):
        textObj = font.render(text, True, color) # Set boolean (True/False) for antialiasing
        textRect = textObj.get_rect() # Get text's occupied space size
        textRect.topleft = (x-1,y-8) # Set the text's position to the x and y position
        surface.blit(textObj, textRect) # Render the text to the surface


    def controlBinding(self):
        # end the program when running is = False
        if self.running == False:
            pygame.quit()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                # IF KEY IS PRESSED DOWN
                if event.key == pygame.key.key_code(str(self.user_ESCAPEKEY)):
                    self.PRESSED_ESCAPEKEY = True
                if event.key == pygame.key.key_code(str(self.user_SELECTKEY)):
                    self.PRESSED_SELECTKEY = True
                if event.key == pygame.key.key_code(str(self.user_RIGHTKEY)):
                    self.PRESSED_RIGHTKEY = True
                if event.key == pygame.key.key_code(str(self.user_LEFTKEY)):
                    self.PRESSED_LEFTKEY = True
                if event.key == pygame.key.key_code(str(self.user_DOWNKEY)):
                    self.PRESSED_DOWNKEY = True
                if event.key == pygame.key.key_code(str(self.user_UPKEY)):
                    self.PRESSED_UPKEY = True
            if event.type == pygame.KEYUP:
                # If key is released
                if event.key == pygame.key.key_code(str(self.user_ESCAPEKEY)):
                    self.PRESSED_ESCAPEKEY = False
                    self.running = False
                if event.key == pygame.key.key_code(str(self.user_SELECTKEY)):
                    self.PRESSED_SELECTKEY = False
                    
                if event.key == pygame.key.key_code(str(self.user_RIGHTKEY)):
                    self.PRESSED_RIGHTKEY = False
                if event.key == pygame.key.key_code(str(self.user_LEFTKEY)):
                    self.PRESSED_LEFTKEY = False
                if event.key == pygame.key.key_code(str(self.user_DOWNKEY)):
                    self.PRESSED_DOWNKEY = False
                if event.key == pygame.key.key_code(str(self.user_UPKEY)):
                    self.PRESSED_UPKEY = False

    def generalKeyPressHandle(self):
        radius = 3
        if self.PRESSED_SELECTKEY:
            # Draw pixel 
            self.redRect = (self.redSquarePosX,self.redSquarePosY)
            # Draw particles
            #Game.drawParticles(self,self.redSquarePosX, self.redSquarePosY,('#FFFFFF'), 0, -2, radius)
            # Check if touching border
            if self.redRect[1] <= 0:
               self.redSquarePosY = 0
            if self.redRect[1] >= self.DISPLAY_H:
               # Set to max height subtract the pixel height
               self.redSquarePosY = self.DISPLAY_H - 300
            # Move
            self.redSquarePosY -= 10
            # Update screen
        
        else:
            # Draw pixel
            #self.pixelRect = Game.drawPixels(self,(255,0,0),self.redSquarePosX,self.redSquarePosY,5,5)
            self.redRect = (self.redSquarePosX,self.redSquarePosY)
            # Draw particles
           # Game.drawParticles(self,self.redSquarePosX, self.redSquarePosY,('#111111'), 0, -2, 4)
            # Check if touching border
            if self.redRect[1] <= 0:
                self.redSquarePosY = 0
            if self.redRect[1] >= self.DISPLAY_H:
                # Set to max height subtract the pixel height
                self.redSquarePosY = self.DISPLAY_H -300
            self.particles.clear()
            # Move
            self.redSquarePosY += 10
            # Update screen
        #self.screen.blit(self.red,self.rect)
        
        
        
        self.screen.blit(self.redList[self.i],self.redRect)  
        #pygame.display.update()
        self.i += 1
        if self.i > 6:
            self.i = 0
        
        
    def mainLoop(self):
        # Go through this initial logic to set window up
        Game.checkFullscreen(self) # determine if window should be fullscreened or not, based on the loadedFile's parameters
        pygame.mouse.set_visible(False)
        self.running = True # Set control logic variable to True
        # Loop to run while control logic variable is set to True
        self.PRESSED_ESCAPEKEY = False  # Pressed key logic reset
        self.PRESSED_UPKEY  = False# Pressed key logic reset
        self.PRESSED_DOWNKEY  = False# Pressed key logic reset
        self.PRESSED_RIGHTKEY  = False# Pressed key logic reset
        self.PRESSED_LEFTKEY  = False# Pressed key logic reset
        self.PRESSED_SELECTKEY = False# Pressed key logic reset
        
        while self.running:
            # Draw background
            Game.renderBackground(self)

            # Get mouse coordinates
            self.Mouse_x, self.Mouse_y = pygame.mouse.get_pos()
            
            # Check for key input
            Game.controlBinding(self)
            #pygame.draw.rect(self.screen,('#9e482c'),(0,self.DISPLAY_H-self.DISPLAY_H/8,self.DISPLAY_W,self.DISPLAY_H/8)
            
            Game.generalKeyPressHandle(self)
            
            # Delta t to be used for framerate independence
            # Wait for next frame render time
            self.delta_t = time.time() - self.last_time
            self.delta_t *= self.FPS
            self.last_time = time.time()
            pygame.display.flip()
            self.mainClock.tick(self.FPS)

            self.averageFPS = int(self.FPS/self.delta_t)
            # Update to next frame
            pygame.display.flip()

if __name__ == '__main__':
    g = Game()
    g.mainLoop()