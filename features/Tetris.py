from settings import *
import pygame
from features.State import State
from model.Tetromino import Tetromino
import random
from copy import deepcopy
import os
import time
from features.TetrisUI import TetrisUI

class Tetris(State):
    """
        Class handling the execution of a Tetris game
    """
    key_dict = {pygame.K_LEFT: "left", pygame.K_RIGHT: "right"}

    def __init__(self, app):
        self.app = app
        
        self.field_arr = [[0 for col in range(FIELD_WIDTH)] for row in range(FIELD_HEIGHT)]
        self.accelerate = False

        self.bag = random.sample(list(Tetromino.SHAPE.keys()), len(Tetromino.SHAPE.keys()))
        self.tetromino = Tetromino(self, self.bag.pop(0))

        self.hold_piece_shape = None
        self.has_hold = False

        self.lines_cleared = 0

        self.game_over = False
        
        self.ui = TetrisUI(self)
        """
            Delayed Autho Shift (in milliseconds)
        """
        self.last_time_interval = 0
        self.last_time_delay = 0
        self.key_down_pressed = True

        self.load_sound()
        self.set_sound_channel()
        pygame.mixer.Channel(OST_CHANNEL).play(self.ost, -1)

    def add_new_bag(self):
        self.bag += random.sample(list(Tetromino.SHAPE.keys()), len(Tetromino.SHAPE.keys()))
    
    def hold(self):
        if not self.has_hold:
            self.has_hold = True
            pygame.mixer.Channel(SFX_CHANNEL).play(self.hold_sfx)
            if not self.hold_piece_shape:
                self.hold_piece_shape, self.tetromino = self.tetromino.shape, Tetromino(self, self.bag.pop())
                return
            self.hold_piece_shape, self.tetromino = self.tetromino.shape, Tetromino(self, self.hold_piece_shape)

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
        hasLineClear = False
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
                hasLineClear = True
                self.lines_cleared += 1
                for i in range(len(self.field_arr[row])):
                    self.field_arr[line][i] = 0

        if hasLineClear: 
            # self.clear_line_sfx.play()
            pygame.mixer.Channel(SFX_CHANNEL).play(self.clear_line_sfx)

    def place_tetromino(self):
        for block in self.tetromino.blocks:
            x, y = int(block.pos.x), int(block.pos.y)
            if x in range(0, FIELD_WIDTH) and y in range(0, FIELD_HEIGHT):
                self.field_arr[y][x] = block
        self.get_new_tetromino()
    
    def get_new_tetromino(self):
        self.tetromino = Tetromino(self, self.bag.pop(0))
        if len(self.bag) <= 1:
            self.add_new_bag()
            
    def update(self, events):
        trigger = [self.app.animation_flag, self.app.accelerate_event][self.accelerate]
        if trigger: 
            self.tetromino.update()

        if self.tetromino.has_landed:
            pygame.mixer.Channel(SFX_CHANNEL).play(self.land_sfx)
            self.accelerate = False
            self.has_hold = False
            if self.tetromino.blocks[0].pos.y == INITIAL_TETROMINO_OFFSET[1]:
                self.game_over = True
                self.reset()
                return
            self.place_tetromino()

        self.check_full_line()

        ## Check events
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.handle_key_down_pressed(event.key)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    self.accelerate = False
        
        self.handle_key_pressed(pygame.key.get_pressed())

    def hard_drop(self):
        """
            Move the current tetromino down until it has landed
        """
        while not self.tetromino.has_landed:
            self.tetromino.update()
        pygame.mixer.Channel(SFX_CHANNEL).play(self.hard_drop_sfx)

    def hard_drop2(self, tetromino):
        """
            Move [tetromino] down until it has landed
        """
        while not tetromino.has_landed:
            tetromino.update()

    def handle_key_down_pressed(self, key):
        if key == pygame.K_UP:
            self.rotate()
        elif key == pygame.K_x:
            self.rotate(-90)
        elif key == pygame.K_DOWN:
            self.accelerate = True
        elif key == pygame.K_SPACE:
            self.hard_drop()
        elif key == pygame.K_c:
            self.hold()
    
    def handle_key_pressed(self, key_pressed):
        if key_pressed[pygame.K_LEFT]:
            if not self.key_down_pressed:
                self.tetromino.update("left")
                self.last_time_delay = time.time() * 1000
                self.key_down_pressed = True
            elif time.time() * 1000 - self.last_time_delay > KEY_DELAY and time.time() * 1000 - self.last_time_interval > KEY_INTERVAL:
                self.tetromino.update("left")
                self.last_time_interval = time.time() * 1000

        elif key_pressed[pygame.K_RIGHT]:
            if not self.key_down_pressed:
                self.tetromino.update("right")
                self.last_time_delay = time.time() * 1000
                self.key_down_pressed = True
            elif time.time() * 1000 - self.last_time_delay > KEY_DELAY and time.time() * 1000 - self.last_time_interval > KEY_INTERVAL:
                self.tetromino.update("right")
                self.last_time_interval = time.time() * 1000
        else:
            self.last_time_interval = 0
            self.last_time_delay = 0
            self.key_down_pressed = False

    def rotate(self, degree = 90):
        self.tetromino.rotate(degree)
        pygame.mixer.Channel(SFX_CHANNEL).play(self.rotate_sfx)

    def get_hard_drop_indication(self):
        """
            Return a new tetromino with updated position after a hard drop of current tetromino
        """
        new_tetromino = Tetromino.copy(self.tetromino)
        self.hard_drop2(new_tetromino)
        return new_tetromino
    
    def reset(self):
        self.ost.stop()
        self.__init__(self.app)
    
    """
        Sound Functions
    """
    def set_sound_channel(self):
        pygame.mixer.Channel(SFX_CHANNEL).set_volume(0.7)
        pygame.mixer.Channel(OST_CHANNEL).set_volume(0.1)

    def load_sound(self):
        self.ost = pygame.mixer.Sound(os.path.join(SOUND_DIR, "tetrisOst.mp3"))

        self.move_sfx = pygame.mixer.Sound(os.path.join(TETRIS_SOUND_SFX_DIR, "clutch.mp3"))
        self.land_sfx = pygame.mixer.Sound(os.path.join(TETRIS_SOUND_SFX_DIR, "floor.ogg"))
        self.rotate_sfx = pygame.mixer.Sound(os.path.join(TETRIS_SOUND_SFX_DIR, "rotate.ogg"))
        self.hold_sfx = pygame.mixer.Sound(os.path.join(TETRIS_SOUND_SFX_DIR, "hold.ogg"))

        self.hard_drop_sfx = pygame.mixer.Sound(os.path.join(TETRIS_SOUND_SFX_DIR, "harddrop.ogg"))
        self.clear_line_sfx = pygame.mixer.Sound(os.path.join(TETRIS_SOUND_SFX_DIR, "clearline.ogg"))
    """
        Drawing Fuctions
    """
    def draw(self):
        self.ui.draw()