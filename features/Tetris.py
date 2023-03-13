from settings import *
import pygame
from features.State import State
from model.Tetromino import Tetromino
import random
from copy import deepcopy

class Tetris(State):
    """
        Class handling the execution of a Tetris game
    """
    key_dict = {pygame.K_LEFT: "left", pygame.K_RIGHT: "right", pygame.K_DOWN: "down"}

    def __init__(self, app):
        self.app = app
        
        self.field_arr = [[0 for col in range(FIELD_WIDTH)] for row in range(FIELD_HEIGHT)]
        self.accelerate = False

        self.bag = random.sample(list(Tetromino.SHAPE.keys()), len(Tetromino.SHAPE.keys()))
        self.tetromino = Tetromino(self, self.bag.pop(0))

        self.nextPieceText = "Next Piece"
        self.textSize = 30
        self.textFont = pygame.font.SysFont("comicsans", self.textSize)
    
    def add_new_bag(self):
        self.bag += random.sample(list(Tetromino.SHAPE.keys()), len(Tetromino.SHAPE.keys()))

    # def check_full_line(self):
    #     lines_cleared = 0
    #     row_index_cleared = -1
    #     has_cleared = False
    #     for row in range(len(self.field_arr) - 1, -1, -1):
    #         flag = True
    #         for col in range(len(self.field_arr[row])):
    #             if not self.field_arr[row][col]: 
    #                 flag = False
    #                 break
    #         if flag: 
    #             if not has_cleared: 
    #                 has_cleared = True
    #             lines_cleared += 1
    #             if row_index_cleared == -1: 
    #                 row_index_cleared = row

    #             for col in range(len(self.field_arr[row])):
    #                 self.field_arr[row][col] = 0

    #     ## Move Block bottom if a line is cleared
    #     if has_cleared:
    #         print(f"row indexed cleared: {row_index_cleared}")
    #         print(f"lines cleared: {lines_cleared}")
            
    #         for row in range(len(self.field_arr) - 1, -1, -1): 
    #             for col in range(len(self.field_arr[row])):
    #                 if row < row_index_cleared:
    #                     self.field_arr[row + lines_cleared][col] = self.field_arr[row][col]
    #                     self.field_arr[row][col] = 0
    
    def check_full_line(self):
        line = len(self.field_arr) - 1
        for row in range(len(self.field_arr) - 1, -1, -1):
            count = 0
            for col in range(len(self.field_arr[row])):
                if self.field_arr[row][col]:
                    count += 1
                self.field_arr[line][col] = self.field_arr[row][col]
                if self.field_arr[row][col]:
                    self.field_arr[line][col].pos = vec(col, row)

            if count < len(self.field_arr[row]):
                line -= 1
            else:
                for i in range(len(self.field_arr[row])):
                    self.field_arr[line][i] = 0

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
            self.tetromino = Tetromino(self, self.bag.pop(0))
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

    def hard_drop(self):
        while not self.tetromino.has_landed:
            self.tetromino.update()

    def handle_key_pressed(self, key):
        if key in list(self.key_dict.keys()):
            self.tetromino.update(self.key_dict[key])
        elif key == pygame.K_UP:
            self.tetromino.rotate()
        elif key == pygame.K_a:
            self.accelerate = True
        elif key == pygame.K_SPACE:
            self.hard_drop()
     
    """
        Drawing Fuctions
    """
    def draw(self):
        self.tetromino.draw(self.app.screen)
        self.draw_field()
        self.draw_grid()

        self.draw_side_bar()
        pass
    
    def draw_field(self):
        for row in range(len(self.field_arr)):
            for col in range(len(self.field_arr[row])):
                if self.field_arr[row][col] != 0:
                    self.field_arr[row][col].draw(self.app.screen)
    
    def draw_side_bar(self):
        pygame.draw.rect(self.app.screen, (100,200,0), (BOARD_WIDTH, 0, SIDEBAR_WIDTH, BOARD_HEIGHT))

        nextItemTextObj = self.textFont.render(self.nextPieceText, 1, "black")
        nextItemRect = nextItemTextObj.get_rect()
        nextItemRect.center = (BOARD_WIDTH + SIDEBAR_WIDTH//2, BOARD_HEIGHT//2)

        nextTetromino = Tetromino(self, self.bag[0])
        nextTetromino.move((7,13))
        nextTetromino.draw(self.app.screen)
        # nextTetromino.setPivotAbsPosition((nextItemRect.x - 10, nextItemRect.y + 30))
        # nextTetromino.drawAbsolute(self.app.screen)
        self.app.screen.blit(nextItemTextObj, nextItemRect)
    
    def draw_grid(self):
        for row in range(FIELD_HEIGHT):
            pygame.draw.line(self.app.screen, "black", (0, row * BLOCK_SIZE), (BOARD_WIDTH, row * BLOCK_SIZE), 1)
            for col in range(FIELD_WIDTH):
                pygame.draw.line(self.app.screen, "black", (col * BLOCK_SIZE, 0), (col * BLOCK_SIZE, BOARD_HEIGHT), 1)
        
        pygame.draw.line(self.app.screen, "black", (10 * BLOCK_SIZE, 0), (10 * BLOCK_SIZE, BOARD_HEIGHT), 1)