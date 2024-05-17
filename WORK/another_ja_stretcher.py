# -*- coding: utf-8 -*-
"""
Created on Tue May 14 11:13:16 2024

@author: mens
"""


import numpy as np
import sys

pfad = __file__
pfad = pfad.replace("\\","/") #folder conventions windows linux stuff
pfad = pfad.lower()
ind = pfad.rfind("lasercad")
pfad = pfad[0:ind-1]
if not pfad in sys.path:
  sys.path.append(pfad)
  
from LaserCAD.basic_optics import Ray, Grating, Composition, Beam
from LaserCAD.freecad_models import freecad_da, setview, clear_doc

if freecad_da:
  clear_doc()

grating_const = 1/450 # in mm (450 lines per mm)
lambda_mid = 2400e-9 * 1e3 # central wave length in mm

angle_of_incidence = 10 * np.pi/180

seperation = 210

b0 = Beam()
for ray in b0._rays:
  ray.wavelength = lambda_mid

half_comp = Composition(name="Half_Compressor")
half_comp.set_light_source(b0)
half_comp.redefine_optical_axis(b0.inner_ray())
half_comp.propagate(30)

grat1 = Grating(grat_const=grating_const, order=-1)
half_comp.add_on_axis(grat1)

gnormal = np.array( [np.cos(angle_of_incidence), np.sin(angle_of_incidence), 0] )
grat1.normal = gnormal
half_comp.recompute_optical_axis()

half_comp.propagate(seperation)

grat2 = Grating(grat_const=grating_const, order=-1)
half_comp.add_on_axis(grat2)
grat2.normal = - gnormal
half_comp.recompute_optical_axis()

half_comp.propagate(450)

grat3 = Grating(grat_const=grating_const, order=1)
half_comp.add_on_axis(grat3)
grat3.normal = grat2.normal * (-1,1,1)
half_comp.recompute_optical_axis()

half_comp.propagate(seperation)

grat4 = Grating(grat_const=grating_const, order=1)
half_comp.add_on_axis(grat4)
grat4.normal = - grat3.normal
half_comp.recompute_optical_axis()
half_comp.propagate(123)


half_comp.draw()

kbm = half_comp.kostenbauder()
print("Kostenbauer ---------------------------")
print(kbm)

from scipy.constants import speed_of_light as c

lam0 = lambda_mid * 1e-3
d0 = grating_const * 1e-3
beams = half_comp.compute_beams()
b1 = beams[1]
theta = b1.angle_to(grat1)
sep = seperation * 1e-3

GDD = - lam0**3 * sep / (np.pi * c**2 * d0**2 * np.cos(theta)**2) * 1e30
print()
print("GDD analytical", GDD)
print("My GDD: ", kbm[2,3]/2/np.pi*1e30)

if freecad_da:
  setview()