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
        self.button_color = "Red"
        self.button_hover_color = (200,0,0)
        self.button_x = self.app.screen.get_width()//2 - self.button_width//2
        self.set_up_buttons()
    
    def set_up_buttons(self):
        self.clear_button = AnimatedButton(self, self.button_x, self.app.screen.get_height()//10,
                                  self.button_width, self.button_height, 
                                  color = self.button_color, text = "Clear", textSize=18, textColor="black",
                                  hoverColor= self.button_color, elevation=6)
        
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
        self.tetris_stat_file_manager.clear_data()
        self.data = self.tetris_stat_file_manager.get_data()
    
    def on_hover(self, button, first_hover):
        if first_hover: self.sound_manager.play_menu(SoundManager.MENU_HOVER_SFX)