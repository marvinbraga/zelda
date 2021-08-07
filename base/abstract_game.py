# coding=utf-8
"""
Abstract Game Module
"""
from abc import ABCMeta, abstractmethod

import pygame


class AbstractGame(metaclass=ABCMeta):
    """ Class main to game Zelda """

    def __init__(self, display_size, mps=60):
        self._mps = mps
        self._display_size = display_size
        self._screen = None
        self.running = True
        self.timer = pygame.time.Clock()
        self.background = None

    @property
    def display_size(self):
        """ Return tuple with display size. """
        return self._display_size

    @property
    def screen(self):
        """ Return screen """
        return self._screen

    def fill_background(self, color=(0, 0, 0)):
        """ Update background. """
        self.timer.tick(self._mps)
        self._screen.fill(color)
        if self.background:
            self._screen.blit(self.background, (0, 0))
        return self

    @property
    @abstractmethod
    def title(self):
        """ Get title to window screen. """
        pass

    @abstractmethod
    def update(self):
        """ Method to update game history. """
        pass

    @abstractmethod
    def check_events(self, event):
        """ Method to check events updates. """
        pass
