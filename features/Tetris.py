from settings import *
import pygame
from features.State import State
from model.Tetromino import Tetromino
import random
from copy import deepcopy
import os
import time
from features.TetrisUI import TetrisUI
from SoundManager import SoundManager

class Tetris(State):
    """
        Class handling the execution of a Tetris.py game
    """
    key_dict = {pygame.K_LEFT: "left", pygame.K_RIGHT: "right"}

    def __init__(self, app):
        self.app = app
        
        self.field_arr = [[0 for col in range(FIELD_WIDTH)] for row in range(FIELD_HEIGHT)]
        self.accelerate = False

        self.bag = random.sample(list(Tetromino.SHAPE.keys()), len(Tetromino.SHAPE.keys()))
        self.bag_min_items = 5
        self.tetromino = None
        self.get_new_tetromino()

        self.hold_piece_shape = None
        self.has_hold = False

        self.lines_cleared = 0
        self.combo = -1
        self.score = 0

        self.score_system = {
            0: 0,
            1: 100,
            2: 200,
            3: 500,
            4: 800
        }

        self.ui = TetrisUI(self)
        self.sound_manager = SoundManager()

        # Delayed Auto Shift (in milliseconds)
        self.last_time_interval = 0
        self.last_time_delay = 0
        self.key_down_pressed = True

        # Lock delay (in milliseconds)
        self.last_time_lock = 0
        self.lock_moves = 0

        # Appearance Delay (in milliseconds)
        self.last_time_are = 0 

        self.sound_manager.play_ost()

    def add_new_bag(self):
        self.bag += random.sample(list(Tetromino.SHAPE.keys()), len(Tetromino.SHAPE.keys()))
    
    def hold(self):
        if not self.has_hold:
            self.has_hold = True
            self.sound_manager.play_sfx(SoundManager.HOLD_SFX)
            if not self.hold_piece_shape:
                self.hold_piece_shape, self.tetromino = self.tetromino.shape, Tetromino(self, self.bag.pop())
                self.check_bag()
                return
            self.hold_piece_shape, self.tetromino = self.tetromino.shape, Tetromino(self, self.hold_piece_shape)
    
    def check_bag(self):
        """
            Checks and update if a new tetris bag should be added
        """
        if len(self.bag) < self.bag_min_items:
            self.add_new_bag()

    def is_row_full(self, row_index):
        for col in range(len(self.field_arr[row_index])):
            if not self.field_arr[row_index][col]:
                return False
        return True
    
    def move_row_down(self, row_index, num_down):
        for col in range(len(self.field_arr[row_index])):
            self.field_arr[row_index + num_down][col] = self.field_arr[row_index][col]
            self.field_arr[row_index][col] = 0

    def clear_row(self, row_index):
        for col in range(len(self.field_arr[row_index])):
            self.field_arr[row_index][col] = 0

    def clear_full_line(self) -> int:
        cleared = 0
        for row in range(len(self.field_arr) - 1, -1, -1):
            if self.is_row_full(row):
                self.clear_row(row)
                cleared += 1
            elif cleared > 0:
                self.move_row_down(row, cleared)

        for row in range(len(self.field_arr) - 1, -1, -1):
            for col in range(len(self.field_arr[row])):
                if self.field_arr[row][col]:
                    self.field_arr[row][col].pos = vec(col, row)
        
        self.lines_cleared += cleared
        return cleared

    def place_tetromino(self):
        self.sound_manager.play_sfx(SoundManager.LAND_SFX)

        for block in self.tetromino.blocks:
            x, y = int(block.pos.x), int(block.pos.y)
            if x in range(0, FIELD_WIDTH) and y in range(0, FIELD_HEIGHT):
                self.field_arr[y][x] = block

        self.get_new_tetromino()
        self.last_time_are = self.current_milliseconds()
        
        lines_cleared = self.clear_full_line()

        if lines_cleared > 0:
            self.combo += 1
            combo = min(self.combo, 16)
            self.sound_manager.play_combo(combo)
        else:
            if self.combo != -1:
                self.sound_manager.play_combo(-1)
            self.combo = -1

        self.score += self.score_system[lines_cleared]
        self.score += max(0, self.combo) * 50
        
    
    def get_new_tetromino(self):
        self.tetromino = Tetromino(self, self.bag.pop(0))
        self.check_bag()
            
    def update(self, events):
        trigger = [self.app.animation_flag, self.app.accelerate_event][self.accelerate]
        if trigger and self.check_are(): 
            is_success = self.tetromino.update()
            if is_success: 
                if self.accelerate:  self.score += 1
                self.last_time_lock = self.current_milliseconds()

        if self.tetromino.has_landed:
            if self.check_lock_delay():
                self.accelerate = False
                self.has_hold = False
                if self.tetromino.blocks[0].pos.y == INITIAL_TETROMINO_OFFSET[1]:
                    self.reset()
                    return
                self.place_tetromino()
                self.last_time_lock = self.current_milliseconds()
                
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
        num_move_down = 0
        while not self.tetromino.has_landed:
            num_move_down += 1
            self.tetromino.update()

        self.sound_manager.play_sfx(SoundManager.HARD_DROP_SFX)
        self.last_time_lock = 0
        self.score += num_move_down * 2

    def hard_drop2(self, tetromino):
        """
            Move [tetromino] down until it has landed
        """
        while not tetromino.has_landed:
            tetromino.update()

    def handle_key_down_pressed(self, key):
        """
            Handle key events from pygame.KEYDOWN (fired when key is first pressed)
        """
        if key in [pygame.K_UP, pygame.K_x]:
            self.rotate()
        elif key in [pygame.K_z, pygame.K_LCTRL, pygame.K_RCTRL]:
            self.rotate(False)
        elif key == pygame.K_DOWN:
            self.accelerate = True
        elif key == pygame.K_SPACE:
            self.hard_drop()
        elif key in [pygame.K_c, pygame.K_LSHIFT, pygame.K_RSHIFT]:
            self.last_time_lock = self.current_milliseconds()
            self.hold()
        elif key == pygame.K_m:
            self.sound_manager.toggle_mute()
    
    def handle_key_pressed(self, key_pressed):
        """
            Handle key events from pygame.key.get_pressed(). Fired when key is pressed during each frame 
        """
        if key_pressed[pygame.K_LEFT]:
            self.move(Tetromino.DIRECTIONS_LEFT)
        elif key_pressed[pygame.K_RIGHT]:
            self.move(Tetromino.DIRECTIONS_RIGHT)
        else:
            self.last_time_interval = 0
            self.last_time_delay = 0
            self.key_down_pressed = False
    
    def move(self, direction):
        if direction not in [Tetromino.DIRECTIONS_RIGHT, Tetromino.DIRECTIONS_LEFT]: 
            return
        if not self.key_down_pressed:
            self.sound_manager.play_sfx(SoundManager.MOVE_SFX)

            is_move_success = self.tetromino.update(direction)
            if is_move_success: 
                self.last_time_lock = self.current_milliseconds()
                self.update_lock_move()

            self.key_down_pressed = True

            # self.last_time_lock = self.current_milliseconds()
            self.last_time_delay = self.current_milliseconds()

        elif self.check_das():
            self.sound_manager.play_sfx(SoundManager.MOVE_SFX)

            is_move_success = self.tetromino.update(direction)
            if is_move_success: self.update_lock_move()

            self.last_time_interval = self.current_milliseconds()

    def check_das(self):
        """
            Checks condition for Delay Auto Shift Rule
        """
        return self.current_milliseconds() - self.last_time_delay >= KEY_DELAY and \
            self.current_milliseconds() - self.last_time_interval >= KEY_INTERVAL
    
    def check_lock_delay(self):
        """
            Checks condition for Lock Delay Rule
        """
        return self.current_milliseconds() - self.last_time_lock >= LOCK_DELAY or self.lock_moves >= MAX_LOCK_MOVES
    
    def check_are(self):
        """
            Check condition for Appearance Delay Rule
        """
        return self.current_milliseconds() - self.last_time_are >= APPEARANCE_DELAY
    
    def update_lock_move(self):
        if self.tetromino.has_landed : 
            self.lock_moves += 1 
        else:
            self.lock_moves = 0

    def rotate(self, clockwise = True):
        self.sound_manager.play_sfx(SoundManager.ROTATE_SFX)
        is_rotate_success = self.tetromino.rotate(clockwise)
        if is_rotate_success: 
            self.last_time_lock = self.current_milliseconds()
            self.update_lock_move()

    def get_ghost_tetromino(self):
        """
            Return a new tetromino with updated position after a hard drop of current tetromino
        """
        new_tetromino = Tetromino.copy(self.tetromino)
        self.hard_drop2(new_tetromino)
        return new_tetromino
    
    def check_t_spin(self):
        if self.tetromino.shape == "T":
            pass
    
    def current_milliseconds(self):
        return time.time() *1000 
    
    def reset(self):
        self.sound_manager.stop()
        self.__init__(self.app)
    

    """
        Drawing Fuctions
    """
    def draw(self):
        self.ui.draw()