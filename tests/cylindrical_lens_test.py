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
cyl = Cylindrical_Lens(f=100)
cyl.height = 25

print(cyl.get_coordinate_system())

# cyl.Mount = Stripe_Mirror_Mount(mirror_thickness=cyl.thickness)
# cyl.aperture = 75

cyl.pos += (100,0,0)

comp.add_on_axis(cyl)
cyl.rotate(cyl.normal, np.pi/2)
print(cyl.get_coordinate_system())

# comp.recompute_optical_axis()
comp.propagate(105)

IP = Intersection_plane()
comp.add_on_axis(IP)
comp.draw()

IP.draw()
IP.spot_diagram(comp._beams[2])



ls2 = SquareBeam(radius =5,ray_in_line = 10)
comp2 = Composition()
comp2.set_light_source(ls)

comp2.propagate(100)
cyl2 = Cylindrical_Lens(f=180)
cyl2.height = 40
cyl2.aperture = 50

comp2.add_on_axis(cyl2)
comp2.propagate(200)

comp2.pos += (0,80,0)
comp2.draw()


# B=SquareBeam(radius =5,ray_in_line = 10)
# B._radius = 5
# C = Composition()
# comp.set_light_source(B)
# comp.propagate(100)
# a= Curved_Mirror()
# cyl.height =25
# cyl.rotate(cyl.normal, np.pi/2)
# # cyl.Mount = Stripe_Mirror_Mount(mirror_thickness=cyl.thickness)
# # cyl.aperture = 75
# cyl.pos += (100,0,0)
# cyl.phi = -90
# comp.add_on_axis(a)
# # comp.recompute_optical_axis()
# comp.propagate(100)
# IP = Intersection_plane()
# # comp.add_on_axis(IP)
# comp.pos += (300,0,0)
# comp.draw()

if freecad_da:
  setview()