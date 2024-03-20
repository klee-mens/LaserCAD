# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 16:06:47 2024

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


from LaserCAD.freecad_models import clear_doc, setview, freecad_da
from LaserCAD.basic_optics import Mirror, Beam, Composition, inch
from LaserCAD.basic_optics import Curved_Mirror, Ray, Component
from LaserCAD.basic_optics import LinearResonator, Lens
from LaserCAD.basic_optics import Grating, Crystal
import matplotlib.pyplot as plt
from LaserCAD.freecad_models.utils import thisfolder, load_STL
from LaserCAD.non_interactings import Faraday_Isolator, Pockels_Cell, Lambda_Plate
from LaserCAD.basic_optics.mirror import Stripe_mirror
from LaserCAD.moduls import Make_RoofTop_Mirror
from LaserCAD.basic_optics.mount import Unit_Mount, Composed_Mount
from LaserCAD.non_interactings.table import Table
if freecad_da:
  clear_doc()
  
Comp = Composition()
Comp.set_light_source(Beam())
Comp.propagate(50)
M = Mirror(phi = 90)
Comp.add_on_axis(M)
Comp.propagate(50)

Comp_cam = Composition()
ls = M.through_out_beam(Comp._beams[0])
Comp_cam.set_geom(ls.get_geom())
Comp_cam.set_light_source(ls)
Comp_cam.propagate(50)
Comp_cam.add_on_axis(Lens())
Comp_cam.propagate(100)

Comp.draw()
Comp_cam.draw()