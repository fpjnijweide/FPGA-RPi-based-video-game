import pygame, sys
from pygame.locals import *
import constants
import random

class Block(pygame.sprite.Sprite):
    """
    """
    def __init__(self, type, width, height):

        super().__init__()
        
        if type=="default":
            color=constants.colors["WHITE"]
            self.initialhp = constants.BLOCK_INITIAL_HP
        if type=="red":
            color=constants.colors["RED"]
            self.initialhp = constants.BLOCK_INITIAL_HP*8
        if type=="green":
            color=constants.colors["GREEN"]
            self.initialhp = constants.BLOCK_INITIAL_HP*2
        if type=="blue":
            color=constants.colors["BLUE"]
            self.initialhp = constants.BLOCK_INITIAL_HP*3

        
        self.hp = self.initialhp

        self.initialColor = color
        (self.initialRed, self.initialGreen, self.initialBlue) = color
        self.currentColor = self.initialColor
        self.image = pygame.Surface([width, height])
        self.image.fill(self.currentColor)
        self.rect = self.image.get_rect()

        self.rect.x = random.randint(300,constants.WINDOW_WIDTH-300-constants.BLOCKWIDTH)
        self.rect.y = random.randint(100,constants.WINDOW_HEIGHT//2)

    def reduceHP(self,xspeed,yspeed):
        if abs(yspeed) > abs(xspeed):
            self.hp = self.hp - abs(yspeed)
        else:
            self.hp = self.hp - abs(xspeed)

        if self.hp > 0:
            print(self.hp)
            print(self.initialhp)
            redcolor= int(self.initialRed*(self.hp/self.initialhp))
            greencolor= int(self.initialGreen*(self.hp/self.initialhp))
            bluecolor= int(self.initialBlue*(self.hp/self.initialhp))
            self.image.fill((    redcolor   ,greencolor,bluecolor))
        if self.hp <= 0:
            self.image.fill((0,0,0))
        return self.hp
        # self.currentColor = tuple(map(lambda x:   x*(self.hp//self.initialhp), self.initialColor))
        
        # TODO if hp is 0, remove the object instead of letting the game crash


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
        self.xspeed=constants.INITIAL_BALL_XSPEED
        self.yspeed=constants.INITIAL_BALL_YSPEED

        #set position on screen
        self.rect.x = constants.INITIAL_BALL_X
        self.rect.y = constants.INITIAL_BALL_Y

        self.xfloat = float(self.rect.x)
        self.yfloat = float(self.rect.y)


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
        self.xfloat += self.xspeed
        self.yfloat += self.yspeed
        self.rect.x = self.xfloat
        self.rect.y = self.yfloat


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
    location is int from 0 to 3 meaning left,top,right,bottom
    """
    def __init__(self, color, size, location):
        
        super().__init__()

        if location == 0:   # left wall
            w_h = [size, constants.WINDOW_HEIGHT]
            x,y = 0, 0
            self.name = "left_wall"
            
        elif location == 1:  # top wall
            w_h = [constants.WINDOW_WIDTH, size]
            x,y = 0, 0
            self.name = "top_wall"

        elif location == 2:  # right wall
            w_h = [size, constants.WINDOW_HEIGHT]
            x,y = constants.WINDOW_WIDTH - size, 0
            self.name = "right_wall"

        elif location == 3:  # bottom wall
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

class PowerUp:
    """

    """
    # ('name', rng_chance)
    types = [('speed', 0.7, 'CYAN'), ('rocket', 0.2, 'ORANGE')]
    type = None
    color = None

    def __init__(self):
        self.type = PowerUp.generateType()
        self.color = self.getTypeInfo()[2]

    @staticmethod
    def generateType():
        rngchoose = 0.0
        rngtotal = 0.0
        for t in PowerUp.types:
            rngtotal += t[1]
            print(rngtotal)
        rngnum = random.uniform(0, rngtotal)
        for t in PowerUp.types:
            rngchoose += t[1]
            if rngnum <= rngchoose:
                return t[0]
        else:
            print("Warning, no PowerUp type was generated")

    def getTypeInfo(self):
        for t in self.types:
            if t[0] == self.type:
                return t
        print("getTypeInfo error!")

    def activate(self):
        pass

    class PowerUpSprite(pygame.sprite.Sprite):
        """
        Contains the object of a powerup that is displayed on the screen.
        """
        width  = 10
        height = 20
        powerUp = None

        def __init__(self, x, y):
            super().__init__()

            self.powerUp = PowerUp()
            print("generated %s powerup." % self.powerUp.type)

            self.image = pygame.Surface([self.width, self.height])
            self.image.fill(constants.colors[self.powerUp.color])
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

        def update(self):
            self.rect.y += 1