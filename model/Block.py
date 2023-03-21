from copy import deepcopy
from enum import Enum

import pygame

from settings import *


class Block:
    """
        Stores information of each block in the tetromino
    """
    MODE_FULL_COLOR = 1
    MODE_BORDER_INDICATION = 2
    MODE_BORDER_INDICATION_COLOR = 3

    @staticmethod
    def copy(block):
        """
            Returns a copy of the [block] object
        """
        new_block = Block(block.tetromino, block.pos, block.color)
        new_block.pos = deepcopy(block.pos)
        return new_block

    def __init__(self, tetromino, pos, color):
        self.tetromino = tetromino
        self.pos = vec(pos) + INITIAL_TETROMINO_OFFSET
        self.color = color
    
    #* Update state *#
    
    def rotate(self, pivot, clockwise = True):
        """
        Rotates the tetromino [clockwise] with the [pivot] position as the origin
        """
        translated = self.pos - pivot
        rotated = translated.rotate(90) if clockwise else translated.rotate(-90)
        return rotated + pivot
    
    #* Information Retrieval*#
    
    def is_collide(self, pos) -> bool:
        """
        Checks if the tetromino collides with the given position
        """
        x, y = int(pos.x), int(pos.y)
        if x in range(0, FIELD_WIDTH) and y < FIELD_HEIGHT: # Does not hits the border
            if y < 0 or not self.tetromino.tetris.field_arr[y][x]: # Does not Collide with other block
                return False
        return True
    
    def drop_distance(self) -> int:
        """
        Returns the number of blocks the tetromino needs to drop to reach until a collision is detected
        """
        drop = 0
        while( (int(self.pos.y) + drop + 1)  < FIELD_HEIGHT) and\
               not self.tetromino.tetris.field_arr[int(self.pos.y) + drop + 1][int(self.pos.x)]:
            drop += 1
        
        return drop
    
    #* Drawing functions *#
    def draw(self, screen, offset = (0, 0), mode = MODE_FULL_COLOR):
        """
        Draws the Block on the [screen]

        Args:
            screen: the screen to display
            offset: the coordinates to offset the tetromino
            mode: the type of drawing mode to draw the blocks. Defaults to Block.MODE_FULL_COLOR.
        """
        if mode == Block.MODE_FULL_COLOR:
            pygame.draw.rect(screen, self.color, ((self.pos * BLOCK_SIZE) + offset ,(BLOCK_SIZE, BLOCK_SIZE)),
                             border_radius=BLOCK_BORDER_RADIUS)
            pygame.draw.rect(screen, "black", ((self.pos * BLOCK_SIZE) + offset,(BLOCK_SIZE, BLOCK_SIZE)), 1, 
                             border_radius=BLOCK_BORDER_RADIUS)
        elif mode == Block.MODE_BORDER_INDICATION:
            pygame.draw.rect(screen, "gray", ((self.pos * BLOCK_SIZE) + offset,(BLOCK_SIZE, BLOCK_SIZE)), 1,
                             border_radius=BLOCK_BORDER_RADIUS)
        elif mode == Block.MODE_BORDER_INDICATION_COLOR:    
            pygame.draw.rect(screen, self.color, ((self.pos * BLOCK_SIZE) + offset,(BLOCK_SIZE, BLOCK_SIZE)), 1, 
                             border_radius=BLOCK_BORDER_RADIUS)
    
    @staticmethod
    def draw_custom(screen, abs_pos, block_size, color ,mode = MODE_FULL_COLOR):
        """
        Draws a block based onto the [screen] with the given position [abs_pos]

        Args:
            screen: the screen to display
            abs_pos: the absolute position of the tetromino
            color: the color of the block
            block_size: the size of each block
            mode: the type of drawing mode to draw the blocks. 
        """
        rect= pygame.Rect(abs_pos, (block_size, block_size))

        if mode == Block.MODE_FULL_COLOR:
            pygame.draw.rect(screen, color, rect, border_radius=8)
            pygame.draw.rect(screen, "black", rect, 1, border_radius=8)
        elif mode == Block.MODE_BORDER_INDICATION:
            pygame.draw.rect(screen, "gray", rect, 1, border_radius=8)
        elif mode == Block.MODE_BORDER_INDICATION_COLOR:    
            pygame.draw.rect(screen, color, rect, 1, border_radius=8)
    