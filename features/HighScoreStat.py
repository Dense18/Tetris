import pygame

from features.HighScoreStatUI import HighScoreStatUI
from features.State import State
from settings import *
from SoundManager import SoundManager
from TetrisStatFileManager import TetrisStatFileManager
from ui.widget.AnimatedButton import AnimatedButton


class HighScoreStat(State):
    def __init__(self, app):
        super().__init__(app)
        self.ui = HighScoreStatUI(self)
        self.sound_manager = SoundManager.getInstance()
        self.tetris_stat_file_manager = TetrisStatFileManager()
        self.data = self.tetris_stat_file_manager.get_data()
        
        self.button_width = 60
        self.button_height = 30
        self.button_x = self.app.screen.get_width() - self.button_width - 30
        self.button_y = 30
        self.set_up_buttons()
    
    def set_up_buttons(self):
        self.clear_button = AnimatedButton(self, self.button_x, self.button_y,
                                  self.button_width, self.button_height, 
                                  color = CLEAR_BUTTON_COLOR, hoverColor= CLEAR_BUTTON_HOVER_COLOR,
                                  text = "Clear", textSize=18, textColor="black",
                                 elevation=6)
        
        self.clear_button.setOnClickListener(self.on_click)

        self.button_list = [self.clear_button]
    
    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.exit_state()
    
    def draw(self):
        self.ui.draw()
        
    """
        Button Listeners
    """
    def on_click(self, button):
        self.sound_manager.play_menu(SoundManager.MENU_HIT_SFX)
        self.tetris_stat_file_manager.clear_data()
        self.data = self.tetris_stat_file_manager.get_data()
    
    def on_hover(self, button, first_hover):
        if first_hover: self.sound_manager.play_menu(SoundManager.MENU_HOVER_SFX)