from settings import *
import pygame
from features.State import State

class Tetris(State):
    """
        Class handling the execution of a Tetris game
    """
    def __init__(self, app):
        self.app = app
        pass
    
    def update(self, events):
        pass

    def draw(self):
        self.draw_grid()
        pass

    def draw_grid(self):
        for col in range(FIELD_WIDTH):
            for row in range(FIELD_HEIGHT):
                pygame.draw.rect(self.app.screen, "black", (col * BLOCK_SIZE, row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)