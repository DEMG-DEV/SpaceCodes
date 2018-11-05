import sys
import math
import pygame
import random
from collections import defaultdict


class Derivative:
    """Class representing velocity and acceleration."""

    def __init__(self, dx, dy, dvx, dvy):
        self._dx = dx
        self._dy = dy
        self._dvx = dvx
        self._dvy = dvy

    def __repr__(self):
        return 'dx:{dx} dy:{dy} dvx:{dvx} dvy:{dvy}'.format(dx=self._dx, dy=self._dy, dvx=self._dvx, dvy=self._dvy)
