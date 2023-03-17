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
        if self.state.game_mode == Tetris.Tetris.MODE_MARATHON or self.state.game_mode == Tetris.Tetris.MODE_ZEN:
            score_text_obj = self.text_font.render("Score: " + str(int(self.state.score)), 1, "white")
            score_text_rect = score_text_obj.get_rect(center = (WIDTH//2, HEIGHT//2))
            self.state.app.screen.blit(score_text_obj, score_text_rect)
            
            
            best_score = self.state.data[self.state.game_mode]
            best_score = int(best_score) if best_score is not None else best_score
            
            best_score_text_obj = self.text_font.render("Old Best score: " + str(best_score), 1, "white")
            best_score_text_rect = best_score_text_obj.get_rect(center = (WIDTH//2, score_text_rect.bottom + 20))
            self.state.app.screen.blit(best_score_text_obj, best_score_text_rect)
        
        elif self.state.game_mode == Tetris.Tetris.MODE_SPRINT:
            time_text = convert_seconds_to_time_str(self.state.time_passed)
            text = "Time Taken: " + time_text if self.state.lines_cleared >= 40 else "Try again next time!"
            time_text_obj = self.text_font.render(text, 1, "white")
            time_text_rect = time_text_obj.get_rect(center = (WIDTH//2, HEIGHT//2))
            self.state.app.screen.blit(time_text_obj, time_text_rect)
            
            best_time = self.state.data[self.state.game_mode]
            best_time = int(best_time) if best_time is not None else 0
            
            best_time_taken_text = "Old Best Time Taken: " + convert_seconds_to_time_str(best_time)
            best_time_taken_obj  = self.text_font.render(best_time_taken_text, 1, "white")
            best_time_taken_rect = best_time_taken_obj.get_rect(center = (WIDTH//2, time_text_rect.bottom + 20))
            self.state.app.screen.blit(best_time_taken_obj, best_time_taken_rect)
        
        elif self.state.game_mode == Tetris.Tetris.MODE_ULTRA:
            text = "Lines cleared: " + str(self.state.lines_cleared) if self.state.time_passed >= ULTRA_TIME_SPAN/1000 else "Try again next time!"
            line_cleared_text_obj = self.text_font.render(text, 1, "white")
            line_cleared_text_rect = line_cleared_text_obj.get_rect(center = (WIDTH//2, HEIGHT//2))
            self.state.app.screen.blit(line_cleared_text_obj, line_cleared_text_rect)
            
            
            best_line_clear = self.state.data[self.state.game_mode]
            best_line_clear = int(best_line_clear) if best_line_clear is not None else best_line_clear
            
            best_line_cleared_text = "Old Best Lines cleared: " + str(best_line_clear)
            best_line_cleared_obj = self.text_font.render(best_line_cleared_text, 1, "white")
            best_line_cleared_rect = best_line_cleared_obj.get_rect(center = (WIDTH//2, line_cleared_text_rect.bottom + 20))
            self.state.app.screen.blit(best_line_cleared_obj, best_line_cleared_rect)