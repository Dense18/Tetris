import pygame

from App import App
from settings import *


def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tetris")
    
    # pygame.mixer.pre_init(22050, -16, 2, 64)
    # pygame.mixer.pre_init(44100, -16, 2, 32)
    pygame.init()
    # pygame.mixer.quit()
    # pygame.mixer.init(22050, -16, 2, 64)
    # pygame.mixer.init(44100, -16, 2, 32, allowedchanges=0)
    print(pygame.mixer.get_init())
    
    # pygame.mixer.pre_init(44100, -16, 2, 2048)
    # pygame.mixer.init() 
    # pygame.init()

    app = App(screen)
    app.run()

if __name__ == "__main__":
    main()