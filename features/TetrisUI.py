import pygame

import features.Tetris as Tetris
from model.Block import Block
from model.Tetromino import Tetromino
from settings import *
from utils.utils import *


class TetrisUI:
    """
        Manages the UI elements for the Tetris game
    """
    def __init__(self, tetris) -> None:
        self.tetris = tetris
        
        self.num_next_piece = min(self.tetris.bag_min_items, NUM_NEXT_PIECE_TO_DISPLAY)

        self.next_piece_text = "Next Piece:"
        self.hold_piece_text = "Hold Piece:"
        self.lines_cleared_text = "Lines cleared:"
        self.level_label_text = "Level:"
        self.score_text = "Score:"

        self.textFont = pygame.font.SysFont("comicsans", TEXT_SIZE)

    def draw(self):
        """
            Draws all UI elements onto the screen
        """
        self.draw_left_side_bar()
        self.draw_middle()
        self.draw_right_side_bar()
    
    #* Left side bar *#
    
    def draw_left_side_bar(self):
        """
            Draw the left side bar UI with its corresponding elements
            
            UI includes:
                -Hold Piece\n
                -Action\n
                -Score\n
                -Level
        """
        pygame.draw.rect(self.tetris.app.screen, SIDEBAR_BG_COLOR, (INITIAL_LEFT_SIDEBAR_X, 0, SIDEBAR_WIDTH, BOARD_HEIGHT))

        self.draw_hold_piece()
        self.draw_action()
        if self.tetris.game_mode == Tetris.Tetris.MODE_MARATHON:
            self.draw_score()
            self.draw_level()
        elif self.tetris.game_mode in [Tetris.Tetris.MODE_ULTRA, Tetris.Tetris.MODE_ULTRA]:
            self.draw_timer()
            
    def draw_hold_piece(self):
        """
        Draws the hold piece UI
        """
        hold_item_text_obj = self.textFont.render(self.hold_piece_text, 1, TEXT_LABEL_COLOR)
        hold_item_rect = hold_item_text_obj.get_rect(center = (INITIAL_LEFT_SIDEBAR_X + SIDEBAR_WIDTH//2, BOARD_HEIGHT//7))
        self.tetris.app.screen.blit(hold_item_text_obj, hold_item_rect)

        if self.tetris.hold_piece_shape != None:
            block_size = 30

            hold_tetromino_rect = pygame.Rect(0,0, block_size, block_size)
            hold_tetromino_rect.centerx = (INITIAL_LEFT_SIDEBAR_X + SIDEBAR_WIDTH//2)
            hold_tetromino_rect.top = hold_item_rect.bottom + (block_size * 3)
            Tetromino.draw_custom_position(
                self.tetris.app.screen,
                self.tetris.tetromino.shape if self.tetris.has_hold else self.tetris.hold_piece_shape,
                (hold_tetromino_rect.x, hold_tetromino_rect.y),
                block_size,
                Block.MODE_BORDER_INDICATION_COLOR if self.tetris.has_hold else Block.MODE_FULL_COLOR
            )
    
    def draw_action(self):
        """
        Draws the action UI
        """
        b2b_text = "B2B!" if self.tetris.is_b2b else ""
        full_clear_text = "Full Clear!" if self.tetris.is_current_perfect_clear else ""
        bonus_action_text = b2b_text + full_clear_text
        bonus_action_obj = self.textFont.render(bonus_action_text, 1, BONUS_ACTION_COLOR)
        
        action_text = ACTION_TO_TEXT[self.tetris.action]
        action_obj = self.textFont.render(action_text, 1, ACTION_COLOR)
        action_rect = action_obj.get_rect()

        combo_text = f"x {self.tetris.combo}" if self.tetris.combo >= 1 else ""
        combo_text_obj = self.textFont.render(combo_text, 1, COMBO_SCORE_COLOR)
        
        bonus_action_rect = bonus_action_obj.get_rect(center = (INITIAL_LEFT_SIDEBAR_X + SIDEBAR_WIDTH//2, BOARD_HEIGHT//2.2 - action_obj.get_height()))
        action_rect = action_obj.get_rect(centerx = INITIAL_LEFT_SIDEBAR_X + SIDEBAR_WIDTH//2, top = bonus_action_rect.bottom + 10)
        combo_text_rect = combo_text_obj.get_rect(centerx = INITIAL_LEFT_SIDEBAR_X + SIDEBAR_WIDTH//2, top = action_rect.bottom + 10)

        self.tetris.app.screen.blit(bonus_action_obj, bonus_action_rect)
        self.tetris.app.screen.blit(action_obj, action_rect)
        self.tetris.app.screen.blit(combo_text_obj, combo_text_rect)

    def draw_score(self):
        """
        Draw the score UI
        """ 
        score_label_obj = self.textFont.render(self.score_text, 1, TEXT_LABEL_COLOR)
        score_label_rect = score_label_obj.get_rect(center = (INITIAL_LEFT_SIDEBAR_X + SIDEBAR_WIDTH//2, BOARD_HEIGHT//1.5))
        self.tetris.app.screen.blit(score_label_obj, score_label_rect)

        score_text_obj = self.textFont.render(str(round(self.tetris.score)), 1, TEXT_LABEL_COLOR)
        score_text_rect = score_text_obj.get_rect(centerx = (INITIAL_LEFT_SIDEBAR_X + SIDEBAR_WIDTH//2), top = score_label_rect.bottom + 30)
        self.tetris.app.screen.blit(score_text_obj, score_text_rect)
    
    def draw_level(self):
        """
        Draw the level UI
        """
        level_label_obj = self.textFont.render(self.level_label_text + " "+str(self.tetris.level), 1, TEXT_LABEL_COLOR)
        level_label_rect = level_label_obj.get_rect(center = (INITIAL_LEFT_SIDEBAR_X + SIDEBAR_WIDTH//2, BOARD_HEIGHT//1.15))
        self.tetris.app.screen.blit(level_label_obj, level_label_rect)

    def draw_timer(self):
        time_passed_seconds = int(self.tetris.get_time_passed())
        
        if self.tetris.game_mode == Tetris.Tetris.MODE_ULTRA:
            time_left_seconds = int(max((ULTRA_TIME_SPAN/1000) - time_passed_seconds, 0))
            time_left_seconds = max(0, time_left_seconds)   
        
        time_to_show = time_passed_seconds if self.tetris.game_mode == Tetris.Tetris.MODE_SPRINT else \
            time_left_seconds if self.tetris.game_mode == Tetris.Tetris.MODE_ULTRA else\
            0
        time_text = convert_seconds_to_time_str(time_to_show)
        
        time_text_obj = self.textFont.render(time_text, 1, TEXT_LABEL_COLOR)
        time_text_rect = time_text_obj.get_rect(center = (INITIAL_LEFT_SIDEBAR_X + SIDEBAR_WIDTH//2, BOARD_HEIGHT//1.4))
        self.tetris.app.screen.blit(time_text_obj, time_text_rect)
    #* Middle *#
    
    def draw_middle(self):
        """
        Draw the all the UI elements for the middle of the screen
        
        UI include:
            Tetris Field\n
            Tetrominos on the field\n
            Ghost Tetromino \n
        """
        self.draw_grid()
        self.tetris.tetromino.draw(self.tetris.app.screen, offset = (SIDEBAR_WIDTH, 0))
        self.draw_field()
        self.draw_ghost_tetromino()
        
    
    def draw_field(self):
        """
        Draw the Tetris field UI
        """
        for row in range(len(self.tetris.field_arr)):
            for col in range(len(self.tetris.field_arr[row])):
                if self.tetris.field_arr[row][col] != 0:
                    self.tetris.field_arr[row][col].draw(self.tetris.app.screen, offset = (SIDEBAR_WIDTH, 0))
    
    def draw_ghost_tetromino(self):
        """
        Draw the ghost tetromino UI
        """
        tetro = self.tetris.get_ghost_tetromino()
        tetro.draw(self.tetris.app.screen, offset = (SIDEBAR_WIDTH, 0), mode = Block.MODE_BORDER_INDICATION)
    
    def draw_grid(self):
        """
        Draw the grid UI for the Tetris Field
        """
        for row in range(FIELD_HEIGHT):
            # draw horizontal line
            pygame.draw.line(self.tetris.app.screen, "black", 
                             (INITIAL_BOARD_X, row * BLOCK_SIZE), 
                             (BOARD_WIDTH + SIDEBAR_WIDTH, row * BLOCK_SIZE), 
                             1)
            # draw vertical  line
            for col in range(FIELD_WIDTH):
                pygame.draw.line(self.tetris.app.screen, "black", 
                                 (col * BLOCK_SIZE + INITIAL_BOARD_X, 0), 
                                 (col * BLOCK_SIZE + SIDEBAR_WIDTH, BOARD_HEIGHT), 
                                 1)
    #* Left side bar *#
    def draw_right_side_bar(self):
        """
            Draw the right side bar UI with its corresponding elements
            
            UI includes:
                Next Piece\n
                Lines cleared
        """
        pygame.draw.rect(self.tetris.app.screen, SIDEBAR_BG_COLOR, (INITIAL_RIGHT_SIDEBAR_X, 0, SIDEBAR_WIDTH, BOARD_HEIGHT))

        self.draw_next_piece()
        self.draw_lines_cleared()

    def draw_next_piece(self):
        """
        Draw the next tetromino piece UI
        """
        next_item_label_obj = self.textFont.render(self.next_piece_text, 1, TEXT_LABEL_COLOR)
        next_item_label_rect = next_item_label_obj.get_rect(center = (INITIAL_RIGHT_SIDEBAR_X + SIDEBAR_WIDTH//2, BOARD_HEIGHT//7))
        self.tetris.app.screen.blit(next_item_label_obj, next_item_label_rect)

        block_size = 30

        next_tetromino_rect = pygame.Rect(0,0, block_size, block_size)
        next_tetromino_rect.centerx = (INITIAL_RIGHT_SIDEBAR_X + SIDEBAR_WIDTH//2)
        next_tetromino_rect.top = next_item_label_rect.bottom + 70

        y_offset = 0
        for i in range(self.num_next_piece):
            Tetromino.draw_custom_position(self.tetris.app.screen, 
                                                self.tetris.bag[i],
                                                (next_tetromino_rect.x, next_tetromino_rect.y + y_offset), 
                                                block_size)
            y_offset += block_size * 3

    def draw_lines_cleared(self):
        """
        Draw the lines cleared UI
        """
        cleared_label_obj = self.textFont.render(self.lines_cleared_text, 1, TEXT_LABEL_COLOR)
        cleared_label_rect = cleared_label_obj.get_rect(center = (INITIAL_RIGHT_SIDEBAR_X + SIDEBAR_WIDTH//2, BOARD_HEIGHT//1.2))
        self.tetris.app.screen.blit(cleared_label_obj, cleared_label_rect)

        line_cleared_obj = self.textFont.render(str(self.tetris.lines_cleared), 1, TEXT_LABEL_COLOR)
        line_cleared_rect = line_cleared_obj.get_rect(center = (INITIAL_RIGHT_SIDEBAR_X + SIDEBAR_WIDTH//2, BOARD_HEIGHT//1.1))
        self.tetris.app.screen.blit(line_cleared_obj, line_cleared_rect)