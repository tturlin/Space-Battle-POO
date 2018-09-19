# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

from spacecraft import Spacecraft
from black_hole import Black_hole

dist = float(input("Distance to the event horizon , in Rs : "))
angle = float(input("Angle from axis, in rad : "))
vt = float(input("Tangential speed, in percentage of c : "))
vr = float(input("Radial speed, in percentage of c : "))

hole = Black_hole(100)
player = Spacecraft(dist, angle, vr, vt, 'b')
foe = Spacecraft(round(float(np.random.uniform(1, 10)), 3),\
                 player.theta + np.pi, round(float(np.random.rand()), 3),\
                 round(float(np.random.rand()), 3), 'r')


hole.event_horizon_display()
player.display_spacecraft()
foe.display_spacecraft()

plt.show()
