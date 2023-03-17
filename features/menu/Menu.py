import pygame

from features.State import State
from features.Tetris import Tetris
from settings import *
from ui.widget.AnimatedButton import AnimatedButton


class Menu(State):
    """
        Menu State of the program. 
        Contains the VsPlayer, VSComputer, and Quit options
    """
    def __init__(self, app):
        super().__init__(app)
        self.buttonWidth = 300
        self.buttonHeight = 100
        self.paddingTop = 50

        self.buttonX = self.app.screen.get_width()//2 - self.buttonWidth//2
        self.paddingTop = (self.app.screen.get_height() - (self.buttonHeight * 1)) / 2

        self.button_color = (128, 0, 128)
        self.button_hover_color = (150, 0, 150)
        self.setUpButtons()

        
    def setUpButtons(self):
        self.play_level_button = AnimatedButton(self, self.buttonX, self.paddingTop,
                                  self.buttonWidth, self.buttonHeight, 
                                  color = self.button_color, text = "Level Mode", hoverColor= self.button_hover_color)
        self.play_level_button.setOnClickListener(self.on_play_level_click)


        self.button_list = [self.play_level_button]

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
    def on_play_level_click(self):
        tetris_activity = Tetris(self.app)
        tetris_activity.enter_state()
    
    # def onQuitButtonClick(self):
    #     self.app.running = False