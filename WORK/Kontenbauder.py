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
from LaserCAD.basic_optics import Curved_Mirror, Composition

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

A = Make_Telescope()
point=(A.Kostenbauder_matrix())
print(point)
for i in point:
  M = Mirror()
  M.pos = i
  M.draw()
A.draw()