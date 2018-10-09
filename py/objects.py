import pygame, sys
from pygame.locals import *

class Block(pygame.sprite.Sprite):
    def __init__(self):
        self.blockWidth = 50
        self.blockHeight = 20
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((self.blockWidth, self.blocHeight))
        self.rect = self.image.get_rect()
        self.name = BLOCK



