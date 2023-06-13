# -*- coding: utf-8 -*-
"""
Created on Thu Jun  8 12:36:21 2023

@author: 12816
"""

import os
import sys

pfad = __file__

def list_files(folder_path):
    files = []
    for file_name in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, file_name)) and  not ('data' in file_name):
            files.append(file_name)
    return files

# folder_path = 'C:/Users/12816/Desktop/research/LaserCAD'  # Replace with the actual folder path
# file_names = list_files(folder_path)
# print(file_names)

pfad = __file__
pfad = pfad.replace("\\", "/") #just in case
ind = pfad.rfind("/")
pfad = pfad[0:ind+1]
sys.path.append(pfad)

from basic_optics import Mirror,Lens,Gaussian_Beam,Beam,Cylindrical_Mirror,Intersection_plane,Lam_Plane

from basic_optics.freecad_models import clear_doc, setview, freecad_da, freecad_model_lens, model_table

from basic_optics import Opt_Element, Geom_Object, Curved_Mirror
from basic_optics import Ray, Composition, Grating
# from basic_optics import Refractive_plane
from basic_optics.freecad_models import add_to_composition

# from basic_optics.mirror import curved_mirror_test
from basic_optics.tests import all_moduls_test
from basic_optics.moduls import Make_White_Cell
import matplotlib.pyplot as plt

import numpy as np
from copy import deepcopy

if freecad_da:
  clear_doc()

TFP1 = Mirror(pos=(0,0,0))
TFP1.normal = (-1,1,0)
TFP1.draw_dict["model_type"] = "45_polarizer"
lam_4 = Lam_Plane()
lam_4.pos = (65,0,0)
ip1 = Intersection_plane(name="amplifier")
ip1.pos = (65+80,0,0)
M1 = Mirror(pos=(65+80+175,0,0))
p0 = (0,0,0)
p1 = M1.pos - (np.sqrt(825**2-270**2),-270,0)
M1.set_normal_with_2_points(p0, p1)
CM1 = Curved_Mirror(radius=1000,pos=p1)
p0 = M1.pos
p1 = CM1.pos+(1000,0,0)
CM1.set_normal_with_2_points(p0, p1)
CM2 = Curved_Mirror(radius=500,pos=p1,normal=(-1,0,0))
lam_2 = Lam_Plane()
lam_2.pos = (-185,0,0)
ip2 = Intersection_plane(name="amplifier")
ip2.pos = (-185-150,0,0)
TFP2 = Mirror()
TFP2.pos = (-185-150-165,0,0)
TFP2.normal = (-1,1,0)
TFP2.draw_dict["model_type"] = "45_polarizer"
M2 = Mirror(pos = (0,-30,0))
M2.normal = (0,-1,0)

ls=Beam(radius=1,angle=0)

comp=Composition(pos = (-550,0,0),normal=(1,0,0))
opt_ax = Ray(pos = (-550,0,0),normal=(1,0,0))
comp.redefine_optical_axis(opt_ax)
comp.set_light_source(ls)
comp.add_fixed_elm(TFP1) #0
comp.add_fixed_elm(lam_4)
comp.add_fixed_elm(ip1)
comp.add_fixed_elm(M1)
comp.add_fixed_elm(CM1)
comp.add_fixed_elm(CM2) #5
comp.add_fixed_elm(lam_2)
comp.add_fixed_elm(ip2)
comp.add_fixed_elm(TFP2)
comp.add_fixed_elm(M2)

# seq = np.array([0,1,2,3,4,5,4,3,2,1,6,7,8])
seq = np.array([7,6,1,2,3,4,5,4,3,2,1,0,9,0,1,2,3,4,5,4,3,2,1,6,7,8])

comp.set_sequence(seq)
comp.propagate(50)
comp.pos = (0,0,100)
comp.draw()