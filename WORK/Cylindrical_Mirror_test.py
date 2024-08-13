# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 14:01:12 2024

@author: 12816
"""
from LaserCAD.basic_optics import Beam,Cylindrical_Mirror,Curved_Mirror
from LaserCAD.basic_optics.beam import SquareBeam
from LaserCAD.basic_optics import Intersection_plane,Composition
# from LaserCAD.basic_optics import Curved_Mirror,Ray, Composition, Grating
# from LaserCAD.basic_optics import Unit_Mount,Composed_Mount
# from LaserCAD.non_interactings import Lambda_Plate

from LaserCAD.freecad_models import clear_doc, setview, add_to_composition
from LaserCAD.freecad_models import freecad_da
# from LaserCAD.moduls import Make_RoofTop_Mirror
from LaserCAD.basic_optics.mount import Stripe_Mirror_Mount
import numpy as np

if freecad_da:
  clear_doc()

B=SquareBeam(radius =5,ray_in_line = 10)
B._radius = 5
C = Composition()
C.set_light_source(B)
C.propagate(100)
a= Cylindrical_Mirror(radius=100)
a.height =25
print(a.get_coordinate_system())
a.rotate(a.normal, np.pi/2)
print(a.get_coordinate_system())
a.Mount = Stripe_Mirror_Mount(mirror_thickness=a.thickness)
a.aperture = 75
a.pos += (100,0,0)
a.phi = -90
C.add_on_axis(a)
C.recompute_optical_axis()
C.propagate(70.6)
IP = Intersection_plane()
C.add_on_axis(IP)
C.draw()
IP.draw()
IP.spot_diagram(C._beams[-1])

B=SquareBeam(radius =5,ray_in_line = 10)
B._radius = 5
C = Composition()
C.set_light_source(B)
C.propagate(100)
a= Curved_Mirror()
a.height =25
a.rotate(a.normal, np.pi/2)
# a.Mount = Stripe_Mirror_Mount(mirror_thickness=a.thickness)
# a.aperture = 75
a.pos += (100,0,0)
a.phi = -90
C.add_on_axis(a)
# C.recompute_optical_axis()
C.propagate(100)
IP = Intersection_plane()
# C.add_on_axis(IP)
C.pos += (300,0,0)
C.draw()

if freecad_da:
  setview()