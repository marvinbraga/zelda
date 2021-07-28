# coding=utf-8
"""
Game Module
"""
import pygame.time
from pygame.locals import (K_UP, K_DOWN, K_LEFT, K_RIGHT, K_SPACE)

from abstract_game import AbstractGame
from zeld_gun import ZeldaDefaultGun
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
        self._guns = pygame.sprite.Group()
        self._blocks = pygame.sprite.Group()
        self._all_sprites = pygame.sprite.Group()
        # actors
        self._player = ZeldaPlayer(self._screen, sprites=[self._all_sprites])
        self._world = ZeldaWorld(self._screen, sprites=[self._all_sprites, self._blocks])

    def title(self):
        """ Get title to window screen. """
        return 'My First Zelda Game in Pygame'

    @staticmethod
    def _get_pressed_key():
        """ Return pressed key  """
        key = K_RIGHT
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_UP]:
            key = K_UP
        elif pressed_keys[K_DOWN]:
            key = K_DOWN
        elif pressed_keys[K_LEFT]:
            key = K_LEFT
        # elif pressed_keys[K_RIGHT]:
        #     key = K_RIGHT
        return key

    def update(self):
        """ Method to update de zelda game. """
        # Check block collision
        if pygame.sprite.spritecollideany(self._player, self._blocks):
            self._player.undo()
        if pygame.sprite.spritecollideany(self._player, self._enemies):
            self._player.kill()
            self.running = False
        for gun in self._guns:
            if pygame.sprite.spritecollideany(gun, self._blocks):
                gun.kill()
            # if pygame.sprite.collide_rect(self._player, gun):
            #     gun.kill()

        # Draw all objects
        self._all_sprites.draw(self.screen)
        # Update world.
        self._world.update()
        self._enemies.update()
        self._guns.update()
        self._player.update(pressed_keys=pygame.key.get_pressed())

        return self

    def check_events(self, event):
        """ Method to check events updates. """
        # if event.type == self.ADD_ENEMY:
        #     self.create_enemies(1)
        # elif event.type == self.ADD_BLOCK:
        #     self.create_blocks(1)
        if event.key == K_SPACE:
            ZeldaDefaultGun(self._screen, [self._all_sprites, self._guns], self._get_pressed_key(), self._player.rect)
