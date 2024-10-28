# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 00:08:36 2024

@author: mens
"""

import numpy as np
import sys

pfad = __file__
pfad = pfad.replace("\\","/") #folder conventions windows linux stuff
pfad = pfad.lower()
ind = pfad.rfind("lasercad")
pfad = pfad[0:ind-1]
if not pfad in sys.path:
  sys.path.append(pfad)

from LaserCAD.basic_optics import Geom_Object, Ray, Beam, Curved_Mirror, Composed_Mount, Unit_Mount
from LaserCAD.freecad_models import freecad_da, setview, clear_doc


if freecad_da:
  clear_doc()

g = Geom_Object()
# g.draw()

r = Ray()
# r.draw()

b = Beam(angle=0.005)
# b.draw()

cm = Curved_Mirror(radius=50)
# cm.draw()

um = Unit_Mount(model="POLARIS-K1")
# um.draw()

cpm = cm.Mount
# cpm.draw()

if freecad_da:
  setview()