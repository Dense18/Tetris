import pygame

vec = pygame.math.Vector2

FPS = 60
BG_COLOR = (40,40,40)
BLOCK_SIZE = 40 # Size of each block of tetromino
FIELD_SIZE = FIELD_WIDTH, FIELD_HEIGHT = 10, 20 # Number of block available on the field
BOARD_WIDTH, BOARD_HEIGHT = BLOCK_SIZE * FIELD_WIDTH, BLOCK_SIZE * FIELD_HEIGHT # Total width and height of the game screen

SIDEBAR_WIDTH = 200

INITIAL_TETROMINO_OFFSET = vec(FIELD_WIDTH//2 , 0)
WIDTH, HEIGHT = BOARD_WIDTH + SIDEBAR_WIDTH, BOARD_HEIGHT

ANIMATION_INTERVAL = 200 # milliseconds
ACCELERATE_INTERVAL = 150 # milliseconds

TETROMINO_COLOR = {
        'T': (128,0,128), #Purple
        'O': (255,255,0), #Yellow
        'J': (0, 0, 255), #Blue
        'L': (255,127,0), #Dark Orange
        'I': (0,255,255), #Cyan
        'S': (0,255,0), #Green
        'Z': (255,0,0)#Red
}

# Directory
SOUND_DIR= "Assets\\Sound"
TETRIS_SOUND_SFX_DIR = SOUND_DIR + "\\" + "TetrisSfx" 

# Sound Channel
SFX_CHANNEL = 1
OST_CHANNEL = 0

# Das (Delayed Auto Shift) in milliseconds
KEY_DELAY = 133
KEY_INTERVAL = 80

"""
Links
SFX: https://you.have.fail/at/tetrioplus/#sfx-25Pi25-soundpack
Ost: https://archive.org/details/TetrisThemeMusic
"""


