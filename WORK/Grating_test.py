# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 09:57:01 2024

@author: 12816
"""

import sys
import os
from copy import deepcopy

pfad = __file__
pfad = pfad.replace("\\", "/") #just in case
ind = pfad.rfind("/")
pfad = pfad[0:ind]
ind = pfad.rfind("/")
pfad = pfad[0:ind]
ind = pfad.rfind("/")
pfad = pfad[0:ind+1]
path_added = False
for path in sys.path:
  if path ==pfad:
    path_added = True
if not path_added:
  sys.path.append(pfad)

from LaserCAD.basic_optics import Mirror,Beam,Cylindrical_Mirror,Intersection_plane,Cylindrical_Mirror1,Curved_Mirror,Ray, Composition, Grating
# from LaserCAD.basic_optics.mirror import 
from LaserCAD.basic_optics import Unit_Mount,Composed_Mount
from LaserCAD.non_interactings import Lambda_Plate

from LaserCAD.freecad_models import clear_doc, setview, add_to_composition
from LaserCAD.freecad_models import freecad_da
from LaserCAD.moduls import Make_RoofTop_Mirror
# from basic_optics import Curved_Mirror
# from basic_optics import Ray, Composition, Grating, Lam_Plane
# from basic_optics import Refractive_plane
# from freecad_models import add_to_composition

# from basic_optics.mirror import curved_mirror_test
import matplotlib.pyplot as plt

import numpy as np
# from copy import deepcopy

if freecad_da:
  clear_doc()

number_of_rays = 1
lam_mid = 1030E-6
delta_lamda = 60E-6
Ring_number = 2
Beam_radius = 2
lightsource = Beam(radius=0, angle=0)
wavels = np.linspace(lam_mid-delta_lamda/2, lam_mid+delta_lamda/2, number_of_rays)
rays = []
cmap = plt.cm.gist_rainbow
for wavel in wavels:
  rn = Ray()
  # rn.normal = vec
  # rn.pos = pos0
  rn.wavelength = wavel
  x = 1-(wavel - lam_mid + delta_lamda/2) / delta_lamda
  rn.draw_dict["color"] = cmap( x )
  rg = Beam(radius=Beam_radius, angle=0,wavelength=wavel)
  rg.make_circular_distribution(ring_number=Ring_number)
  for ray_number in range(0,rg._ray_count):
    rn = rg.get_all_rays()[ray_number]
    rn.draw_dict["color"] = cmap( x )
    rays.append(rn)
lightsource.override_rays(rays)
lightsource.draw_dict['model'] = "ray_group"
Grat = Grating(grat_const=1/1480,order=1)
Grat.pos += (100,0,0)
Grat.normal = (np.cos(75/180*np.pi),-np.sin(75/180*np.pi),0)
lightsource2 = Grat.next_beam(lightsource)
lightsource.draw()
Grat.draw()
lightsource2.draw()
ip = Intersection_plane()
ip.pos = lightsource2.length()*lightsource2.normal+lightsource2.pos
ip.normal = lightsource2.normal 
# ip.spot_diagram(lightsource2)
ip.draw()

Grat2 = deepcopy(Grat)
Grat2.pos -= (0,100,0)

B1 = Beam(radius=10, angle=-np.arctan(0.1))
B1._Bwavelength = 1000E-6
B1.pos -= (0,100,0)
B1.make_circular_distribution(ring_number=1)
B2=Grat2.next_beam(B1)
B1.draw()
B2.draw()
Grat2.draw()

print(Grat.matrix(inray=lightsource.get_all_rays()[0]))