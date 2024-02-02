#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 16 19:06:21 2023

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
  
  
from LaserCAD.moduls import Make_Periscope, Make_RoofTop_Mirror
from LaserCAD.basic_optics import Composition, Beam
from LaserCAD.freecad_models.utils import load_STL, freecad_da, setview, clear_doc, thisfolder

if freecad_da:
  clear_doc()

ls = Beam()
comp = Composition()
comp.propagate(300)

peris = Make_Periscope(backwards=True)
rtm = Make_RoofTop_Mirror(up=False)

# comp.add_supcomposition_on_axis(peris)
comp.add_supcomposition_on_axis(rtm)


comp.propagate(300)

comp.draw()


if freecad_da:
  setview()