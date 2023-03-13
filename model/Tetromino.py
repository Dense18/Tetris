import pygame
from model.Block import Block
import random
from settings import *

class Tetromino:
    """
        Manages state of tetromino (4 squares block)
    """
    # Available shapes of the tetromino. posisition is (x, y)
    SHAPE = {
        'T': [(0, 0), (-1, 0), (1, 0), (0, -1)],
        'O': [(0, 0), (0, -1), (1, 0), (1, -1)],
        'J': [(0, 0), (-1, 0), (0, -1), (0, -2)],
        'L': [(0, 0), (1, 0), (0, -1), (0, -2)],
        'I': [(0, 0), (0, 1), (0, -1), (0, -2)],
        'S': [(0, 0), (-1, 0), (0, -1), (1, -1)],
        'Z': [(0, 0), (1, 0), (0, -1), (-1, -1)]
    }

    MOVE_DIRECTIONS = {"left": vec(-1, 0), "right": vec(1, 0), "up": vec(0, -1), "down": vec(0, 1)}

    def __init__(self):
        self.shape = random.choice(list(self.SHAPE.keys()))
        self.blocks = [Block(self, pos) for pos in self.SHAPE[self.shape] ]
        pass

    def update(self, direction = "down"):
        move_direction = self.MOVE_DIRECTIONS[direction]
        for block in self.blocks: 
            block.pos += move_direction
        pygame.time.wait(200)

    def draw(self, screen):
        [block.draw(screen) for block in self.blocks]