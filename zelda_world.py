# coding=utf-8
"""
Zelda World Module
"""
from zelda_block import ZeldaBlock


class ZeldaWorld:
    """ World class """

    def __init__(self, screen):
        self._screen = screen
        self.blocks = []

    def _create_blocks(self):
        """ Init blocks """
        size = ZeldaBlock.SIZE
        display_size = self._screen.get_size()
        col_blocks = int(display_size[0] / size)
        row_blocks = int(display_size[1] / size)
        for x in range(col_blocks):
            self.blocks.append(ZeldaBlock(x * size, 0).set_screen(self._screen))
        for x in range(col_blocks):
            self.blocks.append(ZeldaBlock(x * size, display_size[1] - size).set_screen(self._screen))
        for y in range(row_blocks):
            self.blocks.append(ZeldaBlock(0, y * size).set_screen(self._screen))
        for y in range(row_blocks):
            self.blocks.append(ZeldaBlock(display_size[0] - size, y * size).set_screen(self._screen))
        return self

    def set_screen(self, screen):
        """ Set block _screen """
        self._screen = screen
        self._create_blocks()
        return self

    def is_free(self, obj):
        """ Verify if is free position """
        result = True
        for block in self.blocks:
            if not obj.is_free(block):
                result = False
                break
        return result

    def update(self):
        """ Update world. """
        # Render all blocks.
        for block in self.blocks:
            block.update()
        return self
