import pygame

import features.Tetris as Tetris
from settings import *
from utils import *


class GameOverUI:
    def __init__(self, game_over_state):
        self.state = game_over_state
        
        self.text_font = pygame.font.SysFont('comicsans', 30)
    
    def draw(self):
        self.state.app.screen.fill((0, 0, 0))
        
        # text_obj = self.text_font.render('GAME OVER', 1, "white")
        # text_obj_rect = text_obj.get_rect(center = (WIDTH//2, HEIGHT//2))
        # self.state.app.screen.blit(text_obj, text_obj_rect)
        
        self.draw_information()
    
    def draw_information(self):
        """
            Draws the necessary information to the screen.
        """
        if self.state.game_mode == Tetris.Tetris.MODE_LEVEL or self.state.game_mode == Tetris.Tetris.MODE_ZEN:
            score_text_obj = self.text_font.render("Score: " + str(self.state.score), 1, "white")
            score_text_rect = score_text_obj.get_rect(center = (WIDTH//2, HEIGHT//2))
            self.state.app.screen.blit(score_text_obj, score_text_rect)
        
        elif self.state.game_mode == Tetris.Tetris.MODE_FORTY_LINES:
            time_text = convert_seconds_to_time_str(self.state.time_passed)
            
            
            text = "Time Taken: " + time_text if self.state.lines_cleared >= 40 else "Try again next time!"
            time_text_obj = self.text_font.render(text, 1, "white")
            time_text_rect = time_text_obj.get_rect(center = (WIDTH//2, HEIGHT//2))
            self.state.app.screen.blit(time_text_obj, time_text_rect)
        
        elif self.state.game_mode == Tetris.Tetris.MODE_ULTRA:
            text = "Lines cleared: " + str(self.state.lines_cleared) if self.state.time_passed >= ULTRA_TIME_SPAN/1000 else "Try again next time!"
            line_cleared_text_obj = self.text_font.render(text, 1, "white")
            line_cleared_text_rect = line_cleared_text_obj.get_rect(center = (WIDTH//2, HEIGHT//2))
            self.state.app.screen.blit(line_cleared_text_obj, line_cleared_text_rect)