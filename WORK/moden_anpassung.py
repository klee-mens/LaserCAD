# -*- coding: utf-8 -*-
"""
Created on Fri Jul 26 13:08:23 2024

@author: mens
"""

from chromeo_sketch import Seed, Stretcher, PulsePicker, Amplifier_I
from sympy import solve, symbols, Matrix
import numpy as np

amplifier_lengths = [r.length for r in Amplifier_I._optical_axis]
#
target_radius = 1.408 # see nextcloud\coding\regen-amp-calc\note_3p_10mm_klt_pump.py

lengs_ater_amp_cm = amplifier_lengths[5:-1]
# s2 = np.sum(lengs_ater_amp_cm)

s1 = lengs_ater_amp_cm[0]
s2 = np.sum(amplifier_lengths)/2 - s1
R = 5000 # see chromeo_sketch
x = symbols('x')

def propMat(s):
  mat = np.eye(2)
  mat[0,1] = s
  return mat

def CmMat(R):
  mat = np.eye(2)
  mat[1,0] = -2/R
  return mat



ResonMat = propMat(s2) @ CmMat(R) @ propMat(s2) @ propMat(s1) @ CmMat(R) @ propMat(s1)

[[a,b], [c,d]] = ResonMat

zt = (d-a)/ 2/ c #z target
zrt = abs( np.sqrt((4 - (d+a)**2)) / (2*c) ) # rayleigh target

a, b, f, z1, zr1 = symbols("a b f z1 zr1")
A,B,C,D, q1, q2 = symbols("A B C D, q1, q2")

system_matrix = Seed.matrix() @ Stretcher.matrix() @ PulsePicker.matrix()

#approx: only B
prop = system_matrix[0,1]


equ1 = (A*q1 + B)
