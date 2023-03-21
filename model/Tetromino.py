from copy import deepcopy

from model.Block import Block
from settings import *


class Tetromino:
    """
        Manages state of tetromino (4 squares block)
    """
    
    """
        Initial block position for a given tetromino shape
    """
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
    OFFSET_JLSTZ = [
        [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0)], # 0
        [(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)], # R
        [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0)], # 2
        [(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)], # L

    ]

    # Offset data for shape [I]
    OFFSET_I = [
        [(0, 0), (-1, 0), (2, 0), (-1, 0), (2, 0)], # 0
        [(-1, 0), (0, 0), (0, 0), (0, -1), (0, 2)], # R
        [(-1, -1), (1, -1), (-2, -1), (1, 0), (-2, 0)], # 2
        [(0, -1), (0, -1), (0, -1), (0, 1), (0, -2)], #L
    ]

    # Offset data for shape [O]
    OFFSET_O = [
        [(0, 0)], # 0
        [(0, 1)], # R
        [(-1, 1)], # 2
        [(-1, 0)], #L
    ]

    # Offset data dictionary  
    SHAPE_OFFSET= {
        'T': OFFSET_JLSTZ,
        'J': OFFSET_JLSTZ,
        'L': OFFSET_JLSTZ,
        'S': OFFSET_JLSTZ,
        'Z': OFFSET_JLSTZ,

        'I': OFFSET_I,

        'O': OFFSET_O
    }

    # Variables for Directions
    DIRECTIONS_LEFT = "left"
    DIRECTIONS_RIGHT = "right"
    DIRECTIONS_UP  = "up"
    DIRECTIONS_DOWN = "down"
    MOVE_DIRECTIONS = {DIRECTIONS_LEFT: vec(-1, 0), DIRECTIONS_RIGHT: vec(1, 0), DIRECTIONS_UP: vec(0, -1), DIRECTIONS_DOWN: vec(0, 1)}

    @staticmethod
    def copy(tetromino):
        """
            Returns a copy of the [tetromino] object
        """
        copy_tetromino = Tetromino(tetromino.tetris, tetromino.shape)
        copy_tetromino.blocks = [Block.copy(block) for block in tetromino.blocks]
        copy_tetromino.has_landed = tetromino.has_landed
        return copy_tetromino


    def __init__(self, tetris, shape):
        self.shape = shape
        self.blocks = [Block(self, pos, TETROMINO_COLOR[self.shape]) for pos in self.SHAPE[self.shape]]
        self.has_landed = False
        self.has_previously_landed = False
        self.has_locked = False
        
        self.tetris = tetris
        self.rotation_state = 0

        self.is_rotate = False
        self.is_wall_kick = False
        


    #* Update State functions*#
    
    def update(self, direction = DIRECTIONS_DOWN) -> bool:
        """
            Updates the tetromino state based on the given [direction]
        """
        move_direction = self.MOVE_DIRECTIONS[direction]
        new_positions = [block.pos + move_direction for block in self.blocks]

        if not self.is_collide(new_positions):
            for block in self.blocks: 
                block.pos += move_direction
            self.is_wall_kick = False
            self.is_rotate = False
            self.has_landed = False
            if self.drop_distance() == 0: 
                self.has_previously_landed = True
                self.has_landed = True
            return True
        
        if direction == Tetromino.DIRECTIONS_DOWN:
            self.has_previously_landed = True
            self.has_landed = True
        
        return False
    
    def rotate(self, clockwise = True) -> bool:
        """
           Rotates the tetromino [clockwise] and returns a boolean indicating if the rotation was successful
        """
        pivot = self.blocks[0].pos
        new_position = [block.rotate(pivot, clockwise) for block in self.blocks]

        # O-piece is special as it needs to use the offset table, otherwise it will wobble and not stay in place when rotated.
        # Hence, it shouldnt have a wall kick
        for i, offset in enumerate(self.get_offset(clockwise)):
            offset = vec(offset)
            new_position_kick = [position + offset for position in new_position]

            if not self.is_collide(new_position_kick):
                self.is_rotate = True
                
                self.is_wall_kick = False if i == 0 or self.shape == "O" else True
                # self.is_wall_kick = True if i != 0 and self.shape != "O" else False

                for i, block in enumerate(self.blocks):
                    block.pos = new_position_kick[i]
                self.update_rotation_state(clockwise)
                return True
        
        return False
    
    def update_rotation_state(self, clockwise: bool):
        """
        Updates the rotation state after the given [clockwise] rotation

        Args:
            clockwise: True if the rotation is clockwise, False if the rotation is counterclockwise
        """
        if clockwise:
            self.rotation_state = (self.rotation_state + 1) % 4
        else:
            self.rotation_state = (self.rotation_state - 1) % 4
    
    #* Information Retrieval*#
    
    def drop_distance(self) -> int:
        """
            Returns the number of blocks the tetromino needs to drop to reach until a collision is detected
        """
        return min(map(Block.drop_distance, self.blocks))

    def get_lowest_y(self):
        """
        Returns the bottom y coordinate of the tetromino. 
        Note: the higher the y coordinate, the more bottom it is
        """
        return max([int(block.pos.y) for block in self.blocks])

    def get_offset(self, clockwise: bool):
        """
        Returns the list of offsets for the given [clockwise] rotation
        """
        initial_offset = self.SHAPE_OFFSET[self.shape][self.rotation_state]
        next_offset = self.SHAPE_OFFSET[self.shape][self.get_next_rotation_state(clockwise)]

        offset = [vec(initial_offset[i]) - vec(next_offset[i]) for i in range(len(initial_offset))]
        return offset

    def get_next_rotation_state(self, clockwise) -> int:
        """
         Returns the tetromino rotation state after the given rotation [clockwise]
        
        Args:
            clockwise: True if the rotation is clockwise, False if the rotation is counterclockwise
        """
        return  (self.rotation_state + 1) % 4 if clockwise else (self.rotation_state - 1) % 4
        
    #* Collision functions *#
    
    def is_collide(self, position) -> bool:
        """
        Checks if the tetromino is colliding with the given [position]
        """
        return any(map(Block.is_collide, self.blocks, position))
    
    
    #* Corner Blocks *#
    
    def get_num_occupied_corner_blocks(self) -> int:
        """
            Returns the number of occupied corner blocks in the tetromino
        """
        count = 0
        for elem in self.get_corner_blocks():
            if elem: 
                count += 1
        return count
    
    def get_num_unoccupied_corner_blocks(self):
        """
            Returns the number of unoccupied corner blocks in the tetromino
        """
        return len(self.get_corner_blocks()) - self.get_num_occupied_corner_blocks()
    
    def get_corner_blocks(self):
        """
            Returns a list of all corner blocks in the tetromino

        Returns:
            _type_: _description_
        """
        offsets = [(-1, -1), (1, -1), (-1, 1), (1, 1)] #Up-Left, Up-Right, Down_Left, Down-Right. (x, y)
        pivot_pos = self.blocks[0].pos

        corner_list = []
        for offset in offsets:
            new_pos_x = int(pivot_pos.x) + offset[0]
            new_pos_y = int(pivot_pos.y) + offset[1]

            if new_pos_x in range(0, FIELD_WIDTH) and new_pos_y in range(0, FIELD_HEIGHT):
                corner_list.append(self.tetris.field_arr[new_pos_y][new_pos_x] )
            else:
                corner_list.append(None)
        return corner_list
    

    #* Drawing functions *#
    
    def draw(self, screen, offset = (0, 0), mode = Block.MODE_FULL_COLOR):
        """
        Draws the tetromino on the [screen]

        Args:
            screen: the screen to display
            offset: the coordinates to offset the tetromino
            mode: the type of drawing mode to draw the blocks. Defaults to Block.MODE_FULL_COLOR.
        """
        [block.draw(screen, offset = offset, mode = mode) for block in self.blocks]

    @staticmethod
    def draw_custom_position(screen, shape, abs_pos, block_size, mode = Block.MODE_FULL_COLOR):
        """
        Draws a tetromino based on the given[shape] onto the [screen] with the given position [abs_pos]

        Args:
            screen: the screen to display
            shape: shape of the tetromino
            abs_pos: the absolute position of the tetromino
            block_size: the size of each block
            mode: the type of drawing mode to draw the blocks. 
        """
        for block_pos in Tetromino.SHAPE[shape]:
            new_abs_pos = vec(abs_pos) + (block_size * vec(block_pos))

            Block.draw_custom(screen, 
                              (new_abs_pos[0], new_abs_pos[1]), 
                              block_size,
                              TETROMINO_COLOR[shape],
                              mode)