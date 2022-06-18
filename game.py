import pygame
from archive.App import Game as Menu
import pygame.freetype

class Game():
    def __init__(self) -> None:
        pygame.init()
        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False
        self.DISPLAY_W = 480
        self.DISPLAY_H = 270
        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.window = pygame.display.set_mode(((self.DISPLAY_W, self.DISPLAY_H)))
        self.font_name = ("Consolas")
        self.BLACK, self.WHITE = (0,0,0), (255,255,255)
    
    def game_loop(self):
        while self.playing:
            self.check_events()
            if self.START_KEY:
                self.playing = False
            self.display.fill(self.BLACK)
            self.draw_text("Hello There", 24, 0, 0, self.WHITE)
            pygame.display.flip()
            self.window.blit(self.display, (0,0))
            #pygame.display.update() # render image
            self.reset_keys()

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




