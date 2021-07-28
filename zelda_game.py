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
from zelf_enemy import ZeldaEnemy


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
        # events
        self.ADD_ENEMY = pygame.USEREVENT + 1
        pygame.time.set_timer(self.ADD_ENEMY, 20000)
        # actors
        self._player = ZeldaPlayer(self._screen, sprites=[self._all_sprites])
        self._world = ZeldaWorld(self._screen, sprites=[self._all_sprites, self._blocks])
        self.create_enemies(5)

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
        return key

    def update(self):
        """ Method to update de zelda game. """
        # Check block collision
        if pygame.sprite.spritecollideany(self._player, self._blocks):
            self._player.undo()
        # Guns and blocks
        for gun in self._guns:
            if pygame.sprite.spritecollideany(gun, self._blocks):
                gun.show_explosion()

        for gun in self._guns:
            for enemy in self._enemies:
                if pygame.sprite.collide_mask(gun, enemy):
                    gun.show_explosion()
                    enemy.kill()

        # Player and enemies
        if pygame.sprite.spritecollideany(self._player, self._enemies):
            self._player.kill()
            self.running = False

        # Draw all objects
        self._all_sprites.draw(self.screen)
        # Update world.
        self._world.update()
        self._enemies.update()
        self._guns.update()
        self._player.update(pressed_keys=pygame.key.get_pressed())

        return self

    def check_keys(self, event):
        """ Check key events """
        if event.key == K_SPACE:
            # Create a shot gun
            ZeldaDefaultGun(
                pos=self._player.rect, screen=self._screen, sprites=[self._all_sprites, self._guns],
                key=self._get_pressed_key()
            )

    def check_events(self, event):
        """ Method to check events updates. """
        if event.type == self.ADD_ENEMY:
            self.create_enemies(1)
        # elif event.type == self.ADD_BLOCK:
        #     self.create_blocks(1)

    def create_enemies(self, count):
        """ Create instance of enemy """
        for i in range(count):
            ZeldaEnemy(screen=self._screen, sprites=[self._all_sprites, self._enemies], speed=2)
        return self

