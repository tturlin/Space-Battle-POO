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
