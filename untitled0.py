# -*- coding: utf-8 -*-
"""
Created on Thu Feb 29 08:20:37 2024

@author: 庄赫
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
sys.path.append("D:/")

from LaserCAD.freecad_models import clear_doc, setview, freecad_da,add_to_composition
from LaserCAD.basic_optics import Mirror, Beam, Composition, Component, inch, Curved_Mirror, Ray, Geom_Object
from LaserCAD.basic_optics import Grating, Opt_Element
import matplotlib.pyplot as plt
from LaserCAD.freecad_models.utils import thisfolder, load_STL
from LaserCAD.non_interactings import Faraday_Isolator, Pockels_Cell, Lambda_Plate
from LaserCAD.basic_optics import Composed_Mount,Unit_Mount

if freecad_da:
  clear_doc()
  
def dont():
    return None

a=Grating()
a.height = 25
a.set_mount_to_default()
a.pos = (50,100,100)
a.normal = (1.5,1.5,0)
a.draw()
a.draw_mount()
from LaserCAD.freecad_models.freecad_model_element_holder import Model_element_holder
if freecad_da:
  b=Model_element_holder(post_distence=20,base_height=20,geom=a.get_geom(),thickness=5,width=50,height=25,ele_type="Grating")