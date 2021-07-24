# coding=utf-8
"""
Zelda Block Module
"""
import pygame


class ZeldaBlock:
    """ Block """
    def __init__(self, x, y):
        self.y = y
        self.x = x
        self.width = 32
        self.height = 32
        self.display = None
        self._screen = None

    def update(self):
        """ Paint block """
        if not self.display:
            self.display = self._screen.get_size()
        pygame.draw.rect(
            self._screen, (255, 0, 255), (self.x, self.y, self.width, self.height))
        return self

    @property
    def screen(self):
        """ Return screen property """
        return self._screen

    def set_screen(self, screen):
        """ Set block _screen """
        self._screen = screen
        return self
