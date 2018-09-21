# -*- coding: utf-8 -*-

from shots import *
from spacecraft import Spacecraft

def action(object, spacecraft):
    if type(object[-1]) == Light_shot or type(object[-1]) == Heavy_shot:
        object[-1].collide_sphere = 0.01
    act = input("What do you wanna do this turn : Wait, Light shot, Heavy shot ? ")
    fire = False
    if act == "Light shot":
        if spacecraft.light_shot:
            phi = float(input("Which direction would you give to the shot, in [0, 2pi[ ? "))
            shot = Light_shot(phi, spacecraft)
            spacecraft.light_shot -= 1
            fire = True
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
            fire = True
            spacecraft.shooting = True
        else:
            print("It dont remain to you any Heavy shot.")
            action(object, spacecraft)
    else:
        pass
    return object, fire

def collide(actual,objects, hole):
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
