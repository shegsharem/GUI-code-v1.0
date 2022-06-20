import pygame, os



import pygame.freetype
from fileget import Files

f = Files('data/settings/gamesettings.json')
loadedFile = f.readSettingsFile()
print("Successfully loaded settings.")

os.environ['SDL_VIDEO_CENTERED'] = '1' # Center the window on the display
pygame.init()

mainClock =  pygame.time.Clock()
UP_KEY, DOWN_KEY, START_KEY, BACK_KEY = False, False, False, False
DISPLAY_W = int(loadedFile['settings']['window_w'])
DISPLAY_H = int(loadedFile['settings']['window_h'])
FULLSCREEN = int(loadedFile['settings']['fullscreen'])

user_ESCAPEKEY = loadedFile['settings']['button_esc']
user_UPKEY = loadedFile['settings']['button_up']
user_DOWNKEY = loadedFile['settings']['button_down']
user_LEFTKEY = loadedFile['settings']['button_left']
user_RIGHTKEY = loadedFile['settings']['button_right']
user_SELECTKEY = loadedFile['settings']['button_select']


# Go through this initial logic to set window up
if FULLSCREEN == 1:
    screen = pygame.display.set_mode(((DISPLAY_W, DISPLAY_H)), pygame.FULLSCREEN)
else:
    screen = pygame.display.set_mode(((DISPLAY_W, DISPLAY_H)))

running, playing = True, True
font = pygame.font.SysFont(None, 20)
BLACK, WHITE = (0,0,0), (255,255,255)
#pygame.K_ESCAPE = loadedFile['settings']['button_esc']

def draw_text(text, font, color, surface, x, y):
    textObj = font.render(text, True, color)# Set boolean (True/False) for antialiasing
    textRect = textObj.get_rect()
    textRect.topleft = (x,y)
    surface.blit(textObj, textRect)

def main_menu():
    while True:

        screen.fill(BLACK)
        draw_text('Hello there',font,WHITE,screen, 20,20)

        controlBinding()
        
        pygame.display.update()
        mainClock.tick(60)


def controlBinding():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        
        if event.type == pygame.KEYDOWN:
            #bind custom key assignments according to gamesettings.json
            user_ESCAPEKEY,user_DOWNKEY,user_LEFTKEY,user_RIGHTKEY,user_UPKEY,user_SELECTKEY = event.key 
            if event.key == pygame.K_ESCAPE:
                pygame.quit()



main_menu()


