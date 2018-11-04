# ==== Global variables should be defined here
# Game name string
GAME_NAME = "Sensor Pong" # use this when referencing the game name so that we can easily change it

# GPIO pin definitions
READ_PINS={"XSPEED":23,
           "YSPEED":24,
           "PADDLESPEED":25,
           "BUTTONS":26}
WRITE_PINS={"XSPEED":17,
            "YSPEED":18,
            "BOUNCINESS":27,
            "IS_VERTICAL":22}
CLOCK_PIN=11
MOSI_PIN=10
CLOCKSPEED=1000
DUTYCYCLE=127

# Offload functions to FPGA and receive from FPGA
FPGA_ENABLED = False

# Do we send and receive data over GPIO at same time, or wait?
GPIO_SEND_RECEIVE_AT_ONCE=False

# Prevent losing the game
GODMODE = False

# Audio settings
SOUND = True
MUSIC = True

# Window resolution
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FULLSCREEN = False

MAINFONT = 70
SUBFONT = 58
#db
SHOW = 7

# Frames per second
FPS = 60
VIEWFPS = True
# MAINMENUMOVES = 5  # indicates amount of times you can move left or write in main menu

# Ball size and pos
BALLRADIUS = 7
INITIAL_BALL_X = 30
INITIAL_BALL_Y = 120

#Ball speed
INITIAL_BALL_XSPEED = 6
INITIAL_BALL_YSPEED = INITIAL_BALL_XSPEED

# Wall size
WALLSIZE = 20

# Paddle size
PADDLEWIDTH  = 113
PADDLEHEIGHT = 13
PADDLE_Y_POS = 520
PADDLEBOUNCINESS=1

# Powerup chance
# TODO chance per destroyed block, not global
POWERUP_CHANCE = 0.2

# Paddle speed
PADDLESPEED = 10

# Block size
BLOCKWIDTH  = 100
BLOCKHEIGHT = 100
BLOCK_INITIAL_HP = 2
BLOCKMARGIN = 5  # (margin of block within grid)

# Block grid size
GRIDX = 10
GRIDY = 3
GRIDMARGIN = 100

# Blocks will not spawn if within n pixels from the ball
MINSPAWNDIST = 150

# Block respawn time range
RESPAWNDELAY = 169
RESPAWNRANGE = 1969

# Powerup fall speed
POWERSPEED = 1.8

# Color definitions
colors = {
        "GRAY"    : (100, 100, 100),
        "NAVYBLUE": ( 60,  60, 100),
        "WHITE"   : (255, 255, 255),
        "RED"     : (255,   0,   0),
        "GREEN"   : (  0, 255,   0),
        "BLUE"    : (  0,   0, 255),
        "YELLOW"  : (255, 255,   0),
        "ORANGE"  : (255, 128,   0),
        "PURPLE"  : (255,   0, 255),
        "CYAN"    : (  0, 255, 255),
        "BLACK"   : (  0,   0,   0),
        "COMBLUE" : (233, 232, 255)
}

# Audio track mapping
# 'audioName':('relative/path/to/file', volume)
sounds = {
        'bounce': ('../resources/audio/bounce.ogg', 0.11),
        'gameover':('../resources/audio/dead.ogg', 0.25)
#        'wallCollision':'../resources/audio/bounce.wav',
#        'blockbreak':'../resources/sound/bounce2.wav'
}
music  = {
        'main': ('../resources/audio/main.ogg', 1.0),
        'menu': ('../resources/audio/menu.ogg', 0.6),
        'highScore': ('../resources/audio/hiscore.ogg', 0.4)
#        'newGame': '../resources/audio/<file>.ogg',
#        'gameOver': '../resources/audio/<file>.ogg',
}
# ms for music to fade out when switching screens
MUSICFADE = 1000

# Image mapping
# 'name':'relative/path'
img = {
    'icon': '../resources/img/icon.bmp'
}


# Font mapping
# 'name':'relative/path'
fonts = {
    'optimusprinceps':'../resources/fonts/OptimusPrinceps.ttf'
}

