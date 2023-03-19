import pygame

from features.menu.PlayMenuUI import PlayMenuUI
from features.State import State
from features.Tetris import Tetris
from settings import *
from SoundManager import SoundManager
from ui.widget.AnimatedButton import AnimatedButton


class PlayMenu(State):
    MARATHON_BUTTON_TAG = "Marathon Button Tag"
    ZEN_BUTTON_TAG = "Zen Button Tag"
    SPRINT_BUTTON_TAG = "Sprint Button Tag"
    ULTRA_BUTTON_TAG = "Ultra Button Tag"
    
    """
        Menu State of the program. 
        Contains the VsPlayer, VSComputer, and Quit options
    """
    def __init__(self, app):
        super().__init__(app)
        self.sound_manager = SoundManager.getInstance()
        self.buttonWidth = 300
        self.buttonHeight = 100
        self.paddingTop = 50

        self.buttonX = self.app.screen.get_width()//3 - self.buttonWidth//2
        self.paddingTop = (self.app.screen.get_height() - (self.buttonHeight * 4)) / 5
        self.setUpButtons()
        
        self.ui = PlayMenuUI(self)

    def setUpButtons(self):
        self.marathon_button = AnimatedButton(self, self.buttonX, self.paddingTop,
                                  self.buttonWidth, self.buttonHeight, 
                                  color = BUTTON_COLOR, text = "Marathon", hoverColor= BUTTON_HOVER_COLOR,
                                  tag = self.MARATHON_BUTTON_TAG)
        self.marathon_button.setOnClickListener(self.on_click)
        self.marathon_button.setOnHoverListener(self.on_hover)
        self.marathon_button.setOnButtonDownListener(self.on_down)
        
        self.zen_button = AnimatedButton(self, self.buttonX, self.paddingTop + self.marathon_button.y + self.marathon_button.height,
                                  self.buttonWidth, self.buttonHeight, 
                                  color = BUTTON_COLOR, text = "Zen", hoverColor= BUTTON_HOVER_COLOR,
                                  tag = self.ZEN_BUTTON_TAG)
        self.zen_button.setOnClickListener(self.on_click)
        self.zen_button.setOnHoverListener(self.on_hover)
        self.zen_button.setOnButtonDownListener(self.on_down)
        
        self.sprint_button = AnimatedButton(self, self.buttonX, self.paddingTop + self.zen_button.y + self.zen_button.height,
                                  self.buttonWidth, self.buttonHeight, 
                                  color = BUTTON_COLOR, text = "Sprint", hoverColor= BUTTON_HOVER_COLOR,
                                  tag = self.SPRINT_BUTTON_TAG)
        self.sprint_button.setOnClickListener(self.on_click)
        self.sprint_button.setOnHoverListener(self.on_hover)
        self.sprint_button.setOnButtonDownListener(self.on_down)
        
        self.ultra_button = AnimatedButton(self, self.buttonX, self.paddingTop + self.sprint_button.y + self.sprint_button.height,
                                  self.buttonWidth, self.buttonHeight, 
                                  color = BUTTON_COLOR, text = "Ultra", hoverColor= BUTTON_HOVER_COLOR,
                                  tag = self.ULTRA_BUTTON_TAG)
        self.ultra_button.setOnClickListener(self.on_click)
        self.ultra_button.setOnHoverListener(self.on_hover)
        self.ultra_button.setOnButtonDownListener(self.on_down)

        self.button_list = [self.marathon_button, self.zen_button,self.sprint_button, self.ultra_button]

    
    def on_resume_state(self):
        self.sound_manager.play_ost(SoundManager.MENU_OST, update = False)
        
    def draw(self):
        self.ui.draw()
    
    def update(self, events):
        for event in events:
            if event.type ==pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.exit_state()
    
    def drawButtons(self):
        for button in self.button_list: button.draw(self.app.screen)

    """
        Button Listener
    """
    def on_click(self, button):
        self.sound_manager.stop()
        if button.tag == self.MARATHON_BUTTON_TAG:
            state = Tetris(self.app, game_mode= Tetris.MODE_MARATHON)
        elif button.tag == self.ZEN_BUTTON_TAG:
            state = Tetris(self.app, game_mode= Tetris.MODE_ZEN)
        elif button.tag == self.SPRINT_BUTTON_TAG:
            state = Tetris(self.app, game_mode= Tetris.MODE_SPRINT)
        elif button.tag == self.ULTRA_BUTTON_TAG:
            state = Tetris(self.app, game_mode= Tetris.MODE_ULTRA)
        
        state.enter_state()
        
    def on_hover(self, button, first_hover):
        if first_hover: 
            self.sound_manager.play_menu(SoundManager.MENU_HOVER_SFX)
        if button.tag == self.MARATHON_BUTTON_TAG:
            self.ui.set_hint_flag(PlayMenuUI.MARATHON_HINT_TAG)
        elif button.tag == self.ZEN_BUTTON_TAG:
            self.ui.set_hint_flag(PlayMenuUI.ZEN_HINT_TAG)
        elif button.tag == self.SPRINT_BUTTON_TAG:
            self.ui.set_hint_flag(PlayMenuUI.SPRINT_HINT_TAG)
        elif button.tag == self.ULTRA_BUTTON_TAG:
            self.ui.set_hint_flag(PlayMenuUI.ULTRA_HINT_TAG)
        
    def on_down(self, button):
        self.sound_manager.play_menu(SoundManager.MENU_HIT_SFX)