# -*- coding: utf-8 -*-

import constants as c

import matplotlib.pyplot as plt

class Spacecraft():
    """Class used to describe all spacecrafts around the black hole."""
    def __init__(self,r ,theta, vr, vt, color):
        self.r = r
        self.theta = theta
        self.vr = vr
        self.vt = vt
        self.color = color
        self.collide_sphere = 0.1
        self.l0 = self.r * self.vt

    def display_spacecraft(self):
        plt.polar(self.theta, self.r, '+', c=self.color)

    def acceleration(self, black_hole):
        self.ar = - (c.G * black_hole.mass * c.M_SOL)/(self.r**2 * black_hole.rs)\
                +(self.r * black_hole.rs - 3/2*black_hole.rs)*(self.l0**2/(self.r**4 * black_hole.rs**4))
