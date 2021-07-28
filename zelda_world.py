# coding=utf-8
"""
Zelda World Module
"""
from zelda_block import ZeldaBlock


class ZeldaWorld:
    """ World class """

    def __init__(self, screen, sprites):
        self._sprites = sprites
        self._screen = screen
        self.blocks = []
        self._create_blocks()

    def _create_blocks(self):
        """ Init blocks """
        size = 32
        w, h = self._screen.get_size()
        col_blocks = int(w / size)
        row_blocks = int(h / size)
        for x in range(col_blocks):
            self.blocks.append(ZeldaBlock(pos=(x * size, 0), sprites=self._sprites))
        for x in range(col_blocks):
            self.blocks.append(ZeldaBlock(pos=(x * size, h - size), sprites=self._sprites))
        # for y in range(row_blocks):
        #     self.blocks.append(ZeldaBlock(pos=(0, y * size), sprites=self._sprites))
        # for y in range(row_blocks):
        #     self.blocks.append(ZeldaBlock(pos=(w - size, y * size), sprites=self._sprites))
        return self

    def update(self):
        """ Update world. """
        # Render all blocks.
        for block in self.blocks:
            block.update()
        return self
