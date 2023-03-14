import pygame
from settings import *
from copy import deepcopy

class Block:
    """
        Stores information of each block in the tetromino
    """
    @staticmethod
    def copy(block):
        new_block = Block(block.tetromino, block.pos, block.color)
        new_block.pos = deepcopy(block.pos)
        return new_block

    def __init__(self, tetromino, pos, color):
        self.tetromino = tetromino
        self.pos = vec(pos) + INITIAL_TETROMINO_OFFSET
        self.color = color
        # self.rect = pygame.Rect((self.pos * BLOCK_SIZE),(BLOCK_SIZE, BLOCK_SIZE))
        
    def draw(self, screen, indication = False):
        if indication:
            pygame.draw.rect(screen, "gray", ((self.pos * BLOCK_SIZE),(BLOCK_SIZE, BLOCK_SIZE)), 1, border_radius=8)
            return
        pygame.draw.rect(screen, self.color, ((self.pos * BLOCK_SIZE),(BLOCK_SIZE, BLOCK_SIZE)),border_radius=8)
        pygame.draw.rect(screen, "black", ((self.pos * BLOCK_SIZE),(BLOCK_SIZE, BLOCK_SIZE)), 1, border_radius=8)
    
    
    def rotate(self, pivot, degree = 90):
        translated = self.pos - pivot
        rotated = translated.rotate(degree)
        return rotated + pivot
    
    def is_collide(self, pos):
        x, y = int(pos.x), int(pos.y)
        if x in range(0, FIELD_WIDTH) and y < FIELD_HEIGHT: # hits the border
            if y < 0 or not self.tetromino.tetris.field_arr[y][x]: # Collision with other block
                return False
        return True