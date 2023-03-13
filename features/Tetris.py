from settings import *
import pygame
from features.State import State
from model.Tetromino import Tetromino
import random

class Tetris(State):
    """
        Class handling the execution of a Tetris game
    """
    # key_dict = {pygame.K_LEFT: "left", pygame.K_RIGHT: "right", pygame.K_UP: "up", pygame.K_DOWN: "down"}
    key_dict = {pygame.K_LEFT: "left", pygame.K_RIGHT: "right", pygame.K_DOWN: "down"}

    def __init__(self, app):
        self.app = app
        
        self.field_arr = [[0 for col in range(FIELD_WIDTH)] for row in range(FIELD_HEIGHT)]
        self.accelerate = False

        self.bag = random.sample(list(Tetromino.SHAPE.keys()), len(Tetromino.SHAPE.keys()))
        self.tetromino = Tetromino(self, self.bag.pop())
    
    def add_new_bag(self):
        self.bag += random.sample(list(Tetromino.SHAPE.keys()), len(Tetromino.SHAPE.keys()))

    def check_full_line(self):
        pass
        # lines_cleared = 0
        # row_index_cleared = -1
        # has_cleared = False
        # for row in range(len(self.field_arr) - 1, -1, -1):
        #     flag = True
        #     for col in range(len(self.field_arr[row])):
        #         if not self.field_arr[row][col]: 
        #             flag = False
        #             break
        #     if flag: 
        #         if not has_cleared: 
        #             has_cleared = True
        #         lines_cleared += 1
        #         if row_index_cleared == -1: 
        #             row_index_cleared = row

        #         for col in range(len(self.field_arr[row])):
        #             self.field_arr[row][col] = 0

        # ## Move Block bottom if a line is cleared
        # if has_cleared:
        #     print(f"row indexed cleared: {row_index_cleared}")
        #     print(f"lines cleared: {lines_cleared}")
            
        #     for row in range(len(self.field_arr) - 1, -1, -1): 
        #         for col in range(len(self.field_arr[row])):
        #             if row < row_index_cleared:
        #                 self.field_arr[row + lines_cleared][col] = self.field_arr[row][col]
        #                 self.field_arr[row][col] = 0
        
    def place_tetromino(self):
        for block in self.tetromino.blocks:
            x, y = int(block.pos.x), int(block.pos.y)
            if x in range(0, FIELD_WIDTH) and y in range(0, FIELD_HEIGHT):
                self.field_arr[y][x] = block
            
    def update(self, events):
        trigger = [self.app.animation_flag, self.app.accelerate_event][self.accelerate]
        if trigger: 
            self.tetromino.update()

        if self.tetromino.has_landed:
            self.accelerate = False
            self.place_tetromino()
            self.tetromino = Tetromino(self, self.bag.pop())
            if len(self.bag) <= 1:
                self.add_new_bag()

        self.check_full_line()
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.handle_key_pressed(event.key)

    #     self.handle_key_pressed(pygame.key.get_pressed())
    
    # def handle_key_pressed(self, keys):
    #     if keys[pygame.K_LEFT]:
    #         self.tetromino.update("left")
    #     elif keys[pygame.K_RIGHT]:
    #         self.tetromino.update("right")
    #     elif keys[pygame.K_UP]:
    #         self.tetromino.rotate()
    #     elif keys[pygame.K_DOWN]:
    #         self.accelerate = True

    def handle_key_pressed(self, key):
        if key in list(self.key_dict.keys()):
            self.tetromino.update(self.key_dict[key])
        elif key == pygame.K_UP:
            self.tetromino.rotate()
        elif key == pygame.K_a:
            self.accelerate = True

    def draw(self):
        self.draw_grid()
        self.tetromino.draw(self.app.screen)
        self.draw_field()
        pass

    def draw_field(self):
        for row in range(len(self.field_arr)):
            for col in range(len(self.field_arr[row])):
                if self.field_arr[row][col] != 0:
                    self.field_arr[row][col].draw(self.app.screen)

    def draw_grid(self):
        for row in range(FIELD_HEIGHT):
            for col in range(FIELD_WIDTH):
                pygame.draw.rect(self.app.screen, "black", (col * BLOCK_SIZE, row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)