# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 12:47:12 2024

@author: mens
"""


from LaserCAD.basic_optics import SquareBeam, Lens, Composition, Intersection_plane
from LaserCAD.freecad_models import clear_doc, setview, freecad_da


if freecad_da:
  clear_doc()

C = Composition()

B = SquareBeam(radius=3, ray_in_line=10)

C.set_light_source(B)
C.propagate(100)
a= Lens(f=150)
C.add_on_axis(a)
C.propagate(150)
IP = Intersection_plane()
C.add_on_axis(IP)
IP.draw()
C.propagate(30)
C.draw()

IP.spot_diagram(C._beams[1])

if freecad_da:
  setview()