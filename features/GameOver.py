import json
import os

import pygame

import features.menu.Menu as Menu
import features.Tetris as Tetris
from features.GameOverUI import GameOverUI
from features.State import State
from SaveLoadSystem import SaveLoadSystem
from settings import *


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
        
        self.save_load_system = SaveLoadSystem(file_path = "")
        
        
        self.data = self.load_data(BEST_SCORE_FILE_NAME)  
        self.save_data(BEST_SCORE_FILE_NAME)
        
    def on_leave_state(self):
        data_to_save = self.score if self.game_mode == Tetris.Tetris.MODE_MARATHON \
            else self.lines_cleared if self.game_mode == Tetris.Tetris.MODE_ULTRA \
            else self.time_passed if self.game_mode == Tetris.Tetris.MODE_SPRINT \
            else self.score
        self.data[self.game_mode] = self.score
        self.save_data(BEST_SCORE_FILE_NAME)
    
    def save_data(self, file_name):
        self.save_load_system.save(self.data, file_name)
        
    def load_data(self, file_name):
        data = self.save_load_system.load(file_name)
        return data if data else {
            Tetris.Tetris.MODE_MARATHON: 0,
            Tetris.Tetris.MODE_ZEN: 0,
            Tetris.Tetris.MODE_ULTRA: 0,
            Tetris.Tetris.MODE_SPRINT: 0
        }
        
    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu_state = Menu.Menu(self.app)
                    menu_state.enter_state(State.CLEAR_TOP)
    
    def draw(self):
        self.ui.draw()