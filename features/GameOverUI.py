import pygame

from settings import *


class GameOverUI:
    def __init__(self, game_over_state):
        self.state = game_over_state
        
        self.text_font = pygame.font.SysFont('comicsans', 30)
    
    def draw(self):
        self.state.app.screen.fill((0, 0, 0))
        
        text_obj = self.text_font.render('GAME OVER', 1, "white")
        text_obj_rect = text_obj.get_rect(center = (WIDTH//2, HEIGHT//2))
        self.state.app.screen.blit(text_obj, text_obj_rect)
        