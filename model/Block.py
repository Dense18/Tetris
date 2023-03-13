import pygame
from settings import *

class Block:
    """
        Stores information of each block in the tetromino
    """
    def __init__(self, tetromino, pos, color):
        self.tetromino = tetromino
        self.pos = vec(pos) + INITIAL_TETROMINO_OFFSET
        self.color = color
        self.rect = pygame.Rect((self.pos * BLOCK_SIZE),(BLOCK_SIZE, BLOCK_SIZE))

        self.absolutePosition = vec(0,0)
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, ((self.pos * BLOCK_SIZE),(BLOCK_SIZE, BLOCK_SIZE)),border_radius=8)
        pygame.draw.rect(screen, "black", ((self.pos * BLOCK_SIZE),(BLOCK_SIZE, BLOCK_SIZE)), 1, border_radius=8)
    
    def drawAbsolute(self, screen):
        pygame.draw.rect(screen, self.color, ((self.absolutePosition),(BLOCK_SIZE, BLOCK_SIZE)),border_radius=8)
        pygame.draw.rect(screen, "black", ((self.absolutePosition),(BLOCK_SIZE, BLOCK_SIZE)), 1, border_radius=8)
    
    def rotate(self, pivot):
        #TODO: Implement this urself
        translated = self.pos - pivot
        rotated = translated.rotate(90)
        return rotated + pivot
    
    def is_collide(self, pos):
        x, y = int(pos.x), int(pos.y)
        if x in range(0, FIELD_WIDTH) and y < FIELD_HEIGHT: # hits the border
            if y < 0 or not self.tetromino.tetris.field_arr[y][x]: # Collision with other block
                return False
        return True