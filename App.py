import pygame
from features.Tetris import Tetris
from settings import *

class App:
    """
        Main Application of the program
    """
    def __init__(self, screen) -> None:
        self.screen = screen
        self.isRunning = True
        self.tetris = Tetris(self)
        self.clock = pygame.time.Clock()

        self.set_animation_event()
        pass

    def set_animation_event(self):
        self.animation_event = pygame.USEREVENT + 1
        self.speed_event = pygame.USEREVENT + 2

        self.animation_flag = False
        self.accelerate_event = True

        pygame.time.set_timer(self.animation_event, ANIMATION_INTERVAL)
        pygame.time.set_timer(self.accelerate_event, ACCELERATE_INTERVAL)
    
    def loop(self):
        self.clock.tick(FPS)
        self.getEvents()
        self.update()
        self.draw()
    
    def getEvents(self):
        self.events = pygame.event.get()

    def update(self):
        self.animation_flag = False
        for event in self.events:
            if event.type == pygame.QUIT:
                self.isRunning = False
            if event.type == self.animation_event:
                self.animation_flag = True
            if event.type == self.accelerate_event:
                self.accelerate_event = True
        self.tetris.update(self.events)
        pass

    def draw(self):
        pygame.draw.rect(self.screen, BG_COLOR, (0,0,self.screen.get_width(), self.screen.get_height()))
        self.tetris.draw()
        pygame.display.update()
        pass

    def run(self):
        while self.isRunning:
            self.loop()