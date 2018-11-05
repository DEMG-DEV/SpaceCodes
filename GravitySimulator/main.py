import sys
import math
import pygame
import random
from collections import defaultdict
from State import State
from Deritative import Derivative
from Planet import Planet


def main():
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))

    keysPressed = defaultdict(bool)

    def ScanKeyboard():
        while True:
            # Update the keysPressed state:
            evt = pygame.event.poll()
            if evt.type == pygame.NOEVENT:
                break
            elif evt.type in [pygame.KEYDOWN, pygame.KEYUP]:
                keysPressed[evt.key] = evt.type == pygame.KEYDOWN

    global g_listOfPlanets, PLANETS
    if len(sys.argv) == 2:
        PLANETS = int(sys.argv[1])

    # And God said: Let there be lights in the firmament of the heavens...
    g_listOfPlanets = []
    for i in xrange(0, PLANETS):
        g_listOfPlanets.append(Planet())

    def planetsTouch(p1, p2):
        dx = p1._st._x - p2._st._x
        dy = p1._st._y - p2._st._y
        dsq = dx*dx + dy*dy
        dr = math.sqrt(dsq)
        return dr <= (p1._r + p2._r)

    sun = Planet()
    sun._st._x, sun._st._y = WIDTHD2, HEIGHTD2
    sun._st._vx = sun._st._vy = 0.
    sun._m *= 1000
    sun.setRadiusFromMass()
    g_listOfPlanets.append(sun)
    for p in g_listOfPlanets:
        if p is sun:
            continue
        if planetsTouch(p, sun):
            p._merged = True  # ignore planets inside the sun

    # Zoom factor, changed at runtime via the '+' and '-' numeric keypad keys
    zoom = 1.0
    # t and dt are unused in this simulation, but are in general,
    # parameters of engine (acceleration may depend on them)
    t, dt = 0., 1.

    bClearScreen = True
    pygame.display.set_caption('Gravity simulation (SPACE: show orbits, '
                               'keypad +/- : zoom in/out)')
    while True:
        t += dt
        pygame.display.flip()
        if bClearScreen:  # Show orbits or not?
            win.fill((0, 0, 0))
        win.lock()
        for p in g_listOfPlanets:
            if not p._merged:  # for planets that have not been merged, draw a
                # circle based on their radius, but take zoom factor into account
                pygame.draw.circle(win, (255, 255, 255),
                                   (int(WIDTHD2+zoom*WIDTHD2*(p._st._x-WIDTHD2)/WIDTHD2),
                                    int(HEIGHTD2+zoom*HEIGHTD2*(p._st._y-HEIGHTD2)/HEIGHTD2)),
                                   int(p._r*zoom), 0)
        win.unlock()
        ScanKeyboard()

        # Update all planets' positions and speeds (should normally double
        # buffer the list of planet data, but turns out this is good enough :-)
        for p in g_listOfPlanets:
            if p._merged or p is sun:
                continue
            # Calculate the contributions of all the others to its acceleration
            # (via the gravity force) and update its position and velocity
            p.updatePlanet(t, dt)

        # See if we should merge the ones that are close enough to touch,
        # using elastic collisions (conservation of total momentum)
        for p1 in g_listOfPlanets:
            if p1._merged:
                continue
            for p2 in g_listOfPlanets:
                if p1 is p2 or p2._merged:
                    continue
                if planetsTouch(p1, p2):
                    if p1._m < p2._m:
                        p1, p2 = p2, p1  # p1 is the biggest one (mass-wise)
                    p2._merged = True
                    if p1 is sun:
                        continue  # No-one can move the sun :-)
                    newvx = (p1._st._vx*p1._m+p2._st._vx*p2._m)/(p1._m+p2._m)
                    newvy = (p1._st._vy*p1._m+p2._st._vy*p2._m)/(p1._m+p2._m)
                    p1._m += p2._m  # maintain the mass (just add them)
                    p1.setRadiusFromMass()  # new mass --> new radius
                    p1._st._vx, p1._st._vy = newvx, newvy

        # update zoom factor (numeric keypad +/- keys)
        if keysPressed[pygame.K_KP_PLUS]:
            zoom /= 0.99
        if keysPressed[pygame.K_KP_MINUS]:
            zoom /= 1.01
        if keysPressed[pygame.K_ESCAPE]:
            break        
        if keysPressed[pygame.K_SPACE]:
            while keysPressed[pygame.K_SPACE]:
                ScanKeyboard()
            bClearScreen = not bClearScreen
            verb = "show" if bClearScreen else "hide"
            pygame.display.set_caption(
                'Gravity simulation (SPACE: '
                '%s orbits, keypad +/- : zoom in/out)' % verb)


if __name__ == "__main__":
    try:
        import psyco
        psyco.profile()
    except:
        print('Psyco not found, ignoring it')
