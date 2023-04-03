# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 11:11:57 2023

@author: mens
"""

import sys

pfad = __file__
pfad = pfad.replace("\\", "/") #just in case
ind = pfad.rfind("/")
pfad = pfad[0:ind+1]
sys.path.append(pfad)

from basic_optics import Mirror,Lens
from basic_optics.freecad_models import clear_doc, setview, freecad_da
from basic_optics.freecad_models.freecad_model_mirror import mirror_mount



if freecad_da:
  clear_doc()


m = Mirror(name="Standard_Mirror", pos=(0,0,60))
m.normal = (1,1,0)
m.draw_dict["mount_type"] = "POLARIS-K1"
m.aperture = 25.4
m.draw()
m.draw_mount()



if freecad_da:
  setview()
