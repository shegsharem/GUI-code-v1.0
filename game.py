import pygame, os
import pygame.freetype
from fileget import Files
from time import sleep
from random import randint

f = Files('data/settings/gamesettings.json')

print("Successfully loaded settings.")


class Game():
    def __init__(self):
        pygame.init()
        os.environ['SDL_VIDEO_CENTERED'] = '1' # Center the window on the display
        loadedFile = f.readSettingsFile()
        self.mainClock =  pygame.time.Clock()
        self.DISPLAY_W = int(loadedFile['settings']['window_w'])
        self.DISPLAY_H = int(loadedFile['settings']['window_h'])
        self.FULLSCREEN = int(loadedFile['settings']['fullscreen'])

        self.controlsList = loadedFile['settings']
        self.customControlsList =  f.newDictFromKeySearch(self.controlsList,'button')


        self.user_ESCAPEKEY = loadedFile['settings']['button_esc']
        self.user_UPKEY = loadedFile['settings']['button_up']
        self.user_DOWNKEY = loadedFile['settings']['button_down']
        self.user_LEFTKEY = loadedFile['settings']['button_left']
        self.user_RIGHTKEY = loadedFile['settings']['button_right']
        self.user_SELECTKEY = loadedFile['settings']['button_select']

        print(self.user_ESCAPEKEY)

        self.screen = pygame.display.set_mode(((self.DISPLAY_W, self.DISPLAY_H)))
        

        self.running, self.playing = True, True
        self.font = pygame.font.SysFont(None, 50)
        self.BLACK, self.WHITE = (0,0,0), (255,255,255)

        self.redSquarePosX = 10
        self.redSquarePosY = 10

        
        
        
        #pygame.K_ESCAPE = loadedFile['settings']['button_esc']

    def draw_text(self,text, font, color, surface, x, y):
        textObj = font.render(text, True, color)# Set boolean (True/False) for antialiasing
        textRect = textObj.get_rect()
        textRect.topleft = (x,y)
        surface.blit(textObj, textRect)

    def main_menu(self):
        # Go through this initial logic to set window up
        Game.checkFullscreen(self)
        self.screen.fill(self.BLACK)
        
        self.running = True
        while self.running:
            pygame.draw.rect(self.screen, (randint(0,255),randint(0,255),randint(0,255)), 
                (self.redSquarePosX, self.redSquarePosY, self.DISPLAY_W/40, self.DISPLAY_H/22.5))

            Game.controlBinding(self)
            
            pygame.display.update()
            self.mainClock.tick(60)

    def checkFullscreen(self):
        
        if self.FULLSCREEN == 1:
            self.screen = pygame.display.set_mode(((self.DISPLAY_W, self.DISPLAY_H)), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(((self.DISPLAY_W, self.DISPLAY_H)))

    def writeKEYSTRING(self):
        Game.draw_text(self,text='Select Key Pressed',font=self.font,color=self.WHITE, surface=self.screen, x=5,y=5)

    def controlBinding(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            #print(event)
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.key.key_code(str(self.user_ESCAPEKEY)):
                    pygame.quit()
                
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
                    
            
            #if event.type == pygame.KEYUP:
                #self.screen.fill(self.WHITE)






if __name__ == '__main__':
    g = Game()
    g.main_menu()


