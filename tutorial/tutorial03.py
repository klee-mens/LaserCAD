
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 17:38:55 2023

@author: mens
"""

# =============================================================================
# some usefull imports that should be copied to ANY project
# =============================================================================
import numpy as np
import sys
pfad = __file__
pfad = pfad.replace("\\","/") #folder conventions windows linux stuff
pfad = pfad.lower()
ind = pfad.rfind("lasercad")
pfad = pfad[0:ind-1]
if not pfad in sys.path:
  sys.path.append(pfad)

from LaserCAD.basic_optics import Mirror, Component
from LaserCAD.freecad_models import freecad_da, clear_doc, setview


if freecad_da:
  clear_doc()
  
"""
Cosmetics tutorial

For comparision a standard <mir1> is drawn
Note that all essential draw parameters are gathered in the draw_dict.
For the passable arguments study the functions in the "freecad_models" folder

mir2: changed color and thickness

mir3: changed the mount model to something extravagant

seed_laser: example of a component that gets a fancy stl file for rendering

All objects could be easily added to a composition
"""

# =============================================================================
# Playground
# =============================================================================

mir1 = Mirror()
mir1.draw()
print()
print(mir1.draw_dict)


mir2 = Mirror()
mir2.name = "FancyMirror"
mir2.pos += (0,42*2,0)

mir2.aperture = 50
mir2.draw_dict["thickness"] = 8
mir2.draw_dict["color"] = (1.0, 0.0, 1.0)

mir2.draw()


mir3 = Mirror()
mir3.pos += (180, -170, 10)
mir3.normal = (1,2,0)
print()
print(mir3.mount_dict)
# mir3.mount_dict["model"] = thisfolder + "\mount_meshes\special mount\spartan.stl"
mir3.mount_dict["model"] = "\spartan"

mir3.mount.post.elm_type = "dont_draw"
mir3.mount.docking_obj.pos += (-19, -46, -15)

# mir3.mount.dr

mir3.draw()
mir3.draw_mount()

from LaserCAD.freecad_models.utils import load_STL, thisfolder
seed_laser = Component()
stl_file=thisfolder+"\mount_meshes\special mount\Laser_Head-Body.stl"
seed_laser.draw_dict["stl_file"]=stl_file
color = (170/255, 170/255, 127/255)
seed_laser.draw_dict["color"]=color
seed_laser.freecad_model = load_STL
seed_laser.pos = (-100,-100, 90)
seed_laser.draw()

# =============================================================================
# Playground End
# =============================================================================
if freecad_da:
  setview()