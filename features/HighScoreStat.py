import pygame

from features.HighScoreStatUI import HighScoreStatUI
from features.State import State
from TetrisStatFileManager import TetrisStatFileManager


class HighScoreStat(State):
    def __init__(self, app):
        super().__init__(app)
        self.ui = HighScoreStatUI(self)
        self.tetris_stat_file_manager = TetrisStatFileManager()
        self.data = self.tetris_stat_file_manager.get_data()

    
    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.exit_state()
    
    def draw(self):
        self.ui.draw()