# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 13:20:55 2024

@author: 12816
"""
from LaserCAD.freecad_models import clear_doc, freecad_da, setview
from LaserCAD.basic_optics import Beam, Composition, Gaussian_Beam
from LaserCAD.basic_optics import Curved_Mirror,Lens
from LaserCAD.basic_optics import Intersection_plane

if freecad_da:
  clear_doc()
  
ls = Gaussian_Beam(radius=5,angle=0.1)
# ls.make_Gaussian_distribution()
Comp = Composition()
Comp.set_light_source(ls)
Comp.propagate(50)
Comp.add_on_axis(Lens())
Comp.propagate(200)
Comp.draw()

if freecad_da:
  setview()