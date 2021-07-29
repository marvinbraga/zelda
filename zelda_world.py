# coding=utf-8
"""
Zelda World Module
"""
import random

from zelda_block import ZeldaBlock


class ZeldaWorld:
    """ World class """

    def __init__(self, screen, sprites):
        self._size = 32
        self._sprites = sprites
        self._screen = screen
        self.blocks = []
        self._create_blocks()

    def _create_blocks(self):
        """ Init blocks """
        w, h = self._screen.get_size()
        col_blocks = int(w / self._size)
        row_blocks = int(h / self._size)
        for x in range(col_blocks):
            self.blocks.append(ZeldaBlock(pos=(x * self._size, 0), sprites=self._sprites))
        for x in range(col_blocks):
            self.blocks.append(ZeldaBlock(pos=(x * self._size, h - self._size), sprites=self._sprites))
        # for y in range(row_blocks):
        #     self.blocks.append(ZeldaBlock(pos=(0, y * size), sprites=self._sprites))
        # for y in range(row_blocks):
        #     self.blocks.append(ZeldaBlock(pos=(w - size, y * size), sprites=self._sprites))
        return self

    def add_block(self, count=1):
        """ Add new Block """
        w, h = self._screen.get_size()
        for i in range(count):
            self.blocks.append(ZeldaBlock(
                pos=(random.randint(32, w - 64), random.randint(32, h - 64)), sprites=self._sprites))
        return self

    def update(self):
        """ Update world. """
        # Render all blocks.
        for block in self.blocks:
            block.update()
        return self
