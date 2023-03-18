import json
import os

import pygame

import features.menu.PlayMenu as PlayMenu
import features.Tetris as Tetris
from features.GameOverUI import GameOverUI
from features.State import State
from model.TetrisInformation import TetrisInformation, TetrisInformationEncoder
from SaveLoadSystem import SaveLoadSystem
from settings import *
from SoundManager import SoundManager


class GameOver(State):
    """
        Class that represents the Game Over state of a Tetris game
    """
    def __init__(self, app, tetris_info: TetrisInformation):
        super().__init__(app)
        self.ui = GameOverUI(self)
        
        self.tetris_info = tetris_info
        self.sound_manager = SoundManager.getInstance()
    
        
        self.save_load_system = SaveLoadSystem(file_path = "")    
        self.data = self.load_data(BEST_SCORE_FILE_NAME)  
        # self.save_data(BEST_SCORE_FILE_NAME)
    
    def on_start_state(self):
        self.sound_manager.play_ost(SoundManager.GAME_OVER_OST, loops = 0)
        
    def on_leave_state(self):
        self.save_data(BEST_SCORE_FILE_NAME)
    
    def is_game_sucess(self):
        if self.tetris_info.game_mode == Tetris.Tetris.MODE_SPRINT and self.tetris_info.lines_cleared < SPRINT_LINE_TO_CLEAR:
            return False
        elif self.tetris_info.game_mode == Tetris.Tetris.MODE_ULTRA and self.tetris_info.time_passed >= ULTRA_TIME_SPAN / 1000:
            return False
        
        return True
    
    def is_new_best_score(self, tetris_info: TetrisInformation):
        if tetris_info.game_mode not in self.data.keys():
            return True
        
        if tetris_info.game_mode in [Tetris.Tetris.MODE_MARATHON, Tetris.Tetris.MODE_ZEN]:
            if tetris_info.score > self.data[Tetris.Tetris.MODE_MARATHON]["Score"]:
                return True
        elif tetris_info.game_mode == Tetris.Tetris.MODE_SPRINT:
            if tetris_info.time_passed < self.data[Tetris.Tetris.MODE_SPRINT]["Time Passed"]:
                return True
        elif tetris_info.game_mode == Tetris.Tetris.MODE_ULTRA:
            if tetris_info.lines_cleared > self.data[Tetris.Tetris.MODE_ULTRA]["Lines Cleared"]:
                return True
        return False
    
    def save_data(self, file_name):
        if self.is_new_best_score(self.tetris_info) and self.is_game_sucess():
            self.data[self.tetris_info.game_mode] = self.tetris_info
        self.save_load_system.save(self.data, file_name, cls = TetrisInformationEncoder)
        
    def load_data(self, file_name):
        data = self.save_load_system.load(file_name)
        return data if data else {
            "__meta": "_GameMode"
        }
        
    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu_state = PlayMenu.PlayMenu(self.app)
                    menu_state.enter_state(State.CLEAR_TOP)
    
    def draw(self):
        self.ui.draw()
        