# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 14:01:12 2024

@author: 12816
"""
from LaserCAD.basic_optics import Mirror,Beam,Cylindrical_Mirror,Intersection_plane,Curved_Mirror,Ray, Composition, Grating
# from LaserCAD.basic_optics.mirror import 
from LaserCAD.basic_optics import Unit_Mount,Composed_Mount
from LaserCAD.non_interactings import Lambda_Plate
from LaserCAD.basic_optics.mount import Stages_Mount
from LaserCAD.freecad_models import clear_doc, setview, add_to_composition
from LaserCAD.freecad_models import freecad_da
from LaserCAD.moduls import Make_RoofTop_Mirror
from LaserCAD.basic_optics.mount import Stripe_Mirror_Mount
import numpy as np


if freecad_da:
  clear_doc()

M0 = Mirror()
Mount0 = M0.Mount
M0.Mount = Stages_Mount(basic_mount=Mount0,x_aligned=False)
M0.Mount.set_geom(M0.get_geom())
M0.draw()
M0.draw_mount()

M1 = Mirror()
M1.pos = (200,0,100)
M1.normal = (1,1,0)
Mount1 = M1.Mount
M1.Mount = Stages_Mount(basic_mount=Mount1,x_aligned=True)
M1.Mount.set_geom(M1.get_geom())
M1.draw()
M1.draw_mount()

M1_5 = Mirror()
M1_5.pos = (200,250,100)
M1_5.normal = (1,1,0)
Mount1 = M1_5.Mount
M1_5.Mount = Stages_Mount(basic_mount=Mount1,x_aligned=False)
M1_5.Mount.set_geom(M1_5.get_geom())
M1_5.draw()
M1_5.draw_mount()

M2 = Mirror()
M2.pos = (0,250,100)
Mount2 = M2.Mount
M2.Mount = Stages_Mount(basic_mount=Mount2,x_aligned=False)
M2.Mount.set_geom(M2.get_geom())
M2.Mount.find_screw_hole()
M2.draw()
M2.draw_mount()


if freecad_da:
  setview()