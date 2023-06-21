# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 11:11:57 2023

@author: mens
"""

import sys

pfad = __file__
pfad = pfad.replace("\\", "/") #just in case
ind = pfad.rfind("/")
pfad = pfad[0:ind+1]
sys.path.append(pfad)

from basic_optics import Mirror,Lens,Gaussian_Beam,Beam,Cylindrical_Mirror,Ray,Curved_Mirror,Intersection_plane
from basic_optics.freecad_models import clear_doc, setview, freecad_da
from basic_optics.freecad_models.freecad_model_mounts import mirror_mount
from basic_optics.freecad_models.freecad_model_beam import model_Gaussian_beam
from basic_optics.freecad_models.freecad_model_mounts import model_table,model_lamda_plane
from basic_optics import Iris, Composition

import numpy as np
if freecad_da:
  clear_doc()

# rg=Beam(radius=2.5,angle=0,pos=(-100,0,100))
# rg.normal = (1,0,0)
# rg.make_circular_distribution(ring_number=4)
# m = Cylindrical_Mirror(name="Standard_Mirror",radius=200, pos=(100,0,100))

# # m = Mirror(name="Standard_Mirror", pos=(100,0,100))
# # m.normal = (1,0,0)
# m.normal = (1,1,0)
# # m.draw_dict["model_type"]="Rooftop"
# m.aperture = 100
# # m.normal = (1,0,0)
# # m.draw_dict["mount_type"] = "rooftop_mirror"
# ip = Intersection_plane()
# ip.pos = (100,-71,100)
# ip.normal = (0,-1,0)
# # m.aperture = 25.4*4
# m.draw()
# ip.draw()
# m.draw_mount()
# rg1 = m.next_beam(rg)
# ip.spot_diagram(rg1)
# rg.draw()
# rg1.draw()
# if freecad_da:
#   model_table()

# b=model_Gaussian_beam("laser1", -100+100j, 200, 1030E-3)
# m=Mirror(pos=(0,0,100))
# m.draw()
# m.draw_mount()
# gb1 = Beam(radius=10, angle=0.05,wavelength=1030E-6,pos=(0,0,100),distribution="Gaussian")
# # gb1.q_para = 10E5j
# le = Lens(f=100,pos = (100,0,100))
# mr = Mirror(phi=90, pos = (295,0,100))
# mr.aperture = 100
# gb2 = le.next_beam(gb1)
# gb3 = mr.next_beam(gb2)
# gb1.draw()
# le.draw()
# mr.draw()
# gb2.draw()
# gb3.draw()
# ==========================================================

from basic_optics.tests import all_moduls_test
# all_moduls_test()
pure_cosmetic = Mirror(name="RoofTop_Mirror")
pure_cosmetic.draw_dict["model_type"]="Rooftop"
pure_cosmetic.draw_dict["mount_type"] = "rooftop_mirror_mount"
pure_cosmetic.pos = (0,0,100)
pure_cosmetic.normal = (-1,0.,0)
pure_cosmetic.aperture = 10
pure_cosmetic.draw()
pure_cosmetic.draw_mount()
# a.draw_mount()

from basic_optics.moduls import Make_Periscope, Make_Telescope, Make_Amplifier_Typ_II_simple, Make_Stretcher, Make_White_Cell
# a=Make_White_Cell(roundtrips4=8)
# amp = Make_Amplifier_Typ_II_simple(roundtrips2=3)
# amp.pos = (0, 1000, 100)
# amp.draw()
if freecad_da:
  setview()
