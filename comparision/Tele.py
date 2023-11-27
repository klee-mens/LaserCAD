# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 13:05:48 2023

@author: 12816
"""

import numpy as np
import sys

pfad = __file__
pfad = pfad.replace("\\","/") #folder conventions windows linux stuff
ind = pfad.rfind("/")
pfad = pfad[0:ind-1]
ind = pfad.rfind("/")
pfad = pfad[0:ind-1]
ind = pfad.rfind("/")
pfad = pfad[0:ind]
if not pfad in sys.path:
  sys.path.append(pfad)

from LaserCAD.freecad_models import clear_doc, freecad_da
from LaserCAD.basic_optics import Beam, Composition
from LaserCAD.basic_optics import Curved_Mirror,Lens
from LaserCAD.basic_optics import Intersection_plane

if freecad_da:
  clear_doc()

teles = Composition(name="KepplerTelescope")
liso = Beam(radius=5, angle=0)
liso.make_square_distribution(10)
teles.set_light_source(liso)
f1 = 100; f2 = 200
ip = Intersection_plane()
ip1 = Intersection_plane()
le1 = Lens(f=f1); le2 = Lens(f=f2)
le2.aperture = 25.4*2
teles.propagate(f1)
teles.add_on_axis(le1)
teles.propagate(f1)
teles.add_on_axis(ip)
teles.propagate(f2)
teles.add_on_axis(le2)
teles.propagate(f2)
teles.add_on_axis(ip1)
teles.propagate(10)
teles.draw()
ip.spot_diagram(teles._beams[2])