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


from basic_optics.freecad_models import clear_doc, setview, freecad_da, freecad_model_lens

from basic_optics import Beam, Mirror, Opt_Element, Geom_Object, Curved_Mirror
from basic_optics import Lens, Ray, Composition, Grating, Propagation, Intersection_plane

# from basic_optics.mirror import curved_mirror_test
from basic_optics.tests import all_moduls_test
from basic_optics.moduls import Make_White_Cell

import numpy as np

if freecad_da:
  clear_doc()


# peris, teles, amp, stretch, wcell = all_moduls_test()

from basic_optics.moduls import Make_Telescope,Make_Amplifier_Typ_I_simpler,Make_Stretcher,Make_Amplifier_Typ_II_simpler,Make_Amplifier_Typ_II_simple,Make_Amplifier_Typ_I_simple
from basic_optics.moduls import diaphragms_test

from basic_optics.tests import iris_test

# rg=Beam(radius=2.5,angle=0)
# rg.make_square_distribution(15)
# rg.draw()


cm_radius = 200
cavity_length = 425
angle_shift = 2.796834341
cav_height = 100
l_from_m1_to_cm1 = 1/(2/cm_radius - 2/cavity_length) - 35
cm1_x = l_from_m1_to_cm1*np.cos(angle_shift*2/180*np.pi)

ls = Beam(radius=0.1,angle=0.05, pos=(0,0,cav_height))
cavset=Composition(name="Cavity Setting")
cavset.set_light_source(ls)
cavset.normal=(0,-1,0)
cavset.pos=(0,20,cav_height)

m1 = Mirror()
m1.pos = (0,-15,cav_height)
point0 = (0,20,cav_height)
point1 = (-cm1_x,0,cav_height) 
m1.set_normal_with_2_points(point0, point1)
m1.aperture=25.4/2

cm1 = Curved_Mirror(radius= cm_radius)
cm1.pos = (-cm1_x,0,cav_height) 
cm1.normal = (-1,0,0)
point1 = (0,-15,cav_height)
point0 = cm1.pos+(cavity_length,0,0)
cm1.set_normal_with_2_points(point0, point1)
cm1.aperture = 25.4*2

cm2 = Curved_Mirror(radius= cm_radius,theta=-angle_shift*2)
cm2.pos = cm1.pos+(cavity_length,0,0)
cm2.aperture = 25.4*2

l_from_m2_to_cm2 = 1/(2/cm_radius-2/cavity_length) - 15
cm2_x =l_from_m2_to_cm2*np.cos(angle_shift*2/180*np.pi)
cm2_z = l_from_m2_to_cm2*np.sin(angle_shift*2/180*np.pi)
m2 = Mirror()
m2.pos = cm2.pos -( cm2_x,0, cm2_z)
point0 = cm2.pos
point1 = m2.pos - (0,15,0)
m2.set_normal_with_2_points(point0, point1)
m2.aperture=25.4/2


ip = Intersection_plane()
ip.pos = m2.pos - (0,13.17,0)
ip.normal = (0,-1,0)

cavset.add_fixed_elm(m1)
cavset.add_fixed_elm(cm1)
cavset.add_fixed_elm(cm2)
cavset.add_fixed_elm(m2)
cavset.add_fixed_elm(ip)
cavset.propagate(25)

cavset.draw()

# table= model_table()



# iris_test()


# from basic_optics.tests import Intersection_plane_spot_diagram_test



# results = all_moduls_test()



if freecad_da:

  setview()