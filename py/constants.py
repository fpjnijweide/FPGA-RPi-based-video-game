# ==== Global variables should be defined here
# Note: User-Customizable variables (settings) should be defined in a different, not-yet created .txt or .conf or whatever file [TODO]
# Game name string
GAME_NAME = "Sensor Pong" # use this when referencing the game name so that we can easily change it
# GAME_VERSION = '0.0.1' # not used currently but might be nice eventually

# Audio settings
Sound = True
Music = True

# Window resolution
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Frames per second
FPS = 60

# Ball size
BALLRADIUS = 5

# Wall size
WALLSIZE = 10

# Paddle size
PADDLEWIDTH  = 70
PADDLEHEIGHT = 25
PADDLE_Y_POS = 520

# Block size
BLOCKWIDTH  = 50
BLOCKHEIGHT = 20

# Color definitions
colors = {
        "GRAY"      : (100, 100, 100),
        "NAVYBLUE"  : ( 60,  60, 100),
        "WHITE"     : (255, 255, 255),
        "RED"       : (255,   0,   0),
        "GREEN"     : (  0, 255,   0),
        "BLUE"      : (  0,   0, 255),
        "YELLOW"    : (255, 255,   0),
        "ORANGE"    : (255, 128,   0),
        "PURPLE"    : (255,   0, 255),
        "CYAN"      : (  0, 255, 255),
        "BLACK"     : (  0,   0,   0),
        "COMBLUE"   : (233, 232, 255)
}

# Audio track mapping
# 'audioName':'relative/path/to/file'
sounds = {
#        'wallCollision':'../resources/audio/bounce.wav',
#        'blockbreak':'../resources/sound/bounce2.wav'
}
music  = {
        #'mainGameMusic':'../resources/audio/main3.ogg',
#        'menu':'../resources/audio/menu.wav',
#        'newGame':'../resources/audio/new game.wav',
#        'mainGameMusic':'../resources/audio/main soundtrack _sample.wav',
#        'gameOver':'../resources/audio/game over.wav',
#        'highScore':'../resources/audio/new hiscore.wav'
}



