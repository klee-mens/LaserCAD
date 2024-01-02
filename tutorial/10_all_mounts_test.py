# -*- coding: utf-8 -*-
"""
Created on Sat Aug 19 13:16:37 2023

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


# from LaserCAD.non_interactings import Iris
# from LaserCAD.non_interactings import Lambda_Plate

from LaserCAD.freecad_models import clear_doc, setview, freecad_da
from LaserCAD.basic_optics import Mirror,Crystal
from LaserCAD.basic_optics import Beam,Grating, Composition, inch, Curved_Mirror, Ray, Geom_Object, LinearResonator, Lens, Component
from LaserCAD.freecad_models.utils import thisfolder, load_STL
from LaserCAD.basic_optics.mount2 import Unit_Mount,Post, Composed_Mount
from LaserCAD.basic_optics.mount2 import MIRROR_LIST,LENS_LIST

if freecad_da:
  clear_doc()
  
for i in range(len(MIRROR_LIST)):
  M = Composed_Mount(unit_model_list=[MIRROR_LIST[i],"1inch_post"])
  aperture = M.mount_list[0].aperture
  mir= Mirror()
  mir.aperture = aperture
  mir.Mount = M
  mir.pos = (i*50,0,50+i*10)
  mir.draw()
  mir.Mount.draw()
  
for i in range(len(LENS_LIST)):
  M = Composed_Mount(unit_model_list=[LENS_LIST[i],"0.5inch_post"])
  aperture = M.mount_list[0].aperture
  mir= Lens()
  mir.aperture = aperture
  mir.Mount = M
  mir.pos = (i*50,-100,100+i*10)
  mir.draw()
  mir.Mount.draw()

if freecad_da:
  setview()