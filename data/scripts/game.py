import pygame, os
import pygame.freetype
from data.scripts.fileget import Files
from time import sleep
from random import randint, random
import time

# Game settings file(*.json) location
f = Files('data/settings/gamesettings.json')


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
        self.FPS = 60

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

        # Set the window to window variables defined earlier
        self.screen = pygame.display.set_mode(((self.DISPLAY_W, self.DISPLAY_H)))
        
        # Event logic variables to control game loops
        self.running, self.playing = True, True

        # Useful variables to be reused later 
        self.font = pygame.font.SysFont(None, 20)
        self.BLACK, self.WHITE = (0,0,0), (255,255,255)

        # Sprite xy coordinate variables
        self.redSquarePosX = 10
        self.redSquarePosY = 10

        # [location, velocity, timer]
        self.particles = []

        # get starting time
        self.last_time = time.time()
        
        self.averageFPS = ''
        


    def checkFullscreen(self): 
        if self.FULLSCREEN == 1:
            self.screen = pygame.display.set_mode(((self.DISPLAY_W, self.DISPLAY_H)), pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWACCEL)
        else:
            self.screen = pygame.display.set_mode(((self.DISPLAY_W, self.DISPLAY_H)),pygame.NOFRAME | pygame.DOUBLEBUF | pygame.HWACCEL)

    def writeKEYSTRING(self):
        Game.draw_text(self,text='Select Key Pressed',font=self.font,color=self.WHITE, surface=self.screen, x=5,y=5)
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
            particle[2] -= 0.2
            particle[1][1] += randint(0,10)/10
            pygame.draw.circle(self.screen, (color), [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
        
            radius = particle[2] * 2
            self.screen.blit(Game.circle_surf(self,radius, ('#333333')),
                (int(particle[0][0] - radius), int(particle[0][1] - radius)), special_flags=pygame.BLEND_RGB_ADD)

            if particle[2] <= 0:
                self.particles.remove(particle)

    # Function to draw text on screen. 
    # Arguments: text, font, text color, surface to render on, x position, y position
    def draw_text(self,text, font, color, surface, x, y):
        textObj = font.render(text, True, color) # Set boolean (True/False) for antialiasing
        textRect = textObj.get_rect() # Get text's occupied space size
        textRect.topleft = (x,y) # Set the text's position to the x and y position
        surface.blit(textObj, textRect) # Render the text to the surface


    def controlBinding(self):
        # end the program when running is = False
        if self.running == False:
            pygame.quit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            #print(event)
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.key.key_code(str(self.user_ESCAPEKEY)):
                    #pygame.quit()
                    self.running = False
                    
                
                if event.key == pygame.key.key_code(str(self.user_SELECTKEY)):
                    Game.writeKEYSTRING(self)

                if event.key == pygame.key.key_code(str(self.user_RIGHTKEY)):
                    self.redSquarePosX += self.DISPLAY_H*0.1
                
                if event.key == pygame.key.key_code(str(self.user_LEFTKEY)):
                    self.redSquarePosX -= self.DISPLAY_H*0.1
                
                if event.key == pygame.key.key_code(str(self.user_DOWNKEY)):
                    self.redSquarePosY += self.DISPLAY_H*0.1

                if event.key == pygame.key.key_code(str(self.user_UPKEY)):
                    self.redSquarePosY -= self.DISPLAY_H*0.1
                    
    def renderBackground(self):
        self.screen.fill(self.BLACK)
        # Show FPS count
        
        Game.draw_text(self,text=str(self.averageFPS),font=self.font,color=self.WHITE, surface=self.screen, x=0,y=0),90

    def mainLoop(self):
        # Go through this initial logic to set window up
        Game.checkFullscreen(self) # determine if window should be fullscreened or not, based on the loadedFile's parameters
        #self.screen.fill(self.BLACK) # Fill the window with the color black
        pygame.mouse.set_visible(False)
        self.running = True # Set control logic variable to True
        # Loop to run while control logic variable is set to True
        while self.running:
            Game.renderBackground(self)
            # Get mouse coordinates
            self.Mouse_x, self.Mouse_y = pygame.mouse.get_pos()

            
            #pygame.draw.rect(self.screen,('#9e482c'),(90,90,200,300))
            Game.drawParticles(self, 500,500,('#FFFFFF'), randint(0,5)/10 - 1, randint(13,20), randint(8,13))
            
            Game.drawParticles(self,self.DISPLAY_W/2, self.DISPLAY_H/2,('#FFFFFF'), randint(-50,50)/10 - 1, randint(13,20), randint(8,9))
            
            #pygame.draw.rect(self.screen, (randint(0,255),randint(0,255),randint(0,255)), 
                #((self.Mouse_x - (self.DISPLAY_W/40)/2), (self.Mouse_y - (self.DISPLAY_H/22.5)/2), self.DISPLAY_W/40, self.DISPLAY_H/22.5))
            
            # Check for key input
            Game.controlBinding(self)
            
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


