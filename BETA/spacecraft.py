# -*- coding: utf-8 -*-

import constants as c

import matplotlib.pyplot as plt
import numpy as np

class Spacecraft():
    """Class used to describe all spacecrafts around the black hole."""
    def __init__(self,r ,theta, vr, vt, color):
        self.r = r
        self.theta = theta
        self.vr = vr
        self.vt = vt
        self.color = color
        self.collide_sphere = 1.
        self.l0 = self.r * self.vt
        self.loose = False
        self.heavy_shot = 3
        self.light_shot = 3
        self.mass = 1e6 #kg
        self.om = np.array([[self.r], [self.theta]])
        self.v = np.array([[self.vr], [self.vt]])
        self.trajplot = np.zeros((1, 2), dtype=float)
        self.trajplot[0, 0] = self.theta
        self.trajplot[0, 1] = self.r
        self.shooting = False

    def __repr__(self):
        return """Your position is {0}Rs, {1}rad.
Your tangential speed is {2}c.
Your radial speed is {3}c.
Heavy shot(s) remaining : {4}
Light shot(s) remaining : {5}""".format(self.r, self.theta, self.vt,
                                                self.vr, self.heavy_shot,
                                                self.light_shot)

    def display(self):
        plt.polar(self.theta, self.r, '*', c=self.color, markersize=5)

    def acceleration(self, r,  black_hole):
        self.ar = - (black_hole.g * black_hole.mass)/(self.r**2) + (self.r - 3/2)*(self.l0**2/(self.r**4))

    def leapfrog(self, black_hole):
        traj = np.zeros((c.LEN_INTEGRATION, 2), dtype=float)
        velocity = np.zeros((c.LEN_INTEGRATION, 2), dtype=float)

        traj[0, 0] = self.theta
        traj[0, 1] = self.r


        velocity[0, 0] = self.vt
        velocity[1, 1] = self.vr

        for i in range(1,c.LEN_INTEGRATION-1):
            traj[i, 1] = traj[i-1, 1] + velocity[i, 1] * c.DT
            self.acceleration(traj[i, 1],black_hole)
            velocity[i+1, 1] = float(velocity[i, 1]) + self.ar * c.DT
            self.r =  float(traj[i, 1])
            self.vr = velocity[i, 1]

            velocity[i, 0] = self.l0 / traj[i-1, 1]**2
            traj[i, 0] = traj[i-1, 0] + velocity[i, 0] * c.DT
            self.theta = float(traj[i, 0])
            self.vt = velocity[i, 0]

            if i%100 == 0:
                self.trajplot = np.append(self.trajplot, [traj[i,:]], axis=0)

            self.stop_condition()
            if self.loose:
                break


    def display_trajectory(self):
        plt.polar(self.trajplot[:,0], self.trajplot[:,1], c=self.color, linestyle = '', marker = ',' )

    def stop_condition(self):
        if self.r <= 1.:
            self.loose = True
