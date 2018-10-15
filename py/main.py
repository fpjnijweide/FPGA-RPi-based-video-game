"""


Sensor Pong


"""
import pygame, sys
import objects, constants, keyBindings
from enum import Enum

def init():
    """
    init() is called once at the very start of the program and sets up pygame.
    It also set some global variables used inside the pygame loop.
    Note: creating a multiline string using triple quotation marks is how you create python documentation
    """
    pygame.init()
    
    #set up screen
    global Screen
    Screen = pygame.display.set_mode((constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT)) 
    #set title of screen
    pygame.display.set_caption(constants.GAME_NAME) 
    
    
    global AllSpritesList
    AllSpritesList = pygame.sprite.Group() #get list of sprites

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
    main() contains the pygame draw loop and is called once every frame.
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


        Screen.fill(constants.colors["GRAY"])


        AllSpritesList.update()

        #draw sprites and refresh Screen
        AllSpritesList.draw(Screen)
        pygame.display.flip()

        #then wait until tick has fully passed
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

    playerBall = None
    paddle = None

    def __init__(self):
        self.playerBall = objects.Ball(constants.colors["WHITE"], constants.BALLRADIUS)
        AllSpritesList.add(self.playerBall)
        self.paddle = objects.Paddle(constants.colors["WHITE"], constants.PADDLE_Y_POS, constants.PADDLEWIDTH, constants.PADDLEHEIGHT)
        AllSpritesList.add(self.paddle)

    def handleKeys(self, keysPressed):
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
        self.playerBall.rect.x += self.playerBall.xspeed
        self.playerBall.rect.y += self.playerBall.yspeed

class MainMenu:
    """
    contains menu rendering and keyhandling specific to menu
    i mean not yet but it should
    """
    def __init__(self):
        pass # do nothing as of now

    def handleKeys():
        pass

# Execute init() and main() only when program is run directly (not imported)
# Note: this needs to be at the end of the file,
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
    print("Imported main.py")




