# coding=utf-8
"""
Abstract Player Module.
"""

from abc import ABCMeta, abstractmethod


class AbstractPlayer(metaclass=ABCMeta):
    """ Abstract class to player. """

    @abstractmethod
    def tick(self):
        """ Apply _movement. """
        pass

    @abstractmethod
    def update(self):
        """ Paint screen with player setup. """
        pass
