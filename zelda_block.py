# coding=utf-8
"""
Zelda Block Module
"""

import pygame
from pygame.locals import RLEACCEL

from abstract_sprite_manager import AbstractSpriteManager
from settings import FileUtil


class BlockSpritesImages(AbstractSpriteManager):
    """ Images to sprite """

    def __init__(self, filename, pos, scale=1.0, color_key=(116, 116, 116)):
        super(BlockSpritesImages, self).__init__()
        self._color_key = color_key
        self._scale = scale
        self._pos = pos
        self._filename = filename
        self._load_sprites()

    def _load_sprites(self):
        img = FileUtil(self._filename).get()
        rect = (385, 201, 32, 32)
        self._image = pygame.image.load(img).subsurface(rect).convert_alpha()
        self._image.set_colorkey(self._color_key, RLEACCEL)
        self._rect = self._image.get_rect(topleft=self._pos)
        return self


class ZeldaBlock(pygame.sprite.Sprite):
    """ Sprite to block """

    def __init__(self, pos, sprites):
        super(ZeldaBlock, self).__init__()
        self._sprites = sprites
        self.image, self.rect = BlockSpritesImages('./sprites/zelda world.png', pos).image_rect
        self._add_sprites()

    def _add_sprites(self):
        """ Add object to sprites. """
        for s in self._sprites:
            s.add(self)
        return self

    def update(self, *args, **kwargs) -> None:
        """ Update """
        pass
