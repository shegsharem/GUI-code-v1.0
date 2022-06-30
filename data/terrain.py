import pygame

class Dirt(pygame.sprite.Sprite):
    def __init__(self, image, pos, scaledSideLength) -> None:
        super().__init__()
        self.image = pygame.image.load('data/images/terrain/'+image+'.png').convert_alpha()
        self.image = pygame.transform.scale(self.image,(scaledSideLength,scaledSideLength))
        self.rect = self.image.get_rect(topleft = pos)

class WhiteSquare(pygame.sprite.Sprite):
    def __init__(self, image, pos, scaledSideWidth, scaledSideHeight) -> None:
        super().__init__()
        self.image = pygame.image.load('data/images/terrain/'+image+'.png').convert_alpha()
        self.image = pygame.transform.scale(self.image,(scaledSideWidth,scaledSideHeight))
        self.rect = self.image.get_rect(topleft = pos)
