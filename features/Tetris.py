from settings import *
import pygame
from features.State import State
from model.Tetromino import Tetromino

class Tetris(State):
    """
        Class handling the execution of a Tetris game
    """
    key_dict = {pygame.K_LEFT: "left", pygame.K_RIGHT: "right", pygame.K_UP: "up", pygame.K_DOWN: "down"}

    def __init__(self, app):
        self.app = app
        self.tetromino = Tetromino()
        
    def update(self, events):
        self.tetromino.update()
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.handle_key_pressed(event.key)
        pass

    def handle_key_pressed(self, key):
        if key in list(self.key_dict.keys()):
            self.tetromino.update(self.key_dict[key])

    def draw(self):
        self.draw_grid()
        self.tetromino.draw(self.app.screen)
        pass

    def draw_grid(self):
        for col in range(FIELD_WIDTH):
            for row in range(FIELD_HEIGHT):
                pygame.draw.rect(self.app.screen, "black", (col * BLOCK_SIZE, row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)