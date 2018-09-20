# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

from spacecraft import Spacecraft
from black_hole import Black_hole

dist = 0
angle = 'q'
vt = 0
vr = 0

while dist <= 1. or dist > 20.:
    try:
        dist = float(input("Distance to the event horizon , in Rs : "))
    except:
        pass

while type(angle) != type(1.):
    try:
        angle = float(input("Angle from axis, in rad : "))
    except:
        pass

while 0. >= vt or vt >= 1.:
    try:
        vt = float(input("Tangential speed, in percentage of c : "))
    except:
        pass

while 0. >= vr or vr >= 1.:
    try:
        vr = float(input("Radial speed, in percentage of c : "))
    except:
        pass


hole = Black_hole(100)
player = Spacecraft(dist, angle, vr, vt, 'b')
foe = Spacecraft(round(float(np.random.uniform(1, 15)), 3),\
                 player.theta + np.pi, round(float(np.random.rand()), 3),\
                 round(float(np.random.rand()), 3), 'r')


while not player.loose and not foe.loose:
    player.display_spacecraft()
    hole.event_horizon_display()
    foe.display_spacecraft()

    player.leapfrog(hole)
    foe.leapfrog(hole)
    player.display_trajectory()
    foe.display_trajectory()
    plt.show()

if player.loose:
    print("you loose")
else:
    print("you win")
