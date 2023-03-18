import pygame

from App import App
from settings import *


def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tetris")
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.mixer.init()
    pygame.init()

    app = App(screen)
    app.run()

if __name__ == "__main__":
    main()