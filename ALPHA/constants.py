# -*- coding: utf-8 -*-

import numpy as np


C = 1

M_SOL = 1.988e30 # unit kg

G = 6.67e-11 # unit m3/kg/s2

DTHETA = 1 / 100

NTHETA = int(2 * np.pi / DTHETA)

THETA_ARRAY = np.linspace(0, 2*np.pi, NTHETA, dtype=float)
