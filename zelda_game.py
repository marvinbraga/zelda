# coding=utf-8
"""
Game Module
"""
import pygame.time
from abstract_game import AbstractGame
from zelda_player import ZeldaPlayer
from zelda_world import ZeldaWorld


class ZeldaGame(AbstractGame):
    """ Class main to game Zelda """

    def __init__(self, display_size):
        super(ZeldaGame, self).__init__(display_size)
        # Screen
        self._screen = pygame.display.set_mode(display_size)
        # sprite groups
        self._enemies = pygame.sprite.Group()
        self._blocks = pygame.sprite.Group()
        self._all_sprites = pygame.sprite.Group()
        # actors
        self._player = ZeldaPlayer(self._screen, sprites=[self._all_sprites])
        self._world = ZeldaWorld(self._screen, sprites=[self._all_sprites, self._blocks])

    def title(self):
        """ Get title to window screen. """
        return 'My First Zelda Game in Pygame'

    def update(self):
        """ Method to update de zelda game. """
        self._all_sprites.draw(self.screen)

        # Check block collision
        if pygame.sprite.spritecollideany(self._player, self._blocks):
            self._player.undo()

        # Update world.
        self._world.update()
        self._player.update(pressed_keys=pygame.key.get_pressed())

        return self

    def check_events(self, event):
        """ Method to check events updates. """
        # if event.type == self.ADD_ENEMY:
        #     self.create_enemies(1)
        # elif event.type == self.ADD_BLOCK:
        #     self.create_blocks(1)
