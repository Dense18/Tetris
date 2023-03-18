import pygame

from features.menu.MainMenu import MainMenu
from features.Tetris import Tetris
from settings import *


class App:
    """
        Main Application state of the program
    """
    def __init__(self, screen) -> None:
        self.screen = screen
        self.isRunning = True
        self.clock = pygame.time.Clock()
        
        self.state_stack = []

        self.set_custom_events()
        
        self.load_initial_state()
    
    def load_initial_state(self):
        """
            Loads the first state of the program to the system
        """
        tetris_activity = MainMenu(self)
        tetris_activity.enter_state()

    def set_custom_events(self):
        """
            Set custom events for the Animation event and Accelerate event
            
            Informations:
                Animation event - the time between each frame for the moving tetromino.
                
                Accelerate event - the time between each frame for the accelerating tetromino. 
        """
        self.animation_event = pygame.USEREVENT + 1
        self.accelerate_event = pygame.USEREVENT + 2

        self.animation_flag = False
        self.accelerate_event = False

        pygame.time.set_timer(self.animation_event, ZEN_MODE_FALL_SPEED)
        pygame.time.set_timer(self.accelerate_event, ACCELERATE_INTERVAL)
    
    def loop(self):
        """
            Run the program in one loop/frame
        """
        self.clock.tick(FPS)
        self.getEvents()
        self.update()
        self.draw()
    
    def getEvents(self):
        """
            Retreive information about the pygame events
        """
        self.events = pygame.event.get()

    def update(self):
        """
            Updates the application state
        """
        self.animation_flag = False
        self.accelerate_event = False
        
        for event in self.events:
            if event.type == pygame.QUIT:
                self.isRunning = False
            if event.type == self.animation_event:
                self.animation_flag = True
            if event.type == self.accelerate_event:
                self.accelerate_event = True
        
        self.state_stack[-1].notify(pygame.mouse.get_pos(), pygame.mouse.get_pressed())
        if len(self.state_stack): # State stack might be empty from an observer update
            self.state_stack[-1].update(self.events)
        pass

    def draw(self):
        """
            Draws the application state to the screen
        """
        if len(self.state_stack) <= 0:
            return
        pygame.draw.rect(self.screen, BG_COLOR, (0,0,self.screen.get_width(), self.screen.get_height()))
        self.state_stack[-1].draw()
        pygame.display.update()
        pass

    def run(self):
        """
            Run the application
        """
        while self.isRunning and len(self.state_stack):
            self.loop()
