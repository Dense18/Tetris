import pygame

vec = pygame.math.Vector2

FPS = 60
BG_COLOR = (40,40,40)
SIDEBAR_BG_COLOR = (0,0,0)

BLOCK_SIZE = 40 # Size of each block of tetromino
FIELD_SIZE = FIELD_WIDTH, FIELD_HEIGHT = 10, 20 # Number of block available on the field
BOARD_WIDTH, BOARD_HEIGHT = BLOCK_SIZE * FIELD_WIDTH, BLOCK_SIZE * FIELD_HEIGHT # Total width and height of the game screen

SIDEBAR_WIDTH = 200

INITIAL_LEFT_SIDEBAR_X = 0
INITIAL_BOARD_X = INITIAL_LEFT_SIDEBAR_X + SIDEBAR_WIDTH
INITIAL_RIGHT_SIDEBAR_X = INITIAL_BOARD_X + BOARD_WIDTH

INITIAL_TETROMINO_OFFSET = vec(FIELD_WIDTH//2 , 0)
# INITIAL_TETROMINO_OFFSET = vec(FIELD_SIZE) //2 #Middle of the field

WIDTH, HEIGHT = BOARD_WIDTH + SIDEBAR_WIDTH + SIDEBAR_WIDTH, BOARD_HEIGHT

ANIMATION_INTERVAL = 1000 # milliseconds
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

LINES_TO_ADVANCE_LEVEL = 10 #Uses fixed goal levelling system
# Directory
SOUND_DIR= "Assets\\Sound"
TETRIS_SOUND_SFX_DIR = SOUND_DIR + "\\" + "TetrisSfx" 

# Sound Channel
COMBO_CHANNEL = 2
SFX_CHANNEL = 1
OST_CHANNEL = 0

# Das (Delayed Auto Shift) in milliseconds
KEY_DELAY = 133
KEY_INTERVAL = 80

# Lock Delay in milliseconds
LOCK_DELAY = 500 # Based on Teris Guideline
MAX_LOCK_MOVES = 15 # Number

# ARE (Appearance Delay)
APPEARANCE_DELAY = 500

#SCORE
B2B_MULTIPLIER = 1.5
# Links
"""
SFX: https://you.have.fail/at/tetrioplus/#sfx-25Pi25-soundpack
Ost: https://archive.org/details/TetrisThemeMusic
Tetris GuideLine: https://tetris.fandom.com/wiki/Tetris_Guideline 
Rotation System: https://tetris.wiki/Super_Rotation_System
Score System:  https://tetris.fandom.com/wiki/Scoring#Guideline_scoring_system  
Combo System: https://tetris.wiki/Combo#:~:text=Combo%20system%20(consecutive%20line%20clears)&text=The%20combo%20counter%20starts%20at,clears%20equals%20a%201%2Dcombo. 
"""


