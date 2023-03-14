from settings import *
import pygame
from model.Tetromino import Tetromino
from model.Block import Block_Draw_Mode
class TetrisUI:
    def __init__(self, tetris) -> None:
        self.tetris = tetris

        self.next_piece_text = "Next Piece:"
        self.hold_piece_text = "Hold Piece:"
        self.score_text = "Lines cleared:"
        self.textSize = 30
        self.textColor = (255,255,255)
        self.textFont = pygame.font.SysFont("comicsans", self.textSize)

    def draw(self):
        self.draw_grid()
        self.tetris.tetromino.draw(self.tetris.app.screen)
        self.draw_field()
        self.draw_indication()

        self.draw_side_bar()
    
    def draw_field(self):
        for row in range(len(self.tetris.field_arr)):
            for col in range(len(self.tetris.field_arr[row])):
                if self.tetris.field_arr[row][col] != 0:
                    self.tetris.field_arr[row][col].draw(self.tetris.app.screen)
    
    def draw_side_bar(self):
        pygame.draw.rect(self.tetris.app.screen, (0,0,0), (BOARD_WIDTH, 0, SIDEBAR_WIDTH, BOARD_HEIGHT))

        self.draw_next_piece()
        self.draw_hold_piece()
        self.draw_score()

    def draw_next_piece(self):
        nextItemTextObj = self.textFont.render(self.next_piece_text, 1, self.textColor)
        nextItemRect = nextItemTextObj.get_rect()
        nextItemRect.center = (BOARD_WIDTH + SIDEBAR_WIDTH//2, BOARD_HEIGHT//2)
        self.tetris.app.screen.blit(nextItemTextObj, nextItemRect)

        next_tetromino = Tetromino(self, self.tetris.bag[0])
        next_tetromino.move((7,13))
        next_tetromino.draw(self.tetris.app.screen)
    
    def draw_hold_piece(self):
        hold_item_text_obj = self.textFont.render(self.hold_piece_text, 1, self.textColor)
        hold_item_rect = hold_item_text_obj.get_rect()
        hold_item_rect.center = (BOARD_WIDTH + SIDEBAR_WIDTH//2, BOARD_HEIGHT//6)
        self.tetris.app.screen.blit(hold_item_text_obj, hold_item_rect)

        if self.tetris.hold_piece_shape != None:
            hold_tetromino = Tetromino(self, self.tetris.hold_piece_shape)
            hold_tetromino.move((7, 7))
            mode  = Block_Draw_Mode.BORDER_INDICATION_COLOR if self.tetris.has_hold else Block_Draw_Mode.FUll_COLOR
            if self.tetris.has_hold:
                temp_tetromino = Tetromino(self.tetris, self.tetris.tetromino.shape)
                temp_tetromino.move((7,7))
                temp_tetromino.draw(self.tetris.app.screen, mode) 
            else:
                hold_tetromino.draw(self.tetris.app.screen, mode) 

    def draw_score(self):
        score_text_obj = self.textFont.render(self.score_text, 1, self.textColor)
        score_text_rect = score_text_obj.get_rect()
        score_text_rect.center = (BOARD_WIDTH + SIDEBAR_WIDTH//2, BOARD_HEIGHT//1.2)
        self.tetris.app.screen.blit(score_text_obj, score_text_rect)

        score_obj = self.textFont.render(str(self.tetris.lines_cleared), 1, self.textColor)
        score_rect = score_obj.get_rect()
        score_rect.center = (BOARD_WIDTH + SIDEBAR_WIDTH//2, BOARD_HEIGHT//1.1)
        self.tetris.app.screen.blit(score_obj, score_rect)

    def draw_indication(self):
        tetro = self.tetris.get_hard_drop_indication()
        tetro.draw(self.tetris.app.screen, Block_Draw_Mode.BORDER_INDICATION)
        
    def draw_grid(self):
        for row in range(FIELD_HEIGHT):
            pygame.draw.line(self.tetris.app.screen, "black", (0, row * BLOCK_SIZE), (BOARD_WIDTH, row * BLOCK_SIZE), 1)
            for col in range(FIELD_WIDTH):
                pygame.draw.line(self.tetris.app.screen, "black", (col * BLOCK_SIZE, 0), (col * BLOCK_SIZE, BOARD_HEIGHT), 1)
        
        pygame.draw.line(self.tetris.app.screen, "black", (10 * BLOCK_SIZE, 0), (10 * BLOCK_SIZE, BOARD_HEIGHT), 1)