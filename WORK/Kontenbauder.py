# -*- coding: utf-8 -*-
"""
Created on Thu May 23 12:37:58 2024

@author: 12816
"""

import sys
# import os

pfad = __file__
pfad = pfad.replace("\\","/") #folder conventions windows linux stuff
pfad = pfad.lower()
ind = pfad.rfind("lasercad")
pfad = pfad[0:ind-1]
if not pfad in sys.path:
  sys.path.append(pfad)
from copy import deepcopy

from LaserCAD.basic_optics import Mirror,Beam,Cylindrical_Mirror,Grating,Ray
from LaserCAD.basic_optics import Intersection_plane,Cylindrical_Mirror1
from LaserCAD.basic_optics import Curved_Mirror, Composition,Lens

from LaserCAD.basic_optics import Unit_Mount,Composed_Mount, Crystal
from LaserCAD.non_interactings import Pockels_Cell
from LaserCAD.non_interactings import Lambda_Plate

from LaserCAD.freecad_models import clear_doc, setview, add_to_composition
from LaserCAD.freecad_models import freecad_da
from LaserCAD.moduls import Make_RoofTop_Mirror, Make_Telescope
from LaserCAD.moduls.periscope import Rooftop_Mirror_Component

import matplotlib.pyplot as plt
import numpy as np

if freecad_da:
  clear_doc()

# A = Make_Telescope()
# kostenbauder_matrix=(A.Kostenbauder_matrix())


# print(kostenbauder_matrix)

# C1 = Composition()
# C1.propagate(123)
# print(C1.Kostenbauder_matrix())

# Comp=Composition()
# Comp.set_light_source(Beam())
# Comp.propagate(100)
# a= Lens(f=500)
# Comp.add_on_axis(a)
# # a.normal = (-1,1,0)
# Comp.propagate(250)
# print(Comp.Kostenbauder_matrix())

# # Comp1=Composition()
# # Comp1.propagate(100)
# # Comp1.propagate(100)
# # print(Comp1.Kostenbauder_matrix())

Comp2=Composition()
Comp2.propagate(50)
Comp2.propagate(50)
Comp2.add_on_axis(Curved_Mirror(radius=1000))
Comp2.propagate(125)
# Comp2.add_on_axis(Mirror(phi=90))
Comp2.propagate(125)
print(Comp2.Kostenbauder_matrix())
# Comp2.draw()
# A.draw()

# Com = Composition()
# Com.pos += (0,10,10)
# Com.add_fixed_elm(Comp._elements[0])
# Com.recompute_optical_axis()
# Com.propagate(250)
# print(Com.Kostenbauder_matrix())
# Com.draw()