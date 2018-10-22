# -*- coding: utf-8 -*-

import constants as c

import matplotlib.pyplot as plt
import numpy as np

class Black_hole():
    """The black hole"""
    def __init__(self, mass):
        self.mass = mass
        self.g = 1/(2*mass)
        self.rs = 2 * c.G * self.mass * c.M_SOL / c.C**2
        self.eh = np.ones(c.NTHETA)

    def event_horizon_display(self):
        plt.polar(c.THETA_ARRAY, self.eh, 'k')
