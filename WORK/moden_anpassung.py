# -*- coding: utf-8 -*-
"""
Created on Fri Jul 26 13:08:23 2024

@author: mens
"""

# from chromeo_sketch import Seed, Stretcher, PulsePicker, Amplifier_I
from sympy import solve, symbols, Matrix
import numpy as np

# amplifier_lengths = [r.length for r in Amplifier_I._optical_axis]
#
target_radius = 1.408 # see nextcloud\coding\regen-amp-calc\note_3p_10mm_klt_pump.py

# lengs_ater_amp_cm = amplifier_lengths[5:-1]
# s2 = np.sum(lengs_ater_amp_cm)

# s1 = lengs_ater_amp_cm[0]

x = symbols('x')

