# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import time

from black_hole import Black_hole
import constants as c
import functions as f
from shots import *
from spacecraft import Spacecraft

hole = Black_hole(100)

two_player = int(input("Would you play in solo mode or two player mode ?\nSolo mode = 1\nTwo player mode = 2\n"))
if two_player == 1:
    player1, player2 , two_player = f.one_player()
else:
    player1, player2 , two_player = f.two_player()


plt.ion()
hole.event_horizon_display()
c.display_game_zone()

object = [player1, player2]

for i in object:
    i.display()
plt.show(block=False)
input("This is the initial position, press Enter to continue.")

while not player1.loose and not player2.loose:
    plt.clf()
    hole.event_horizon_display()
    c.display_game_zone()




    if two_player:
        if player1.light_shot + player1.heavy_shot == 0 and player2.light_shot + player2.heavy_shot == 0:
            for j in range(4000):
                plt.clf()
                hole.event_horizon_display()
                c.display_game_zone()
                for i in object:
                    i.leapfrog(hole)
                    f.collide(i, object, hole)
                    i.display()
                    i.display_trajectory()
                if j%100==0:
                    plt.show()
                    plt.pause(0.01)
                if player1.loose or player2.loose:
                    break
            break
    else:
        if player1.light_shot + player1.heavy_shot == 0:
            for j in range(4000):
                plt.clf()
                hole.event_horizon_display()
                c.display_game_zone()
                for i in object:
                    i.leapfrog(hole)
                    f.collide(i, object, hole)
                    i.display()
                    i.display_trajectory()
                if j%500==0:
                    plt.show()
                    plt.pause(0.02)
                if player1.loose or player2.loose:
                    break
            break

    for j in range(200):
        for i in object:
            i.leapfrog(hole)
            if i.shooting:
                f.collide(i, object[0:-2], hole)
                if i == object[-1]:
                    f.collide(i, object[1:], hole)
            else:
                f.collide(i, object, hole)
            i.display_trajectory()

    for i in object:
        i.display()

    if player1.loose or player2.loose:
        plt.show(block=False)
        break

    plt.show(block=False)

    if two_player:
        print("Player 1 : ")
        print(player1.__repr__())
        object = f.action(object, player1)
        print("")
        print("Player 2 : ")
        print(player2.__repr__())
        object = f.action(object, player2)
        print("")

    else:
        print(player1.__repr__())
        object = f.action(object, player1)
    
if not two_player:
    if player1.loose or player2.r >= c.GAME_ZONE:
        print("You loose.")
    else:
        print("You win.")
else:
    if (not player1.loose and not player2.loose) or (player1.loose and player2.loose):
        print("There is no winner.")
    elif player1.loose:
        print("Player 2 win.")
    else:
        print("Player 1 win.")
input("Press Enter to quit game.")
