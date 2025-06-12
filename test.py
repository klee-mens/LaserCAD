# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 14:35:32 2023

@author: Martin
"""

import numpy as np
import sys

# pfad = __file__
# pfad = pfad.replace("\\","/") #folder conventions windows linux stuff
# ind = pfad.rfind("/")
# pfad = pfad[0:ind-1]
# ind = pfad.rfind("/")
# pfad = pfad[0:ind]
# if not pfad in sys.path:
#   sys.path.append(pfad)

# sys.path.append(rf"D:\Martin\GitHub\LaserCAD\venv\Lib\site-packages")
# sys.path.append(rf"D:\Martin\GitHub\LaserCAD\LaserCAD")
# sys.path.append(rf"D:\Martin\GitHub\LaserCAD")

#for p in sys.path:
#	print(p)

from LaserCAD.freecad_models import clear_doc, setview, freecad_da, model_mirror
from LaserCAD.basic_optics import Mirror, Beam, Composition, Component, inch, Curved_Mirror, Ray, Geom_Object
# from LaserCAD.basic_optics import Grating, Opt_Element
# import matplotlib.pyplot as plt
# from LaserCAD.freecad_models.utils import thisfolder, load_STL
from LaserCAD.non_interactings import Crystal, Faraday_Isolator, Pockels_Cell, Lambda_Plate
# from LaserCAD.freecad_models.utils import thisfolder, load_STL

if freecad_da:
  clear_doc()
  

  
# beam = Beam(radius=1, angle=0)
# beam.pos = [0,0,0]
# beam.draw()

class Cylindric_Crystal(Component):
  def __init__(self, name="LaserCrystal", aperture=6, thickness=3, **kwargs):
    print("AAAAAAAAAAAAAAAAAAAAAAAAAA")
    super().__init__(name=name, **kwargs)
    self.aperture = aperture
    print("AAAAAAAAAAAAAAA", self.aperture)
    self.thickness = thickness
    self.draw_dict["color"] = (0.8, 0.3, 0.1)
    self.freecad_model = model_mirror


LiMgAS_crystal1 = Cylindric_Crystal(name="LiMgAs", aperture=10, thickness=11)
# LiMgAS_crystal1.pos += offset_axis
LiMgAS_crystal1.draw()

table = Crystal(width=900,height=10,thickness=1500)
table.pos = (0,450,-5)
table.draw_dict["Transparency"] = 0
table.draw_dict["color"] = (0.3,0.3,0.3)
table.draw()

# Setup = Composition()

# Setup.propagate(100)
# glan_taylor = Component()
# stl_file = thisfolder+"\mount_meshes\A2_mounts\Glan_Taylor.stl"
# glan_taylor.draw_dict["stl_file"]=stl_file
# glan_taylor.freecad_model = load_STL

# M1 = Mirror(phi=60)

# Setup.add_on_axis(glan_taylor)
# Setup.add_on_axis(M1)
def dont():
    return None
# M1.draw = dont
# M1.mount.elm_type = "dont_draw"
# Setup.propagate(100)
# Setup.draw()

if freecad_da:
  setview()