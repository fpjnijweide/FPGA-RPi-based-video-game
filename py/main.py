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
    pygame.mixer.pre_init()  # TODO set right variables inside this
    # Initialize pygame
    pygame.init()
    pygame.font.init()
    # set up screen
    global Screen
    Screen = pygame.display.set_mode((constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT))

    # Set title of screen
    pygame.display.set_caption(constants.GAME_NAME) 
    # TODO: pygame.display.set_icon(Surface icon)

    global AudioObj
    AudioObj = Audio()

    global ClockObj
    ClockObj = pygame.time.Clock()  # create game clock

    # Call Game.__init__() and set gamestate
    global GameState
    GameState = GameStates.MAINMENU
    global GameObj
    GameObj = Game()
    global MainMenuObj
    MainMenuObj = MainMenu()


def main():
    """
    main.main() contains the pygame draw loop and is called once every frame.
    Level generation etc should be defined in the objects.Game class
    """
    while True:
        # ==== Event handling ====
        # Internally process events
        pygame.event.pump()
        # Iterate through each event
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                # When the game window's [x] is pressed,
                #   exit main() function to end program.
                return

        # ==== Keypress handling
        # Get boolean array of key pressed
        # TODO use events to handle presses (maybe)
        keysPressed = pygame.key.get_pressed()

        if GameState == GameStates.PLAYING:

            GameObj.handleKeys(keysPressed)
            GameObj.updateGame()

        elif GameState == GameStates.MAINMENU:
            MainMenuObj.handleKeys(keysPressed)
            MainMenuObj.updateMenu()

        # Update entire graphical display, TODO can be heavily optimized
        # (by using display.update() and passing it only the screen area that needs to be updated)
        # see https://www.pygame.org/docs/tut/newbieguide.html and look for "Dirty rect animation." section
        pygame.display.flip()

        # update music
        # TODO use pygame.music.set_endevent() and only update if music end event happens.
        AudioObj.updateMusic()

        # then wait until tick has fully passed
        ClockObj.tick(constants.FPS)
        
        # End of game loop.
        # Note that the game stops updating but is not quit entirely


class GameStates(Enum):
    """
    An Enum links names to integer, accessible with e.g. GameStates.MAINMENU
    GameState is a global variable within main.py,
        it should always keep track of the screen that the player is on.
    Using this class to assign the GameState variable ensures that it is always one of the defined options.
    """
    MAINMENU = 0 # unused as of now
    PLAYING  = 1
    # GAMEOVER = 2 # unused as of now
    HIGHSCORES = 2
    OPTIONS = 3


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
        # AudioObj.playMusic('highScore')
        # AudioObj.playMusic('menu')
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
            pygame.event.post(pygame.event.Event(pygame.QUIT))

        if keyBindings.checkPress('up', keysPressed):
            self.playerBall.yspeed -= 0.1
        if keyBindings.checkPress('down', keysPressed):
            self.playerBall.yspeed += 0.1
        if keyBindings.checkPress('left', keysPressed):
            self.playerBall.xspeed -= 0.1
        if keyBindings.checkPress('right', keysPressed):
            self.playerBall.xspeed += 0.1

        # (re)set ball location when pressing K_HOME (cheat)
        if keyBindings.checkPress('restart', keysPressed):
            self.playerBall.xfloat = 100
            self.playerBall.yfloat = 100

    def updateGame(self):
        """
        Updates sprites and stuff. Called once every frame while playing game.
        """
        
        # Handle collisions
        CollisionHandling.evaluate(self.playerBall, self.CollisionSpritesList)

        # Note: collision handling is less broken yet once again, but the ball still disappears into the walls
        self.playerBall.update()

        Screen.fill(constants.colors["BLACK"])

        self.AllSpritesList.update()

        # draw sprites
        self.AllSpritesList.draw(Screen)


class CollisionHandling:
    """
    Abstract class containing collision handling functions 
    """
    pygame.font.init()
    mainFont = None
    subFont = None
    highlight = None
    mainmenu = None
    startgamemenu = None
    highscoremenu = None
    optionsmenu = None
    exitmenu = None
    texts = None
    # widths
    mainmenu_Width = None
    startgamemenu_Width = None
    highscoremenu_Width = None
    optionsmenu_Width = None
    exitmenu_Width = None
    # heights
    mainmenu_Height = None
    startgamemenu_Height = None
    highscoremenu_Height = None
    optionsmenu_Height = None
    exitmenu_Height = None
    selectedItem = None
    # menuItems = [mainmenu, optionsmenu, highscoremenu, startgamemenu]
    menuItems = None
    menucolor = None
    def __init__(self):
        pygame.display.set_caption(constants.GAME_NAME + ' - Main menu' )
        self.mainFont = pygame.font.SysFont('arial', 60) # 76? HEIGTH
        self.subFont = pygame.font.SysFont('arial', 50) # 58 HEIGTH
        self.highlight = pygame.font.SysFont('arial', 50, italic=True, bold=True)
        self.highlight.set_underline(True)

        self.texts = ['Start game','Highscores','Options', 'exit']
        self.mainmenu = self.writeText('Main Menu', self.mainFont)
        self.startgamemenu = self.writeText('Start game', self.highlight)
        self.highscoremenu = self.writeText('Highscores', self.subFont)
        self.optionsmenu = self.writeText('Options', self.subFont)
        self.exitmenu = self.writeText('Exit', self.subFont)
        self.menuItems = { 0:self.startgamemenu, 1:self.highscoremenu, 2:self.optionsmenu, 3:self.exitmenu}
        self.selectedItem = 0
        # for x in range(0, len(self.menuItems)):
        #     print(self.menuItems[x].get_size())# width, height
        self.mainmenu_Width = constants.WINDOW_HW - self.mainmenu.get_width()//2
        self.startgamemenu_Width = 30 #constants.WINDOW_WIDTH/1000 # + self.startgamemenu.get_width()//2
        self.highscoremenu_Width = self.startgamemenu_Width + self.startgamemenu.get_width()
        self.optionsmenu_Width = self.highscoremenu_Width + self.highscoremenu.get_width()
        self.exitmenu_Width = self.optionsmenu_Width + self.optionsmenu.get_width()
        # height menuItems
        self.mainmenu_Height = constants.WINDOW_HEIGHT*1/4 - self.mainmenu.get_height()//2
        self.startgamemenu_Height = self.mainmenu_Height + constants.MAINFONT
        self.highscoremenu_Height = self.startgamemenu_Height + constants.SUBFONT
        self.optionsmenu_Height = self.highscoremenu_Height + constants.SUBFONT
        self.exitmenu_Height = self.optionsmenu_Height + constants.SUBFONT
        self.menucolor = 'RED'

    def handleKeys(self, keysPressed):
        if keyBindings.checkPress('exit', keysPressed):
            pygame.quit()
        if keyBindings.checkPress('left', keysPressed):
            self.menuItems[self.selectedItem] = self.writeText(self.texts[self.selectedItem], self.subFont)
            self.selectedItem = (self.selectedItem - 1) % len(self.menuItems)
            self.menuItems[self.selectedItem] = self.writeText(self.texts[self.selectedItem], self.highlight)
        if keyBindings.checkPress('right', keysPressed):
            self.menuItems[self.selectedItem] = self.writeText(self.texts[self.selectedItem], self.subFont)
            self.selectedItem = (self.selectedItem + 1) % len(self.menuItems)
            self.menuItems[self.selectedItem] = self.writeText(self.texts[self.selectedItem], self.highlight)
            if keyBindings.checkPress('activate', keysPressed):
                print('entered loop')
                global GameState
                if self.selectedItem == 0:
                    GameState = GameStates.PLAYING
                    # return
                if self.selectedItem == 1:
                    GameState = GameStates.HIGHSCORES
                    # return
                if self.selectedItem == 2:
                    GameState = GameStates.OPTIONS
                    # return
                if self.selectedItem == 3:
                    pygame.quit()
                    # return

    def writeText(self, text, font):
        if font == self.mainFont:
            return self.mainFont.render(text, False, constants.colors['YELLOW'])
        if font == self.subFont:
            return self.subFont.render(text, False, constants.colors['YELLOW'])
        if font == self.highlight:
            return self.highlight.render(text, False, constants.colors['RED'])

    def updateMenu(self):
        Screen.fill(constants.colors["BLACK"])
        # Screen.blit(self.mainmenu, (self.mainmenu_Width, self.mainmenu_Height))
        # Screen.blit(self.startgamemenu, (self.startgamemenu_Width, self.startgamemenu_Height))
        # Screen.blit(self.highscoremenu, (self.highscoremenu_Width, self.highscoremenu_Height))
        # Screen.blit(self.optionsmenu, (self.optionsmenu_Width, self.optionsmenu_Height))
        # Screen.blit(self.exitmenu, (self.exitmenu_Width, self.exitmenu_Height))

        Screen.blit(self.mainmenu, (self.mainmenu_Width, self.mainmenu_Height))
        Screen.blit(self.menuItems[0], (self.startgamemenu_Width, self.startgamemenu_Height))
        Screen.blit(self.menuItems[1], (self.highscoremenu_Width, self.highscoremenu_Height))
        Screen.blit(self.menuItems[2], (self.optionsmenu_Width, self.optionsmenu_Height))
        Screen.blit(self.menuItems[3], (self.exitmenu_Width, self.exitmenu_Height))


    @staticmethod
    def evaluate(ballObj, collisionSpritesList):
        """
        Detect collisions, check findBounceIsVertical and objects.Ball.bounce()
        """
        collisions = pygame.sprite.spritecollide(ballObj, collisionSpritesList, False)

        # If no collisions happen
        if len(collisions) == 0:

            # then speeds do not change and function exits
            return

        # If there are collisions iterate through them
        # print(len(collisions), " collisions this frame")
        for c in collisions:

            # TODO decide which algorithm is better at detecting
            # TODO                              collision issues.
            isVertical_old = CollisionHandling.findBounceIsVertical_old(ballObj, c)
            isVertical = CollisionHandling.findBounceIsVertical(ballObj, c)
            if (isVertical != isVertical_old):
                # This print statement can be used to inspect discrepancies between the two
                # print("old vertical %s, new vertical %s" % (isVertical_old, isVertical))
                pass

            ballObj.bounce(isVertical)  # or change to the old one

            # Should be handled at the object collided with, not here
            AudioObj.playSound('bounce')

    @staticmethod
    def findBounceIsVertical(ballObj, collisionObj):
        """
        Returns True if the ball collides on a vertical surface
        If True, the ball's xspeed should be flipped
        :param ballObj: the ball object with which the collision happens
        :param collisionObj: the object collided with
        :return: True for vertical surface, False for horizontal surface
        """
        # see this link for explanation:
        # https://gamedev.stackexchange.com/questions/61705/pygame-colliderect-but-how-do-they-collide

        # phi = arctan(yspeed / xspeed)
        # result is in radians, ranging from -pi to pi
        # can be flipped by adding or subtracting pi
        tau = 2 * math.pi

        ball_in_angle = math.atan2(ballObj.yspeed, ballObj.xspeed)
        # Flip angle but keep range intact.
        ball_out_angle = ((ball_in_angle + tau) % tau) - math.pi

        coll_x = collisionObj.rect.width
        coll_y = collisionObj.rect.height

        topLeft  = math.atan2(-coll_y, -coll_x)
        topRight = math.atan2(-coll_y,  coll_x)
        botRight = math.atan2( coll_y,  coll_x)
        botLeft  = math.atan2( coll_y, -coll_x)

        # TODO simplify chained comparisons with a < b <= c
        top = topLeft < ball_out_angle <= topRight
        right = topRight < ball_out_angle <= botRight
        bottom = botRight < ball_out_angle <= botLeft
        # TODO surfaces hit on the left do not work.
        # TODO detecting the top and bottom should be enough but ill leave this todo in here in case weird stuff occurs
        left = botLeft < ball_out_angle <= topLeft

        return not (top or bottom)

    @staticmethod
    def findBounceIsVertical_old(ballObj, collisionObj):
        """
        returns True if bounce happens on a vertical surface
        This function seems to do alright, except for at large ball speeds.
        """
        # i copied this monster from stackoverflow so be warned
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
        # print(not top, not bot, not rgt, not lft)
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
    gameSounds = dict()

    def __init__(self):
        # Create gameSounds dictionary from the constants.sounds dictionary containing Sound objects
        for key in constants.sounds.keys():
            self.gameSounds[key] = pygame.mixer.Sound(constants.sounds[key])

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
        # TODO use pygame.mixer.music.set_endevent() for optimization

    def playSound(self, soundName):

        # Don't do anything if game sounds are disabled.
        if not constants.SOUND:
            return

        # TODO make it not create a new sound object instance every time it plays
        #   but instead save instances to be reused.
        self.gameSounds[soundName].play(0)


# Execute init() and main() only when program is run directly (not imported)
# Note: this needs to be at the end of this file,
#   otherwise stuff will be executed before python knows it exists
if __name__ == '__main__':
    print("\n\nWelcome to %s!\n\n" % constants.GAME_NAME)

    init()

    main()

    # Game loop broken, program exits
    pygame.quit()

    print("\n\nThank you for playing %s!\n\n" % constants.GAME_NAME)

    sys.exit()

else:
    print("Imported module main.py")


