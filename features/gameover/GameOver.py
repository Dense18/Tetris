import copy

import pygame

import features.menu.PlayMenu as PlayMenu
import features.tetrisgame.Tetris as Tetris
from features.gameover.GameOverUI import GameOverUI
from features.State import State
from model.TetrisStat import TetrisStat, TetrisStatEncoder
from settings import *
from SoundManager import SoundManager
from utils.TetrisStatFileManager import TetrisStatFileManager


class GameOver(State):
    """
        Class that represents the Game Over state of a Tetris game
    """
    def __init__(self, app, tetris_stat: TetrisStat):
        super().__init__(app)
        self.ui = GameOverUI(self)
        
        self.tetris_stat = tetris_stat
        
        self.sound_manager = SoundManager.getInstance()
        self.tetris_stat_manager = TetrisStatFileManager()   
        
        ## Load the old best data
        self.data = self.tetris_stat_manager.get_data()  
        
        self.is_high_score = self.is_game_successful() and self.is_new_best_score(self.tetris_stat)
        
        ## Save the new tetris_state data if needed
        self.save_tetris_stat()
        
        
    def on_start_state(self):
        if self.is_game_successful() and self.is_new_best_score(self.tetris_stat):
            self.sound_manager.play_ost(SoundManager.HIGH_SCORE_OST, loops = 0)
            return
        self.sound_manager.play_ost(SoundManager.GAME_OVER_OST, loops = 0)
    
    def is_game_successful(self):
        """
        Check whether the game is successful based on the game mode
        
        For Sprint Mode, the game is successful if the number of lines is larger than SPRINT_LINE_TO_CLEAR
            
        For Ultra mode, the game is successful if the time passed is larger than ULTRA_TIME_SPAN
        
        In other modes, the game will always be a successful game
        """
        if self.tetris_stat.game_mode == Tetris.Tetris.MODE_SPRINT and self.tetris_stat.lines_cleared < SPRINT_LINE_TO_CLEAR:
            return False
        elif self.tetris_stat.game_mode == Tetris.Tetris.MODE_ULTRA and self.tetris_stat.time_passed < ULTRA_TIME_SPAN/1000:
            return False
        
        return True
    
    def is_new_best_score(self, tetris_stat: TetrisStat):
        """
        Checks it the current tetris stats is better than the old best stats
        """
        if tetris_stat.game_mode not in self.data.keys():
            return True
        
        if tetris_stat.game_mode in [Tetris.Tetris.MODE_MARATHON, Tetris.Tetris.MODE_ZEN]:
            if tetris_stat.score > self.data[Tetris.Tetris.MODE_MARATHON]["Score"]:
                return True
        elif tetris_stat.game_mode == Tetris.Tetris.MODE_SPRINT:
            if tetris_stat.time_passed < self.data[Tetris.Tetris.MODE_SPRINT]["Time Passed"]:
                return True
        elif tetris_stat.game_mode == Tetris.Tetris.MODE_ULTRA:
            if tetris_stat.lines_cleared > self.data[Tetris.Tetris.MODE_ULTRA]["Lines Cleared"]:
                return True
        return False
    
    def save_tetris_stat(self):
        """
        Saves thes tetris stat into the system if it is a high score
        """
        if self.is_new_best_score(self.tetris_stat) and self.is_game_successful():
            data_to_save = copy.deepcopy(self.data)
            data_to_save[self.tetris_stat.game_mode] = self.tetris_stat
            self.tetris_stat_manager.save_dict(data_to_save)
        
    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE \
                or event.type == pygame.MOUSEBUTTONDOWN:
                    menu_state = PlayMenu.PlayMenu(self.app)
                    menu_state.enter_state(State.CLEAR_TOP)
    
    def draw(self):
        self.ui.draw()
        