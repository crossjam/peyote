"""Graphics module for peyote."""

__all__ = ['Context', 'Canvas', 'PeyoteError']

from .Context import Context
from .Canvas import Canvas

import pygame

class PeyoteError(Exception): pass
