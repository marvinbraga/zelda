# coding=utf-8
"""
Main Module
"""
import pygame
from pygame.locals import *

from zelda_game import ZeldaGame


def start(game):
    """  Start game method """
    pygame.display.set_caption(game.title())
    # Game Loop
    while game.running:
        # Update background
        game.fill_background(color=(0, 128, 0))
        # Event loop
        for event in pygame.event.get():
            if event.type == QUIT:
                game.running = False
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    game.running = False
            else:
                game.check_events(event)

        game.update()
        # Update pygame screen.
        pygame.display.flip()


if __name__ == '__main__':
    pygame.mixer.init()
    pygame.init()
    try:
        start(ZeldaGame(display_size=(640, 480)))
    finally:
        # pygame.mixer.music.stop()
        pygame.mixer.quit()
        pygame.quit()
