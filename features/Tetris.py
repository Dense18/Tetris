import time
from copy import deepcopy

import pygame

from features.GameOver import GameOver
from features.State import State
from features.TetrisUI import TetrisUI
from model.Block import Block
from model.TetrisStat import TetrisStat
from model.Tetromino import Tetromino
from model.TetrominoBag import TetrominoBag
from settings import *
from SoundManager import SoundManager
from utils.utils import *


class Tetris(State):
    """
        Class handling the execution of a Tetris.py game
    """
    key_dict = {pygame.K_LEFT: "left", pygame.K_RIGHT: "right"}
    
    MODE_MARATHON = "Marathon"
    MODE_ZEN = "Zen"
    MODE_SPRINT = "Sprint"
    MODE_ULTRA = "Ultra"
    
    def __init__(self, app, game_mode = MODE_MARATHON):
        super().__init__(app)
        
        self.field_arr = [[0 for col in range(FIELD_WIDTH)] for row in range(FIELD_HEIGHT)]
        self.accelerate = False
        
        self.lock_out = False
        self.block_out = False

        self.level = 1
        self.game_mode = game_mode
        if game_mode != Tetris.MODE_MARATHON:
            pygame.time.set_timer(self.app.animation_event, ZEN_MODE_FALL_SPEED)
            pygame.time.set_timer(self.app.accelerate_event, ACCELERATE_INTERVAL)
        else:
            self.update_time_speed()

        self.bag_min_items = 5
        self.bag = TetrominoBag(self.bag_min_items)
        
        self.tetromino = None
        self.get_new_tetromino()
        

        self.hold_piece_shape = None
        self.has_hold = False

        self.lines_cleared = 0
        self.combo = -1

        self.score = 0
        # Key is based on lines cleared
        self.basic_score_system = {0: 0, 1: 100, 2: 200, 3: 500, 4: 800 }
        self.t_spin_score_system = {0: 400, 1: 800, 2: 1200, 3: 1600,}
        self.mini_t_spin_score_system = {0: 100, 1: 200, 2: 400}
        self.score_perfect_clear_system = {0: 0, 1: 800, 2: 1200, 3: 1800, 4: 200 }
        self.score_perfect_clear_b2b = 3200
        # Key is based on score type
        self.score_dict = { 0: self.basic_score_system, 1: self.t_spin_score_system, 2: self.mini_t_spin_score_system}

        self.action = LINE_0
        # Key is based on lines cleared
        self.action_basic = {0: LINE_0, 1: LINE_1, 2: LINE_2, 3: LINE_3, 4: LINE_4}
        self.action_t_spin = {0: T_SPIN_0, 1: T_SPIN_1, 2: T_SPIN_2, 3: T_SPIN_3}
        self.action_mini_t_spin = {0: MINI_T_SPIN_0, 1: MINI_T_SPIN_1, 2: MINI_T_SPIN_2}
        # Key is based on score type
        self.action_dict = { 0: self.action_basic, 1: self.action_t_spin, 2: self.action_mini_t_spin}

        self.is_last_action_difficult = False
        self.is_b2b = False
        self.is_current_perfect_clear = False

        self.ui = TetrisUI(self)
        self.sound_manager = SoundManager.getInstance()

        # Delayed Auto Shift (in milliseconds)
        self.last_time_interval = 0
        self.last_time_delay = 0
        self.key_down_pressed = True

        # Lock delay (in milliseconds)
        self.last_time_lock = 0
        self.lock_moves = 0

        # Appearance Delay (in milliseconds)
        self.last_time_are = 0 
        
    
    def on_start_state(self):
        self.sound_manager.play_ost(SoundManager.MAIN_OST)
        
        self.start_time_countdown_ms = current_millis()
        self.time_left_countdown_ms = COUNTDOWN_TIME
        
        self.start_time_in_seconds = time.time() + COUNTDOWN_TIME//1000 if WITH_COUNTDOWN else time.time()
        
    def update(self, events):
        if self.time_left_countdown_ms > 0 and WITH_COUNTDOWN:  
            time_passed = current_millis() - self.start_time_countdown_ms          
            self.time_left_countdown_ms = COUNTDOWN_TIME - time_passed
            return
            
        trigger = [self.app.animation_flag, self.app.accelerate_event][self.accelerate]
        if trigger and self.check_are():             
            is_success = self.tetromino.update()
            if is_success: 
                if self.accelerate:  self.score += 1
                self.last_time_lock = current_millis()

        if self.tetromino.has_landed:
            if self.check_lock_delay():
                self.accelerate = False
                # self.has_hold = False
                self.sound_manager.play_sfx(SoundManager.LAND_SFX)
                # if self.is_game_over():
                #     if self.game_mode == Tetris.MODE_ZEN:
                #         self.reset()
                #         return
                #     tetris_info = TetrisStat(level = self.level,
                #         score = self.score, 
                #         lines_cleared= self.lines_cleared, 
                #         time_passed = self.get_time_passed(),
                #         game_mode = self.game_mode)
                #     game_over_activivity = GameOver(self.app, tetris_info)
                #     game_over_activivity.enter_state()
                #     return
                self.place_tetromino()
                self.last_time_lock = current_millis()
        
        if self.is_game_over():
            if self.game_mode == Tetris.MODE_ZEN:
                self.reset()
                return
            tetris_info = TetrisStat(level = self.level,
                    score = self.score, 
                    lines_cleared= self.lines_cleared, 
                    time_passed = self.get_time_passed(),
                    game_mode = self.game_mode)
            game_over_activivity = GameOver(self.app, tetris_info)
            game_over_activivity.enter_state()
            return
        
        ## Check events
        for event in events:
            if event.type == pygame.KEYDOWN:    
                self.handle_key_down_pressed(event.key)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    self.accelerate = False
        
        self.handle_key_pressed(pygame.key.get_pressed())
    
    def on_leave_state(self):
        self.sound_manager.stop()
    
    # def on_exit_state(self):
    #     self.sound_manager.stop()

    #* Update Tetromino state *#
    
    def rotate(self, clockwise = True):
        """
        Rotates the current tetromino based on the given [clockwise] rotation

        Args:
            clockwise: True if the rotation is clockwise, False if the rotation is counterclockwise
        """
        self.sound_manager.play_sfx(SoundManager.ROTATE_SFX)
        is_rotate_success = self.tetromino.rotate(clockwise)
        if is_rotate_success: 
            self.last_time_lock = current_millis()
            self.update_lock_move()

    def move(self, direction):
        """
            Move the current tetromino on a given [direction]
        """
        if direction not in [Tetromino.DIRECTIONS_RIGHT, Tetromino.DIRECTIONS_LEFT]: 
            return
        if not self.key_down_pressed:

            is_move_success = self.tetromino.update(direction)
            if is_move_success: 
                self.sound_manager.play_sfx(SoundManager.MOVE_SFX, override=False)
                self.last_time_lock = current_millis()
                self.update_lock_move()

            self.key_down_pressed = True

            self.last_time_delay = current_millis()

        elif self.check_das():

            is_move_success = self.tetromino.update(direction)
            if is_move_success: 
                self.sound_manager.play_sfx(SoundManager.MOVE_SFX, override=False)
                #self.last_time_lock = current_millis()
                self.update_lock_move()

            self.last_time_interval = current_millis()
    
    #* Tetromino Information Retreieval*#
    
    def get_ghost_tetromino(self):
        """
            Return a new tetromino with updated position after a hard drop of current tetromino
        """
        new_tetromino = Tetromino.copy(self.tetromino)
        self.hard_drop2(new_tetromino)
        return new_tetromino

    #* Update Field state *#
    
    def place_tetromino(self, get_new_tetromino = True):
        """
        Places the current tetromino onto the Tetris field and updates score and combo accordingly
        """
        #Check the total number of blocks in the tetromino that is above the skyline. Lock out Condition
        count = 0
        
        #Place current tetromino to the field
        for block in self.tetromino.blocks:
            x, y = int(block.pos.x), int(block.pos.y)
            if x in range(0, FIELD_WIDTH) and y in range(0, FIELD_HEIGHT): 
                self.field_arr[y][x] = block
                
                #Update count if it is above the skyline
                if y < SKY_LINE:  
                    count += 1
        
        #If all of the blocks are above the sky line, updated the lock out game over conidition
        if count == 4:
            self.lock_out = True
            return
        
        self.tetromino.has_locked = True
        self.has_hold = False
        
        is_t_spin = self.is_t_spin()
        is_mini_t_spin = self.is_mini_t_spin()

        lines_cleared = self.clear_full_line()
        if lines_cleared > 0:
            self.combo += 1
            combo = min(self.combo, 16)
            self.sound_manager.play_combo(combo)
        else:
            if self.combo != -1:
                self.sound_manager.play_combo(num_combo= -1)
            self.combo = -1

        ##Check B2B
        
        ## Difficult action includes a tetris, a t-spin, or a mini t-spin.
        # Note that a t-spin with no lines is still considered a diffcult acytion
        is_current_action_difficult = lines_cleared == 4 or is_t_spin or is_mini_t_spin
        
        ## Alternatively, any action that is not a single, double or triple
        # is_current_action_difficult = not (lines_cleared < 4 and not (is_t_spin or is_mini_t_spin))

        self.is_b2b = self.is_last_action_difficult and is_current_action_difficult
        self.is_last_action_difficult = is_current_action_difficult
        self.is_current_perfect_clear = self.is_perfect_clear()
        
        if self.is_current_perfect_clear:
            self.sound_manager.play_sfx(SoundManager.ALL_CLEAR_SFX)
        
        perfect_clear_score = 0 if not self.is_perfect_clear()\
            else self.score_perfect_clear_b2b if self.is_b2b \
            else self.score_perfect_clear_system[lines_cleared]            

            
        dict_index = 1 if is_t_spin else 2 if is_mini_t_spin else 0
        ## Update score
        self.score += self.score_dict[dict_index][lines_cleared] * self.level + (self.is_b2b * B2B_MULTIPLIER)
        self.score += max(0, self.combo) * 50 * self.level
        self.score += perfect_clear_score * self.level if self.is_current_perfect_clear else 0
        self.action = self.action_dict[dict_index][lines_cleared]
        
        self.last_time_are = current_millis()
    
        if self.game_mode == Tetris.MODE_MARATHON: 
            self.check_next_nevel() 
        
        
        if get_new_tetromino: self.get_new_tetromino()

    def hard_drop(self):
        """
            Move the current tetromino down until it has landed
        """
        self.sound_manager.play_sfx(SoundManager.HARD_DROP_SFX)
        drop_distance = self.tetromino.drop_distance()

        # num_move_down = 0
        while not self.tetromino.has_landed:
            # num_move_down += 1
            self.tetromino.update()

        # self.last_time_lock = 0
        self.score += drop_distance * 2
        
        self.place_tetromino()
        self.last_time_lock = current_millis()


    def hard_drop2(self, tetromino):
        """
            Move [tetromino] down until it has landed
        """
        while not tetromino.has_landed:
            tetromino.update()
   
    def is_perfect_clear(self):
        """
        Checks if the Tetris field is a full clear, i.e all the blocks are empty

        Note:
        The method only checks if the first row is empty 
        """
        for i in range(len(self.field_arr[-1])):
            if self.field_arr[-1][i]:
                return False
        return True
    
    # *Clear Full lines* #
    
    def is_row_full(self, row_index):
        """
        Checks if the given row [row_index] is a full line on the Tetris field
        """
        for col in range(len(self.field_arr[row_index])):
            if not self.field_arr[row_index][col]:
                return False
        return True
    
    def move_row_down(self, row_index, num_down):
        """
        Move all elements in the row [row_index] down [num_down] times on the Tetris field
        """
        for col in range(len(self.field_arr[row_index])):
            self.field_arr[row_index + num_down][col] = self.field_arr[row_index][col]
            self.field_arr[row_index][col] = 0
            
            # Update Block position
            if self.field_arr[row_index + num_down][col]:
                self.field_arr[row_index + num_down][col].pos = vec(col, row_index + num_down)

    def clear_row(self, row_index):
        """
        Clears all elements the row from the field based on the given [row_index]
        """
        for col in range(len(self.field_arr[row_index])):
            self.field_arr[row_index][col] = 0

    def clear_full_line(self) -> int:
        """
        Clear all full lines on the Tetris field
        """
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

    
    #* Update Tetris state *#
    
    def get_new_tetromino(self):
        self.tetromino = Tetromino(self, self.bag.pop(0))
        
        #Check Block Out condition. The newly spawned Tetromino is blocked by an existing block on the field
        for block in self.tetromino.blocks:
            if self.field_arr[int(block.pos.y)][int(block.pos.x)]:
                self.block_out = True
                return
    
    def hold(self):
        """
        Holds the current tetromino piece and updates the current tetromino to a new tetromino if needed
        """
        if not self.has_hold:
            self.has_hold = True
            self.sound_manager.play_sfx(SoundManager.HOLD_SFX)
            if not self.hold_piece_shape:
                self.hold_piece_shape, self.tetromino = self.tetromino.shape, Tetromino(self, self.bag.pop(0))
                return
            self.hold_piece_shape, self.tetromino = self.tetromino.shape, Tetromino(self, self.hold_piece_shape)
    
    def update_time_speed(self):
        """
        Update the speed of the Tetris game based on the current level
        """
        speed = pow((0.8 - ((self.level-1) * 0.007)), self.level - 1) #https://tetris.fandom.com/wiki/Tetris_Worlds
        pygame.time.set_timer(self.app.animation_event, int(speed * 1000))
        pygame.time.set_timer(self.app.accelerate_event, int(speed * 1000 / 20))
    
    def check_next_nevel(self):
        """
        Checks and updates the level of the game if necessary
        """
        if self.lines_cleared >= self.level * LINES_TO_ADVANCE_LEVEL:
            if self.level + 1 <= MAX_LEVEL:
                self.sound_manager.play_sfx(SoundManager.LEVEL_UP_SFX, override= False)
            self.level = min(self.level + 1, MAX_LEVEL)
            self.update_time_speed()

    def check_lock_out(self) -> bool:
        """
        Checks Lock out Game Over condition. Use this method before getting the next tetromino
        """
        #Only checks condition if the current tetromino has already been locked to the field
        if not self.tetromino.has_locked: return False
        
        #check the number of blocks on the tetromino that is above the sky line
        count = 0
        for block in self.tetromino.blocks:
            x, y = int(block.pos.x), int(block.pos.y)
            if x in range(0, FIELD_WIDTH) and y < SKY_LINE: 
                count += 1
        
        # If all the blocks are above the sky line, the tetromino is locked out
        return count == 4
        
    def check_block_out(self) -> bool:
        """
        Checks Block out Game Over condition. Use this method before getting the next tetromino
        """
        
        #Only checks condition if the current tetromino has already been locked to the field
        if not self.tetromino.has_locked: return False
        
        new_tetromino = Tetromino(self, self.bag[0])
        
        #If the next Tetromino spawn position is blocked by an existing block on the field, return True
        for block in new_tetromino.blocks:
            if self.field_arr[int(block.pos.y)][int(block.pos.x)]:
                return True
        return False
        
        
    def is_game_over(self):
        """
        Identify if the current game should be over
        """
        if self.lock_out or self.block_out:
            if self.lock_out: print("Lock out")
            if self.block_out: print("Block out")
            return True
        
        if self.game_mode == Tetris.MODE_SPRINT and self.lines_cleared >= SPRINT_LINE_TO_CLEAR:
            return True
        
        if self.game_mode == Tetris.MODE_ULTRA and self.get_time_passed() > ULTRA_TIME_SPAN/1000:
            return True
            
    
    def get_time_passed(self):
        """
        Return the time passed since since the game started in seconds
        """
        return time.time() - self.start_time_in_seconds
    
    def reset(self):
        """
        Reset the game and start a new level
        """
        self.__init__(self.app, game_mode = self.game_mode)
    
    def exit(self):
        self.exit_state()
    
    #* Handle events *#
    
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
            self.last_time_lock = current_millis()
            self.hold()
        elif key == pygame.K_ESCAPE:
            self.exit()
    
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
    
    #* Special conditions *#
    
    def check_das(self):
        """
            Checks condition for Delay Auto Shift Rule
        """
        return current_millis() - self.last_time_delay >= KEY_DELAY and \
            current_millis() - self.last_time_interval >= KEY_INTERVAL
    
    def check_lock_delay(self):
        """
            Checks condition for Lock Delay Rule
        """
        return current_millis() - self.last_time_lock >= LOCK_DELAY or self.lock_moves >= MAX_LOCK_MOVES
    
    def update_lock_move(self):
        """
            Updates the number of moves while during the lock delay
        """
        if self.tetromino.has_landed : 
            self.lock_moves += 1 
        else:
            self.lock_moves = 0
    
    def check_are(self):
        """
            Check condition for Appearance Delay Rule
        """
        return current_millis() - self.last_time_are >= APPEARANCE_DELAY
    
    #* Check actions *#
    
    def is_t_spin(self) -> bool:
        """
        Checks if the current action is a T-Spin
        """
        # return self.tetromino.shape == "T" and self.tetromino.get_num_occupied_corner_blocks() == 3 and self.tetromino.is_rotate
        return self.tetromino.shape == "T" and self.tetromino.get_num_unoccupied_corner_blocks() <= 1 and self.tetromino.is_rotate

    def is_mini_t_spin(self): 
        """
        Checks if the current action is a mini T-Spin
        """
        # return self.is_t_spin() and self.tetromino.is_wall_kick
        return self.tetromino.shape == "T" and self.tetromino.get_num_unoccupied_corner_blocks() <= 1 and self.tetromino.is_wall_kick  
    

    """
        Drawing Fuctions
    """
    def draw(self):
        self.ui.draw()