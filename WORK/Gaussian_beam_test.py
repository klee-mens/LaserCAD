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
  
ls = Gaussian_Beam(radius=1,angle=-0.01,wavelength=10000E-6)
ls.draw_dict["model"] = "cone"
# ls.make_Gaussian_distribution()
Comp = Composition()
Comp.set_light_source(ls)
Comp.propagate(300)
Comp.add_on_axis(Lens(f =80))
Comp.propagate(500)
Comp.draw()
ls.draw_dict["model"] = "Gaussian"
ls.draw()

B= Beam()
B.pos= (0,0,70)
B.draw()
if freecad_da:
  setview()