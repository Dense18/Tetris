import pygame

import features.Tetris as Tetris
from features.menu.PlayMenuUI import PlayMenuUI
from features.State import State
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
        self.button_width = 300
        self.button_height = 100
        self.margin_top = 50

        self.button_x = self.app.screen.get_width()//3 - self.button_width//2
        self.margin_top = (self.app.screen.get_height() - (self.button_height * 4)) / 5
        self.setUpButtons()
        
        self.ui = PlayMenuUI(self)

    def setUpButtons(self):
        self.marathon_button = AnimatedButton(self, self.button_x, self.margin_top,
                                  self.button_width, self.button_height, 
                                  color = BUTTON_COLOR, hoverColor= BUTTON_HOVER_COLOR,
                                   text = "Marathon",textSize = MENU_BUTTON_TEXT_SIZE, 
                                   borderRadius= MENU_BUTTON_BORDER_RADIUS,
                                  tag = self.MARATHON_BUTTON_TAG)
        self.marathon_button.setOnClickListener(self.on_click)
        self.marathon_button.setOnHoverListener(self.on_hover)
        self.marathon_button.setOnButtonDownListener(self.on_down)
        
        self.zen_button = AnimatedButton(self, self.button_x, self.margin_top + self.marathon_button.y + self.marathon_button.height,
                                  self.button_width, self.button_height, 
                                  color = BUTTON_COLOR, text = "Zen", hoverColor= BUTTON_HOVER_COLOR,
                                  textSize = MENU_BUTTON_TEXT_SIZE, borderRadius= MENU_BUTTON_BORDER_RADIUS,
                                  tag = self.ZEN_BUTTON_TAG)
        self.zen_button.setOnClickListener(self.on_click)
        self.zen_button.setOnHoverListener(self.on_hover)
        self.zen_button.setOnButtonDownListener(self.on_down)
        
        self.sprint_button = AnimatedButton(self, self.button_x, self.margin_top + self.zen_button.y + self.zen_button.height,
                                  self.button_width, self.button_height, 
                                  color = BUTTON_COLOR, hoverColor= BUTTON_HOVER_COLOR,
                                  text = "Sprint", textSize = MENU_BUTTON_TEXT_SIZE, 
                                  borderRadius= MENU_BUTTON_BORDER_RADIUS,
                                  tag = self.SPRINT_BUTTON_TAG)
        self.sprint_button.setOnClickListener(self.on_click)
        self.sprint_button.setOnHoverListener(self.on_hover)
        self.sprint_button.setOnButtonDownListener(self.on_down)
        
        self.ultra_button = AnimatedButton(self, self.button_x, self.margin_top + self.sprint_button.y + self.sprint_button.height,
                                  self.button_width, self.button_height, 
                                  color = BUTTON_COLOR, hoverColor= BUTTON_HOVER_COLOR,
                                  text = "Ultra", textSize = MENU_BUTTON_TEXT_SIZE,
                                  borderRadius= MENU_BUTTON_BORDER_RADIUS,
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
            state = Tetris.Tetris(self.app, game_mode= Tetris.Tetris.MODE_MARATHON)
        elif button.tag == self.ZEN_BUTTON_TAG:
            state = Tetris.Tetris(self.app, game_mode= Tetris.Tetris.MODE_ZEN)
        elif button.tag == self.SPRINT_BUTTON_TAG:
            state = Tetris.Tetris(self.app, game_mode= Tetris.Tetris.MODE_SPRINT)
        elif button.tag == self.ULTRA_BUTTON_TAG:
            state = Tetris/Tetris(self.app, game_mode= Tetris.Tetris.MODE_ULTRA)
        
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