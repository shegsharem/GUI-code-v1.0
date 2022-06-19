import pygame
import pygame.freetype
import json

class Game():
    def __init__(self) -> None:
        self.settingsFile = 'data/settings/gamesettings.json'
        self.loadedFile = {}
        Game.openSettingsFile(self)

        
        pygame.init()
        self.running, self.playing = True, True
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False
        self.DISPLAY_W = int(self.loadedFile['settings']['window_w'])
        self.DISPLAY_H = int(self.loadedFile['settings']['window_h'])
        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.window = pygame.display.set_mode(((self.DISPLAY_W, self.DISPLAY_H)))
        self.font_name = ("Consolas")
        self.BLACK, self.WHITE = (0,0,0), (255,255,255)
    
    def openSettingsFile(self):
        # Read json
        settingsFile = open(self.settingsFile, 'r')
        self.loadedFile = json.load(settingsFile)
        settingsFile.close()
        print(self.loadedFile)



    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                #Menu.SettingsMenu()
            if event.type ==  pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY == True
                if event.key == pygame.K_DOWN or pygame.K_s:
                    self.DOWN_KEY == True
                if event.key == pygame.K_UP or pygame.K_w:
                    self.UP_KEY == True
            
    
    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False

    def draw_text(self, text, size, x, y, color=None):
        if color == None:
            color = self.WHITE
        font = pygame.freetype.SysFont(self.font_name, size, True) # Set boolean (True/False) for antialiasing
        textRect = font.get_rect(text).width
        textRect = (x,y)

        font.render_to(self.window, textRect, text, color)
        pygame.display.flip()

    def game_loop(self):
        while self.playing:
            self.check_events()

            self.display.fill(self.BLACK)
            self.draw_text("Hello There", 24, 0, 0, self.WHITE)
            pygame.display.flip()
            self.window.blit(self.display, (0,0))
            #pygame.display.update() # render image
            self.reset_keys()
        #pygame.quit()

def main():
    g = Game()
    g.settingsFile = 'data/settings/gamesettings.json'
    g.openSettingsFile
    g.game_loop()

if __name__ == "__main__":
    main()


