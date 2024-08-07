# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 12:56:06 2024

@author: 12816
"""

import sys
# import os

pfad = __file__
pfad = pfad.replace("\\","/") #folder conventions windows linux stuff
pfad = pfad.lower()
ind = pfad.rfind("lasercad")
pfad = pfad[0:ind-1]
if not pfad in sys.path:
  sys.path.append(pfad)
from copy import deepcopy

from LaserCAD.basic_optics import Mirror,Beam,Cylindrical_Mirror,Grating,Ray
from LaserCAD.basic_optics import Intersection_plane,Cylindrical_Mirror1
from LaserCAD.basic_optics import Curved_Mirror, Composition

from LaserCAD.basic_optics import Unit_Mount,Composed_Mount, Crystal
from LaserCAD.non_interactings import Pockels_Cell
from LaserCAD.non_interactings import Lambda_Plate

from LaserCAD.freecad_models import clear_doc, setview, add_to_composition
from LaserCAD.freecad_models import freecad_da
from LaserCAD.moduls import Make_RoofTop_Mirror, Make_Periscope
from LaserCAD.moduls.periscope import Rooftop_Mirror_Component

import matplotlib.pyplot as plt
import numpy as np

if freecad_da:
  clear_doc()


# draw the setup
Comp = Composition()
ls = Beam()
ray = Ray()
ls.override_rays([ray])
ls.draw_dict['model'] = "ray_group"
Comp.set_light_source(ls)
Comp.pos = (100,0,80)
Comp.normal = (-1,0,0)
M1 = Mirror(phi = 90.28)
Comp.propagate(100)
Comp.add_on_axis(M1)
Comp.propagate(500)
M2 = Mirror(phi = 90)
Comp.add_on_axis(M2)
Comp.propagate(600)
Comp.compute_beams()
ip1 = Intersection_plane()
ip1.pos = (100,-500,80)
ip2 = Intersection_plane()
ip2.pos = (600,-500,80)
p1 = Comp._beams[-1].get_all_rays()[0].intersection(ip1)
p2 = Comp._beams[-1].get_all_rays()[0].intersection(ip2)
# print(p1,p2)
# Comp.draw()
# ip1.draw()
# ip2.draw()
if freecad_da:
  setview()

def ray_tracing_test():
  Comp = Composition()
  ls = Beam()
  ray = Ray()
  ls.override_rays([ray])
  ls.draw_dict['model'] = "ray_group"
  Comp.set_light_source(ls)
  Comp.pos = (100,0,80)
  Comp.normal = (-1,0,0)
  M1 = Mirror(phi = 90.28)
  Comp.propagate(100)
  Comp.add_on_axis(M1)
  Comp.propagate(500)
  M2 = Mirror(phi = 90)
  Comp.add_on_axis(M2)
  Comp.propagate(600)
  Comp.compute_beams()
  ip1 = Intersection_plane()
  ip1.pos = (100,-500,80)
  ip2 = Intersection_plane()
  ip2.pos = (600,-500,80)
  p1 = Comp._beams[-1].get_all_rays()[0].intersection(ip1)
  p2 = Comp._beams[-1].get_all_rays()[0].intersection(ip2)
  # p1 = Comp._optical_axis[-1].intersection(ip1)
  # p2 = Comp._optical_axis[-1].intersection(ip2)
  return (p1,p2)

def pure_ray_tracing():
  Comp.compute_beams()
  p1 = Comp._beams[-1].get_all_rays()[0].intersection(ip1)
  p2 = Comp._beams[-1].get_all_rays()[0].intersection(ip2)
  return (p1,p2)

def ray_tracing_with_rotation():
  Comp._elements[0].rotate(vec=(0,0,1),phi=-1E-4)
  Comp.compute_beams()
  p1 = Comp._beams[-1].get_all_rays()[0].intersection(ip1)
  p2 = Comp._beams[-1].get_all_rays()[0].intersection(ip2)
  return (p1,p2)

import time
start = time.time()
for i in range(10000):
  p1,p2 = ray_tracing_test()
  # print(p1,p2)
end = time.time()
print(end-start)