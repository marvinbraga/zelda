# coding=utf-8
"""
Abstract Sprite Manager Module.
"""
from abc import ABCMeta, abstractmethod

import pygame


class AbstractSpriteManager(metaclass=ABCMeta):
    """ Class to Abstract Sprite Manager """

    _ITER_IMAGE = 0.2

    def __init__(self):
        self._sprites = []
        self._index, self._scale = 0, 1.0
        self._image, self._rect = None, None
        self._tag, self._old_tag = None, None

    @abstractmethod
    def _load_sprites(self):
        pass

    def set_index(self, min_max):
        """ Set movement to player """
        self._tag = min_max
        if self._old_tag != self._tag:
            self._old_tag = min_max
            self._index = min(*min_max)
        else:
            if self._index >= max(*min_max):
                self._index = min(*min_max)
            else:
                self._index += self._ITER_IMAGE
        return self

    def _transform(self):
        width, height = self._image.get_size()
        width, height = int(width * self._scale), int(height * self._scale)
        self._image = pygame.transform.scale(self._image, (width, height))
        return self

    def prepare_image(self, **kwargs):
        """ Prepare image from sprite """
        try:
            self._image = self._sprites[int(self._index)]
            self._transform()
            self._rect = self._image.get_rect(**kwargs)
        except Exception as e:
            print('Error: ', e, 'Index: ', int(self._index))
        return self

    @property
    def image_rect(self):
        """ returns image """
        return self._image, self._rect
