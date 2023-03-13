import pygame
from settings import *
from App import App


def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tetris")
    pygame.init()

    app = App(screen)
    app.run()

if __name__ == "__main__":
    main()