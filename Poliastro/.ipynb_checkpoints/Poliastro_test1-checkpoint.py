import numpy as np
import matplotlib.pyplot as plt
plt.ion()  # To immediately show plots

from astropy import units as u

from poliastro.bodies import Earth, Mars, Sun
from poliastro.twobody import Orbit

plt.style.use("seaborn")  # Recommended

# Data from Curtis, example 4.3
r = [-6045, -3490, 2500] * u.km
v = [-3.457, 6.618, 2.533] * u.km / u.s

ss = Orbit.from_vectors(Earth, r, v)

from poliastro.plotting import plot
plot(ss)