import sys
import math
import pygame
import random
from collections import defaultdict


class Planet:
    """Class representing a planet. The "_st" member is an instance of "State",
    carrying the planet's position and velocity - while the "_m" and "_r"
    members represents the planet's mass and radius."""

    def __init__(self):
        if PLANETS == 1:
            # A nice example of a planet orbiting around our sun :-)
            self._st = State(150, 300, 0, 2)
        else:
            # otherwise pick a random position and velocity
            self._st = State(
                float(random.randint(0, WIDTH)),
                float(random.randint(0, HEIGHT)),
                float(random.randint(0, 300)/100.)-1.5,
                float(random.randint(0, 300)/100.)-1.5)
        self._r = 1.5
        self.setMassFromRadius()
        self._merged = False

    def __repr__(self):
        return repr(self._st)

    def acceleration(self, state, unused_t):
        """Calculate acceleration caused by other planets on this one."""
        ax = 0.0
        ay = 0.0
        for p in g_listOfPlanets:
            if p is self or p._merged:
                continue  # ignore ourselves and merged planets
            dx = p._st._x - state._x
            dy = p._st._y - state._y
            dsq = dx*dx + dy*dy  # distance squared
            dr = math.sqrt(dsq)  # distance
            force = GRAVITYSTRENGTH*self._m*p._m/dsq if dsq > 1e-10 else 0.
            # Accumulate acceleration...
            ax += force*dx/dr
            ay += force*dy/dr
        return (ax, ay)

    def initialDerivative(self, state, t):
        """Part of Runge-Kutta method."""
        ax, ay = self.acceleration(state, t)
        return Derivative(state._vx, state._vy, ax, ay)

    def nextDerivative(self, initialState, derivative, t, dt):
        """Part of Runge-Kutta method."""
        state = State(0., 0., 0., 0.)
        state._x = initialState._x + derivative._dx*dt
        state._y = initialState._y + derivative._dy*dt
        state._vx = initialState._vx + derivative._dvx*dt
        state._vy = initialState._vy + derivative._dvy*dt
        ax, ay = self.acceleration(state, t+dt)
        return Derivative(state._vx, state._vy, ax, ay)

    def updatePlanet(self, t, dt):
        """Runge-Kutta 4th order solution to update planet's pos/vel."""
        a = self.initialDerivative(self._st, t)
        b = self.nextDerivative(self._st, a, t, dt*0.5)
        c = self.nextDerivative(self._st, b, t, dt*0.5)
        d = self.nextDerivative(self._st, c, t, dt)
        dxdt = 1.0/6.0 * (a._dx + 2.0*(b._dx + c._dx) + d._dx)
        dydt = 1.0/6.0 * (a._dy + 2.0*(b._dy + c._dy) + d._dy)
        dvxdt = 1.0/6.0 * (a._dvx + 2.0*(b._dvx + c._dvx) + d._dvx)
        dvydt = 1.0/6.0 * (a._dvy + 2.0*(b._dvy + c._dvy) + d._dvy)
        self._st._x += dxdt*dt
        self._st._y += dydt*dt
        self._st._vx += dvxdt*dt
        self._st._vy += dvydt*dt

    def setMassFromRadius(self):
        """From _r, set _m: The volume is (4/3)*Pi*(r^3)..."""
        self._m = DENSITY*4.*math.pi*(self._r**3.)/3.

    def setRadiusFromMass(self):
        """Reversing the setMassFromRadius formula, to calculate radius from
        mass (used after merging of two planets - mass is added, and new
        radius is calculated from this)"""
        self._r = (3.*self._m/(DENSITY*4.*math.pi))**(0.3333)
