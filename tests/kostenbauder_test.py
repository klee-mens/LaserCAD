# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 13:42:19 2024

@author: mens
"""

import sys
pfad = __file__
pfad = pfad.replace("\\","/") #folder conventions windows linux stuff
pfad = pfad.lower()
ind = pfad.rfind("lasercad")
pfad = pfad[0:ind-1]
if not pfad in sys.path:
  sys.path.append(pfad)
  

from LaserCAD.basic_optics import Grating, Ray
import numpy as np

r0 = Ray()
r0.wavelength = 2400e-6 # in mm
r0.normal = (0,-1,0)
r0.pos += -r0.normal *50 

grat = Grating()
grat.grating_constant = 1/450 # in mm
grat.normal = [ 0.46676, -0.88438,  0.     ]
grat.diffraction_order = 1

r1 = grat.next_ray(r0)

r0.draw()
grat.draw()
r1.draw()

print()
print("AOI:", r0.angle_to(grat) * 180/np.pi)
print("AO0:", r1.angle_to(grat) * 180/np.pi)
print()
print(grat.kostenbauder(r0))
