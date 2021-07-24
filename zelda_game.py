# coding=utf-8
"""
Game Module
"""
import pygame.time
from pygame.constants import *

from abstract_game import AbstractGame
from zelda_player import ZeldaPlayer, Movement


class ZeldaGame(AbstractGame):
    """ Class main to game Zelda """

    _KEYS_MOV = {
        K_UP: Movement.UP,
        K_DOWN: Movement.DOWN,
        K_LEFT: Movement.LEFT,
        K_RIGHT: Movement.RIGHT,
        K_SPACE: Movement.NONE,
    }

    def __init__(self, display_size):
        super(ZeldaGame, self).__init__(display_size)
        self.player = ZeldaPlayer(self._screen, 10, 10)

    def title(self):
        """ Get title to window screen. """
        return 'My First Zelda Game in Pygame'

    def set_player_movement(self):
        """ Set _movement to player. """
        for key, mov in self._KEYS_MOV.items():
            if pygame.key.get_pressed()[key]:
                self.player.set_movement(mov)
                break

        return self

    def update(self):
        """ Method to update de zelda game. """
        if not self.player.screen:
            self.player.set_screen(self._screen)

        # Update player in screen.
        self.player.update()
        self.player.set_movement(Movement.NONE)

        return self
