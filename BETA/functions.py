# -*- coding: utf-8 -*-

from shots import *
from spacecraft import Spacecraft

def action(object, spacecraft):
    """Managing actions of players, that is waiting, light shot launching and
    heavy shot launching."""
    if type(object[-2]) == Light_shot or type(object[-2]) == Heavy_shot:
        object[-2].collide_sphere = 1
    act = input("What do you wanna do this turn : Wait, Light shot, Heavy shot ? ")
    spacecraft.shooting = False
    if act == "Light shot":
        if spacecraft.light_shot:
            phi = float(input("Which direction would you give to the shot, in [0, 2pi[ ? "))
            shot = Light_shot(phi, spacecraft)
            spacecraft.light_shot -= 1
            object.append(shot)
            spacecraft.shooting = True
        else:
            print("It dont remain to you any light shot.")
            action(object, spacecraft)
    elif act == "Heavy shot":
        if spacecraft.heavy_shot:
            phi = float(input("Which direction would you give to the shot, in [0, 2pi[ ? "))
            hshot = Heavy_shot(phi, spacecraft)
            spacecraft.heavy_shot -= 1
            object.append(hshot)
            spacecraft.shooting = True
            recoil(spacecraft, hshot)
        else:
            print("It dont remain to you any Heavy shot.")
            action(object, spacecraft)
    else:
        spacecraft.shooting = False
        pass
    return object

def collide(actual,objects, hole):
    """Collision algorithm"""
    for i in objects:
        if i != actual:# and (not i.loose and not actual.loose):
            dist = np.sqrt(i.r**2 + actual.r**2 - 2*i.r*actual.r*np.cos(abs(i.theta - actual.theta)))
            if i.collide_sphere != 0. and actual.collide_sphere !=0.:
                if dist <= (i.collide_sphere + actual.collide_sphere):
                    if type(i) == Light_shot or type(actual) == Light_shot or (type(i) == Spacecraft and type(actual) == Spacecraft):
                        i.loose = True
                        actual.loose = True
                    else:
                        print("Collide")
                        print(i.om)
                        print(i.v)

                        # collide for i
                        scali = np.vdot((i.v-actual.v),(i.om - actual.om))
                        scalx = np.vdot((i.om - actual.om),(i.om - actual.om))
                        i.v -= (2*actual.mass/(i.mass + actual.mass))*((scali/scalx))*(i.om-actual.om)
                        i.vr = float(i.v[0])
                        i.vt = float(i.v[1])

                        # collide for actual
                        scali = np.vdot((actual.v-i.v),(actual.om - i.om))
                        scalx = np.vdot((actual.om - i.om),(actual.om - i.om))
                        actual.v -= (2*i.mass/(actual.mass + i.mass))*((scali/scalx))*(actual.om-i.om)
                        actual.vr = float(actual.v[0])
                        actual.vt = float(actual.v[1])

                        i.leapfrog(hole)
                        actual.leapfrog(hole)
        for i in objects:
            if i.loose:
                objects.remove(i)


def one_player():
    """One player mode initialization."""
    two_player = False
    dist = 0
    angle = 'q'
    vt = 0
    vr = 0


    print("The game zone is between 1Rs and ", c.GAME_ZONE,"RS.")
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


    player = Spacecraft(dist, angle, vr, vt, 'b')
    foe = Spacecraft(round(float(np.random.uniform(10, 35)), 3),\
                     player.theta + np.pi, round(float(np.random.uniform(-0.1, 0.1)), 3),\
                     round(float(np.random.choice([-1., 1.])* np.random.normal(0.3, 0.1)), 3), 'r')

    return player, foe, two_player


def two_player():
    """Two player mode initialization"""
    two_player = True
    dist = 0
    angle = 'q'
    vt = 0
    vr = 0

    print("Player 1 : ")
    print("The game zone is between 1Rs and ", c.GAME_ZONE,"RS.")
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

    player1 = Spacecraft(dist, angle, vr, vt, 'b')


    dist = 0
    vt = 0
    vr = 0

    print("Player 2 : ")
    print("The game zone is between 1Rs and ", c.GAME_ZONE,"RS.")
    while dist <= 1. or dist > c.GAME_ZONE:
        try:
            dist = float(input("Distance to the event horizon , in Rs : "))
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

    player2 = Spacecraft(dist, angle + np.pi, vr, vt, 'r')
    return player1, player2, two_player


def recoil(spacecraft, heavy_shot):
    """Calculation of the spacecraft recoil when lauching a heavy shot"""
    spacecraft.v = np.array([spacecraft.vt, spacecraft.vr])
    heavy_shot.v = np.array([heavy_shot.vt, heavy_shot.vr])
    spacecraft.v -= spacecraft.v*np.log(spacecraft.mass/(spacecraft.mass - heavy_shot.mass))
    spacecraft.mass -= heavy_shot.mass
    spacecraft.vt = spacecraft.v[0]
    spacecraft.vr = spacecraft.v[1]

def zone_verification(object, hole):
    """Verify if object is in the game, with a periodical limit condition return"""
    for i in object:
        if i.r >= c.GAME_ZONE:
            i.theta = i.theta + np.pi
            i.vr = -i.vr
            i.vt = -i.vt
            i.trajplot = np.zeros((1, 2), dtype=float)
            i.trajplot[0, 0] = i.theta
            i.trajplot[0, 1] = i.r

def zone_verification_vlib(object, hole):
    """Verification of the spacecraft's speed and compare it with the liberation
    speed of the black hole when spacecraft is a the limit of the game zone"""
    for i in object:
        vlib = np.sqrt((2*hole.g*hole.mass)/i.r)
        v = np.sqrt(np.vdot([[i.vr], [i.vt]],[[i.vr], [i.vt]]))
        if v < vlib and i.r > c.GAME_ZONE and type(i) == Spacecraft:
            many = 0
            while i.r > c.GAME_ZONE or many < (c.LEN_VLIB + 1):
                i.leapfrog(hole)
                many += 1
            if many == c.LEN_VLIB:
                i.etat = False
            for j in object:
                if j != i:
                    for k in range(many+1):
                        j.leapfrog(hole)
        elif v >= vlib and i.r > c.GAME_ZONE:
            i.loose = True
