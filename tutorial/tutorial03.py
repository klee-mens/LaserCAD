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

from LaserCAD.basic_optics import Mirror
from LaserCAD.freecad_models import freecad_da, clear_doc, setview


if freecad_da:
  clear_doc()
  
"""
Cosmetics tutorial
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
mir3.mount.docking_obj.pos += (-19, -46, -15)
# mir3.mount.dr

mir3.draw()
mir3.draw_mount()

# =============================================================================
# Playground End
# =============================================================================
if freecad_da:
  setview()