import pygame

from features.State import State
from features.Tetris import Tetris
from settings import *
from SoundManager import SoundManager
from ui.widget.AnimatedButton import AnimatedButton


class Menu(State):
    """
        Menu State of the program. 
        Contains the VsPlayer, VSComputer, and Quit options
    """
    def __init__(self, app):
        super().__init__(app)
        self.sound_manager = SoundManager()
        self.buttonWidth = 300
        self.buttonHeight = 100
        self.paddingTop = 50

        self.buttonX = self.app.screen.get_width()//2 - self.buttonWidth//2
        self.paddingTop = (self.app.screen.get_height() - (self.buttonHeight * 4)) / 5

        self.button_color = (128, 0, 128)
        self.button_hover_color = (150, 0, 150)
        self.setUpButtons()

        
    def setUpButtons(self):
        self.level_mode_button = AnimatedButton(self, self.buttonX, self.paddingTop,
                                  self.buttonWidth, self.buttonHeight, 
                                  color = self.button_color, text = "Level Mode", hoverColor= self.button_hover_color)
        self.level_mode_button.setOnClickListener(self.level_mode_click)
        self.level_mode_button.setOnHoverListener(self.on_hover)
        self.level_mode_button.setOnButtonDownListener(self.on_down)
        
        self.zen_mode_button = AnimatedButton(self, self.buttonX, self.paddingTop + self.level_mode_button.y + self.level_mode_button.height,
                                  self.buttonWidth, self.buttonHeight, 
                                  color = self.button_color, text = "Zen Mode", hoverColor= self.button_hover_color)
        self.zen_mode_button.setOnClickListener(self.zen_mode_click)
        self.zen_mode_button.setOnHoverListener(self.on_hover)
        self.zen_mode_button.setOnButtonDownListener(self.on_down)
        
        self.forty_lines_mode_button = AnimatedButton(self, self.buttonX, self.paddingTop + self.zen_mode_button.y + self.zen_mode_button.height,
                                  self.buttonWidth, self.buttonHeight, 
                                  color = self.button_color, text = "Forty Mode", hoverColor= self.button_hover_color)
        self.forty_lines_mode_button.setOnClickListener(self.forty_lines_mode_click)
        self.forty_lines_mode_button.setOnHoverListener(self.on_hover)
        self.forty_lines_mode_button.setOnButtonDownListener(self.on_down)
        
        self.ultra_mode_button = AnimatedButton(self, self.buttonX, self.paddingTop + self.forty_lines_mode_button.y + self.forty_lines_mode_button.height,
                                  self.buttonWidth, self.buttonHeight, 
                                  color = self.button_color, text = "Ultra Mode", hoverColor= self.button_hover_color)
        self.ultra_mode_button.setOnClickListener(self.ultra_mode_click)
        self.ultra_mode_button.setOnHoverListener(self.on_hover)
        self.ultra_mode_button.setOnButtonDownListener(self.on_down)

        self.button_list = [self.level_mode_button, self.zen_mode_button,self.forty_lines_mode_button, self.ultra_mode_button]

    def draw(self):
        rect = pygame.Rect(0,0, WIDTH, HEIGHT)
        pygame.draw.rect(self.app.screen, (0,0,0), rect)
        self.drawButtons()
    
    def update(self, events):
        pass
    
    def drawButtons(self):
        for button in self.button_list: button.draw(self.app.screen)

    """
        Button Listener
    """
    def level_mode_click(self):
        tetris_activity = Tetris(self.app, game_mode= Tetris.MODE_LEVEL)
        tetris_activity.enter_state()
    
    def zen_mode_click(self):
        tetris_activity = Tetris(self.app, game_mode= Tetris.MODE_ZEN)
        tetris_activity.enter_state()
    
    def forty_lines_mode_click(self):
        tetris_activity = Tetris(self.app, game_mode= Tetris.MODE_FORTY_LINES)
        tetris_activity.enter_state()
    
    def ultra_mode_click(self):
        tetris_activity = Tetris(self.app, game_mode= Tetris.MODE_ULTRA)
        tetris_activity.enter_state()
    
    def on_hover(self):
        self.sound_manager.play_menu(SoundManager.MENU_HOVER_SFX)
    
    def on_down(self):
        self.sound_manager.play_menu(SoundManager.MENU_HIT_SFX)