from model.Block import Block, Block_Draw_Mode
import random
from settings import *
from copy import deepcopy
class Tetromino:
    """
        Manages state of tetromino (4 squares block)
    """
    # Available shapes of the tetromino. posisition is (x, y)
    SHAPE = {
        'T': [(0, 0), (-1, 0), (1, 0), (0, -1)],
        'O': [(0, 0), (0, -1), (1, 0), (1, -1)],
        'J': [(0, 0), (-1, 0), (0, -1), (0, -2)],
        'L': [(0, 0), (1, 0), (0, -1), (0, -2)],
        'I': [(0, 0), (0, 1), (0, -1), (0, -2)],
        'S': [(0, 0), (-1, 0), (0, -1), (1, -1)],
        'Z': [(0, 0), (1, 0), (0, -1), (-1, -1)]
    }

    MOVE_DIRECTIONS = {"left": vec(-1, 0), "right": vec(1, 0), "up": vec(0, -1), "down": vec(0, 1)}

    @staticmethod
    def copy(tetromino):
        copy_tetromino = Tetromino(tetromino.tetris, tetromino.shape)
        copy_tetromino.blocks = [Block.copy(block) for block in tetromino.blocks]
        copy_tetromino.has_landed = tetromino.has_landed
        return copy_tetromino


    def __init__(self, tetris, shape):
        self.shape = shape
        self.blocks = [Block(self, pos, TETROMINO_COLOR[self.shape]) for pos in self.SHAPE[self.shape]]
        self.has_landed = False
        
        self.tetris = tetris

    def update(self, direction = "down"):
        move_direction = self.MOVE_DIRECTIONS[direction]
        new_positions = [block.pos + move_direction for block in self.blocks]

        if not self.is_collide(new_positions):
            for block in self.blocks: 
                block.pos += move_direction
            return
        
        if direction == "down":
            self.has_landed = True
    
    def move(self, pos):
        for block in self.blocks:
            block.pos += pos

    def rotate(self, degree = 90):
        pivot = self.blocks[0].pos
        new_position = [block.rotate(pivot, degree) for block in self.blocks]

        if not self.is_collide(new_position):
            for i, block in enumerate(self.blocks):
                block.pos = new_position[i]
            return
        
        ## Wall Kick

        #Left
        new_position = [vec(position.x - 1, position.y) for position in new_position]
        if not self.is_collide(new_position):
            for i, block in enumerate(self.blocks):
                block.pos = new_position[i]
            return
        #Right
        new_position = [vec(position.x + 1, position.y) for position in new_position]
        if not self.is_collide(new_position):
            for i, block in enumerate(self.blocks):
                block.pos = new_position[i]
    
    def is_collide(self, pos):
        return any(map(Block.is_collide, self.blocks, pos))

    def draw(self, screen, mode = Block_Draw_Mode.FUll_COLOR):
        [block.draw(screen, mode) for block in self.blocks]