# -*- coding: utf-8 -*-
"""
Created on Thu May 23 12:37:58 2024

@author: 12816
"""

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

Comp=Composition()
Comp.set_light_source(Beam())
Comp.propagate(100)
Comp.add_on_axis(Lens(f=500))
Comp.propagate(250)
print(Comp.Kostenbauder_matrix())

# Comp1=Composition()
# Comp1.propagate(100)
# Comp1.propagate(100)
# print(Comp1.Kostenbauder_matrix())

Comp1=Composition()
Comp1.propagate(100)
Comp1.add_on_axis(Curved_Mirror(radius=1000))
Comp1.propagate(250)
print(Comp1.Kostenbauder_matrix())
# A.draw()