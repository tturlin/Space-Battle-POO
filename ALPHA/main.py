# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

from black_hole import Black_hole
import constants as c
from shots import *
from spacecraft import Spacecraft


def action(object, spacecraft):
    act = input("What do you wanna do this turn : Wait, Shot, Heavy shot ? ")

    if act == "Shot":
        if spacecraft.shot:
            phi = float(input("Which direction would you give to the shot, in [0, 2pi[ ? "))
            shot = Shot(phi, spacecraft)
            spacecraft.shot -= 1
            object.append(shot)
        else:
            print("It dont remain to you any light shot.")
            action(object, spacecraft)
    elif act == "Heavy shot":
        if spacecraft.heavy_shot:
            phi = float(input("Which direction would you give to the shot, in [0, 2pi[ ? "))
            hshot = Heavy_shot(phi, spacecraft)
            spacecraft.heavy_shot -= 1
            object.append(hshot)
        else:
            print("It dont remain to you any Heavy shot.")
            action(object, spacecraft)
    else:
        pass
    return object

dist = 0
angle = 'q'
vt = 0
vr = 0


while dist <= 1. or dist > c.GAME_ZONE:
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
foe = Spacecraft(round(float(np.random.uniform(5, 15)), 3),\
                 player.theta + np.pi, round(float(np.random.uniform(0, 0.1)), 3),\
                 round(float(np.random.rand()), 3), 'r')

object=[player, foe]

hole.event_horizon_display()
c.display_game_zone()

for i in object:
    i.display()
plt.show(block=False)
input()

while not player.loose and not foe.loose:
    for j in range(200):
        for i in object:
            i.leapfrog(hole)
            i.display_trajectory()

    for i in object:
        i.display()

    plt.show(block=False)
    object = action(object, player)

if player.loose:
    print("you loose")
else:
    print("you win")
