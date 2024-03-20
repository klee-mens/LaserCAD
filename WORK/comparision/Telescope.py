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
from LaserCAD.basic_optics import Beam, Composition
from LaserCAD.basic_optics import Curved_Mirror,Lens
from LaserCAD.basic_optics import Intersection_plane

if freecad_da:
  clear_doc()

teles = Composition(name="KepplerTelescope")
liso = Beam(radius=5, angle=0,wavelength=780E-6)
liso.make_square_distribution(10)
for ray in liso.get_all_rays():
  ray.wavelength = 1030E-6
  ray.draw_dict["color"]= (255/255,0/255,0/255)
L1 = Lens(f=100)
# L1.pos=(100,0,0)
L2 = Lens(f=200)
L2.aperture = 25.4*2
L2.set_mount_to_default()
# L2.pos=(300,0,0)
ip=Intersection_plane()
ip_end=Intersection_plane()
# ip.pos=(200-0.09,0,0)
ls= Beam(radius=5, angle=0,wavelength=780E-6)
ls.make_square_distribution(10)
comp=Composition()
comp.set_light_source(ls)
comp.propagate(100)
comp.add_on_axis(L1)
comp.propagate(100-0.09)
comp.add_on_axis(ip)
comp.propagate(200+0.09)
comp.add_on_axis(L2)
comp.propagate(100)
comp.add_on_axis(ip_end)
comp.draw()
ip.spot_diagram(comp._beams[-3])
ip_end.spot_diagram(comp._beams[-1])


if freecad_da:
  setview()
