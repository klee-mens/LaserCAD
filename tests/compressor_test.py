# -*- coding: utf-8 -*-
"""
Created on Thu Mar 20 10:07:25 2025

@author: mens
"""

# from LaserCAD.moduls import Make_Compressor

from LaserCAD.moduls import Make_Compressor
from LaserCAD.freecad_models import freecad_da, clear_doc, setview
import numpy as np

if freecad_da:
  clear_doc()

comp = Make_Compressor(separation_angle = 20 /180 *np.pi, # sep between in and outgoing middle ray
    grating_const = 1/1000, # in 1/mm
    separation = 200, # difference grating position und radius_concave
    lambda_mid = 800e-9 * 1e3, # central wave length in mm
    bandwidth = 100e-9*1e3, # full bandwidth in mm
    number_of_rays = 20,
    height_separation = 16, # separation between incomming and outgoing beam,
    first_propagation = 120, # legnth of the first ray_bundle to grating 1 mm
    distance_roof_top_grating = 600,
    grating1_dimensions = (25, 25, 5),
    grating2_dimensions = (50, 50, 5))

comp.draw()

print("Compressor GDD:", np.round(comp.GDD * 1e30), "fs^2")
print("Compressor TOD:", np.round(comp.TOD * 1e45), "fs^3")

if freecad_da:
  setview()
