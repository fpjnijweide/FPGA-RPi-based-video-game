# ==== Global variables should be defined here
# Note: User-Customizable variables (settings) should be defined in a different,
# not-yet created .txt or .conf or whatever file [TODO]
# Game name string
GAME_NAME = "Sensor Pong" # use this when referencing the game name so that we can easily change it
# GAME_VERSION = '0.0.1' # not used currently but might be nice eventually


# Offload functions to FPGA and receive from FPGA
FPGA_ENABLED = False


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
BALLRADIUS = 7*3
INITIAL_BALL_X = 30
INITIAL_BALL_Y = 30

#Ball speed
INITIAL_BALL_XSPEED = 5*3
INITIAL_BALL_YSPEED = INITIAL_BALL_XSPEED

# Wall size
WALLSIZE = 5

# Paddle size
PADDLEWIDTH  = 80
PADDLEHEIGHT = 15
PADDLE_Y_POS = 520
PADDLEBOUNCINESS=1

# Powerup chance
POWERUP_CHANCE = 0.01

# Paddle speed
PADDLESPEED = 6

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
RESPAWNDELAY = 1000
RESPAWNRANGE = 1500

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



