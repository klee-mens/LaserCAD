# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 12:39:52 2024

@author: 12816
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
from LaserCAD.basic_optics import Mirror, Beam, Composition, Component, inch, Curved_Mirror, Ray, Geom_Object
from LaserCAD.basic_optics import Grating, Opt_Element
import matplotlib.pyplot as plt
from LaserCAD.freecad_models.utils import thisfolder, load_STL
from LaserCAD.non_interactings import Faraday_Isolator, Pockels_Cell, Lambda_Plate
from LaserCAD.basic_optics import Composed_Mount,Unit_Mount,Lens
from copy import deepcopy

if freecad_da:
  clear_doc()
  
def dont():
    return None

focal_length = 125

beam = Beam(radius=1,angle=0)
Comp = Composition()
Comp.set_light_source(beam)
Comp.pos -= (205,0,-20)

Laser_Head_in = Component()
stl_file = thisfolder+"\misc_meshes\PM19_2.stl"
Laser_Head_in.draw_dict["stl_file"]=stl_file
Laser_Head_in.freecad_model = load_STL

Laser_Head_out = Component()
stl_file = thisfolder+"\misc_meshes\PM19_2.stl"
Laser_Head_out.draw_dict["stl_file"]=stl_file
Laser_Head_out.freecad_model = load_STL

lens1 = Lens(f=focal_length)
lens1.aperture = 25.4*2
lens1.set_mount_to_default()
lens2 = Lens(f=focal_length)
lens2.aperture = 25.4*2
lens2.set_mount_to_default()
lens3 = deepcopy(lens2)
lens4 = deepcopy(lens1)

M1 = Mirror(phi=-90)
M1.aperture = 25.4*3
M1.set_mount_to_default()
M2 = deepcopy(M1)

Comp.add_on_axis(Laser_Head_in)
Comp.propagate(75)
Comp.add_on_axis(lens1)
Comp.propagate(310)
Comp.add_on_axis(lens2)
Comp.propagate(50)
Comp.add_on_axis(M1)
Comp.propagate(250)
Comp.add_on_axis(M2)
Comp.propagate(50)
Comp.add_on_axis(lens3)
Comp.propagate(310)
Comp.add_on_axis(lens4)
Comp.propagate(75)
Comp.add_on_axis(Laser_Head_out)
Laser_Head_out.normal = -Laser_Head_out.normal

Comp.draw()