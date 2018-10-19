"""


Sensor Pong


"""
import pygame, sys
import objects, constants, keyBindings
from enum import Enum


def init():
    """
    main.init() is called once at the very start of the program and sets up pygame.
    It also set some global variables used inside the pygame loop.
    Note: creating a multiline string using triple quotation marks is how you create python documentation
    """
    # Initialize pygame
    pygame.init()


    #set up screen
    global Screen
    Screen = pygame.display.set_mode((constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT)) 
    #set title of screen
    pygame.display.set_caption(constants.GAME_NAME) 
    #TODO pygame.display.set_icon(Surface icon)


    global AudioObj
    AudioObj = Audio()

#    playerBall = objects.Ball(constants.colors["WHITE"], constants.BALLRADIUS)
#    playerBall.rect.x = constants.WINDOW_WIDTH  // 2
#    playerBall.rect.y = constants.WINDOW_HEIGHT // 2
    
#    AllSpritesList.add(playerBall) #add this ball to the list of sprites
    global clock
    clock = pygame.time.Clock() #create game clock

    #call Game.__init__() and set gamestate
    global GameState
    GameState = GameStates.PLAYING
    global GameObj
    GameObj = Game()


def main():
    """
    main.main() contains the pygame draw loop and is called once every frame.
    Level generation etc should be defined in the objects.Game class
    """
    while True:
        # ==== Event handling ====
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                # When the game window's [x] is pressed,
                #   exit main() function to end program.
                return

        # ==== Keypress handling
        # Get boolean array of key pressed
        keysPressed = pygame.key.get_pressed()

        if GameState == GameStates.PLAYING:

            GameObj.handleKeys(keysPressed)
            GameObj.updateGame()

        # elif GameState == GameStates.MAINMENU:
            # Do MainMenuObj.handleKeys and updateGame

        # Update entire graphical display, can be optimized
        # (by using display.update() and passing it the screen area that needs to be updated)
        pygame.display.flip()

        # then wait until tick has fully passed
        clock.tick(constants.FPS)
        
        # End of game loop.
        # Note that the game stops updating but is not quit entirely



class GameStates(Enum):
    """
    An Enum links names to integer, accessible with e.g. GameStates.MAINMENU
    GameState is a global variable within main.py,
        it should always keep track of the screen that the player is on.
    Using this class to assign the GameState variable ensures that it is always one of the defined options.
    """
    # MAINMENU = 0 # unused as of now
    PLAYING  = 1
    # GAMEOVER = 2 # unused as of now


class Game:
    """
    main.Game class contains game generation and handling functionality.
    """
    # define variables to be initialized
    playerBall = None
    paddle = None
    AllSpritesList = None
    CollisionSpritesList = None
    walls = [None, None, None, None]

    def __init__(self):
        # Create two empty sprite groups.
        # One for sprites to render, another for sprites to collision detect
        self.AllSpritesList = pygame.sprite.Group()
        self.CollisionSpritesList = pygame.sprite.Group()

        # Create Ball object
        self.playerBall = objects.Ball(constants.colors["WHITE"], constants.BALLRADIUS)
        self.AllSpritesList.add(self.playerBall)

        # Create paddle object
        self.paddle = objects.Paddle(constants.colors["WHITE"], constants.PADDLE_Y_POS, constants.PADDLEWIDTH, constants.PADDLEHEIGHT)
        self.block = objects.Block(constants.colors["RED"],constants.BLOCKWIDTH, constants.BLOCKHEIGHT)
        self.AllSpritesList.add(self.paddle)
        self.CollisionSpritesList.add(self.paddle)
        
        self.AllSpritesList.add(self.block)
        self.CollisionSpritesList.add(self.block)
        # Play some music!
        # use one of these
        #AudioObj.playMusic('highScore')
        #AudioObj.playMusic('menu')
        AudioObj.playMusic('mainGameMusic')

        # Create 4 walls
        for i in range(4):
            self.walls[i] = objects.Wall(constants.colors["GRAY"], constants.WALLSIZE, i)
            self.AllSpritesList.add(self.walls[i])
            self.CollisionSpritesList.add(self.walls[i])


    def handleKeys(self, keysPressed):
        """
        Calls keyBindings.checkPress and responds accordingly
        """
        if keyBindings.checkPress('exit', keysPressed):
            pygame.quit()

        if keyBindings.checkPress('left', keysPressed):
            self.paddle.rect.x -= 6
        if keyBindings.checkPress('right', keysPressed):
            self.paddle.rect.x += 6

        #(re)set ball location when pressing K_HOME (cheat)
        if keyBindings.checkPress('restart', keysPressed):
            self.playerBall.rect.x = 30
            self.playerBall.rect.y = 30
            self.playerBall.xspeed = 2
            self.playerBall.yspeed = 2
    def updateGame(self):
        """
        Updates sprites and stuff. Called once every frame while playing game.
        """
        
        # Handle collisions
        CollisionHandling.evaluate(self.playerBall.xspeed, self.playerBall.yspeed, self.playerBall, self.CollisionSpritesList)
        # Note: collision handling is less broken once again, but the ball still disappears into the walls
        self.playerBall.update()

        Screen.fill(constants.colors["BLACK"])


        self.AllSpritesList.update()

        #draw sprites
        self.AllSpritesList.draw(Screen)


class CollisionHandling:
    """
    Abstract class containing collision handling functions 
    """
    def evaluate(ballXspeed, ballYspeed, ballObj, collisionSpritesList):
        """
        returns new (xspeed, yspeed)
        """

        collisions = pygame.sprite.spritecollide(ballObj, collisionSpritesList, False)

        # if no collisions happen
        if len(collisions) == 0:

            # then speeds do not change and function exits
            return


        # if there are collisions iterate through them
        #print(len(collisions), " collisions")
        for c in collisions:

            isVertical = CollisionHandling.findBounceIsVertical(ballObj, c)
            ballObj.bounce(isVertical)
            if isinstance(c, objects.Block):
                c_newhp = c.reduceHP(ballXspeed,ballYspeed)
                if c_newhp <= 0:
                    Game.AllSpritesList.remove(c)
                    Game.CollisionSpritesList.remove(c)
                    #TODO get this working


    def findBounceIsVertical(ballObj, collisionObj):
        """
        returns True if bounce happens on a vertical surface
        """
        # i copied this monster from stackoverflow and yet it doesnt do what i intended, i am stunned
        # all booleans are reversed
        top = ballObj.rect.top < collisionObj.rect.bottom and ballObj.rect.top > collisionObj.rect.top
        bottom = ballObj.rect.bottom > collisionObj.rect.top and ballObj.rect.bottom < collisionObj.rect.bottom
        right = ballObj.rect.right > collisionObj.rect.left and ballObj.rect.right < collisionObj.rect.right 
        left = ballObj.rect.left < collisionObj.rect.right and ballObj.rect.left > collisionObj.rect.left
        # so unreverse in the return statement
        return not right or not left

class MainMenu:
    """
    contains menu rendering and keyhandling specific to menu
    i mean not yet but it should
    """
    def __init__(self):
        pass # do nothing as of now

    def handleKeys():
        pass



class Audio:
    """
    Handles playing music and sound effects. Uses sound mapping from constants.sounds and constants.music
    """
    def __init__(self):
        #pygame.init()
        pygame.mixer.init() # TODO set mixer audio settings that work with raspberry pi if applicable

    def playMusic(self, musicName):

        # Don't do anything if music is disabled.
        if not constants.Music:
            return

        pygame.mixer.music.load(constants.music[musicName])
        pygame.mixer.music.play(-1) # loop music forever
        #self.__playAudio(constants.music[musicName], True)

    def playSound(self, soundName):

        # Don't do anything if game sounds are disabled.
        if not constants.Sound:
            return

        pass #pygame.something.goes.here
       # self.__playAudio(constants.sounds[soundName], False)








# Execute init() and main() only when program is run directly (not imported)
# Note: this needs to be at the end of this file,
#   otherwise stuff will be executed before python knows it exists
if __name__ == '__main__':

    init()

    main()

    # Game loop broken, program exits
    pygame.quit()
    print("Thank you for playing")
    print("Program exited.")
    sys.exit()

else:
    print("Imported module main.py")


