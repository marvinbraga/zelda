# coding=utf-8
"""
Game Module
"""
import pygame.time
from pygame.locals import (K_UP, K_DOWN, K_LEFT, K_RIGHT, K_SPACE)

from base.abstract_game import AbstractGame
from game.zelda_gun import ZeldaDefaultGun
from game.zelda_player import ZeldaPlayer
from game.zelda_world import ZeldaWorld
from game.zelda_enemy import ZeldaEnemy


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
        pygame.time.set_timer(self.ADD_ENEMY, 10000)
        self.ADD_BLOCK = pygame.USEREVENT + 2
        pygame.time.set_timer(self.ADD_BLOCK, 5000)
        # actors
        self._player = ZeldaPlayer(self._screen, sprites=[self._all_sprites])
        self._world = ZeldaWorld(screen=self._screen, sprites=[self._all_sprites, self._blocks], player=self._player)
        self.create_enemies(3)
        self._enemies_count = 1

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

    def enemies_move(self):
        """ Make enemies moves """
        x, y = self._player.rect.center
        for enemy in self._enemies:
            ex, ey = enemy.rect.center
            if ex < x:
                enemy.update(pressed_keys={K_RIGHT: True, K_LEFT: False, K_DOWN: False, K_UP: False})
            elif ex > x:
                enemy.update(pressed_keys={K_RIGHT: False, K_LEFT: True, K_DOWN: False, K_UP: False})
            if ey < y:
                enemy.update(pressed_keys={K_RIGHT: False, K_LEFT: False, K_DOWN: True, K_UP: False})
            elif ey > y:
                enemy.update(pressed_keys={K_RIGHT: False, K_LEFT: False, K_DOWN: False, K_UP: True})

        return self

    def update(self):
        """ Method to update de zelda game. """
        self.enemies_move()
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

        for block in self._blocks:
            for enemy in self._enemies:
                if pygame.sprite.collide_rect(block, enemy):
                    enemy.undo()

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
            self._enemies_count *= 2
            self.create_enemies(self._enemies_count)
        elif event.type == self.ADD_BLOCK:
            self._world.add_block()

    def create_enemies(self, count):
        """ Create instance of enemy """
        for i in range(count):
            ZeldaEnemy(screen=self._screen, sprites=[self._all_sprites, self._enemies], speed=2)
        return self
