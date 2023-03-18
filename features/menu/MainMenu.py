import pygame

from features.menu.PlayMenu import PlayMenu
from features.State import State
from features.Tetris import Tetris
from settings import *
from SoundManager import SoundManager
from ui.widget.AnimatedButton import AnimatedButton


class MainMenu(State):
    """
        MainMenu State of the program. 
        Contains the Play, High Score, and Quit options
    """
    def __init__(self, app):
        super().__init__(app)
        self.sound_manager = SoundManager.getInstance()
        self.buttonWidth = 300
        self.buttonHeight = 100
        self.paddingTop = 50

        self.buttonX = self.app.screen.get_width()//2 - self.buttonWidth//2
        self.paddingTop = (self.app.screen.get_height() - (self.buttonHeight * 3)) / 4

        self.button_color = BUTTON_COLOR
        self.button_hover_color = BUTTON_HOVER_COLOR
        self.setUpButtons()
        
        # self.sound_manager.play_ost(SoundManager.MENU_OST)

    def setUpButtons(self):
        self.play_button = AnimatedButton(self, self.buttonX, self.paddingTop,
                                  self.buttonWidth, self.buttonHeight, 
                                  color = self.button_color, text = "Play", hoverColor= self.button_hover_color)
        self.play_button.setOnClickListener(self.on_play_click)
        self.play_button.setOnHoverListener(self.on_hover)
        self.play_button.setOnButtonDownListener(self.on_down)
        
        self.high_score_button = AnimatedButton(self, self.buttonX, self.paddingTop + self.play_button.y + self.play_button.height,
                                  self.buttonWidth, self.buttonHeight, 
                                  color = self.button_color, text = "High Score", hoverColor= self.button_hover_color)
        self.high_score_button.setOnClickListener(self.on_high_score_click)
        self.high_score_button.setOnHoverListener(self.on_hover)
        self.high_score_button.setOnButtonDownListener(self.on_down)
        
        self.quit_button = AnimatedButton(self, self.buttonX, self.paddingTop + self.high_score_button.y + self.high_score_button.height,
                                  self.buttonWidth, self.buttonHeight, 
                                  color = self.button_color, text = "Quit", hoverColor= self.button_hover_color)
        self.quit_button.setOnClickListener(self.on_quit_click)
        self.quit_button.setOnHoverListener(self.on_hover)
        self.quit_button.setOnButtonDownListener(self.on_down)
        

        self.button_list = [self.play_button, self.high_score_button, self.quit_button]

    
    def on_resume_state(self):
        self.sound_manager.play_ost(SoundManager.MENU_OST, update = False)
        pass
    
    def on_exit_state(self):
        self.sound_manager.stop()
        
    def draw(self):
        rect = pygame.Rect(0,0, WIDTH, HEIGHT)
        pygame.draw.rect(self.app.screen, (0,0,0), rect)
        self.drawButtons()
    
    def update(self, events):
        for event in events:
            if event.type ==pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.exit_state()
                if event.key == pygame.K_p:
                    self.on_play_click()
    
    def drawButtons(self):
        for button in self.button_list: button.draw(self.app.screen)

    """
        Button Listener
    """
    def on_play_click(self):
        play_menu_activity = PlayMenu(self.app)
        play_menu_activity.enter_state()
    
    def on_high_score_click(self):
        #TODO: Implement high score state activity
        pass
    
    def on_quit_click(self):
        self.exit_state()
    
    def on_hover(self):
        self.sound_manager.play_menu(SoundManager.MENU_HOVER_SFX)
    
    def on_down(self):
        self.sound_manager.play_menu(SoundManager.MENU_HIT_SFX)