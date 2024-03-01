# -*- coding: utf-8 -*-
"""
Created on Thu Feb 29 12:56:24 2024

@author: marti
"""

import numpy as np
import sys

pfad = __file__
pfad = pfad.replace("\\","/") #folder conventions windows linux stuff
ind = pfad.rfind("/")
pfad = pfad[0:ind-1]
ind = pfad.rfind("/")
pfad = pfad[0:ind]
if not pfad in sys.path:
  sys.path.append(pfad)


from LaserCAD.freecad_models import clear_doc, setview, freecad_da,add_to_composition
from LaserCAD.basic_optics import Mirror, Beam, Composition, Component, inch, Curved_Mirror, Ray, Geom_Object, Unit_Mount
from LaserCAD.basic_optics import Grating, Opt_Element
import matplotlib.pyplot as plt
from LaserCAD.freecad_models.utils import thisfolder, load_STL
from LaserCAD.non_interactings import Faraday_Isolator, Pockels_Cell, Lambda_Plate
from LaserCAD.basic_optics import Composed_Mount,Unit_Mount,Lens
from copy import deepcopy

if freecad_da:
  clear_doc()
  
sep = 28.3
theta = 45*np.pi/180
L = 80.3
start_length = 14.496

Housing = Component()
stl_file=thisfolder+"mount_meshes\special_mount\Polarization_rotator-Fusion.stl"
Housing.draw_dict["stl_file"]=stl_file
Housing.draw_dict["color"]=(239/255, 239/255, 239/255)
# self.draw_dict["color"]=(100/255, 100/255, 100/255)
Housing.freecad_model = load_STL

M1 = Mirror()
M1.set_mount(Unit_Mount())
M2 = Mirror()
M2.set_mount(Unit_Mount())
M3 = Mirror()
M3.set_mount(Unit_Mount())
M2.pos += (start_length + sep/2, L*np.cos(theta), L*np.sin(theta))
M3.pos += (start_length + sep,0,0)
Pol_Rotater = Composition(name="Polarisationsdreher")
Pol_Rotater.add_on_axis(Housing)
Pol_Rotater.propagate(start_length)
Pol_Rotater.add_on_axis(M1)
M1.set_normal_with_2_points(Pol_Rotater.pos-(1,0,0), M2.pos)
Pol_Rotater.add_fixed_elm(M2)
M2.set_normal_with_2_points(M1.pos, M3.pos)
Pol_Rotater.add_fixed_elm(M3)
M3.set_normal_with_2_points(M2.pos, M3.pos + (1,0,0))
Pol_Rotater.propagate(start_length)
Pol_Rotater.draw()

# .add_supcomposition_on_axis