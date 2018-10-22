# -*- coding: utf-8 -*-

from shots import *
from spacecraft import Spacecraft


def collide(actual,objects, hole):
    """Colliding algorithm"""
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



def recoil(spacecraft, heavy_shot):
    """Calculate the recoil of the spacecraft when launching an heavy shot"""
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
