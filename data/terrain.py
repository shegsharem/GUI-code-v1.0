import pygame

class Dirt(pygame.sprite.Sprite):
    def __init__(self, image, pos, scaledWidth, scaledHeight) -> None:
        super().__init__()
        self.image = pygame.image.load('data/images/terrain/'+image+'.png').convert()
        self.image = pygame.transform.scale(self.image,(scaledWidth,scaledHeight))
        self.rect = self.image.get_rect(topleft = pos)