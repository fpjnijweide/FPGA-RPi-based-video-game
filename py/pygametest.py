import pygame, sys
from pygame.locals import *

pygame.init()

windowSurface = pygame.display.set_mode((800, 600), 0, 32)
pygame.display.set_caption('Does it work?')

pygame.display.update()

while __name__ == '__main__':
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

