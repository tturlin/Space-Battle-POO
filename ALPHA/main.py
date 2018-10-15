# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import time

from black_hole import Black_hole
import constants as c
import functions as f
from shots import *
from spacecraft import Spacecraft

fire = False

dist = 0
angle = 'q'
vt = 0
vr = 0


while dist <= 1. or dist > c.GAME_ZONE:
    print("")
    try:
        dist = float(input("Distance to the event horizon , in Rs : "))
    except:
        pass

while type(angle) != type(1.):
    try:
        angle = float(input("Angle from axis, in rad : "))
    except:
        pass

while 0. >= abs(vt) or abs(vt) >= 1.:
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
foe = Spacecraft(round(float(np.random.uniform(10, 35)), 3),\
                 player.theta + np.pi, round(float(np.random.uniform(-0.1, 0.1)), 3),\
                 round(float(np.random.choice([-1., 1.])* np.random.normal(0.3, 0.1)), 3), 'r')

object=[player, foe]

hole.event_horizon_display()
c.display_game_zone()

for i in object:
    i.display()
plt.show(block=False)
input()

while not player.loose and not foe.loose:
    plt.clf()
    hole.event_horizon_display()
    c.display_game_zone()

    print(player.__repr__())

    if player.light_shot + player.heavy_shot == 0:
        # If it remain no shots to the player, starting a long leapfrog to see
        # what happen and if any spacecraft win 
        for j in range(4000):
            for i in object:
                i.leapfrog(hole)
                f.collide(i, object, hole)
                i.display_trajectory()
            if j%100==0:
                plt.show(block=False)
                for i in range(10000):
                    i**5
            if player.loose or foe.loose:
                break
        break


    for j in range(200):
        for i in object:
            i.leapfrog(hole)
            if fire:
                f.collide(i, object[0:-2], hole)
                if i == object[-1]:
                    f.collide(i, object[1:], hole)
            else:
                f.collide(i, object, hole)
            i.display_trajectory()

    for i in object:
        i.display()

    if player.loose or foe.loose:
        plt.show(block=False)
        break

    plt.show(block=False)
    object , fire = f.action(object, player)

if player.loose or foe.r >= c.GAME_ZONE:
    print("You loose.")
else:
    print("You win.")
input("Press Enter to quit game.")
