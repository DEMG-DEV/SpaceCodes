import sys
import math
import pygame
import random
from collections import defaultdict


class State:
    """Class representing positio and velocity."""

    def __init__(self, x, y, vx, vy):
        self._x = x
        self._y = y
        self._vx = vx
        self._vy = vy

    def __repr__(self):
        return 'x:{x} y:{y} vx:{vx} vy:{vy}'.format(x=self._x, y=self._y, vx=self._vx, vy=self._vy)
