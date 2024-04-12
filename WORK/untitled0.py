# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 13:40:20 2024

@author: 12816
"""

import sys
import os

pfad = __file__
pfad = pfad.replace("\\","/") #folder conventions windows linux stuff
pfad = pfad.lower()
ind = pfad.rfind("lasercad")
pfad = pfad[0:ind-1]
if not pfad in sys.path:
  sys.path.append(pfad)

from LaserCAD.basic_optics import Mirror,Beam,Cylindrical_Mirror,Intersection_plane,Cylindrical_Mirror1,Curved_Mirror,Ray, Composition, Grating
# from LaserCAD.basic_optics.mirror import 
from LaserCAD.basic_optics import Unit_Mount,Composed_Mount, Crystal
from LaserCAD.non_interactings import Faraday_Isolator, Pockels_Cell, Lambda_Plate

from LaserCAD.freecad_models import clear_doc, setview, add_to_composition
from LaserCAD.freecad_models import freecad_da
from LaserCAD.moduls import Make_RoofTop_Mirror, Make_Periscope
# from basic_optics import Curved_Mirror
# from basic_optics import Ray, Composition, Grating, Lam_Plane
# from basic_optics import Refractive_plane
# from freecad_models import add_to_composition
from LaserCAD.moduls.periscope import Rooftop_Mirror_Component

# from basic_optics.mirror import curved_mirror_test
import matplotlib.pyplot as plt

import numpy as np
# from copy import deepcopy

if freecad_da:
  clear_doc()

focal_length = 150
Comp = Composition()
Comp.set_light_source(Beam())
Comp.propagate(50)
M1 = Mirror(phi=90)
Comp.add_on_axis(M1)
CM1 = Cylindrical_Mirror(theta=5,radius=focal_length*2)
Comp.propagate(focal_length*3)
Comp.add_on_axis(CM1)
Comp.propagate(focal_length*2)
Comp.recompute_optical_axis()
CM2 = Cylindrical_Mirror(radius=focal_length*2)
CM2.set_geom(Comp.last_geom())
Comp.add_on_axis(CM2)
CM2.normal = -CM1.normal
Comp.recompute_optical_axis()
Comp.propagate(50)
Comp.draw()