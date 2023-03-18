import pygame

from features.HighScoreStatUI import HighScoreStatUI
from features.State import State


class HighScoreStat(State):
    def __init__(self, app):
        super().__init__(app)
        self.ui = HighScoreStatUI(self)
    
    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.exit_state()
    
    def draw(self):
        self.ui.draw()