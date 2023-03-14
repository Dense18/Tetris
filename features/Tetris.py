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
        self.combo = 0

        self.game_over = False

        self.ui = TetrisUI(self)

        # Delayed Auto Shift (in milliseconds)
        self.last_time_interval = 0
        self.last_time_delay = 0
        self.key_down_pressed = True

        # Lock delay (in milliseconds)
        self.last_time_lock = 0
        self.lock_moves = 0

        # Appearance Delay (in milliseconds)
        self.last_time_are = 0 

        # Sound
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

    def clear_full_line(self):
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
        if cleared > 0:
            self.combo += 1
            combo = min(self.combo, 16)
            pygame.mixer.Channel(COMBO_CHANNEL).play(self.combos_sfx[combo])
        else:
            if self.combo != 0:
                pygame.mixer.Channel(COMBO_CHANNEL).play(self.combo_break_sfx)
            self.combo = 0

    def place_tetromino(self):
        for block in self.tetromino.blocks:
            x, y = int(block.pos.x), int(block.pos.y)
            if x in range(0, FIELD_WIDTH) and y in range(0, FIELD_HEIGHT):
                self.field_arr[y][x] = block

        self.get_new_tetromino()
        self.last_time_are = self.current_milliseconds()
        
        self.clear_full_line()
    
    def get_new_tetromino(self):
        self.tetromino = Tetromino(self, self.bag.pop(0))
        if len(self.bag) <= 1:
            self.add_new_bag()
            
    def update(self, events):
        trigger = [self.app.animation_flag, self.app.accelerate_event][self.accelerate]
        if trigger and self.current_milliseconds() - self.last_time_are >= APPEARANCE_DELAY: 
            if self.tetromino.update(): self.last_time_lock = self.current_milliseconds()

        if self.tetromino.has_landed:
            if time.time() * 1000 - self.last_time_lock >= LOCK_DELAY:
                pygame.mixer.Channel(SFX_CHANNEL).play(self.land_sfx)
                self.accelerate = False
                self.has_hold = False
                if self.tetromino.blocks[0].pos.y == INITIAL_TETROMINO_OFFSET[1]:
                    self.game_over = True
                    self.reset()
                    return
                self.place_tetromino()
                self.last_time_lock = time.time() * 1000
                
        # self.clear_full_line()
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
        self.last_time_lock = 0

    def hard_drop2(self, tetromino):
        """
            Move [tetromino] down until it has landed
        """
        while not tetromino.has_landed:
            tetromino.update()

    def handle_key_down_pressed(self, key):
        if key in [pygame.K_UP, pygame.K_x]:
            self.last_time_lock = self.current_milliseconds()
            self.rotate()
        elif key in [pygame.K_z, pygame.K_LCTRL, pygame.K_RCTRL]:
            self.last_time_lock = self.current_milliseconds()
            self.rotate(-90)
        elif key == pygame.K_DOWN:
            self.accelerate = True
        elif key == pygame.K_SPACE:
            self.hard_drop()
        elif key in [pygame.K_c, pygame.K_LSHIFT, pygame.K_RSHIFT]:
            self.last_time_lock = self.current_milliseconds()
            self.hold()
    
    def handle_key_pressed(self, key_pressed):
        if key_pressed[pygame.K_LEFT]:
            if not self.key_down_pressed:
                pygame.mixer.Channel(SFX_CHANNEL).play(self.move_sfx)
                self.last_time_lock = self.current_milliseconds()
                self.tetromino.update("left")
                self.last_time_delay = self.current_milliseconds()
                self.key_down_pressed = True
            elif self.current_milliseconds() - self.last_time_delay >= KEY_DELAY and self.current_milliseconds() - self.last_time_interval >= KEY_INTERVAL:
                pygame.mixer.Channel(SFX_CHANNEL).play(self.move_sfx)
                self.tetromino.update("left")
                self.last_time_interval = self.current_milliseconds()

        elif key_pressed[pygame.K_RIGHT]:
            if not self.key_down_pressed:
                pygame.mixer.Channel(SFX_CHANNEL).play(self.move_sfx)
                self.last_time_lock = self.current_milliseconds()
                self.tetromino.update("right")
                self.last_time_delay = self.current_milliseconds()
                self.key_down_pressed = True
            elif self.current_milliseconds() - self.last_time_delay >= KEY_DELAY and self.current_milliseconds() - self.last_time_interval >= KEY_INTERVAL:
                pygame.mixer.Channel(SFX_CHANNEL).play(self.move_sfx)
                self.tetromino.update("right")
                self.last_time_interval = self.current_milliseconds()
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
    
    def current_milliseconds(self):
        return time.time() *1000 
    
    def reset(self):
        self.ost.stop()
        self.__init__(self.app)
    
    """
        Sound Functions
    """
    def set_sound_channel(self):
        pygame.mixer.Channel(SFX_CHANNEL).set_volume(0.7)
        pygame.mixer.Channel(COMBO_CHANNEL).set_volume(0.7)
        pygame.mixer.Channel(OST_CHANNEL).set_volume(0.1)

    def load_sound(self):
        self.ost = pygame.mixer.Sound(os.path.join(SOUND_DIR, "tetrisOst.mp3"))

        self.move_sfx = pygame.mixer.Sound(os.path.join(TETRIS_SOUND_SFX_DIR, "move.ogg"))
        self.land_sfx = pygame.mixer.Sound(os.path.join(TETRIS_SOUND_SFX_DIR, "floor.ogg"))
        self.rotate_sfx = pygame.mixer.Sound(os.path.join(TETRIS_SOUND_SFX_DIR, "rotate.ogg"))
        self.hold_sfx = pygame.mixer.Sound(os.path.join(TETRIS_SOUND_SFX_DIR, "hold.ogg"))

        self.hard_drop_sfx = pygame.mixer.Sound(os.path.join(TETRIS_SOUND_SFX_DIR, "harddrop.ogg"))
        self.clear_line_sfx = pygame.mixer.Sound(os.path.join(TETRIS_SOUND_SFX_DIR, "clearline.ogg"))

        self.combo_break_sfx = pygame.mixer.Sound(os.path.join(TETRIS_SOUND_SFX_DIR, "combo_break_2.ogg"))
        self.combos_sfx = {}
        combos = (i for i in range(1, 17))
        for combo in combos:
            self.combos_sfx[combo] = pygame.mixer.Sound(os.path.join(TETRIS_SOUND_SFX_DIR, f"combo_{combo}.mp3"))
    """
        Drawing Fuctions
    """
    def draw(self):
        self.ui.draw()