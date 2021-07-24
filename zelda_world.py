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
        for x in range(15):
            self.blocks.append(ZeldaBlock(x * 32, 0).set_screen(self._screen))
        for x in range(15):
            self.blocks.append(ZeldaBlock(x * 32, 480 - 32).set_screen(self._screen))
        for y in range(15):
            self.blocks.append(ZeldaBlock(0, y * 32).set_screen(self._screen))
        for y in range(15):
            self.blocks.append(ZeldaBlock(480 - 32, y * 32).set_screen(self._screen))
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
