# coding=utf-8
"""
Zelda Block Module
"""
import os

import pygame

from settings import SPRITES_DIR


class ZeldaBlockSprite(pygame.sprite.Sprite):
    """ Sprite to block """
    _COUNT_SPRITE_LIN = 4
    _COUNT_SPRITE_COL = 5
    _ITER_IMAGE = 0.2

    def __init__(self, x, y, scale=1.0):
        super(ZeldaBlockSprite, self).__init__()
        self.scale = scale
        self.index = 0
        self.sprites = []
        self.image, self.rect = None, None
        self.width, self.height = 32, 32
        self._load_sprites()._invalidate(x, y)

    def _load_sprites(self):
        file = os.path.join(SPRITES_DIR, 'zelda world.png')
        sheet = pygame.image.load(file).convert_alpha()
        rect = (385, 201, 32, 32)
        self.sprites.append(sheet.subsurface(rect))
        return self

    def _invalidate(self, *args):
        self.image = self.sprites[int(self.index)]
        self.width, self.height = self.image.get_size()
        self.width, self.height = int(self.width * self.scale), int(self.height * self.scale)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.topleft = args
        return self

    def update(self, *args, **kwargs):
        """ Update image """
        self.index = 0
        self._invalidate(*args)


class ZeldaBlock:
    """ Block """

    def __init__(self, x, y):
        self.y, self.x, self.width, self.height = y, x, 32, 32
        self.display, self.sprite, self._screen = None, None, None
        self.sprites = pygame.sprite.Group()

    def update(self):
        """ Paint block """
        if not self.display:
            self.display = self._screen.get_size()
        self.sprites.draw(self._screen)
        self.sprites.update(self.x, self.y)
        return self

    @property
    def screen(self):
        """ Return screen property """
        return self._screen

    def set_screen(self, screen):
        """ Set block _screen """
        self._screen = screen
        self.sprite = ZeldaBlockSprite(self.x, self.y)
        self.sprites.add(self.sprite)
        self.width = self.sprite.width
        self.height = self.sprite.height
        return self
