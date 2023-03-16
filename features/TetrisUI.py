from settings import *
import pygame
from model.Tetromino import Tetromino
from model.Block import Block

class TetrisUI:
    """
        Manages the UI elements for the Tetris game
    """
    def __init__(self, tetris) -> None:
        self.tetris = tetris
        
        self.num_next_piece = min(self.tetris.bag_min_items, 5)

        self.next_piece_text = "Next Piece:"
        self.hold_piece_text = "Hold Piece:"
        self.lines_cleared_text = "Lines cleared:"
        self.level_label_text = "Level:"
        self.score_text = "Score:"

        self.textSize = 30
        self.textColor = (255,255,255)
        self.textFont = pygame.font.SysFont("comicsans", self.textSize)

    def draw(self):

        self.draw_left_side_bar()

        self.draw_grid()
        self.tetris.tetromino.draw(self.tetris.app.screen, offset = (SIDEBAR_WIDTH, 0))
        self.draw_field()
        self.draw_ghost_tetromino()

        self.draw_right_side_bar()
    
    def draw_left_side_bar(self):
        pygame.draw.rect(self.tetris.app.screen, SIDEBAR_BG_COLOR, (INITIAL_LEFT_SIDEBAR_X, 0, SIDEBAR_WIDTH, BOARD_HEIGHT))

        self.draw_hold_piece()
        self.draw_action_score()
        self.draw_score()
        self.draw_level()
    
    def draw_hold_piece(self):
        hold_item_text_obj = self.textFont.render(self.hold_piece_text, 1, self.textColor)
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
    
    def draw_action_score(self):
        b2b_text = "B2B!" if self.tetris.is_b2b else ""
        b2b_text_obj = self.textFont.render(b2b_text, 1, self.textColor)
        
        action_text = ACTION_TO_TEXT[self.tetris.action]
        action_obj = self.textFont.render(action_text, 1, self.textColor)
        action_rect = action_obj.get_rect()

        combo_text = f"x {self.tetris.combo}" if self.tetris.combo >= 1 else ""
        combo_text_obj = self.textFont.render(combo_text, 1, self.textColor)
        
        b2b_text_rect = b2b_text_obj.get_rect(center = (INITIAL_LEFT_SIDEBAR_X + SIDEBAR_WIDTH//2, BOARD_HEIGHT//2.2 - action_obj.get_height()))
        action_rect = action_obj.get_rect(centerx = INITIAL_LEFT_SIDEBAR_X + SIDEBAR_WIDTH//2, top = b2b_text_rect.bottom + 10)
        combo_text_rect = combo_text_obj.get_rect(centerx = INITIAL_LEFT_SIDEBAR_X + SIDEBAR_WIDTH//2, top = action_rect.bottom + 10)

        self.tetris.app.screen.blit(b2b_text_obj, b2b_text_rect)
        self.tetris.app.screen.blit(action_obj, action_rect)
        self.tetris.app.screen.blit(combo_text_obj, combo_text_rect)


    def draw_score(self):
        score_label_obj = self.textFont.render(self.score_text, 1, self.textColor)
        score_label_rect = score_label_obj.get_rect(center = (INITIAL_LEFT_SIDEBAR_X + SIDEBAR_WIDTH//2, BOARD_HEIGHT//1.5))
        self.tetris.app.screen.blit(score_label_obj, score_label_rect)

        score_text_obj = self.textFont.render(str(round(self.tetris.score)), 1, self.textColor)
        score_text_rect = score_text_obj.get_rect(centerx = (INITIAL_LEFT_SIDEBAR_X + SIDEBAR_WIDTH//2), top = score_label_rect.bottom + 30)
        self.tetris.app.screen.blit(score_text_obj, score_text_rect)
    
    def draw_level(self):
        level_label_obj = self.textFont.render(self.level_label_text + " "+str(self.tetris.level), 1, self.textColor)
        level_label_rect = level_label_obj.get_rect(center = (INITIAL_LEFT_SIDEBAR_X + SIDEBAR_WIDTH//2, BOARD_HEIGHT//1.15))
        self.tetris.app.screen.blit(level_label_obj, level_label_rect)

    def draw_field(self):
        for row in range(len(self.tetris.field_arr)):
            for col in range(len(self.tetris.field_arr[row])):
                if self.tetris.field_arr[row][col] != 0:
                    self.tetris.field_arr[row][col].draw(self.tetris.app.screen, offset = (SIDEBAR_WIDTH, 0))
    
    def draw_right_side_bar(self):
        pygame.draw.rect(self.tetris.app.screen, SIDEBAR_BG_COLOR, (INITIAL_RIGHT_SIDEBAR_X, 0, SIDEBAR_WIDTH, BOARD_HEIGHT))

        self.draw_next_piece()
        self.draw_hold_piece()
        self.draw_lines_cleared()

    def draw_next_piece(self):
        next_item_label_obj = self.textFont.render(self.next_piece_text, 1, self.textColor)
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
        cleared_label_obj = self.textFont.render(self.lines_cleared_text, 1, self.textColor)
        cleared_label_rect = cleared_label_obj.get_rect(center = (INITIAL_RIGHT_SIDEBAR_X + SIDEBAR_WIDTH//2, BOARD_HEIGHT//1.2))
        self.tetris.app.screen.blit(cleared_label_obj, cleared_label_rect)

        line_cleared_obj = self.textFont.render(str(self.tetris.lines_cleared), 1, self.textColor)
        line_cleared_rect = line_cleared_obj.get_rect(center = (INITIAL_RIGHT_SIDEBAR_X + SIDEBAR_WIDTH//2, BOARD_HEIGHT//1.1))
        self.tetris.app.screen.blit(line_cleared_obj, line_cleared_rect)

    def draw_ghost_tetromino(self):
        tetro = self.tetris.get_ghost_tetromino()
        tetro.draw(self.tetris.app.screen, offset = (SIDEBAR_WIDTH, 0), mode = Block.MODE_BORDER_INDICATION)
        
    def draw_grid(self):
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