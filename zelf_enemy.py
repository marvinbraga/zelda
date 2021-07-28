# coding=utf-8
"""
Zelda Enemy Module
"""
import random

import pygame
from pygame.locals import (K_UP, K_DOWN, K_LEFT, K_RIGHT, RLEACCEL)

from abstract_sprite_manager import AbstractSpriteManager
from settings import FileUtil


class EnemySpritesImages(AbstractSpriteManager):
    """ Images to sprite """

    def __init__(self, screen, pos=(0, 0), scale=1.0, color_key=(116, 116, 116)):
        super(EnemySpritesImages, self).__init__()
        self._color_key = color_key
        self._filename = './sprites/aula05-spritesheet.png'
        self._scale = scale
        # transform to scale
        w, h = screen.get_size()
        kwargs = {'topleft': (random.randint(32, w - 64), random.randint(32, h - 64))}
        if pos != (0, 0):
            kwargs = {'topleft': pos}
        self._load_sprites().set_index((0, 1)).prepare_image(**kwargs)

    def _load_sprites(self):
        # constants
        size = (16, 16)
        basic_movement = ((143, 209), (160, 209), (177, 209), (194, 209), (211, 209), (228, 209))
        # get sprites
        img = FileUtil(self._filename).get()
        img = pygame.image.load(img).convert_alpha()
        img.set_colorkey(self._color_key, RLEACCEL)
        for pos in basic_movement:
            rect = (pos[0], pos[1], size[0], size[1])
            self._sprites.append(img.subsurface(rect))
        # Add left movement
        for pos in basic_movement:
            rect = (pos[0], pos[1], size[0], size[1])
            if pos[0] in [35, 52]:
                # Flip the image to left movement
                self._sprites.append(pygame.transform.flip(img.subsurface(rect), True, False))
        return self


class EnemyLimitsRules:
    """ Rules to player walk limits """

    def __init__(self, rect, screen):
        self._screen = screen
        self._rect = rect

    def check(self):
        """ Check rules """
        w, h = self._screen.get_size()
        if self._rect.top < 0 - self._rect.height:
            self._rect.top = h - self._rect.height
        elif self._rect.top > h:
            self._rect.top = 0 - self._rect.height
        elif self._rect.left < 0 - self._rect.width:
            self._rect.left = w - self._rect.width
        elif self._rect.left > w:
            self._rect.left = 0 - self._rect.width


class ZeldaEnemy(pygame.sprite.Sprite):
    """ New Class """

    def __init__(self, screen, sprites, speed=4, scale=1.0):
        super(ZeldaEnemy, self).__init__()
        self._scale = scale
        self._speed = speed
        self._sprites = sprites
        self._screen = screen
        # image load
        self._sprite = EnemySpritesImages(screen=screen, scale=2.0)
        self.image, self.rect = self._sprite.image_rect
        self.rect_undo = self.rect.copy()
        # sprites groups
        self._add_sprites()

    def _add_sprites(self):
        """ Add object to sprites. """
        for s in self._sprites:
            s.add(self)
        return self

    def _update_image_rect(self, *pos):
        self.image, self.rect = self._sprite.set_index(*pos).prepare_image(topleft=self.rect.topleft).image_rect
        return self

    def move(self, pressed_keys):
        """ Set player movement """
        self.rect_undo = self.rect.copy()
        if pressed_keys[K_DOWN]:
            self._update_image_rect((0, 1))
            self.rect.move_ip(0, self._speed)
        if pressed_keys[K_RIGHT]:
            self._update_image_rect((2, 3))
            self.rect.move_ip(self._speed, 0)
        if pressed_keys[K_UP]:
            self._update_image_rect((4, 5))
            self.rect.move_ip(0, -self._speed)
        if pressed_keys[K_LEFT]:
            self._update_image_rect((6, 7))
            self.rect.move_ip(-self._speed, 0)
        self._check_limits()
        return self

    def _check_limits(self):
        """ Check borders limits to _player """
        EnemyLimitsRules(self.rect, self._screen).check()
        return self

    def undo(self):
        """ Undo position """
        self.rect = self.rect_undo.copy()
        return self

    def update(self, *args, **kwargs) -> None:
        """ Update """
        pressed_keys = kwargs.get('pressed_keys')
        if pressed_keys:
            self.move(pressed_keys)
