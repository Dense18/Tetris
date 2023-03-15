from model.Block import Block
import random
from settings import *
from copy import deepcopy
class Tetromino:
    """
        Manages state of tetromino (4 squares block)
    """
    # Available Tetromino Shapes. All tetromino initial posiiton (x, y) is horizontal.
    # Positive x indicated updawards,  Positive y indicated downwards and vice versa
    SHAPE = {
        #Note that the first position is considered as the pivot point for rotation
        'T': [(0, 0), (-1, 0), (1, 0), (0, -1)], 
        'O': [(0, 0), (0, -1), (1, 0), (1, -1)], 
        'J': [(0, 0), (-1, 0), (1, 0), (-1, -1)], 
        'L': [(0, 0), (-1, 0), (1, 0), (1, -1)], 
        'I': [(0, 0), (-1, 0), (1, 0), (2, 0)], 
        'S': [(0, 0), (-1, 0), (0, -1), (1, -1)], 
        'Z': [(0, 0), (1, 0), (0, -1), (-1, -1)] 
    }

    # Rotation based of Basic rotation for SRS

    # Notation: 
        # {0: spawn state}, a.k.a rotation_state = 0
        # {R: rotate right from spawn},  a.k.a rotation_state = 1
        # {2: two same successive rotation from spawn } a.k.a rotation_state = 2
        # {L: rotate left from spawn}, a.k.a rotation_state = 3

    # Offset data for shape [J, L, S, T, Z]
    OFFSET_1 = [
        [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0)], # 0
        [(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)], # R
        [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0)], # 2
        [(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)], # L

    ]

    # Offset data for shape [I]
    OFFSET_2 = [
        [(0, 0), (-1, 0), (2, 0), (-1, 0), (2, 0)], # 0
        [(-1, 0), (0, 0), (0, 0), (0, -1), (0, 2)], # R
        [(-1, -1), (1, -1), (-2, -1), (1, 0), (-2, 0)], # 2
        [(0, -1), (0, -1), (0, -1), (0, 1), (0, -2)], #L
    ]

    # Offset data for shape [O]
    OFFSET_3 = [
        [(0, 0)], # 0
        [(0, 1)], # R
        [(-1, 1)], # 2
        [(-1, 0)], #L
    ]

    SHAPE_OFFSET= {
        'T': OFFSET_1,
        'J': OFFSET_1,
        'L': OFFSET_1,
        'S': OFFSET_1,
        'Z': OFFSET_1,

        'I': OFFSET_2,

        'O': OFFSET_3
    }

    DIRECTIONS_LEFT = "left"
    DIRECTIONS_RIGHT = "right"
    DIRECTIONS_UP  = "up"
    DIRECTIONS_DOWN = "down"

    MOVE_DIRECTIONS = {DIRECTIONS_LEFT: vec(-1, 0), DIRECTIONS_RIGHT: vec(1, 0), DIRECTIONS_UP: vec(0, -1), DIRECTIONS_DOWN: vec(0, 1)}

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
        self.rotation_state = 0

    def update(self, direction = DIRECTIONS_DOWN) -> bool:
        move_direction = self.MOVE_DIRECTIONS[direction]
        new_positions = [block.pos + move_direction for block in self.blocks]

        if not self.is_collide(new_positions):
            for block in self.blocks: 
                block.pos += move_direction
            return True
        
        if direction == Tetromino.DIRECTIONS_DOWN:
            self.has_landed = True
        
        return False
    
    def move(self, pos):
        for block in self.blocks:
            block.pos += pos
    
    def rotate(self, clockwise = True):
        pivot = self.blocks[0].pos
        new_position = [block.rotate(pivot, clockwise) for block in self.blocks]

        for offset in self.get_offset(clockwise):
            offset = vec(offset)
            new_position_kick = [position + offset for position in new_position]

            if not self.is_collide(new_position_kick):
                for i, block in enumerate(self.blocks):
                    block.pos = new_position_kick[i]
                self.set_next_rotation_state(clockwise)
                return
            
    def get_offset(self, clockwise):
        initial_offset = self.SHAPE_OFFSET[self.shape][self.rotation_state]
        next_offset = self.SHAPE_OFFSET[self.shape][self.get_next_rotation_state(clockwise)]

        offset = [vec(initial_offset[i]) - vec(next_offset[i]) for i in range(len(initial_offset))]
        return offset

    def get_next_rotation_state(self, clockwise) -> int:
        return  (self.rotation_state + 1) % 4 if clockwise else (self.rotation_state - 1) % 4
    
    def get_index_wall_kick(self, clockwise) -> int:
        if self.rotation_state == 0:
            return 0 if clockwise else 7
        elif self.rotation_state == 1:
            return 2 if clockwise else 1
        elif self.rotation_state == 2:
            return 3 if clockwise else 4
        elif self.rotation_state == 3:
            return 6 if clockwise else 5
        
    def set_next_rotation_state(self, clockwise):
        if clockwise:
            self.rotation_state = (self.rotation_state + 1) % 4
        else:
            self.rotation_state = (self.rotation_state - 1) % 4
    
    def is_collide(self, pos):
        return any(map(Block.is_collide, self.blocks, pos))

    def draw(self, screen, mode = Block.MODE_FULL_COLOR):
        [block.draw(screen, mode) for block in self.blocks]