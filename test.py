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

import sys
import os

# pfad = __file__
# pfad = pfad.replace("\\", "/") #just in case
# ind = pfad.rfind("/")
# pfad = pfad[0:ind]
# ind = pfad.rfind("/")
# pfad = pfad[0:ind+1]
# path_added = False
# for path in sys.path:
#   if path ==pfad:
#     path_added = True
# if not path_added:
#   sys.path.append(pfad)
sys.path.append('C:\\ProgramData\\Anaconda3')

# from LaserCAD.non_interactings import Iris, Lambda_Plate

from LaserCAD.freecad_models import clear_doc, setview, freecad_da
from LaserCAD.basic_optics import Mirror, Beam, Composition, inch, Curved_Mirror, Ray, Geom_Object, LinearResonator, Lens
from LaserCAD.freecad_models.utils import thisfolder, load_STL

if freecad_da:
  clear_doc()

# iris = Iris()
# iris.draw()
# iris.draw_mount()

# res = LinearResonator(name="Compact")
# m1 = Mirror()
# m2 = Mirror()
# focus = 1500
# foc = Lens(f=focus)
# g1 = 0.5
# g2 = 0.1
# print(g1*g2)
# a = focus*(1-g1)
# b = focus*(1-g2)

# res.set_wavelength(2400e-6)
# res.add_on_axis(m1)
# res.propagate(a)
# res.add_on_axis(foc)
# res.propagate(b)
# res.add_on_axis(m2)

# res.draw()

# from LaserCAD.moduls.periscope import Make_Periscope, RoofTop_Mirror

# m = Lens()
# m.pos += (1,2,3)
# m.normal=(1,20,1)
# m.draw()
# m.draw_mount()
teles = Composition()
teles.propagate(100)
teles.add_on_axis(Lens())
teles.propagate(200)
teles.add_on_axis(Lens())
teles.propagate(100)

teles.draw()
# peris = RoofTop_Mirror(direction=1)

# comp = Composition("qlijfb")
# comp.pos = (0,0,100)
# comp.propagate(200)
# comp.add_supcomposition_on_axis(peris)
# comp.propagate(100)
# comp.draw()
# lam = Lambda_Plate()
# lam.pos += (0,40,0)
# lam.draw()

# lam.draw_mount()


if freecad_da:
  setview()