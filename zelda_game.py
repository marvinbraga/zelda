# coding=utf-8
"""
Game Module
"""
import pygame.time
from pygame.constants import *

from abstract_game import AbstractGame
from zelda_player import ZeldaPlayer, Movement
from zelda_world import ZeldaWorld


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
        self.player = ZeldaPlayer(self._screen, 100, 100)
        self.world = ZeldaWorld(self._screen)

    def title(self):
        """ Get title to window screen. """
        return 'My First Zelda Game in Pygame'

    def set_screen(self, value):
        """ Set screen """
        super().set_screen(value)
        self.world.set_screen(value)
        return self

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

        # Update world.
        self.world.update()
        if not self.world.is_free(self.player):
            self.player.restore()
        # Update player in screen.
        self.player.update()
        self.player.set_movement(Movement.NONE)

        return self
