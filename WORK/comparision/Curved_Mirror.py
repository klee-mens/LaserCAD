# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 13:05:48 2023

@author: 12816
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

from LaserCAD.freecad_models import clear_doc, freecad_da, setview
from LaserCAD.basic_optics import Beam, Composition,Cylindrical_Mirror
from LaserCAD.basic_optics import Curved_Mirror
from LaserCAD.basic_optics import Intersection_plane
# import matplotlib.pyplot as plt

if freecad_da:
  clear_doc()

B=Beam(radius=5,wavelength=780E-6) # define the beam light sourse
B.make_square_distribution(10) # define the distribution of beam
C = Composition(name = "Curved_Mirror")
C.set_light_source(B) 
C.propagate(100)
CM = Curved_Mirror(radius=100)
C.add_on_axis(CM)
C.propagate(50)
IP = Intersection_plane()
C.add_on_axis(IP)
C.propagate(50)
C.draw()
pointx,pointy=IP.spot_diagram(C._beams[-1])
if freecad_da:
  setview()