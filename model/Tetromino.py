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
        'T': [(0, 0), (-1, 0), (1, 0), (0, -1)], # Done
        'O': [(0, 0), (0, -1), (1, 0), (1, -1)], # Done
        'J': [(0, 0), (-1, 0), (1, 0), (-1, -1)], #Done
        'L': [(0, 0), (-1, 0), (1, 0), (1, -1)], #Done 
        'I': [(0, 0), (0, 1), (0, 2), (0, -1)], # Done
        'S': [(0, 0), (-1, 0), (0, -1), (1, -1)], # Done
        'Z': [(0, 0), (1, 0), (0, -1), (-1, -1)] # Done
    }

    
    # Notation: 
        # {0: spawn state}, a.k.a rotation_state = 0
        # {R: rotate right from spawn},  a.k.a rotation_state = 1
        # {2: two same successive rotation from spawn } a.k.a rotation_state = 2
        # {L: rotate left from spawn}, a.k.a rotation_state = 3
        
    # Wall kick data for shape [J, L, S, T, Z]
    WALL_KICK_1 = [ 
                [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)], # 0 -> R
                [(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)], # R -> 0
                [(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)], # R -> 2
                [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)], # 2 -> R
                [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)], # 2 -> L
                [(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)], # L -> 2
                [(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)], # L -> 0
                [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)], # 0 -> L
             ]
    
    # Wall kick data for shape [I]
    WALL_KICK_2 = [ 
                [(0, 0), (-2, 0), (1, 0), (-2, 1), (1, -2)], # 0 -> R  // 0 -> 1
                [(0, 0), (2, 0), (-1, 0), (2, -1), (-1, 2)], # R -> 0  // 1 -> 0
                [(0, 0), (-1, 0), (2, 0), (-1, -2), (2, 1)], # R -> 2  // 1 -> 2
                [(0, 0), (1, 0), (-2, 0), (1, 2), (-2, -1)], # 2 -> R  // 2 -> 1
                [(0, 0), (2, 0), (-1, 0), (2, -1), (-1, 2)], # 2 -> L  // 2 -> 3
                [(0, 0), (-2, 0), (1, 0), (-2, 1), (1, -2)], # L -> 2  // 3 -> 2
                [(0, 0), (1, 0), (-2, 0), (1, 2), (-2, -1)], # L -> 0  // 3 -> 0
                [(0, 0), (-1, 0), (2, 0), (-1, -2), (2, 1)], # 0 -> L  // 0 -> 3
             ]
    
    
    SHAPE_WALL_KICK= {
        'T': WALL_KICK_1,
        'J': WALL_KICK_1,
        'L': WALL_KICK_1,
        'S': WALL_KICK_1,
        'Z': WALL_KICK_1,

        'I': WALL_KICK_2,
        'O': None
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
        if self.shape == "O":
            return
        
        pivot = self.blocks[0].pos
        new_position = [block.rotate(pivot, clockwise) for block in self.blocks]

        if not self.is_collide(new_position):
            for i, block in enumerate(self.blocks):
                block.pos = new_position[i]
                self.set_next_rotation_state(clockwise)
            return
        
        for offset in Tetromino.SHAPE_WALL_KICK[self.shape][self.get_index_wall_kick(clockwise)]:
            offset = vec(offset)
            new_position_kick = [position + offset for position in new_position]

            if not self.is_collide(new_position_kick):
                for i, block in enumerate(self.blocks):
                    block.pos = new_position_kick[i]
                    self.set_next_rotation_state(clockwise)
                return

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

        # self.rotation_state = self.rotation_state + 1 % 4 if clockwise else self.rotation_state - 1 % 4
    
    def is_collide(self, pos):
        return any(map(Block.is_collide, self.blocks, pos))

    def draw(self, screen, mode = Block.MODE_FULL_COLOR):
        [block.draw(screen, mode) for block in self.blocks]