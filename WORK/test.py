# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 14:01:12 2024

@author: 12816
"""
from LaserCAD.basic_optics import Mirror,Beam,Cylindrical_Mirror,Intersection_plane,Cylindrical_Mirror1,Curved_Mirror,Ray, Composition, Grating
# from LaserCAD.basic_optics.mirror import 
from LaserCAD.basic_optics import Unit_Mount,Composed_Mount
from LaserCAD.non_interactings import Lambda_Plate

from LaserCAD.freecad_models import clear_doc, setview, add_to_composition
from LaserCAD.freecad_models import freecad_da
from LaserCAD.moduls import Make_RoofTop_Mirror
from LaserCAD.basic_optics.mount import Stripe_Mirror_Mount
import numpy as np

# B=Beam(radius =5)
# B.make_square_distribution (10)
# C = Composition()
# C.set_light_source(B)
# C.propagate(100)
# a= Cylindrical_Mirror(radius=100)
# a.rotate(a.normal, np.pi/2)
# a.Mount = Stripe_Mirror_Mount(mirror_thickness=a.thickness)
# a.aperture = 75
# a.pos += (100,0,0)
# a.phi = -90
# C.add_on_axis(a)
# # C.recompute_optical_axis()
# C.propagate(70.6)
# IP = Intersection_plane()
# C.add_on_axis(IP)
# C.draw()
# IP.draw()
# IP.spot_diagram(C._beams[-1])

# ray = Ray()
# ray.draw()
# B = Beam(radius=5)
# B.pos += (0,100,0)
# B.draw()
# M = Mirror()
# M.pos += (0,200,0)
# M.draw()
# M.draw_mount()
# G = Grating()
# G.pos += (0,300,0)
# G.draw()
# G.draw_mount()

if freecad_da:
  clear_doc()

# M1 = Cylindrical_Mirror()
# M1.pos += (100,0,0)
# B = Beam()
# B.normal = (1,0.1,0)
# B1 = M1.next_beam(B)
# B.draw()
# B1.draw()
# M1.draw()

import matplotlib.pyplot as plt
from LaserCAD.basic_optics import inch, Stripe_mirror
from LaserCAD.moduls import Make_Stretcher
from LaserCAD.basic_optics.beam import RainbowBeam


from LaserCAD.moduls import Make_Stretcher_chromeo, Make_Stretcher

# Strecker = Make_Stretcher_chromeo()
Strecker = Make_Stretcher()
Strecker.draw()















if freecad_da:
  setview()