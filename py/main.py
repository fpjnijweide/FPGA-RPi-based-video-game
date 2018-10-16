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
    #TODO pygame.display.set_icon(Surface)


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
        self.AllSpritesList.add(self.paddle)
        self.CollisionSpritesList.add(self.paddle)
        
        # Todo convert .wav files to SIGNED 16?-bit Little? Endian, 44.1KHz, Stereo
        #AudioObj.playMusic('mainGameMusic')
        #AudioObj.playMusic('menu')

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

    def updateGame(self):
        """
        Updates sprites and stuff
        """
        self.playerBall.rect.x += self.playerBall.xspeed
        self.playerBall.rect.y += self.playerBall.yspeed
        
        # Return Sprite_List of objects colliding with ball
        collisions = pygame.sprite.spritecollide(self.playerBall, self.CollisionSpritesList, False)
        #print(collisions)

        if len(collisions) != 0: # Placeholder logic for collision handling (it really doesn't work)
            self.playerBall.xspeed = -self.playerBall.xspeed
            self.playerBall.yspeed = -self.playerBall.yspeed
        #else: 
        #    print("No collisions")
        # Collisions should ultimately be forwarded to the FPGA

        Screen.fill(constants.colors["BLACK"])


        self.AllSpritesList.update()

        #draw sprites
        self.AllSpritesList.draw(Screen)


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
        pygame.mixer.music.play(-1)
        #self.__playAudio(constants.music[musicName], True)

    def playSound(self, soundName):

        # Don't do anything if game sounds are disabled.
        if not constants.Sound:
            return

        pass #pygame.something.goes.here
       # self.__playAudio(constants.sounds[soundName], False)

    def __playAudio(self, fileName, loop): 
        """
        private function, for audio playing use playMusic and playSound. Stop using this. delete this once you got it all in order
        """

        if loop: loops = -1
        else: loops = 0

        pygame.mixer.Sound(fileName).play(loops)






























# Execute init() and main() only when program is run directly (not imported)
# Note: this needs to be at the end of this file,
#   otherwise stuff will be executed before python knows it exists
# Optionally, the functionality of this if block can be moved to yet another file.
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

