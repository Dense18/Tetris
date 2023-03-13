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
        pass
    
    def loop(self):
        self.clock.tick(FPS)
        self.getEvents()
        self.update()
        self.draw()
    
    def getEvents(self):
        self.events = pygame.event.get()

    def update(self):
        for event in self.events:
            if event.type == pygame.QUIT:
                self.isRunning = False
        self.tetris.update(self.events)
        pass

    def draw(self):
        pygame.draw.rect(self.screen, (40,40,40), (0,0,self.screen.get_width(), self.screen.get_height()))
        self.tetris.draw()
        pygame.display.update()
        pass

    def run(self):
        while self.isRunning:
            self.loop()