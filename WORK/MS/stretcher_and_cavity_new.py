# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 15:21:13 2024

@author: 12816
"""

import sys
import os

pfad = __file__
pfad = pfad.replace("\\", "/") #just in case
ind = pfad.rfind("/")
pfad = pfad[0:ind]
ind = pfad.rfind("/")
pfad = pfad[0:ind]
ind = pfad.rfind("/")
pfad = pfad[0:ind+1]
path_added = False
for path in sys.path:
  if path ==pfad:
    path_added = True
if not path_added:
  sys.path.append(pfad)

from LaserCAD.basic_optics import Mirror,Beam,Cylindrical_Mirror,Intersection_plane,Cylindrical_Mirror1,Curved_Mirror,Ray, Composition, Grating
# from LaserCAD.basic_optics.mirror import 
from LaserCAD.basic_optics import Unit_Mount,Composed_Mount
from LaserCAD.non_interactings import Lambda_Plate

from LaserCAD.freecad_models import clear_doc, setview, add_to_composition
from LaserCAD.freecad_models import freecad_da
from LaserCAD.moduls import Make_RoofTop_Mirror
# from basic_optics import Curved_Mirror
# from basic_optics import Ray, Composition, Grating, Lam_Plane
# from basic_optics import Refractive_plane
# from freecad_models import add_to_composition

# from basic_optics.mirror import curved_mirror_test
import matplotlib.pyplot as plt

import numpy as np
# from copy import deepcopy

if freecad_da:
  clear_doc()

centerlamda =1030e-9*1e3

Radius = 600 #Radius des großen Konkavspiegels
Aperture_concav = 100
h_StripeM = 10 #Höhe des Streifenspiegels
# gamma = 33.4906043205826 /180 *np.pi # Seperationswinkel zwischen einfallenden und Mittelpunktsstrahl; Alpha = Gamma + Beta
gamma = 18.8239722389914963 /180 *np.pi #AOI = 60
# gamma = 8.3254033412311523321136 /180 *np.pi #AOI = 54
grat_const = 1/1480 # Gitterkonstante in 1/mm
seperation = 150 # Differenz zwischen Gratingposition und Radius
# lam_mid = 1030e-9 * 1e3 # Zentralwellenlänge in mm
lam_mid = centerlamda # Zentralwellenlänge in mm
lam_mid_grating = 1030E-6 # Zentralwellenlänge in mm
delta_lamda = 60e-9*1e3 # Bandbreite in mm
number_of_rays = 15
safety_to_StripeM = 5 #Abstand der eingehenden Strahlen zum Concav Spiegel in mm
periscope_distance = 12
c0 = 299792458*1000 #mm/s
# plt.close("all")
# abgeleitete Parameter
v = lam_mid_grating/grat_const
s = np.sin(gamma)
c = np.cos(gamma)
a = v/2
b = np.sqrt(a**2 - (v**2 - s**2)/(2*(1+c)))
sinB = a - b

