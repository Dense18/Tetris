import pygame

vec = pygame.math.Vector2

FPS = 60

BLOCK_SIZE = 40 # Size of each block of tetromino
FIELD_SIZE = FIELD_WIDTH, FIELD_HEIGHT = 10, 20 # Number of block available on the field
BOARD_WIDTH, BOARD_HEIGHT = BLOCK_SIZE * FIELD_WIDTH, BLOCK_SIZE * FIELD_HEIGHT # Total width and height of the game screen

# INITIAL_TETROMINO_OFFSET = pygame.math.Vector2(FIELD_SIZE) // 2
INITIAL_TETROMINO_OFFSET = vec(FIELD_WIDTH//2 , 0)
WIDTH, HEIGHT = BOARD_WIDTH, BOARD_HEIGHT

ANIMATION_INTERVAL = 150 #milliseconds
ACCELERATE_INTERVAL = 15

TETROMINO_COLOR = {
        'T': (128,0,128), #Purple
        'O': (255,255,0), #Yellow
        'J': (0, 0, 255), #Blue
        'L': (255,127,0), #Dark Orange
        'I': (0,255,255), #Cyan
        'S': (0,255,0), #Green
        'Z': (255,0,0)#Red
}



