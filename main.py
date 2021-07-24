# coding=utf-8
"""
Main Module
"""
import pygame
from pygame.locals import *

from zelda_game import ZeldaGame


def start(game):
    """  Start game method """
    pygame.init()
    screen = pygame.display.set_mode(game.display_size)
    game.set_screen(screen)
    pygame.display.set_caption(game.title())

    # Game Loop
    while True:
        # Update background
        game.fill_background()
        # Event loop
        for event in pygame.event.get():
            # Key to exit
            if event.type == QUIT:
                pygame.quit()
                exit()

        game.update()
        # Update pygame screen.
        pygame.display.flip()


if __name__ == '__main__':
    start(ZeldaGame(display_size=(480, 480)))
