"""


Sensor Pong


"""
import pygame, sys, math
import objects, constants, keyBindings
from enum import Enum
import random
import time


def init():
    """
    main.init() is called once at the very start of the program and sets up pygame.
    It also set some global variables used inside the pygame loop.
    Note: creating a multiline string using triple quotation marks is how you create python documentation
    """
    pygame.mixer.pre_init()  # TODO set right variables inside this
    # Initialize pygame  # TODO only init necessary pygame modules for efficiency
    pygame.init()

    # Set up screen
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
    GameObj = None  # Game()
    global MenuObj
    MenuObj = MainMenu()  # None
    # global HighObj
    # HighObj = HighScores()


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
        if GameState == GameStates.MAINMENU:
            MenuObj.handleKeys(keysPressed)
            MenuObj.updateMenu()
        if GameState == GameStates.HIGHSCORES:
            HighObj.handleKeys(keysPressed)
            HighObj.updateHigh()

        # elif GameState == GameStates.MAINMENU:
        # Do MainMenuObj.handleKeys and updateGame

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
    MAINMENU = 0
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
    PowerUps = None
    readyPowerUp = None

    # self.collisionHandler

    def __init__(self):
        # Create two empty sprite groups.
        # One for sprites to render, another for sprites to collision detect
        self.AllSpritesList = pygame.sprite.Group()
        self.CollisionSpritesList = pygame.sprite.Group()
        # also one for powerups
        self.powerUpSpritesList = pygame.sprite.Group()

        # Create Ball object
        self.playerBall = objects.Ball(constants.colors["WHITE"], constants.BALLRADIUS)
        self.AllSpritesList.add(self.playerBall)

        # Create paddle object
        self.paddle = objects.Paddle(constants.colors["WHITE"], constants.PADDLE_Y_POS, constants.PADDLEWIDTH, constants.PADDLEHEIGHT)
        self.AllSpritesList.add(self.paddle)
        self.CollisionSpritesList.add(self.paddle)

        # Create collision handling object
        self.collisionHandler = CollisionHandling(self)

        # Create object for powerup handling and (empty) sprite list
        self.powerUps = objects.PowerUp()

        self.init_grid()
        self.time_until_next_block = 0
        self.last_block_time = 0
        self.blocklist=[]

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

        if keyBindings.checkPress('left', keysPressed) and (self.paddle.rect.x > (constants.PADDLEWIDTH//2)):
            self.paddle.rect.x -= constants.PADDLESPEED
        if keyBindings.checkPress('right', keysPressed) and (self.paddle.rect.x < (constants.WINDOW_WIDTH - constants.PADDLEWIDTH*1.5)):
            self.paddle.rect.x += constants.PADDLESPEED

        # (re)set ball location when pressing K_HOME (cheat)
        if keyBindings.checkPress('restart', keysPressed):
            self.playerBall.respawn()

        if keyBindings.checkPress('activate', keysPressed) and self.readyPowerUp:
            self.readyPowerUp.activate()
            self.readyPowerUp = None

    def updateGame(self):
        """
        Updates sprites and stuff. Called once every frame while playing game.
        """
        # Handle collisions
        self.collisionHandler.evaluate()

        # Note: collision handling is less broken yet once again, but the ball still disappears into the walls
        #self.playerBall.update()

        if time.time() >= self.last_block_time + self.time_until_next_block:
            self.last_block_time=time.time()
            self.time_until_next_block = self.addBlock()

        Screen.fill(constants.colors["BLACK"])

        # Call the update() function of all sprites
        self.AllSpritesList.update()

        # draw sprites
        self.AllSpritesList.draw(Screen)

    def removeblock(self, obj1):
        self.AllSpritesList.remove(obj1)
        self.CollisionSpritesList.remove(obj1)
        self.blocklist.remove(obj1)
        self.grid[obj1.y_on_grid][obj1.x_on_grid]=None
        del obj1

    def init_grid(self):
        # Okay i tried to rewrite this so we dont need to install numpy for a single line of code
        # self.grid = np.ndarray(([constants.GRIDY,constants.GRIDX]),dtype=np.object)

        self.grid = []
        # grid is list of Y lists with X items (initialized to none)
        for row in range(0, constants.GRIDY):
            # row contains list like [None, None, None, ...]
            self.grid.append([None] * constants.GRIDX)

        self.blocksize = (constants.WINDOW_WIDTH-(2*constants.GRIDMARGIN))//constants.GRIDX

    def addBlock(self):
        throwdice=random.randint(1,100)
        if throwdice >= 70 and throwdice<85:
            blocktype="green"
        elif throwdice >= 85 and throwdice<95:
            blocktype="blue"
        elif throwdice >= 95:
            blocktype="red"
        else:
            blocktype="default"
        newblock = objects.Block(blocktype,self.blocksize-(2*constants.BLOCKMARGIN), self.blocksize-(2*constants.BLOCKMARGIN))
        newblock.x_on_grid=random.randint(1,constants.GRIDX)-1
        newblock.y_on_grid=random.randint(1,constants.GRIDY)-1

        if self.grid[newblock.y_on_grid][newblock.x_on_grid] == None:
            newblock.rect.x=constants.GRIDMARGIN + self.blocksize*newblock.x_on_grid + constants.BLOCKMARGIN
            newblock.rect.y=constants.GRIDMARGIN + self.blocksize*newblock.y_on_grid + constants.BLOCKMARGIN
            self.AllSpritesList.add(newblock)
            self.CollisionSpritesList.add(newblock)
            self.blocklist.append(newblock)
            time_until_next_block = random.randint(constants.RESPAWNDELAY,constants.RESPAWNDELAY+constants.RESPAWNRANGE)
            return time_until_next_block
        else:
            del newblock
            return 0


class CollisionHandling:

    """
    class containing collision handling functions
    """
    # README CollisionHandling:
    # Both verticality-detecting methods have some problems.
    # The old function will behave unpredictably when the ball's speed is high
    # The new function is bad at detecting collisions on small sides of a large rectangle.
    def __init__(self, game):
        self.game = game
        self.next_collision_exclusion=[]
        self.next_collision_exclusion_time=[]

    def evaluate(self):
        self.handle_ball_collisions()
        self.handle_power_up_collisions()

    def handle_ball_collisions(self):
        """
        detect collisions, check findBounceIsVertical and objects.Ball.bounce()
        """
        index=0
        for col_timer in self.next_collision_exclusion_time:
            if time.time()>col_timer:
                del self.next_collision_exclusion[index]
                del self.next_collision_exclusion_time[index]
            index += 1

        collisions = pygame.sprite.spritecollide(self.game.playerBall, self.game.CollisionSpritesList, False)

        if len(collisions) > 1:
            print(collisions)
        for c in collisions:

            if c not in self.next_collision_exclusion:

                # Collision happens with block (instead of paddle or ball)
                if isinstance(c, objects.Block):
                    c_newhp = c.reduceHP(self.game.playerBall.xspeed, self.game.playerBall.yspeed)
                    if c_newhp <= 0:
                        GameObj.removeblock(c)

                        # Randomly generate powerup
                        if random.random() < constants.POWERUP_CHANCE:
                            # Create object and add to relevant sprite lists
                            newPowerUp = objects.PowerUp.PowerUpSprite(self.game.playerBall.rect.x, self.game.playerBall.rect.y)
                            self.game.AllSpritesList.add(newPowerUp)
                            self.game.powerUpSpritesList.add(newPowerUp)

                isVertical_old = CollisionHandling.find_bounce_is_vertical_old(self.game.playerBall, c)
                isVertical = CollisionHandling.find_bounce_is_vertical(self.game.playerBall, c)

                self.game.playerBall.bounce(isVertical)  # or change to the old one

                # Should be handled at the object collided with, not here
                # AudioObj.playSound('bounce')
                self.next_collision_exclusion.append(c)
                self.next_collision_exclusion_time.append(time.time()+0.2)

    def handle_power_up_collisions(self):
        # After checking ball collisions, check for powerups to collect
        powerUpCollisions = pygame.sprite.spritecollide(self.game.paddle, self.game.powerUpSpritesList, True)
        for c in powerUpCollisions:
            self.game.readyPowerUp = c.powerUp
            print("caught %s powerup" % self.game.readyPowerUp.type)

    @staticmethod
    def find_bounce_is_vertical(ballObj, collisionObj):
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

        top_left  = math.atan2(-coll_y, -coll_x)
        top_right = math.atan2(-coll_y,  coll_x)
        bot_right = math.atan2( coll_y,  coll_x)
        bot_left  = math.atan2( coll_y, -coll_x)

        top = top_left < ball_out_angle <= top_right
        bottom = bot_right < ball_out_angle <= bot_left
        # right = top_right < ball_out_angle <= bot_right
        # left = bot_left < ball_out_angle <= top_left

        return not (top or bottom)

    @staticmethod
    def find_bounce_is_vertical_old(ballObj, collisionObj):
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

class HighScores:
    def updateHigh(self):
        pass
    def handleKeys(self, keysPressed):
        pass


class MainMenu:
    """
    contains menu rendering and keyhandling specific to menu
    i mean not yet but it should
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

        AudioObj.playMusic('menu')

    def handleKeys(self, keysPressed):
        if keyBindings.checkPress('exit', keysPressed):
            pygame.event.post(pygame.event.Event(pygame.QUIT))
            return

        if keyBindings.checkPress('left', keysPressed):
            self.menuItems[self.selectedItem] = self.writeText(self.texts[self.selectedItem], self.subFont)
            self.selectedItem = (self.selectedItem - 1) % len(self.menuItems)
            self.menuItems[self.selectedItem] = self.writeText(self.texts[self.selectedItem], self.highlight)

        if keyBindings.checkPress('right', keysPressed):
            self.menuItems[self.selectedItem] = self.writeText(self.texts[self.selectedItem], self.subFont)
            self.selectedItem = (self.selectedItem + 1) % len(self.menuItems)
            self.menuItems[self.selectedItem] = self.writeText(self.texts[self.selectedItem], self.highlight)

        if keyBindings.checkPress('activate', keysPressed):

            global GameState
            global MainObj

            if self.selectedItem == 0:
                GameState = GameStates.PLAYING
                global GameObj
                GameObj = Game()
                MainObj = None

            elif self.selectedItem == 1:
                GameState = GameStates.HIGHSCORES

            elif self.selectedItem == 2:
                GameState = GameStates.OPTIONS

            elif self.selectedItem == 3:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    # TODO use subclass instances for the various screen items
    class menuOption:
        width = None
        height = None

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

        # time.sleep(0.2)


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


