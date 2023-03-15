import pygame
from settings import *
from copy import deepcopy
from enum import Enum

class Block:
    """
        Stores information of each block in the tetromino
    """
    MODE_FULL_COLOR = 1
    MODE_BORDER_INDICATION = 2
    MODE_BORDER_INDICATION_COLOR = 3

    @staticmethod
    def copy(block):
        new_block = Block(block.tetromino, block.pos, block.color)
        new_block.pos = deepcopy(block.pos)
        return new_block

    def __init__(self, tetromino, pos, color):
        self.tetromino = tetromino
        self.pos = vec(pos) + INITIAL_TETROMINO_OFFSET
        self.color = color
    
    def rotate(self, pivot, clockwise = True):
        translated = self.pos - pivot
        rotated = translated.rotate(90) if clockwise else translated.rotate(-90)
        return rotated + pivot
    
    def is_collide(self, pos):
        x, y = int(pos.x), int(pos.y)
        if x in range(0, FIELD_WIDTH) and y < FIELD_HEIGHT: # hits the border
            if y < 0 or not self.tetromino.tetris.field_arr[y][x]: # Collision with other block
                return False
        return True
    
    def draw(self, screen, mode = MODE_FULL_COLOR):
        if mode == Block.MODE_FULL_COLOR:
            pygame.draw.rect(screen, self.color, ((self.pos * BLOCK_SIZE),(BLOCK_SIZE, BLOCK_SIZE)),border_radius=8)
            pygame.draw.rect(screen, "black", ((self.pos * BLOCK_SIZE),(BLOCK_SIZE, BLOCK_SIZE)), 1, border_radius=8)
        elif mode == Block.MODE_BORDER_INDICATION:
            pygame.draw.rect(screen, "gray", ((self.pos * BLOCK_SIZE),(BLOCK_SIZE, BLOCK_SIZE)), 1, border_radius=8)
        elif mode == Block.MODE_BORDER_INDICATION_COLOR:    
            pygame.draw.rect(screen, self.color, ((self.pos * BLOCK_SIZE),(BLOCK_SIZE, BLOCK_SIZE)), 1, border_radius=8)
    
    @staticmethod
    def draw_custom(screen, abs_pos, block_size, color ,mode = MODE_FULL_COLOR):
        rect= pygame.Rect(abs_pos, (block_size, block_size))

        if mode == Block.MODE_FULL_COLOR:
            pygame.draw.rect(screen, color, rect, border_radius=8)
            pygame.draw.rect(screen, "black", rect, 1, border_radius=8)
        elif mode == Block.MODE_BORDER_INDICATION:
            pygame.draw.rect(screen, "gray", rect, 1, border_radius=8)
        elif mode == Block.MODE_BORDER_INDICATION_COLOR:    
            pygame.draw.rect(screen, color, rect, 1, border_radius=8)
    