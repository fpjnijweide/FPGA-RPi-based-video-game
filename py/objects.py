import pygame, sys
from pygame.locals import *
import constants
import random
import time

class Block(pygame.sprite.Sprite):
    """
    """

    #type=None
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
            self.initialhp = constants.BLOCK_INITIAL_HP*4
        if type=="blue":
            color=constants.colors["BLUE"]
            self.initialhp = constants.BLOCK_INITIAL_HP*6

        self.type = type
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
            # print(self.hp)
            # print(self.initialhp)
            redcolor = int(self.initialRed*(self.hp/self.initialhp))
            greencolor = int(self.initialGreen*(self.hp/self.initialhp))
            bluecolor = int(self.initialBlue*(self.hp/self.initialhp))
            self.image.fill((redcolor, greencolor, bluecolor))
        if self.hp <= 0:
            self.image.fill((0,0,0))
        return self.hp
        # self.currentColor = tuple(map(lambda x:   x*(self.hp//self.initialhp), self.initialColor))
        

class Ball(pygame.sprite.Sprite):
    """
    This class represents a Ball.
    It derives from the "Sprite" class in Pygame.
    """ 
    # xspeed = 0
    # yspeed = 0

    # maxSpeed = 50

    def __init__(self, color, radius):
        # Call the parent class (Sprite) constructor
        super().__init__()
        
        # Pass in the color of the Ball, and its x and y position, width and height.
        # Set the background color and set it to be transparent
        
        #self.image.fill(WHITE)
        #self.image.set_colorkey(WHITE)
        self.color=color
        self.radius=radius
        self.image = pygame.Surface([self.radius*2, self.radius*2])
        # Draw the Ball (a circle)
        self.circle = pygame.draw.circle(self.image, self.color, [self.radius,self.radius], self.radius)

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

        self.col_this_frame = [False, False]  # [x, y]

    def update_bonus(self):
        #pass
        #self.image = pygame.Surface([self.radius*2, self.radius*2])
        self.image = pygame.transform.scale(self.image, (self.radius*2, self.radius*2))
        pygame.draw.circle(self.image, self.color, [self.radius,self.radius], self.radius)
        #self.rect = self.image.get_rect()
        #self.image.fill(self.color)

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
            # If collision on an axis has already happened this frame,
            # then don't bounce
            if bounceIsVertical and not self.col_this_frame[0]:
                self.xspeed *= -1
                self.col_this_frame[0] = True

            elif not (bounceIsVertical or self.col_this_frame[1]):
                self.yspeed *= -1
                self.col_this_frame[1] = True

            else:
                print("already bounced this axis")

    def update(self):
        """update ball location"""
        self.xfloat += self.xspeed
        self.yfloat += self.yspeed
        self.rect.x = self.xfloat
        self.rect.y = self.yfloat

        # Reset this so that it can bounce again next frame
        self.col_this_frame = [False, False]

    def respawn(self):
        self.xfloat = constants.INITIAL_BALL_X
        self.yfloat = constants.INITIAL_BALL_Y
        self.xspeed = constants.INITIAL_BALL_XSPEED
        self.yspeed = constants.INITIAL_BALL_YSPEED

    #def updateproperties():



class Paddle(pygame.sprite.Sprite):
    """
    """
    def __init__(self, color, y_position, width, height):

        super().__init__()

        # Paddle located in middle of screen
        left = (constants.WINDOW_WIDTH // 2 ) - (width // 2)

        self.color=color
        self.width=width
        self.height=height
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(self.color)
        self.rect = self.image.get_rect()

        self.rect.x = left
        self.rect.y = y_position
        self.bounciness=1
 
    def update_bonus(self):
        #self.image=pygame.Surface([self.width, self.height]) #TODO check if this works
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(self.color)
        #self.rect = self.image.get_rect()
        #   self.rect = self.image.get_rect()
        
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

    types = ["blue","red","green"]
                    # ('name', rng_chance, color, duration, object, attribute, new_value)
    type_properties= {"blue"  :( 8, "BLUE",  8, "ball",   "radius", constants.BALLRADIUS*2 ),
                      "red"   :( 1, "RED",   7, "ball",   "speed",  constants.INITIAL_BALL_XSPEED*2),
                      "green" :( 3, "GREEN", 5, "paddle", "width",  constants.PADDLEWIDTH*2)}             
    type = None
    color = None

    def __init__(self):
        self.current_powerups=[]


    @staticmethod
    def generateType(power_type):
        if power_type=="random":
            rngchoose = 0.0
            rngtotal = 0.0
            for t in PowerUp.types:
                rngtotal += PowerUp.type_properties[t][0] #add type property
                # print(rngtotal)
            rngnum = random.uniform(0, rngtotal)
            for t in PowerUp.types:
                rngchoose += PowerUp.type_properties[t][0]
                if rngnum <= rngchoose:
                    return t
                else:
                    print("Warning, no PowerUp type was generated")
        else:
            return power_type

    def getTypeInfo(self):
        for t in self.types:
            if t[0] == self.type:
                return t
        print("getTypeInfo error!")

    def activate(self):
        # Do something
        print('activate %s' % self.type)
        print(self.properties[2])
        list_entry = ( ((time.time()+self.properties[2]),self.type  ) ) 
        return (list_entry,self.properties)

        # After doing something, the reference to the object is removed.

    class PowerUpSprite(pygame.sprite.Sprite):
        #TODO fix why are red power ups bugged?
        """
        Contains the object of a powerup that is displayed on the screen.
        """
        width  = 10
        height = 20
        powerUp = None

        def __init__(self, x, y, power_type):
            super().__init__()
            self.powerUp = PowerUp()

            self.powerUp.type = PowerUp.generateType(power_type)


            self.powerUp.properties = PowerUp.type_properties[self.powerUp.type]
            self.powerUp.color = self.powerUp.properties[1]         


            self.image = pygame.Surface([self.width, self.height])
            self.image.fill(constants.colors[self.powerUp.color])
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

        def update(self):
            self.rect.y += 1