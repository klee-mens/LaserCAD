# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 10:53:52 2023

@author: 12816
"""

import sys
pfad = __file__
pfad = pfad.replace("\\","/") #folder conventions windows linux stuff
pfad = pfad.lower()
ind = pfad.rfind("lasercad")
pfad = pfad[0:ind-1]
if not pfad in sys.path:
  sys.path.append(pfad)

from LaserCAD.moduls import Make_Periscope
from LaserCAD.basic_optics import Composition
from LaserCAD.freecad_models import freecad_da, setview, clear_doc

if freecad_da:
  clear_doc()

if __name__ == "__main__":
  comp = Composition()
  comp.propagate(200)
  peris = Make_Periscope()
  comp.add_supcomposition_on_axis(peris)
  comp.propagate(200)
  comp.draw()

if freecad_da:
  setview()