"""


Sensor Pong


"""
import pygame, sys, math
import objects, constants, keyBindings, sensordb
import random
# import time # TODO use pygame.time functionality instead
# Ok so instead of time.time()  (s)
# It's pygame.time.get_ticks() (ms)


def init():
    """
    main.init() is called once at the very start of the program and sets up pygame.
    It also set some global variables used inside the pygame loop.
    Note: creating a multiline string using triple quotation marks is how you create python documentation
    """
    # Initialize all pygame modules
    pygame.mixer.pre_init(buffer=1024)
    pygame.display.init()
    pygame.font.init()
    pygame.mixer.init()

    # Set up screen
    global Screen
    Screen = pygame.display.set_mode((constants.WINDOW_WIDTH,
                                      constants.WINDOW_HEIGHT),
                                     pygame.FULLSCREEN if constants.FULLSCREEN
                                     else 0)

    # Set title of screen
    pygame.display.set_caption(constants.GAME_NAME) 
    # TODO create game icon and pygame.display.set_icon(Surface icon)

    global AudioObj
    AudioObj = Audio()

    global ClockObj
    ClockObj = pygame.time.Clock()  # create game clock

    global GameStateObj
    GameStateObj = MainMenu()

    # Avoid cluttering the pygame event queue
    pygame.event.set_allowed(None)
    pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])


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

        global GameStateObj
        GameStateObj.update(keysPressed)
        GameStateObj = GameStateObj.nextGameState
        # GameStateObj = GameStateObj.update(keysPressed)

        # Display fps in screen
        if constants.VIEWFPS:
            fps = pygame.font.Font(None, 30).render(str(int(ClockObj.get_fps())),
                                                    True,
                                                    constants.colors['WHITE'])
            Screen.blit(fps, (50, 50))

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


class Game:
    """
    main.Game class contains game generation and handling functionality.
    """
    # define variables to be initialized
    score = None
    # scoreMult = None

    playerBall = None
    paddle = None
    AllSpritesList = None
    CollisionSpritesList = None
    walls = [None, None, None, None]
    PowerUps = None
    currentPowerUps = None

    def __init__(self):
        # Create two empty sprite groups.
        # One for sprites to render, another for sprites to collision detect
        pygame.display.set_caption(constants.GAME_NAME + ' - Now Playing')

        self.AllSpritesList = pygame.sprite.Group()
        self.CollisionSpritesList = pygame.sprite.Group()
        self.powerUpSpritesList = pygame.sprite.Group()

        # Create Ball object
        self.playerBall = objects.Ball(constants.colors["WHITE"], constants.BALLRADIUS)
        self.AllSpritesList.add(self.playerBall)

        # Create paddle object
        self.paddle = objects.Paddle(constants.colors["WHITE"], constants.PADDLE_Y_POS,
                                     constants.PADDLEWIDTH, constants.PADDLEHEIGHT)
        self.AllSpritesList.add(self.paddle)
        self.CollisionSpritesList.add(self.paddle)

        # Create collision handling object
        self.collisionHandler = CollisionHandling(self)

        self.init_grid()
        self.time_until_next_block = 0
        self.last_block_time = 0
        self.blocklist=[]
        self.currentPowerUps=[]

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

        # Initialize score
        self.score = 0

        self.nextGameState = self

    def handleKeys(self, keysPressed):
        """
        Calls keyBindings.checkPress and responds accordingly
        """
        if keyBindings.checkPress('exit', keysPressed):
            # pygame.event.post(pygame.event.Event(pygame.QUIT))
            # TODO find some other way of delaying input
            # TODO -- OR use keyevents to handle inputs
            self.gameover()
            return

        if keyBindings.checkPress('left', keysPressed) and (self.paddle.rect.x > constants.WALLSIZE):
            self.paddle.rect.x -= constants.PADDLESPEED
        if keyBindings.checkPress('right', keysPressed) and (self.paddle.rect.x + self.paddle.width < (constants.WINDOW_WIDTH - constants.WALLSIZE)):
            self.paddle.rect.x += constants.PADDLESPEED

        # (re)set ball location when pressing K_HOME (cheat)
        if keyBindings.checkPress('restart', keysPressed):
            self.playerBall.respawn()

        if keyBindings.checkPress('activate', keysPressed):
            pass

    def check_powerup_status(self):
        for p in self.currentPowerUps:
            if p[0] < pygame.time.get_ticks():
                self.paddle.update_bonus()

                self.playerBall.update_bonus()

                self.currentPowerUps.remove(p)
                # TODO actually deactive powerup

    def update(self, keystohandle):
        """
        Updates sprites and stuff. Called once every frame while playing game.
        """
        # Handle collisions
        self.handleKeys(keystohandle)
        self.collisionHandler.evaluate()
        self.check_powerup_status()

        if pygame.time.get_ticks() >= self.last_block_time + self.time_until_next_block:
            self.last_block_time = pygame.time.get_ticks()
            self.addBlock()
            self.time_until_next_block = random.randint(constants.RESPAWNDELAY,constants.RESPAWNDELAY+constants.RESPAWNRANGE)

        Screen.fill(constants.colors["BLACK"])

        # Call the update() function of all sprites
        self.AllSpritesList.update()

        # draw sprites
        self.AllSpritesList.draw(Screen)

        ui_font = pygame.font.SysFont('arial', 30)
        score_view = ui_font.render(str(self.score),
                                        True,
                                        constants.colors['WHITE'])
        score_rect = score_view.get_rect()
        score_rect.right = constants.WINDOW_WIDTH - constants.WALLSIZE - 20
        score_rect.y = 50
        Screen.blit(score_view, score_rect)

        # pygame.time.delay(50)

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
            # each row contains list like [None, None, None, ...]
            self.grid.append([None] * constants.GRIDX)

        self.blocksize = (constants.WINDOW_WIDTH-(2*constants.GRIDMARGIN))//constants.GRIDX

    def addBlock(self):

        newblock = objects.Block(self.blocksize-(2*constants.BLOCKMARGIN), self.blocksize-(2*constants.BLOCKMARGIN))

        # But maybe the grid stuff can stay here

        newblock.x_on_grid=random.randint(1,constants.GRIDX)-1
        newblock.y_on_grid=random.randint(1,constants.GRIDY)-1

        if not self.grid[newblock.y_on_grid][newblock.x_on_grid]:
            newblock.rect.x=constants.GRIDMARGIN + self.blocksize*newblock.x_on_grid + constants.BLOCKMARGIN
            newblock.rect.y=constants.GRIDMARGIN + self.blocksize*newblock.y_on_grid + constants.BLOCKMARGIN
            self.AllSpritesList.add(newblock)
            self.CollisionSpritesList.add(newblock)
            self.blocklist.append(newblock)
            self.grid[newblock.y_on_grid][newblock.x_on_grid] = newblock

    def inc_score(self, points):
        self.score += points

    def gameover(self):
        sensordb.insertscore('jemoeder', self.score)
        print(sensordb.get_scores())
        pygame.time.delay(500)
        self.nextGameState = MainMenu()


class CollisionHandling:
    """
    class containing collision handling functions
    """
    def __init__(self, game):
        self.game = game

    def evaluate(self):
        self.handle_ball_collisions()
        self.handle_power_up_collisions()

    def handle_ball_collisions(self):
        """
        detect collisions, check findBounceIsVertical and objects.Ball.bounce()
        """

        collisions = pygame.sprite.spritecollide(self.game.playerBall, self.game.CollisionSpritesList, False)

        for c in collisions:
            # Collision happens with block (instead of paddle or ball)
            if isinstance(c, objects.Block):
                c_newhp = c.reduceHP(self.game.playerBall.xspeed, self.game.playerBall.yspeed)
                if c_newhp <= 0:

                    self.game.inc_score(c.score)

                    if c.type=="red":
                        newPowerUp = objects.PowerUp.PowerUpSprite(self.game.playerBall.rect.x, self.game.playerBall.rect.y, "red", self.game)
                        self.game.AllSpritesList.add(newPowerUp)
                        self.game.powerUpSpritesList.add(newPowerUp)
                    elif c.type=="blue":
                        newPowerUp = objects.PowerUp.PowerUpSprite(self.game.playerBall.rect.x, self.game.playerBall.rect.y, "blue", self.game)
                        self.game.AllSpritesList.add(newPowerUp)
                        self.game.powerUpSpritesList.add(newPowerUp)
                    elif c.type=="green":
                        newPowerUp = objects.PowerUp.PowerUpSprite(self.game.playerBall.rect.x, self.game.playerBall.rect.y, "green", self.game)
                        self.game.AllSpritesList.add(newPowerUp)
                        self.game.powerUpSpritesList.add(newPowerUp)
                    # Randomly generate powerup
                    elif random.random() < constants.POWERUP_CHANCE:
                        # Create object and add to relevant sprite lists
                        newPowerUp = objects.PowerUp.PowerUpSprite(self.game.playerBall.rect.x, self.game.playerBall.rect.y, "random", self.game)
                        self.game.AllSpritesList.add(newPowerUp)
                        self.game.powerUpSpritesList.add(newPowerUp)

                    self.game.removeblock(c)

            elif isinstance(c, objects.Wall) and c.name == 'bottom_wall':
                if not constants.GODMODE:
                    self.game.gameover()

            isVertical = CollisionHandling.find_bounce_is_vertical(self.game.playerBall, c)

            self.game.playerBall.bounce(isVertical)

            # Should be handled at the object collided with, not here
            AudioObj.playSound('bounce')

    def handle_power_up_collisions(self):
        # After checking ball collisions, check for powerups to collect
        powerUpCollisions = pygame.sprite.spritecollide(self.game.paddle, self.game.powerUpSpritesList, True)
        for c in powerUpCollisions:

            (powerup_entry,powerup_properties) = c.powerUp.activate()
            # TODO actually activate powerup

            powerup_color=constants.colors[  powerup_properties[1]  ]
            factor = powerup_properties[5]

            if powerup_properties[3]=="ball":
                powerup_object=self.game.playerBall
            elif powerup_properties[3]=="paddle":
                powerup_object=self.game.paddle

            powerup_entry.append(powerup_object)
            skip = False
            for entry in self.game.currentPowerUps:
                if powerup_entry[1] == entry [1] and powerup_entry is not entry:
                    skip = True
            if not skip:
                if powerup_properties[4]=="radius":
                    powerup_object.radius = int(factor * powerup_object.radius)

                elif powerup_properties[4]=="speed":
                    powerup_object.xspeed = int(factor * powerup_object.xspeed)
                    powerup_object.yspeed = int(factor * powerup_object.yspeed)

                elif powerup_properties[4]=="width":
                    powerup_object.width = int(factor * powerup_object.width)

            # TODO update paddle size, ball size, ball speed
            # TODO unset powerups

            powerup_object.active_power.append(powerup_entry)
            self.game.currentPowerUps.append(powerup_entry)

            powerup_object.color=powerup_color
            powerup_object.update_bonus()

            self.game.AllSpritesList.remove(c)
            self.game.powerUpSpritesList.remove(c)

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
        ball_in_angle = math.atan2(ballObj.rect.centery - collisionObj.rect.centery,
                                   ballObj.rect.centerx - collisionObj.rect.centerx)

        coll_x = collisionObj.rect.width
        coll_y = collisionObj.rect.height

        top_left  = math.atan2(-coll_y, -coll_x)
        top_right = math.atan2(-coll_y,  coll_x)
        bot_right = math.atan2( coll_y,  coll_x)
        bot_left  = math.atan2( coll_y, -coll_x)

        top = top_left < ball_in_angle <= top_right
        bottom = bot_right < ball_in_angle <= bot_left

        return not (top or bottom)



class MainMenu:
    """
    contains menu rendering and keyhandling specific to menu
    """
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

    ## revamp ##
    entries = None

    def __init__(self):
        pygame.display.set_caption(constants.GAME_NAME + ' - Main menu' )
        self.texts = ['Start game', 'Highscores', 'Options', 'Exit']
        self.mainFont = pygame.font.SysFont('arial', 60) # 76? HEIGTH
        self.subFont = pygame.font.SysFont('arial', 50) # 58 HEIGTH
        self.highlight = pygame.font.SysFont('arial', 50, bold=True)
        self.highlight.set_underline(True)

        self.mainmenu = self.highField('Main Menu', self, self.mainFont)
        self.startgamemenu = self.highField(self.texts[0], self, self.highlight)
        self.highscoremenu = self.highField(self.texts[1], self, self.subFont)
        self.optionsmenu = self.highField(self.texts[2], self, self.subFont)
        self.exitmenu = self.highField(self.texts[3], self, self.subFont)
        self.menuItems = {0: self.startgamemenu, 1: self.highscoremenu, 2: self.optionsmenu, 3: self.exitmenu}
        self.selectedItem = 0

        # self.mainmenu_Width = constants.WINDOW_WIDTH // 2 - self.mainmenu.width//2
        # self.mainmenu_Height = constants.WINDOW_HEIGHT*1/4 - self.mainmenu.height//2
        # self.widths = [ self.mainmenu_Width + constants.MAINFONT, self.widths[0] + constants.SUBFONT,
        #                self.widths[2] + constants.SUBFONT, self.widths[3] + constants.SUBFONT ]
        self.mainmenu_Width = constants.WINDOW_WIDTH // 2 - self.mainmenu.width//2
        self.startgamemenu_Width = 30 #constants.WINDOW_WIDTH/1000 # + self.startgamemenu.get_width()//2
        self.highscoremenu_Width = self.startgamemenu_Width + self.startgamemenu.width
        self.optionsmenu_Width = self.highscoremenu_Width + self.highscoremenu.width
        self.exitmenu_Width = self.optionsmenu_Width + self.optionsmenu.width
        # self.heights = {0: self.mainmenu_Height + constants.MAINFONT, 1: self.heights[0] + constants.SUBFONT,
        #                 2: self.heighs[2] + constants.SUBFONT, 3: self.heights[3] + constants.SUBFONT }
        self.mainmenu_Height = constants.WINDOW_HEIGHT*1/4 - self.mainmenu.height//2
        self.startgamemenu_Height = self.mainmenu_Height + constants.MAINFONT
        self.highscoremenu_Height = self.startgamemenu_Height + constants.SUBFONT
        self.optionsmenu_Height = self.highscoremenu_Height + constants.SUBFONT
        self.exitmenu_Height = self.optionsmenu_Height + constants.SUBFONT

        AudioObj.playMusic('menu')

        self.nextGameState = self

    class highField():
        parent = None
        width = None
        height = None
        text = None

        def __init__(self, text, parent, chosenfont=None):
            self.parent = parent
            if chosenfont == (None or self.parent.subFont):
                # print('none')
                self.text = self.parent.subFont.render(text, False, constants.colors['GREEN'])
            elif chosenfont == self.parent.mainFont:
                # print('main')
                self.text = self.parent.mainFont.render(text, False, constants.colors['WHITE'])
            else:
                print('high')
                self.text = self.parent.highlight.render(text, False, constants.colors['RED'])

            self.width = self.text.get_width()
            self.height = self.text.get_height()

    def handleKeys(self, keysPressed):
        if keyBindings.checkPress('exit', keysPressed):
            pygame.event.post(pygame.event.Event(pygame.QUIT))
            return

        if keyBindings.checkPress('left', keysPressed):
            self.move('left')
            # self.menuItems[self.selectedItem] = self.highField(self.texts[self.selectedItem], self, chosenfont=self.subFont)
            # self.selectedItem = (self.selectedItem - 1) % len(self.menuItems)
            # self.menuItems[self.selectedItem] = self.highField(self.texts[self.selectedItem], self, chosenfont=self.highlight)

        if keyBindings.checkPress('right', keysPressed):
            self.move('right')
            # self.menuItems[self.selectedItem] = self.highField(self.texts[self.selectedItem], self, chosenfont=self.subFont)
            # self.selectedItem = (self.selectedItem + 1) % len(self.menuItems)
            # self.menuItems[self.selectedItem] = self.highField(self.texts[self.selectedItem], self, chosenfont=self.highlight)
        if keyBindings.checkPress('activate', keysPressed):

            global GameStateObj

            if self.selectedItem == 0:
                self.nextGameState = Game()

            elif self.selectedItem == 1:
                self.nextGameState = HighScores()

            elif self.selectedItem == 2:
                pass

            elif self.selectedItem == 3:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    def move(self, move):
        self.menuItems[self.selectedItem] = self.highField(self.texts[self.selectedItem], self,
                                                           chosenfont=self.subFont)
        self.selectedItem = (self.selectedItem + (1 if move == 'right' else - 1)) % len(self.menuItems)
        self.menuItems[self.selectedItem] = self.highField(self.texts[self.selectedItem], self,
                                                           chosenfont=self.highlight)

    def update(self, keystohandle):
        self.handleKeys(keystohandle)
        Screen.fill(constants.colors["BLACK"])
        Screen.blit(self.mainmenu.text, (self.mainmenu_Width, self.mainmenu_Height))
        Screen.blit(self.menuItems[0].text, (self.startgamemenu_Width, self.startgamemenu_Height))
        Screen.blit(self.menuItems[1].text, (self.highscoremenu_Width, self.highscoremenu_Height))
        Screen.blit(self.menuItems[2].text, (self.optionsmenu_Width, self.optionsmenu_Height))
        Screen.blit(self.menuItems[3].text, (self.exitmenu_Width, self.exitmenu_Height))

        pygame.time.delay(80)


class HighScores:
    """
    contains rendering for highscores menu and keyhandling specific to highscores menu
    """
    highMenu = None
    rows = None
    window = 0
    pages = 0

    def __init__(self):
        pygame.display.set_caption(constants.GAME_NAME + ' - HighScores')
        self.mainFont = pygame.font.SysFont('informalroman', 60)  # 76? HEIGTH
        self.subFont = pygame.font.SysFont('couriernew', 50)  # 58 HEIGTH
        self.pageFont = pygame.font.SysFont('courgiernew', 60)
        self.highlight = pygame.font.SysFont('couriernew', 50, bold=True)
        self.highlight.set_underline(True)
        self.highMenu = self.highField('HIGHSCORES', self, chosenfont=self.mainFont)
        scores = sensordb.get_scores()
        self.pages = sensordb.get_pages()
        print('number of pages:' + str(self.pages) )
        self.rows = [None]*constants.SHOW
        for x in range(0, len(scores)):
            # print('concat is: '+ scores[x][0] + ' ' + str(scores[x][1]))
            self.rows[x] = self.highField('{:<9.9s}   {:>4d}'
                                          .format(scores[x][0],  scores[x][1]), self)
        AudioObj.playMusic('highScore')
        self.nextGameState = self

    class highField():
        parent = None
        width = None
        height = None
        text = None

        def __init__(self, text, parent, chosenfont=None):
            self.parent = parent
            if chosenfont == (None or self.parent.subFont):
                # print('none')
                self.text = self.parent.subFont.render(text, False, constants.colors['GREEN'])
            elif chosenfont == self.parent.mainFont:
                # print('main')
                self.text = self.parent.mainFont.render(text, False, constants.colors['WHITE'])
            elif chosenfont == self.parent.pageFont:
                # print('pagefont')
                self.text = self.parent.pageFont.render(text, False, constants.colors['WHITE'])
            else:
                # print('high')
                self.text = self.parent.highlight.render(text, False, constants.colors['RED'])

            self.width = self.text.get_width()
            self.height = self.text.get_height()
        # def settext(self, newtext, chosenfont=None):
        #     if chosenfont == (None or self.parent.subFont):
        #         # print('none')
        #         self.text = self.parent.subFont.render(newtext, False, constants.colors['GREEN'])
        #     elif chosenfont == self.parent.mainFont:
        #         # print('main')
        #         self.text = self.parent.mainFont.render(newtext, False, constants.colors['WHITE'])
        #     elif chosenfont == self.parent.pageFont:
        #         # print('pagefont')
        #         self.text = self.parent.pageFont.render(newtext, False, constants.colors['WHITE'])
        #     else:
        #         # print('high')
        #         self.text = self.parent.highlight.render(newtext, False, constants.colors['RED'])

    def handleKeys(self, keysPressed):

        if keyBindings.checkPress('exit', keysPressed):
            self.nextGameState = MainMenu()
            pygame.time.delay(500)
            return

        if keyBindings.checkPress('left', keysPressed):
            print('entered with window:', self.window)
            if self.window == 0:
                print('should start mainmenu...')
                self.nextGameState = MainMenu()
            else:
                self.window = self.window - 1
                scores = sensordb.get_scores(offset=(constants.SHOW * self.window))
                print('new set:' + str(scores))
                self.rows = [None] * constants.SHOW
                for x in range(0, len(scores)):
                    # print('concat is: ' + scores[x][0] + ' ' + str(scores[x][1]))
                    self.rows[x] = self.highField('{:<9.9s}   {:>4d}'
                                                  .format(scores[x][0], scores[x][1]), self)
            print('current:' + str(self.window))

        if keyBindings.checkPress('right', keysPressed):
            sumNone = sum(x is None for x in self.rows)
            print('entered with window:', self.window)
            if sumNone != 0:
                pass
            else:
                self.window = self.window + 1
                scores = sensordb.get_scores(constants.SHOW*self.window)
                print('new set:' + str(scores))
                self.rows = [None] * constants.SHOW
                for x in range(0, len(scores)):
                    # print('concat is: ' + scores[x][0] + ' ' + str(scores[x][1]))
                    self.rows[x] = self.highField('{:<9.9s}   {:>4d}'
                                                  .format(scores[x][0], scores[x][1]), self)
        print('current:' + str(self.window))

    def update(self, keysPressed):
        self.handleKeys(keysPressed)

        Screen.fill(constants.colors["BLACK"])
        Screen.blit(self.highMenu.text, (constants.WINDOW_WIDTH // 2 - self.highMenu.width//2, self.highMenu.height))
        i = 0
        for x in self.rows:
            if type(x) is self.highField:
                if i == 0:
                    Screen.blit(x.text,
                                (constants.WINDOW_WIDTH // 2 - self.highMenu.width*0.70, (self.highMenu.height + constants.MAINFONT)))

                else:
                    pass
                    Screen.blit(x.text, (constants.WINDOW_WIDTH // 2 -
                                         self.highMenu.width*0.70, (constants.SUBFONT*0.9*i +
                                                                    self.highMenu.height + constants.MAINFONT)))
                i = i + 1
        pagecount = self.highField(str(self.window) + '/' + str(self.pages), self, self.pageFont)
        Screen.blit(pagecount.text, (constants.WINDOW_WIDTH - pagecount.width - 20, constants.WINDOW_HEIGHT - pagecount.height - 20))
        pygame.time.delay(80)


class Audio:
    """
    Handles playing music and sound effects. Uses sound mapping from constants.sounds and constants.music
    """

    trackPlaying = None
    trackToPlay = None
    gameSounds = dict()

    def __init__(self):
        # Create gameSounds dictionary from the constants.sounds dictionary containing Sound objects
        for key in constants.sounds.keys():
            self.gameSounds[key] = pygame.mixer.Sound(constants.sounds[key][0])
            self.gameSounds[key].set_volume(constants.sounds[key][1])

        self.fadeoutTime = constants.MUSICFADE

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
            pygame.mixer.music.load(self.trackToPlay[0])
            pygame.mixer.music.set_volume(self.trackToPlay[1])
            pygame.mixer.music.play(0)
            self.trackPlaying = self.trackToPlay
        # TODO use pygame.mixer.music.set_endevent() for optimization

    def playSound(self, soundName):

        # Don't do anything if game sounds are disabled.
        if not constants.SOUND:
            return

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


