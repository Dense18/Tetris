import pygame

vec = pygame.math.Vector2

FPS = 60
BG_COLOR = (0,0,0) # or (48, 25, 52)
SIDEBAR_BG_COLOR = (0,0,0)
GAME_OVER_BG_COLOR = (0,0,0)
TETRIS_BOARD_COLOR = (40,40,40)

BLOCK_SIZE = 40 # Size of each block of tetromino
FIELD_SIZE = FIELD_WIDTH, FIELD_HEIGHT = 10, 20 # Number of block available on the field
BOARD_WIDTH, BOARD_HEIGHT = BLOCK_SIZE * FIELD_WIDTH, BLOCK_SIZE * FIELD_HEIGHT # Total width and height of the Tetris Board

SIDEBAR_WIDTH = 230

INITIAL_LEFT_SIDEBAR_X = 0
INITIAL_BOARD_X = INITIAL_LEFT_SIDEBAR_X + SIDEBAR_WIDTH
INITIAL_RIGHT_SIDEBAR_X = INITIAL_BOARD_X + BOARD_WIDTH

INITIAL_TETROMINO_OFFSET = vec(FIELD_WIDTH//2 , 0)
# INITIAL_TETROMINO_OFFSET = vec(FIELD_SIZE) //2 #Middle of the field

WIDTH, HEIGHT = BOARD_WIDTH + SIDEBAR_WIDTH + SIDEBAR_WIDTH, BOARD_HEIGHT

ZEN_MODE_FALL_SPEED = 1000 # milliseconds
ACCELERATE_INTERVAL = int(ZEN_MODE_FALL_SPEED / 20) # millisecond. Accelerate speed should be 20 times faster than the normal fall speed


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
MAX_LEVEL = 20
SPRINT_LINE_TO_CLEAR = 40
ULTRA_TIME_SPAN = 120000 #milliseconds

COUNTDOWN_TIME = 3000 #milliseconds
WITH_COUNTDOWN = False # Flag to set if there should be a countdown timer before being able to apply a move in the tetris game
# Directory
SOUND_DIR= "Assets\\Sound"
TETRIS_SOUND_OST_DIR = SOUND_DIR + "\\" "TetrisOst"
TETRIS_SOUND_SFX_DIR = SOUND_DIR + "\\" + "TetrisSfx" 

IMAGES_DIR = "Assets\\Images"

# Sound Channel
LEVEL_UP_CHANNNEL = 6
MOVE_CHANNEL = 5
MENU_CHANNEL = 4
COMBO_CHANNEL = 3
SFX_CHANNEL = 2
OST_CHANNEL = 1

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


# Buttons
BUTTON_COLOR = (220, 0, 0) # (128, 0, 128))
BUTTON_HOVER_COLOR = (136, 8, 8)# (150, 0, 150)
BUTTON_TEXT_COLOR = "white"

CLEAR_BUTTON_COLOR = (240, 0, 0)
CLEAR_BUTTON_HOVER_COLOR = (255, 30, 30)

BACK_BUTTON_WIDTH = 50
BACK_BUTTON_HEIGHT = 30
BACK_BUTTON_ELEVATION = 6
BACK_BUTTON_BORDER_RADIUS = 8
BACK_BUTTON_TEXT_COLOR = "black"

## TEXT_SIZE:
TEXT_SIZE = 30
HINT_TEXT_SIZE = 20
MENU_BUTTON_TEXT_SIZE = 50
MENU_BUTTON_BORDER_RADIUS = 12

## TEXT COLORS:
BONUS_ACTION_COLOR = "purple"
ACTION_COLOR = "green"
COMBO_SCORE_COLOR = "red"
TEXT_LABEL_COLOR = "white"
HINT_TEXT_COLOR = "red"

NUM_NEXT_PIECE_TO_DISPLAY = 5
HIGH_SCORE_TEXT_COLOR = "green"

# NAME OF FILE TO STORING THE BEST SCORE FOR EACH GAME MODE
BEST_SCORE_FILE_NAME = "Best_Score"

#ACTIONS
LINE_0 = 1
LINE_1 = 2
LINE_2 = 3
LINE_3 = 4
LINE_4 = 5

T_SPIN_0 = 6
T_SPIN_1 = 7
T_SPIN_2 = 8
T_SPIN_3 = 9

MINI_T_SPIN_0 = 10
MINI_T_SPIN_1 = 11
MINI_T_SPIN_2 = 12

ACTION_TO_TEXT = {
    LINE_0 : "",
    LINE_1 : "Single",
    LINE_2 : "Double",
    LINE_3 : "Triple",
    LINE_4 : "Tetris",

    T_SPIN_0 : "T Spin",
    T_SPIN_1 : "T Spin Single",
    T_SPIN_2 : "T Spin Double",
    T_SPIN_3 : "T Spin Triple",

    MINI_T_SPIN_0 : "Mini T Spin",
    MINI_T_SPIN_1 : "Mini T Spin Single",
    MINI_T_SPIN_2 : "Mini T Spin Double"
}

# Links
"""
SFX: https://you.have.fail/at/tetrioplus/#sfx-25Pi25-soundpack
Main Ost: https://archive.org/details/TetrisThemeMusic
Menu Ost: https://www.zophar.net/music/gameboy-gbs/tetris
Game Over Ost:https://downloads.khinsider.com/game-soundtracks/album/tetris-rip 
Tetris GuideLine: https://tetris.fandom.com/wiki/Tetris_Guideline 
Rotation System: https://tetris.wiki/Super_Rotation_System
Score System:  https://tetris.fandom.com/wiki/Scoring#Guideline_scoring_system  
Combo System: https://tetris.wiki/Combo#:~:text=Combo%20system%20(consecutive%20line%20clears)&text=The%20combo%20counter%20starts%20at,clears%20equals%20a%201%2Dcombo. 
"""


