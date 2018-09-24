# -*- coding: utf-8 -*-

import constants as c

import matplotlib.pyplot as plt
import numpy as np

class Heavy_shot():
    """Gestion des missiles lourds"""
    def __init__(self, phi, spacecraft):
        self.r = spacecraft.r
        v=0.1
        self.theta =spacecraft.theta
        self.vr = spacecraft.vr + v * np.sin(2*np.pi - phi)
        self.vt = spacecraft.vt + v * np.cos(2*np.pi - phi)
        self.collide_sphere = 0.
        self.l0 = self.r * self.vt
        self.loose = False
        self.color = 'k'
        self.mass = 500 #kg
        self.om = np.array([[self.r], [self.theta]])
        self.v = np.array([[self.vr], [self.vt]])
        self.trajplot = np.zeros((1, 2), dtype=float)
        self.trajplot[0, 0] = self.theta
        self.trajplot[0, 1] = self.r
        self.shooting = False

    def __repr__(self):
        pass

    def display(self):
        plt.polar(self.theta, self.r, '+', c=self.color, markersize=5)

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
        plt.polar(self.trajplot[:,0], self.trajplot[:,1], c=self.color, linestyle = '-', linewidth=0.25)

    def stop_condition(self):
        if self.r <= 1. or self.r > c.GAME_ZONE:
            self.loose = True


class Light_shot():
    """Gestion des missiles leger"""
    def __init__(self, phi, spacecraft):
        self.r = spacecraft.r
        v=0.3
        self.theta =spacecraft.theta
        self.vr = spacecraft.vr + v * np.sin(2*np.pi - phi)
        self.vt = spacecraft.vt + v * np.cos(2*np.pi - phi)
        self.collide_sphere = 0.
        self.l0 = self.r * self.vt
        self.loose = False
        self.color = 'g'
        self.om = np.array([[self.r], [self.theta]])
        self.v = np.array([[self.vr], [self.vt]])
        self.trajplot = np.zeros((1, 2), dtype=float)
        self.trajplot[0, 0] = self.theta
        self.trajplot[0, 1] = self.r
        self.shooting = False

    def display(self):
        plt.polar(self.theta, self.r, '+', c=self.color, markersize=5)

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
        plt.polar(self.trajplot[:,0], self.trajplot[:,1], c=self.color, linestyle = '-', linewidth=0.25)

    def stop_condition(self):
        if self.r <= 1. or self.r > c.GAME_ZONE:
            self.loose = True
