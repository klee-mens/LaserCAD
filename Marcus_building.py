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

TFP1 = Mirror()
TFP1.normal = (1,-1,0)
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
ip1 = Intersection_plane(name="amplifier")
ip1.pos = (-185-150,0,0)
TFP2 = Mirror()
TFP2.pos = (-185-150-165,0,0)
TFP2.normal = (1,-1,0)
TFP2.draw_dict["model_type"] = "45_polarizer"
