# coding=utf-8
"""
Zelda Gun Model
"""
import pygame
from pygame.locals import (K_UP, K_DOWN, K_LEFT, K_RIGHT, RLEACCEL)

from abstract_sprite_manager import AbstractSpriteManager
from settings import FileUtil


class DefaultGunSpritesImages(AbstractSpriteManager):
    """ Default Gun sprite """

    def __init__(self, filename, screen, scale=1.0, color_key=(116, 116, 116)):
        super(DefaultGunSpritesImages, self).__init__()
        self._color_key = color_key
        self._filename = filename
        self._scale = scale
        # transform to scale
        w, h = screen.get_size()
        self._load_sprites().set_index((0, 1)).prepare_image(center=(w / 2 - 16, h / 2 - 16))

    def _load_sprites(self):
        # constants
        weapons = ((1, 185, 8, 16), (10, 185, 16, 16), (53, 185, 8, 16))
        # get sprites
        img = FileUtil('./sprites/aula05-spritesheet.png').get()
        img = pygame.image.load(img).convert_alpha()
        img.set_colorkey(self._color_key, RLEACCEL)
        h, v = False, True
        for pos in weapons:
            self._sprites.append(img.subsurface(pos))
            if pos[0] != 53:
                self._sprites.append(pygame.transform.flip(img.subsurface(pos), h, v))
                h, v = True, False
        return self


class DefaultGunLimitsRules:
    """ Rules to Default Gun limits """
    def __init__(self, rect, screen):
        self._screen = screen
        self._rect = rect

    def check(self):
        """ Check rules """
        w, h = self._screen.get_size()
        result = True
        if self._rect.top < 0 - self._rect.height:
            result = False
        elif self._rect.top > h:
            result = False
        elif self._rect.left < 0 - self._rect.width:
            result = False
        elif self._rect.left > w:
            result = False
        return result


class ZeldaDefaultGun(pygame.sprite.Sprite):
    """ Gun Class """
    def __init__(self, screen, sprites, key, pos, speed=7, scale=1.0):
        super(ZeldaDefaultGun, self).__init__()
        self._key = key
        self._scale = scale
        self._speed = speed
        self._sprites = sprites
        self._screen = screen
        # image load
        self._sprite = DefaultGunSpritesImages('./sprites/aula05-spritesheet.png', screen, 1.9)
        self.image, _ = self._sprite.image_rect
        self.rect = pos
        self.rect_undo = self.rect.copy()
        # sprites groups
        self._add_sprites()

    def _add_sprites(self):
        """ Add object to sprites. """
        for s in self._sprites:
            s.add(self)
        return self

    def _update_image_rect(self, *pos):
        self.image, self.rect = self._sprite.set_index(*pos).prepare_image(topleft=self.rect.topleft).image_rect
        return self

    def move(self):
        """ Set player movement """
        if self._key == K_UP:
            self._update_image_rect((0, 0))
            self.rect.move_ip(0, -self._speed)
        if self._key == K_DOWN:
            self._update_image_rect((1, 1))
            self.rect.move_ip(0, self._speed)
        if self._key == K_LEFT:
            self._update_image_rect((3, 3))
            self.rect.move_ip(-self._speed, 0)
        if self._key == K_RIGHT:
            self._update_image_rect((2, 2))
            self.rect.move_ip(self._speed, 0)
        self._check_limits()
        return self

    def _check_limits(self):
        """ Check borders limits to _player """
        if not DefaultGunLimitsRules(self.rect, self._screen).check():
            self._update_image_rect((4, 4))
            self.kill()
        return self

    def update(self, *args, **kwargs) -> None:
        """ Update """
        self.move()

    def kill(self) -> None:
        """ kill gun """
        super(ZeldaDefaultGun, self).kill()
