import os

import pygame

from features.highscorestat.HighScoreStatUI import HighScoreStatUI
from features.State import State
from settings import *
from ui.widget.AnimatedButton import AnimatedButton, Button
from utils.SoundManager import SoundManager
from utils.TetrisStatFileManager import TetrisStatFileManager


class HighScoreStat(State):
    CLEAR_BUTTON_TAG = "Clear Button Tag"
    BACK_BUTTON_TAG = "Back Button Tag"
    
    def __init__(self, app):
        super().__init__(app)
        self.ui = HighScoreStatUI(self)
        self.sound_manager = SoundManager.getInstance()
        self.tetris_stat_file_manager = TetrisStatFileManager()
        self.data = self.tetris_stat_file_manager.get_data()
        
        self.back_image = pygame.image.load(os.path.join(IMAGES_DIR, "back_ic.png")).convert_alpha()
        
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
                                 elevation=6,tag = self.CLEAR_BUTTON_TAG)
        self.clear_button.setOnClickListener(self.on_click)
        self.clear_button.setOnHoverListener(self.on_hover)
        self.clear_button.setOnButtonDownListener(self.on_down)
        
        self.back_button = AnimatedButton(self, 30, 30,
                                  BACK_BUTTON_WIDTH, BACK_BUTTON_HEIGHT, 
                                  color = BUTTON_COLOR, hoverColor= BUTTON_HOVER_COLOR,
                                  text = "Back", textSize = 20, textColor = BACK_BUTTON_TEXT_COLOR,
                                  borderRadius= BACK_BUTTON_BORDER_RADIUS, elevation= BACK_BUTTON_ELEVATION,
                                  image = self.back_image, tag = self.BACK_BUTTON_TAG)
        self.back_button.setOnClickListener(self.on_click)
        self.back_button.setOnHoverListener(self.on_hover)
        self.back_button.setOnButtonDownListener(self.on_down)
        

        self.button_list = [self.clear_button, self.back_button]
    
    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.exit_state()
    
    def draw(self):
        # self.app.screen.fill((255,255,255))
        # self.app.screen.blit(self.image, (0, 0))
        self.ui.draw()
        
    """
        Button Listeners
    """
    def on_click(self, button):
        if button.tag == self.CLEAR_BUTTON_TAG:
            self.tetris_stat_file_manager.clear_data()
            self.data = self.tetris_stat_file_manager.get_data()
        elif button.tag == self.BACK_BUTTON_TAG:
            self.exit_state()
    
    def on_down(self, button):
        self.sound_manager.play_menu(SoundManager.MENU_HIT_SFX)
        
    def on_hover(self, button, first_hover):
        if first_hover: self.sound_manager.play_menu(SoundManager.MENU_HOVER_SFX)