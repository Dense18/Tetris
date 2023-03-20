import pygame

import features.Tetris as Tetris
from settings import *
from utils.utils import *


class GameOverUI:
    """
        Manages UI elements for the GamOver State
    """
    def __init__(self, game_over_state):
        self.state = game_over_state
        
        self.text_font = pygame.font.SysFont('comicsans', 30)
        self.high_score_text = "High Score!"
    
    def draw(self):
        """
        Draws the UI elements onto the screen
        """
        self.state.app.screen.fill(GAME_OVER_BG_COLOR)
        
        self.draw_information()
        if self.state.is_high_score:
            self.draw_high_score_text()
    
    def draw_information(self):
        """
            Draws the necessary information to the screen.
        """
        game_mode = self.state.tetris_stat.game_mode
        if game_mode == Tetris.Tetris.MODE_MARATHON or game_mode == Tetris.Tetris.MODE_ZEN:
            score_text_obj = self.text_font.render(f"Score: {int(self.state.tetris_stat.score)}", 1, GAME_OVER_SCORE_TEXT_COLOR)
            score_text_rect = score_text_obj.get_rect(center = (WIDTH//2, HEIGHT//2))
            self.state.app.screen.blit(score_text_obj, score_text_rect)
            
            if game_mode in self.state.data.keys():
                best_score = self.state.data[game_mode]["Score"]
                best_score = int(best_score) if best_score is not None else best_score
            else:
                best_score = 0
            
            best_score_text_obj = self.text_font.render(f"Old Best score: {best_score}", 1, "white")
            best_score_text_rect = best_score_text_obj.get_rect(center = (WIDTH//2, score_text_rect.bottom + 20))
            self.state.app.screen.blit(best_score_text_obj, best_score_text_rect)
        
        elif game_mode == Tetris.Tetris.MODE_SPRINT:
            time_text = convert_seconds_to_time_str(self.state.tetris_stat.time_passed)
            text = "Time Taken: " + time_text if self.state.is_game_successful() else "Try again next time!"
            text_color = GAME_OVER_SCORE_TEXT_COLOR if self.state.is_game_successful() else GAME_FAILED_TEXT_COLOR
            time_text_obj = self.text_font.render(text, 1, text_color)
            time_text_rect = time_text_obj.get_rect(center = (WIDTH//2, HEIGHT//2))
            self.state.app.screen.blit(time_text_obj, time_text_rect)
            
            if game_mode in self.state.data.keys():
                best_time = self.state.data[game_mode]["Time Passed"]
                best_time = int(best_time) if best_time is not None else 0
            else:
                best_time = None
            
            best_time_taken_text = f"Old Best Time Taken: {convert_seconds_to_time_str(best_time) if best_time else None}" 
            best_time_taken_obj  = self.text_font.render(best_time_taken_text, 1, "white")
            best_time_taken_rect = best_time_taken_obj.get_rect(center = (WIDTH//2, time_text_rect.bottom + 20))
            self.state.app.screen.blit(best_time_taken_obj, best_time_taken_rect)
        
        elif game_mode == Tetris.Tetris.MODE_ULTRA:
            text = f"Lines cleared: {self.state.tetris_stat.lines_cleared}" if self.state.is_game_successful() else "Try again next time!"
            text_color = GAME_OVER_SCORE_TEXT_COLOR if self.state.is_game_successful() else GAME_FAILED_TEXT_COLOR
            line_cleared_text_obj = self.text_font.render(text, 1, text_color)
            line_cleared_text_rect = line_cleared_text_obj.get_rect(center = (WIDTH//2, HEIGHT//2))
            self.state.app.screen.blit(line_cleared_text_obj, line_cleared_text_rect)
            
            if game_mode in self.state.data.keys():
                best_line_clear = self.state.data[game_mode]["Lines Cleared"]
                best_line_clear = int(best_line_clear) if best_line_clear is not None else best_line_clear
            else:
                best_line_clear = 0 
            
            best_line_cleared_text = f"Old Best Lines cleared: {best_line_clear}" 
            best_line_cleared_obj = self.text_font.render(best_line_cleared_text, 1, "white")
            best_line_cleared_rect = best_line_cleared_obj.get_rect(center = (WIDTH//2, line_cleared_text_rect.bottom + 20))
            self.state.app.screen.blit(best_line_cleared_obj, best_line_cleared_rect)
            
    def draw_high_score_text(self):
        """
        Draws the high score text onto the screen
        """
        self.high_score_obj = self.text_font.render(self.high_score_text, 1, HIGH_SCORE_TEXT_COLOR)
        self.high_score_rect = self.high_score_obj.get_rect(center = (WIDTH//2, HEIGHT//3.5))
        self.state.app.screen.blit(self.high_score_obj, self.high_score_rect)