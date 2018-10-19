"""


Sensor Pong


"""
import pygame, sys, math
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

    # Set up screen
    global Screen
    Screen = pygame.display.set_mode((constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT))

    # Set title of screen
    pygame.display.set_caption(constants.GAME_NAME) 
    # TODO: pygame.display.set_icon(Surface icon)


    global AudioObj
    AudioObj = Audio()

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

        # update music
        AudioObj.updateMusic()


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
        self.AllSpritesList.add(self.paddle)
        self.CollisionSpritesList.add(self.paddle)
        
        # Play some music!
        # use one of these
        #AudioObj.playMusic('highScore')
        #AudioObj.playMusic('menu')
        AudioObj.playMusic('main')

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

        if keyBindings.checkPress('up', keysPressed):
            self.playerBall.yspeed -= 0.1
        if keyBindings.checkPress('down', keysPressed):
            self.playerBall.yspeed += 0.1
        if keyBindings.checkPress('left', keysPressed):
            self.playerBall.xspeed -= 0.1
        if keyBindings.checkPress('right', keysPressed):
            self.playerBall.xspeed += 0.1

        #(re)set ball location when pressing K_HOME (cheat)
        if keyBindings.checkPress('restart', keysPressed):
            self.playerBall.rect.x = 100
            self.playerBall.rect.y = 100

    def updateGame(self):
        """
        Updates sprites and stuff. Called once every frame while playing game.
        """
        
        # Handle collisions
        CollisionHandling.evaluate(self.playerBall, self.CollisionSpritesList)
        # Note: collision handling is less broken once again, but the ball still disappears into the walls
        self.playerBall.update()

        Screen.fill(constants.colors["BLACK"])

        self.AllSpritesList.update()

        # draw sprites
        self.AllSpritesList.draw(Screen)


class CollisionHandling:
    """
    Abstract class containing collision handling functions 
    """
    @staticmethod
    def evaluate(ballObj, collisionSpritesList):
        """
        Detect collisions, check verticality and objects.Ball.bounce()
        """

        collisions = pygame.sprite.spritecollide(ballObj, collisionSpritesList, False)

        # if no collisions happen
        if len(collisions) == 0:

            # then speeds do not change and function exits
            return

        # if there are collisions iterate through them
        print(len(collisions), " collisions this frame")
        for c in collisions:

            isVertical = CollisionHandling.findBounceIsVertical(ballObj, c)
            CollisionHandling.findBounceIsVertical_2(ballObj, c)
            ballObj.bounce(isVertical)
            print("Vertical: ", isVertical, " collision detected with ", c)

    @staticmethod
    def findBounceIsVertical_2(ballObj, collisionObj):

        ballIncomingAngle = math.tanh(ballObj.rect.y / ballObj.rect.x)

        # https://gamedev.stackexchange.com/questions/61705/pygame-colliderect-but-how-do-they-collide

        print(collisionObj.rect.top)

        print(ballIncomingAngle)

        pass

    @staticmethod
    def findBounceIsVertical(ballObj, collisionObj):
        """
        returns True if bounce happens on a vertical surface
        I suspect this function to be the source of the horrendous collision physics.
        """
        # i copied this monster from stackoverflow and yet it doesnt do what i intended, i am stunned
        ball_top = ballObj.rect.top
        ball_bot = ballObj.rect.bottom
        ball_rgt = ballObj.rect.right
        ball_lft = ballObj.rect.left

        coll_top = collisionObj.rect.top
        coll_bot = collisionObj.rect.bottom
        coll_rgt = collisionObj.rect.right
        coll_lft = collisionObj.rect.left

        # all booleans are reversed for some reason
        top = ball_top <= coll_bot and ball_top >= coll_top
        bot = ball_bot >= coll_top and ball_bot <= coll_bot
        rgt = ball_rgt >= coll_lft and ball_rgt <= coll_rgt
        lft = ball_lft <= coll_rgt and ball_lft >= coll_lft
        # so unreverse in the return statement
        print(not top, not bot, not rgt, not lft)
        return not rgt or not lft


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

    fadeoutTime = 1500  # ms
    trackPlaying = None
    trackToPlay = None

    def __init__(self):
        pygame.mixer.init()  # TODO set mixer audio settings that work with raspberry pi if applicable

    def playMusic(self, musicName):

        # Don't do anything if music is disabled.
        if not constants.MUSIC:
            return

        self.trackToPlay = constants.music[musicName]

        if pygame.mixer.music.get_busy() and self.trackToPlay != self.trackPlaying:
            pygame.mixer.music.fadeout(self.fadeoutTime)


    def updateMusic(self):

        # Checks if music track has ended and track exists in queue
        if not pygame.mixer.music.get_busy() and self.trackToPlay:
            pygame.mixer.music.load(self.trackToPlay)
            pygame.mixer.music.play(0)
            self.trackPlaying = self.trackToPlay

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


