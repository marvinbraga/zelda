# coding=utf-8
"""
Settings Module
"""
import os

BASE_DIR = os.path.dirname(__file__)


class FileUtil:
    """ util to files """
    def __init__(self, file):
        self.file = file

    def get(self):
        """ Return the file and path """
        return os.path.join(BASE_DIR, self.file)
