# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 12:39:47 2024

@author: mens
"""

import sys
pfad = __file__
pfad = pfad.replace("\\","/") #folder conventions windows linux stuff
pfad = pfad.lower()
ind = pfad.rfind("lasercad")
pfad = pfad[0:ind-1]
if not pfad in sys.path:
  sys.path.append(pfad)

from LaserCAD.basic_optics import Geom_Object, Mirror
from LaserCAD.freecad_models import load_STL, pfad, clear_doc, setview, freecad_da

if freecad_da:
  clear_doc()

m = Mirror()
m.pos = (0,0,0)
m.draw()

g = Geom_Object()
g.pos = (0,0,0)
g.freecad_model = load_STL
g.draw_dict["stl_file"] = pfad+ "/misc_meshes/Spartan.stl"
g.draw()


if freecad_da:
  setview()
