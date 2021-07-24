# coding=utf-8
"""
ZeldaPlayer Module
"""
import os
from enum import Enum

import pygame

from abstract_player import AbstractPlayer
from settings import SPRITES_DIR


class Movement(Enum):
    """ Movement data """
    NONE = 99
    LEFT = 0
    RIGHT = 5
    UP = 10
    DOWN = 15


class ZeldaPlayerSprite(pygame.sprite.Sprite):
    """ Sprite class to Zelda Player """

    _COUNT_SPRITE_LIN = 4
    _COUNT_SPRITE_COL = 5
    _ITER_IMAGE = 0.2

    def __init__(self, x, y, scale=1.0):
        super(ZeldaPlayerSprite, self).__init__()
        self.index = 0
        self.scale = scale
        self.sprites = []
        self.old_movement, self.movement = Movement.NONE, Movement.NONE
        self.image, self.rect = None, None
        self.width, self.height = 0, 0
        self._load_sprites()._invalidate(x, y)

    def _load_sprites(self):
        file = os.path.join(SPRITES_DIR, 'player.png')
        sheet = pygame.image.load(file).convert_alpha()
        for x in range(self._COUNT_SPRITE_LIN):
            for y in range(self._COUNT_SPRITE_COL):
                rect = (90 * y, 90 * x, 90, 90)
                self.sprites.append(sheet.subsurface(rect))
        return self

    def set_index(self, value):
        """ Set index image to sprite """
        if self.movement == self.old_movement:
            self.index = value
        elif self.movement != Movement.NONE:
            self.index = self.movement.value
        # Restart
        if self.index > self.movement.value + self._COUNT_SPRITE_LIN:
            self.index = self.movement.value
        # Not stopped
        if self.movement != Movement.NONE:
            self.index += self._ITER_IMAGE
        return self

    def update(self, *args, **kwargs):
        """ Update image """
        self.set_index(self.index)._invalidate(*args)

    def _invalidate(self, *args):
        self.image = self.sprites[int(self.index)]
        self.width, self.height = self.image.get_size()
        self.width, self.height = int(self.width * self.scale), int(self.height * self.scale)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.topleft = args
        return self


class ZeldaPlayer(AbstractPlayer):
    """ Class player. """

    def __init__(self, screen, x, y, speed=4):
        self._screen = screen
        self._undo_rect, self.sprite, self.display = None, None, None
        self._is_free = True
        # Position
        self.x, self.y, self.width, self.height = x, y, 0, 0
        # Movement
        self._movement = Movement.NONE
        self.speed = speed
        # Setup
        self.color = (0, 0, 255)
        self.sprites = pygame.sprite.Group()

    def _save_undo(self):
        """ Save rect of old rect data """
        self._undo_rect = (self.x, self.y, self.width, self.height)
        return self

    def restore(self):
        """ Restore data from undo. """
        self.x, self.y, self.width, self.height = self._undo_rect
        return self

    @property
    def movement(self):
        """ Return movement """
        return self._movement

    def set_movement(self, value):
        """ Set movement """
        if self.sprite.movement != Movement.NONE:
            self.sprite.old_movement = self._movement
        self.sprite.movement = value

        self._movement = value
        self.sprite.set_index(self.sprite.index)
        return self

    @property
    def screen(self):
        """ Return screen property """
        return self._screen

    def set_screen(self, screen):
        """ Set player _screen """
        self._screen = screen
        self.sprite = ZeldaPlayerSprite(self.x, self.y, scale=0.9)
        self.sprites.add(self.sprite)
        self.width = self.sprite.width
        self.height = self.sprite.height

    def check_limits(self):
        """ Verify _screen limits """
        # Right
        if self.x > self.display[0]:
            self.x = 0 - self.width
        # Left
        if self.x < 0 - self.width:
            self.x = self.display[0]
        # Bottom
        if self.y > self.display[1]:
            self.y = 0 - self.height
        # Top
        if self.y < 0 - self.height:
            self.y = self.display[1]
        return self

    def tick(self):
        """ Apply _movement. """
        self._save_undo()
        if self._movement == Movement.RIGHT:
            self.x += self.speed
        if self._movement == Movement.LEFT:
            self.x -= self.speed
        if self._movement == Movement.UP:
            self.y -= self.speed
        if self._movement == Movement.DOWN:
            self.y += self.speed
        return self

    def update(self):
        """ Paint _screen with player setup. """
        if not self.display:
            self.display = self._screen.get_size()
        self.tick().check_limits()
        self.sprites.draw(self._screen)
        self.sprites.update(self.x, self.y)
        self._is_free = True
        return self

    def is_free(self, obj):
        """ Verify if players is not in collision. """
        rect_1 = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
        rect_2 = pygame.Rect(self.x, self.y, self.width, self.height)
        self._is_free = not rect_2.colliderect(rect_1)
        return self._is_free
