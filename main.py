# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 13:57:20 2023
hi
i@author: mens
"""


import sys
import os

pfad = __file__
pfad = pfad[0:-7] #nur wenn das Skript auch wirklich main.py heißt
sys.path.append(pfad)


from basic_optics.freecad_models import clear_doc, setview, freecad_da, freecad_model_lens, model_table

from basic_optics import Beam, Mirror, Opt_Element, Geom_Object, Curved_Mirror
from basic_optics import Lens, Ray, Composition, Grating, Propagation, Intersection_plane
from basic_optics import Refractive_plane

# from basic_optics.mirror import curved_mirror_test
from basic_optics.tests import all_moduls_test
from basic_optics.moduls import Make_White_Cell
import matplotlib.pyplot as plt

import numpy as np

if freecad_da:
  clear_doc()


# peris, teles, amp, stretch, wcell = all_moduls_test()

from basic_optics.moduls import Make_Telescope,Make_Stretcher
# from basic_optics.moduls import diaphragms_test

from basic_optics.tests import iris_test

# rg=Beam(radius=2.5,angle=0.1)
# rg.make_square_distribution(10)
# re_test = Composition(name = "refractive test")

# re_test.set_light_source(rg)
# re_test.pos=(0,0,100)
# re_test.normal = (1,0,0)
# # re_test.propagate(20)

# lens1 = Lens(f=20,pos=(10,0,100))
# re_test.add_fixed_elm(lens1)
# re_plane = Refractive_plane(r_ref_index=10,pos=(200,0,100))
# re_test.add_fixed_elm(re_plane)
# re_plane2 = Refractive_plane(r_ref_index=0.1,pos=(240,0,100))
# re_test.add_fixed_elm(re_plane2)
# re_test.propagate(50)
# re_test.draw_elements()
# re_test.draw_beams()


# anor=2.796834341
# cm_radius = 200
# cavity_length = 425
# angle_shift = 5
# cav_height = 100
# ls_shift = 35
# mr_shift = 15
# l_from_m1_to_cm1 = 1/(2/cm_radius - 2/cavity_length) - ls_shift
# cm1_x = l_from_m1_to_cm1*np.cos(angle_shift*2/180*np.pi)
# m1_y = l_from_m1_to_cm1*np.sin(angle_shift*2/180*np.pi)
# aperture_big = 25.4*2
# aperture_small = 25.4/2

# ls = Beam(radius=0.1,angle=0.05,wavelength=1030E-6, distribution="Gaussian", pos=(0,0,cav_height))
# cavset=Composition(name="Cavity Setting")
# cavset.set_light_source(ls)
# cavset.normal=(0,-1,0)
# cavset.pos=(0,ls_shift-m1_y,cav_height)

# m1 = Mirror()
# m1.pos = (0,-m1_y,cav_height)
# point0 = (0,ls_shift,cav_height)
# point1 = (-cm1_x,0,cav_height) 
# m1.set_normal_with_2_points(point0, point1)
# m1.aperture = aperture_small

# cm1 = Curved_Mirror(radius= cm_radius)
# cm1.pos = (-cm1_x,0,cav_height) 
# cm1.normal = (-1,0,0)
# point1 = (0,-m1_y,cav_height)
# point0 = cm1.pos+(cavity_length,0,0)
# cm1.set_normal_with_2_points(point0, point1)
# cm1.aperture = aperture_big

# cm2 = Curved_Mirror(radius= cm_radius,theta=-angle_shift*2)
# cm2.pos = cm1.pos+(cavity_length,0,0)
# cm2.aperture = aperture_big

# l_from_m2_to_cm2 = 1/(2/cm_radius-2/cavity_length) - mr_shift
# cm2_x =l_from_m2_to_cm2*np.cos(angle_shift*2/180*np.pi)
# cm2_z = l_from_m2_to_cm2*np.sin(angle_shift*2/180*np.pi)
# m2 = Mirror()
# m2.pos = cm2.pos -( cm2_x,0, cm2_z)
# point0 = cm2.pos
# point1 = m2.pos - (0,15,0)
# m2.set_normal_with_2_points(point0, point1)
# m2.aperture = aperture_small


# ip = Intersection_plane()
# ip.pos = m2.pos - (0,13.17,0)
# ip.normal = (0,-1,0)

# cavset.add_fixed_elm(m1)
# cavset.add_fixed_elm(cm1)
# cavset.add_fixed_elm(cm2)
# cavset.add_fixed_elm(m2)
# cavset.add_fixed_elm(ip)
# cavset.propagate(25)
# # ip.spot_diagram(cavset._ray_groups[-1])
# cavset.draw()

# table= model_table()

# result = all_moduls_test()

# iris_test()


# from basic_optics.tests import Intersection_plane_spot_diagram_test

stretch = Make_Stretcher()
stretch.pos = (0, 0, 100)
stretch.draw_elements()
stretch.draw_rays()
stretch.draw_mounts()


# results = all_moduls_test()



if freecad_da:

  setview()