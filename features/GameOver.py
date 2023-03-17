import pygame

from features.GameOverUI import GameOverUI
from features.State import State


class GameOver(State):
    """
        Class that represents the Game Over state of a Tetris game
    """
    def __init__(self, app, level, score, lines_cleared, time_passed, game_mode):
        super().__init__(app)
        self.ui = GameOverUI(self)
        
        self.level = level
        self.score = score
        self.lines_cleared = lines_cleared
        self.time_passed = time_passed
        self.game_mode = game_mode
    
    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.exit_state()
    
    def draw(self):
        self.ui.draw()