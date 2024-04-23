# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 13:40:20 2024

@author: 12816
"""

import sys
import os

pfad = __file__
pfad = pfad.replace("\\","/") #folder conventions windows linux stuff
pfad = pfad.lower()
ind = pfad.rfind("lasercad")
pfad = pfad[0:ind-1]
if not pfad in sys.path:
  sys.path.append(pfad)

from LaserCAD.basic_optics import Mirror,Beam,Cylindrical_Mirror,Intersection_plane,Cylindrical_Mirror1,Curved_Mirror,Ray, Composition, Grating
# from LaserCAD.basic_optics.mirror import 
from LaserCAD.basic_optics import Unit_Mount,Composed_Mount, Crystal
from LaserCAD.non_interactings import Faraday_Isolator, Pockels_Cell, Lambda_Plate

from LaserCAD.freecad_models import clear_doc, setview, add_to_composition
from LaserCAD.freecad_models import freecad_da
from LaserCAD.moduls import Make_RoofTop_Mirror, Make_Periscope
# from basic_optics import Curved_Mirror
# from basic_optics import Ray, Composition, Grating, Lam_Plane
# from basic_optics import Refractive_plane
# from freecad_models import add_to_composition
from LaserCAD.moduls.periscope import Rooftop_Mirror_Component

# from basic_optics.mirror import curved_mirror_test
import matplotlib.pyplot as plt

if freecad_da:
  from FreeCAD import Vector, Placement, Rotation
  import Mesh
  import ImportGui
  import Sketcher
  import Part
  from math import pi

import numpy as np
# from copy import deepcopy

if freecad_da:
  clear_doc()
Tele_added = True
vertical_mat = True
focal_length = 430
angle =1
para_d = 10
Tele = Composition()
Tele.set_light_source(Beam())
Tele_M1 = Mirror()
Tele_M1.pos = (50,0,80)
Tele_M1.normal = (1,-1,0)
Tele_M1.aperture = 25.4/2
Tele_M1.set_mount_to_default()
if Tele_added:
  if vertical_mat:  
    Tele_CM1 = Cylindrical_Mirror(radius=focal_length*2,height=20,thickness=10)
    Tele_CM2 = Cylindrical_Mirror(radius=focal_length*2,height=20,thickness=10)
  else:
    Tele_CM1 = Cylindrical_Mirror1(radius=focal_length*2,height=20,thickness=10)
    Tele_CM2 = Cylindrical_Mirror1(radius=focal_length*2,height=20,thickness=10)    
else:
  Tele_CM1 = Mirror()
  Tele_CM2 = Mirror()
Tele_CM1.pos = (50+para_d/2,focal_length/2,80)
Tele_CM1.normal = (0,1,0)
Tele_CM1.rotate((1,0,0), -angle/180*np.pi)
Tele_CM2.pos = (50+para_d/2,focal_length*2*(1-np.cos(angle*2/180*np.pi))-3/2*focal_length,
                np.sin(angle*2/180*np.pi)*focal_length*2+80)
Tele_CM2.normal = (0,-1,0)
Tele_CM2.rotate((1,0,0), -angle/180*np.pi)
Tele_CM1.rotate(Tele_CM1.normal, np.pi/2)
Tele_CM2.rotate(Tele_CM2.normal, np.pi/2)
Tele_CM1.aperture = Tele_CM2.aperture = 30

Tele_pm1 = Mirror()
Tele_pm2 = Mirror()
Tele_pm1.pos = Tele_CM2.pos + (-para_d/2,focal_length/2-para_d/2,0)
Tele_pm1.normal = (-1,1,0)
Tele_pm2.pos = Tele_pm1.pos + (para_d,0,0)
Tele_pm2.normal = (1,1,0)
Tele_pm2.invisible = True
Tele_pm1.invisible = True



Tele_M2 = Mirror()
Tele_M2.pos = (50+para_d,0,80)
Tele_M2.normal = (-1,-1,0)
Tele_M2.aperture = 25.4/2

pure_cosmetic = Rooftop_Mirror_Component(name="RoofTop_Mirror",aperture=5)
pure_cosmetic.pos = (Tele_pm1.pos+Tele_pm2.pos)/2
pure_cosmetic.normal = (Tele_pm1.normal+Tele_pm2.normal)/2
pure_cosmetic.draw_dict["model_type"] = "Rooftop"
pure_cosmetic.Mount= Unit_Mount("dont_draw")
pure_cosmetic.draw_dict["length"] = 10
pure_cosmetic.draw_dict["l_height"] = 15
pure_cosmetic.draw_dict["rotate90"] =True

Tele_M2 = Mirror()
Tele_M2.pos = (50+para_d,0,80)
Tele_M2.normal = (-1,-1,0)
Tele_M2.aperture = 25.4/2

pure_cosmetic1 = Rooftop_Mirror_Component(name="RoofTop_Mirror",aperture=5)
pure_cosmetic1.pos = (Tele_M1.pos+Tele_M2.pos)/2
pure_cosmetic1.normal = -(Tele_M1.normal+Tele_M2.normal)/2
pure_cosmetic1.draw_dict["model_type"] = "Rooftop"
pure_cosmetic1.Mount= Unit_Mount("dont_draw")
pure_cosmetic1.draw_dict["length"] = 10
pure_cosmetic1.draw_dict["l_height"] = 15
pure_cosmetic1.draw_dict["rotate90"] =True

Tele_M1.invisible = Tele_M2.invisible = True
Tele_pm2.Mount = Tele_pm1.Mount = Tele_M1.Mount = Tele_M2.Mount = Unit_Mount("dont_draw")
Tele.add_fixed_elm(Tele_M1)
Tele.add_fixed_elm(Tele_CM1)
Tele.add_fixed_elm(Tele_CM2)
Tele.add_fixed_elm(Tele_pm1)
Tele.add_fixed_elm(Tele_pm2)
Tele.add_fixed_elm(Tele_M2)
Tele.add_fixed_elm(pure_cosmetic)
Tele.add_fixed_elm(pure_cosmetic1)
Tele.set_sequence([0,1,2,3,4,2,1,5])
Tele.recompute_optical_axis()
Tele.propagate(10)
Tele.draw()
