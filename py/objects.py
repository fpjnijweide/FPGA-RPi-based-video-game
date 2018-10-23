import pygame, sys
from pygame.locals import *
import constants
import random

class Block(pygame.sprite.Sprite):
    """
    """
    def __init__(self, color, width, height):

        super().__init__()

        # Paddle located in middle of screen
        #self.blockWidth = constants.BLOCKWIDTH
        #self.blockHeight = constants.BLOCKHEIGHT
        
        self.initialhp = constants.BLOCK_INITIAL_HP
        self.hp = self.initialhp

        self.initialColor = color
        self.currentColor = self.initialColor
        self.image = pygame.Surface([width, height])
        self.image.fill(self.currentColor)
        self.rect = self.image.get_rect()

        self.rect.x = random.randint(200,800)
        self.rect.y = random.randint(100,300)

    def reduceHP(self,xspeed,yspeed):
        if abs(yspeed) > abs(xspeed):
            self.hp = self.hp - abs(yspeed)
        else:
            self.hp = self.hp - abs(xspeed)


        if self.hp > 0:
            print(self.hp)
            print(self.initialhp)
            redcolor= int(255*(self.hp/self.initialhp))
            self.image.fill((    redcolor   ,0,0))
        if self.hp <= 0:
            self.image.fill((0,0,0))
        return self.hp
        #self.currentColor = tuple(map(lambda x:   x*(self.hp//self.initialhp), self.initialColor))
        
        #TODO if hp is 0, remove the object instead of letting the game crash

class Ball(pygame.sprite.Sprite):
    """
    This class represents a Ball.
    It derives from the "Sprite" class in Pygame.
    """ 
   # xspeed = 0
   # yspeed = 0

    maxSpeed = 50

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
        self.xspeed=2
        self.yspeed=2

        #set position on screen
        self.rect.x = 30
        self.rect.y = 30

    def bounce(self, bounceIsVertical):
        """
        Used in conjunction with 
        """
        # This function should 
        # but until the connection is realized this function will take care of that.
        if constants.FPGA_ENABLED:
            #self.rect.x, self.rect.y = fpga_connection.sendBounce(bounceIsVertical, self.xspeed, self.yspeed, bounceConstant)
            pass
        else:
            if bounceIsVertical:
                self.xspeed *= -1
            else:
                self.yspeed *= -1


    def update(self):
        """update ball location"""
        self.rect.x += self.xspeed
        self.rect.y += self.yspeed


        # test if ball is OoB
        # The out of bounds glitch seems to have something to do with how pygame handles
        #     collisions, as well as the way the main.CollisionHandler works.
        # TODO TODO TODO investigate...
        if (self.rect.x < 0 or self.rect.x > constants.WINDOW_WIDTH) or (self.rect.y < 0 or self.rect.y > constants.WINDOW_HEIGHT):

            print("Alert! Ball is out of bounds!")

        else:
            # Can be used to see how many inside-bounds frames are inbetween OoB frames
            #print(".___.")
            pass



class Paddle(pygame.sprite.Sprite):
    """
    """
    def __init__(self, color, y_position, width, height):

        super().__init__()

        # Paddle located in middle of screen
        left = (constants.WINDOW_WIDTH // 2 ) - (width // 2)

        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()

        self.rect.x = left
        self.rect.y = y_position
 
        
class Wall(pygame.sprite.Sprite):
    """
    edges of screen. Used for collision detection as well as graphical purposes
    wall is size pixels thicc
    """


    def __init__(self, color, size, location):
        
        super().__init__()

        if location == 0:   # left wall
            w_h = [size, constants.WINDOW_HEIGHT]
            x,y = 0, 0
            self.name = "left_wall"
            
            
        elif location == 1: # top wall
            w_h = [constants.WINDOW_WIDTH, size]
            x,y = 0, 0
            self.name = "top_wall"

        elif location == 2: # right wall
            w_h = [size, constants.WINDOW_HEIGHT]
            x,y = constants.WINDOW_WIDTH - size, 0
            self.name = "right_wall"

        elif location == 3: # bottom wall
            w_h = [constants.WINDOW_WIDTH, size]
            x,y = 0, (constants.WINDOW_HEIGHT - size) 
            self.name = "bottom_wall"

        else:
            raise IndexError('Wall location out of range (0..3)')


        self.image = pygame.Surface(w_h)
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


