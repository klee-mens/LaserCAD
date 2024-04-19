# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 13:11:22 2024

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
from LaserCAD.basic_optics import Curved_Mirror, Composition,Stripe_mirror

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

d_TFP1_Lam1 = 200
d_lam1_PC =50
d_PC_TFP2 = 150
a_TFP = 50
d_TFP2_M1 = 150
d_M1_CM = 620
R_CM = 7000
d_CM_M2 = 300
d_M2_M3 = 515
d_M2_p = 200
d_p = d_M2_M3-d_M2_p*2
d_M3_Crys = 300

Amp = Composition()
Amp.set_light_source(Beam())
Amp.propagate(100)
TFP1= Mirror(phi=a_TFP)
TFP1.pos = (50,0,80)
TFP1.normal = -TFP1.normal
# TFP1.Mount = Composed_Mount(["65_degree_mounts","POLARIS-K1","1inch_post"])
# TFP1.Mount.set_geom(TFP1.get_geom())
Amp.propagate(d_TFP1_Lam1)
Lam1 = Lambda_Plate()
Amp.add_on_axis(Lam1)
Amp.propagate(d_lam1_PC)
PC = Pockels_Cell()
Amp.add_on_axis(PC)
PC.rotate(vec=PC.normal, phi=np.pi)
Amp.propagate(d_PC_TFP2)
TFP2 = Mirror(phi=-a_TFP)
TFP2.Mount = Composed_Mount(["56_degree_mounts","POLARIS-K1","1inch_post"])
TFP2.Mount.set_geom(TFP2.get_geom())
Amp.add_on_axis(TFP2) #0
Amp.propagate(d_TFP2_M1)
M1 = Mirror(phi=-80)
Amp.add_on_axis(M1) #1
Amp.propagate(d_M1_CM)
CM = Curved_Mirror(phi=178,radius=R_CM)
Amp.add_on_axis(CM) #2
Amp.propagate(d_CM_M2)
M2 = Mirror(phi = 92)
M2.Mount = Composed_Mount(unit_model_list=["MH25_KMSS","1inch_post"])
M2.Mount.set_geom(M2.get_geom())
Amp.add_on_axis(M2) #3
Amp.propagate(d_M2_p)
Amp.recompute_optical_axis()
peri_geom = Amp.last_geom()
peri1 = Mirror()
peri1.set_geom(peri_geom)
Amp.propagate(d_p)
peri4 = Mirror()
peri4.set_geom(Amp.last_geom())
Amp.propagate(d_M2_p)
M3 = Mirror(phi = 92)
Amp.add_on_axis(M3) #8
M3.Mount = Composed_Mount(unit_model_list=["MH25_KMSS","1inch_post"])
M3.Mount.set_geom(M3.get_geom())
Crys = Crystal(width=7.5,model="round",thickness=12.5,n=1.5)
Amp.propagate(d_M3_Crys)
Amp.add_on_axis(Crys) #9
Amp.propagate(15)
Amp.recompute_optical_axis()
M4 = Mirror()
M4.pos = Amp.last_geom()[0]
p0 = M3.pos
p1 = TFP1.pos 
M4.set_normal_with_2_points(p0, p1)
p0 = TFP2.pos
p1 = M4.pos 
TFP1.set_normal_with_2_points(p0, p1)
Amp.add_fixed_elm(M4) #10
Amp.add_fixed_elm(TFP1) #11
seq = np.array([0,1,2,3])
# seq = np.append(seq,list(np.array([4,5,6,7,8,10,11])))
seq = np.append(seq,list(np.array([4,6,7])))
Amp.set_sequence(seq)
Amp.propagate(500)
Amp.draw()