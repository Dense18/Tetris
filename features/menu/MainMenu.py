import pygame

from features.highscorestat.HighScoreStat import HighScoreStat
from features.menu.PlayMenu import PlayMenu
from features.State import State
from settings import *
from ui.widget.AnimatedButton import AnimatedButton
from utils.SoundManager import SoundManager


class MainMenu(State):
    """
        MainMenu State of the program. 
        Contains the Play, High Score, and Quit options
    """
    PLAY_BUTTON_TAG = "Play Button Tag"
    HIGH_SCORE_BUTTON_TAG = "High Score Button Tag"
    QUIT_BUTTON_TAG = "Quit Button Tag"
    
    def __init__(self, app):
        super().__init__(app)
        self.sound_manager = SoundManager.getInstance()
        self.button_width = 300
        self.button_height = 100
        self.margin_top = 50


        self.button_x = self.app.screen.get_width()//2 - self.button_width//2
        self.margin_top = (self.app.screen.get_height() - (self.button_height * 3)) / 4
        self.setUpButtons()
        
        # self.sound_manager.play_ost(SoundManager.MENU_OST)

    def setUpButtons(self):
        self.play_button = AnimatedButton(self, self.button_x, self.margin_top,
                                  self.button_width, self.button_height, 
                                  color = BUTTON_COLOR, hoverColor= BUTTON_HOVER_COLOR, 
                                  text = "Play", textSize = MENU_BUTTON_TEXT_SIZE, textColor = BUTTON_TEXT_COLOR, 
                                  borderRadius= MENU_BUTTON_BORDER_RADIUS,
                                  tag = self.PLAY_BUTTON_TAG)
        self.play_button.setOnClickListener(self.on_click)
        self.play_button.setOnHoverListener(self.on_hover)
        self.play_button.setOnButtonDownListener(self.on_down)
        
        self.high_score_button = AnimatedButton(self, self.button_x, self.margin_top + self.play_button.y + self.play_button.height,
                                  self.button_width, self.button_height, 
                                  color = BUTTON_COLOR, hoverColor = BUTTON_HOVER_COLOR,
                                  text = "High Score", textSize = MENU_BUTTON_TEXT_SIZE, textColor = BUTTON_TEXT_COLOR, 
                                  borderRadius= MENU_BUTTON_BORDER_RADIUS,
                                  tag = self.HIGH_SCORE_BUTTON_TAG)
        self.high_score_button.setOnClickListener(self.on_click)
        self.high_score_button.setOnHoverListener(self.on_hover)
        self.high_score_button.setOnButtonDownListener(self.on_down)
        
        self.quit_button = AnimatedButton(self, self.button_x, self.margin_top + self.high_score_button.y + self.high_score_button.height,
                                  self.button_width, self.button_height, 
                                  color = BUTTON_COLOR, hoverColor= BUTTON_HOVER_COLOR,
                                  text = "Quit", textSize = MENU_BUTTON_TEXT_SIZE, textColor = BUTTON_TEXT_COLOR, 
                                  borderRadius= MENU_BUTTON_BORDER_RADIUS,
                                  tag = self.QUIT_BUTTON_TAG)
        self.quit_button.setOnClickListener(self.on_click)
        self.quit_button.setOnHoverListener(self.on_hover)
        self.quit_button.setOnButtonDownListener(self.on_down)
        

        self.button_list = [self.play_button, self.high_score_button, self.quit_button]

    
    def on_resume_state(self):
        self.sound_manager.play_ost(SoundManager.MENU_OST, update = False)
    
    def on_exit_state(self):
        self.sound_manager.stop()
        
    def draw(self):
        # rect = pygame.Rect(0,0, WIDTH, HEIGHT)
        # pygame.draw.rect(self.app.screen, (0,0,0), rect)
        self.drawButtons()
    
    def update(self, events):
        pass
    
    def drawButtons(self):
        for button in self.button_list: button.draw(self.app.screen)

    """
        Button Listener
    """
    def on_click(self, button):
        if button.tag == self.PLAY_BUTTON_TAG:
            state = PlayMenu(self.app)
        elif button.tag == self.HIGH_SCORE_BUTTON_TAG:
            state = HighScoreStat(self.app)
        elif button.tag == self.QUIT_BUTTON_TAG:
            self.exit_state()
            return
        state.enter_state()
        
    def on_hover(self, button, first_hover):
        if first_hover: self.sound_manager.play_menu(SoundManager.MENU_HOVER_SFX)
        
    
    def on_down(self, button):
        self.sound_manager.play_menu(SoundManager.MENU_HIT_SFX)