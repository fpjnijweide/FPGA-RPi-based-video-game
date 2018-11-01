# ==== Global variables should be defined here
# Game name string
GAME_NAME = "Sensor Pong" # use this when referencing the game name so that we can easily change it
# GAME_VERSION = '0.0.1' # not used currently but might be nice eventually

# GPIO pin definitions
# TODO check if we can still use dictionary in threads? Sequentially, it does not work.
# READ_PINS={"XSPEED:23,
#            "YSPEED":24,
#            "PADDLESPEED":25,
#            "BUTTONS":26}
# WRITE_PINS={"XSPEED":17,
#             "YSPEED":18,
#             "BOUNCINESS":27,
#             "IS_VERTICAL":22}
READ_PINS=[("XSPEED",16),("YSPEED",17),("PADDLESPEED",18),("BUTTONS",19)] #name, BCM, wiringpi
WRITE_PINS=[("XSPEED",23),("YSPEED",24),("BOUNCINESS",25),("IS_VERTICAL",26)]#name, BCM, wiringpi
CLOCK_PIN=20
MOSI_PIN=10
CLOCKSPEED=1000
DUTYCYCLE=127

# Offload functions to FPGA and receive from FPGA
FPGA_ENABLED = False

# Do we send and receive data over GPIO at same time, or wait?
GPIO_SEND_RECEIVE_AT_ONCE=False

# Prevent losing the game
GODMODE = True

# Audio settings
SOUND = True
MUSIC = True

# Window resolution
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FULLSCREEN = True

MAINFONT = 70
SUBFONT = 58
#db
SHOW = 7

# Frames per second
FPS = 60
VIEWFPS = True

# Ball size and pos
BALLRADIUS = 7
INITIAL_BALL_X = 30
INITIAL_BALL_Y = 30

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
POWERUP_CHANCE = 0.9

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


# Block respawn time range
RESPAWNDELAY = 420
RESPAWNRANGE = 2069

# Color definitions
colors = {
        "GRAY"     : (100, 100, 100),
        "NAVYBLUE" : ( 60,  60, 100),
        "WHITE"    : (255, 255, 255),
        "RED"      : (255,   0,   0),
        "GREEN"    : (  0, 255,   0),
        "BLUE"     : (  0,   0, 255),
        "YELLOW"   : (255, 255,   0),
        "ORANGE"   : (255, 128,   0),
        "PURPLE"   : (255,   0, 255),
        "CYAN"     : (  0, 255, 255),
        "BLACK"    : (  0,   0,   0),
        "COMBLUE"  : (233, 232, 255)
}

# Audio track mapping
# 'audioName':('relative/path/to/file', volume)
sounds = {
        'bounce': ('../resources/audio/bounce.ogg', 0.05)
#        'wallCollision':'../resources/audio/bounce.wav',
#        'blockbreak':'../resources/sound/bounce2.wav'
}
music  = {
        'main': '../resources/audio/main.ogg',
        'menu': '../resources/audio/menu.ogg',
        'highScore': '../resources/audio/hiscore.ogg'
#        'newGame': '../resources/audio/<file>.ogg',
#        'gameOver': '../resources/audio/<file>.ogg',
}
# ms for music to fade out when switching screens
MUSICFADE = 1000


