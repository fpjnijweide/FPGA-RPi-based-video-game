# ==== Global variables should be defined here
# Note: User-Customizable variables (settings) should be defined in a different,
# not-yet created .txt or .conf or whatever file [TODO]
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
READ_PINS=[("XSPEED",23,4),("YSPEED",24,5),("PADDLESPEED",25,6),("BUTTONS",26,25)] #name, BCM, wiringpi
WRITE_PINS=[("XSPEED",17,0),("YSPEED",18,1),("BOUNCINESS",27,2),("IS_VERTICAL",22,3)]#name, BCM, wiringpi
CLOCK_PIN=20
MOSI_PIN=10
CLOCKSPEED=1000
DUTYCYCLE=127

# Offload functions to FPGA and receive from FPGA
FPGA_ENABLED = False

# Do we send and receive data over GPIO at same time, or wait?
GPIO_SEND_RECEIVE_AT_ONCE=False

# Audio settings
SOUND = False
MUSIC = True

# Window resolution
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_HW = WINDOW_WIDTH//2
WINDOW_HH = WINDOW_HEIGHT//2
MAINFONT = 70
SUBFONT = 58


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
PADDLEWIDTH  = 90
PADDLEHEIGHT = 13
PADDLE_Y_POS = 520
PADDLEBOUNCINESS=1

# Powerup chance
# TODO chance per destroyed block, not global
POWERUP_CHANCE = 0.9

# Paddle speed
PADDLESPEED = 8

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
# 'audioName':'relative/path/to/file'
sounds = {
        'bounce': '../resources/audio/bounce.ogg'
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



