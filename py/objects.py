import pygame, sys
from pygame.locals import *

class Block(pygame.sprite.Sprite):
    def __init__(self):
        self.blockWidth = 50
        self.blockHeight = 20
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((self.blockWidth, self.blockHeight))
        self.rect = self.image.get_rect()
        self.name = BLOCK



class Ball(pygame.sprite.Sprite):
	#This class represents a Ball. It derives from the "Sprite" class in Pygame.
	
	def __init__(self, color, radius):
		# Call the parent class (Sprite) constructor
		super().__init__()
		
		# Pass in the color of the Ball, and its x and y position, width and height.
		# Set the background color and set it to be transparent
		self.image = pygame.Surface([radius*2, radius*2])
		#self.image.fill(WHITE)
		#self.image.set_colorkey(WHITE)
 
		# Draw the Ball (a circle)
		pygame.draw.circle(self.image, color, [radius,radius], radius)

		# Fetch the rectangle object that has the dimensions of the screen.
		self.rect = self.image.get_rect()

		#set initial speed
		self.xspeed=0
		self.yspeed=0
