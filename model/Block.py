import pygame
from settings import *

class Block:
    """
        Stores information of each block in the tetromino
    """
    def __init__(self, tetromino, pos):
        self.tetromino = tetromino
        self.pos = vec(pos) + INITIAL_TETROMINO_OFFSET
        self.rect = pygame.Rect((self.pos * BLOCK_SIZE),(BLOCK_SIZE, BLOCK_SIZE))
        

    def draw(self, screen):
        # pygame.draw.rect(screen, "orange", self.rect, border_radius=8)
        pygame.draw.rect(screen, "orange", ((self.pos * BLOCK_SIZE),(BLOCK_SIZE, BLOCK_SIZE)), border_radius=8)
        pass