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
from LaserCAD.basic_optics.mount import Unit_Mount,Post, Composed_Mount
from LaserCAD.basic_optics.mount import MIRROR_LIST,LENS_LIST

if freecad_da:
  clear_doc()
  
for i in range(len(MIRROR_LIST)):
  M = Composed_Mount(unit_model_list=[MIRROR_LIST[i],"1inch_post"])
  aperture = M.mount_list[0].aperture
  mir= Mirror()
  mir.aperture = aperture
  mir.Mount = M
  mir.pos = (i*75,0,50+i*10)
  if mir.aperture > 25.4*4:
    mir.pos -= (50,0,0)
    mir.Mount.pos += mir.normal*mir.thickness
  mir.draw()
  mir.Mount.draw()

mir = Mirror() 
M = Composed_Mount(unit_model_list=["Adaptive_Angular_Mount","KS1","1inch_post"])
mir.pos = (0,100,80)
mir.normal = (1,1,-2)
mir.Mount = M
M.set_geom(mir.get_geom())
mir.draw()
mir.draw_mount()
  
for i in range(len(LENS_LIST)):
  M = Composed_Mount(unit_model_list=[LENS_LIST[i],"0.5inch_post"])
  aperture = M.mount_list[0].aperture
  mir= Lens()
  mir.aperture = aperture
  mir.Mount = M
  mir.pos = (i*75,-100,100+i*10)
  mir.draw()
  mir.Mount.draw()



if freecad_da:
  setview()