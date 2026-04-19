#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 16:41:34 2026

@author: clemens
"""

from LaserCAD.basic_optics import Cylindrical_Mirror, SquareBeam
from LaserCAD.basic_optics.lens import Cylindrical_Lens
from LaserCAD.basic_optics import Curved_Mirror
from LaserCAD.basic_optics import Intersection_plane,Composition
from LaserCAD.freecad_models import clear_doc, setview, freecad_da
from LaserCAD.basic_optics.mount import Stripe_Mirror_Mount
import numpy as np

if freecad_da:
  clear_doc()



ls = SquareBeam(radius =5,ray_in_line = 10)
comp = Composition()
comp.set_light_source(ls)

comp.propagate(100)
cyl = Cylindrical_Lens(f=100, height=50, thickness=5, aperture=40, vertical=False)

comp.add_on_axis(cyl)
comp.propagate(105)

IP = Intersection_plane()
comp.add_on_axis(IP)
comp.draw()

IP.draw()
IP.spot_diagram(comp._beams[2])



ls2 = SquareBeam(radius =5,ray_in_line = 10)
ls2.set_ray_color((0.5, 0.0, 0.8))
comp2 = Composition()
comp2.set_light_source(ls2)

comp2.propagate(100)
cyl2 = Cylindrical_Lens(f=180)

comp2.add_on_axis(cyl2)
comp2.propagate(200)

comp2.pos += (0,80,0)
comp2.draw()

if freecad_da:
  setview()