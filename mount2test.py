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


# from LaserCAD.non_interactings import Iris
# from LaserCAD.non_interactings import Lambda_Plate

from LaserCAD.freecad_models import clear_doc, setview, freecad_da
from LaserCAD.basic_optics import Mirror,Crystal
from LaserCAD.basic_optics import Beam,Grating, Composition, inch, Curved_Mirror, Ray, Geom_Object, LinearResonator, Lens, Component
from LaserCAD.freecad_models.utils import thisfolder, load_STL
from LaserCAD.basic_optics.mount2 import Unit_Mount
from LaserCAD.basic_optics.mount2 import MIRROR_LIST,LENS_LIST

if freecad_da:
  clear_doc()

mir = Lens()
mir.aperture = 2*inch
mir.set_mount_to_default()
mir.draw()
mir.Mount.draw()

# M = Unit_Mount(model="KS2")
# M.draw()

# mir2 = Lens()
# mir2.set_geom(M.docking_obj.get_geom())
# mir2.draw()

if freecad_da:
  setview()