# -*- coding: utf-8 -*-
"""
Created on Sat Aug 19 13:16:37 2023

@author: mens
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


from LaserCAD.non_interactings import Iris, Lambda_Plate

from LaserCAD.freecad_models import clear_doc, setview, freecad_da
from LaserCAD.basic_optics import Mirror, Beam, Composition, inch, Curved_Mirror, Ray, Geom_Object
from LaserCAD.freecad_models.utils import thisfolder, load_STL

if freecad_da:
  clear_doc()

iris = Iris()
iris.draw()
iris.draw_mount()



lam = Lambda_Plate()
lam.pos += (0,40,0)
lam.draw()

lam.draw_mount()


if freecad_da:
  setview()