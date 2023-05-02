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

from basic_optics import Mirror,Lens,Gaussian_Beam,Beam,Cylindrical_Mirror,Ray,Curved_Mirror
from basic_optics.freecad_models import clear_doc, setview, freecad_da
from basic_optics.freecad_models.freecad_model_mirror import mirror_mount
from basic_optics.freecad_models.freecad_model_beam import model_Gaussian_beam

import numpy as np
if freecad_da:
  clear_doc()

# rg=Beam(radius=2.5,angle=0.1,pos=(-100,0,100))
# rg.normal = (1,0,0)
# rg.make_square_distribution(10)
# m = Cylindrical_Mirror(name="Standard_Mirror",radius=-200, pos=(100,0,100))

# m = Mirror(name="Standard_Mirror", pos=(100,0,100))
# # m.normal = (1,1,0)
# m.draw_dict["model_type"]="Rooftop"
# m.aperture = 0
# m.normal = (1,0,0)
# m.draw_dict["mount_type"] = "rooftop_mirror"

# # m.aperture = 25.4*4
# m.draw()
# m.draw_mount()
# rg1 = m.next_beam(rg)
# rg.draw()
# rg1.draw()

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
Radius = 600 #Radius des großen Konkavspiegels
Aperture_concav = 100
h_StripeM = 10 #Höhe des Streifenspiegels
# gamma = 33.4906043205826 /180 *np.pi # Seperationswinkel zwischen einfallenden und Mittelpunktsstrahl; Alpha = Gamma + Beta
gamma = 36 /180 *np.pi
grat_const = 1/1480 # Gitterkonstante in 1/mm
seperation = 120 # Differenz zwischen Gratingposition und Radius
lam_mid = 1030e-9 * 1e3 # Zentralwellenlänge in mm
delta_lamda = 50e-9*1e3 # Bandbreite in mm
number_of_rays = 20
safety_to_StripeM = 5 #Abstand der eingehenden Strahlen zum Concav Spiegel in mm
periscope_distance = 10
# ray0 = Ray(pos=[208.49408, 137.95006, 100.     ],normal=[-0.83397755, -0.55179838,  0.        ])
# ray0 = Ray(pos=[0,0,0],normal=[1,1,0])
# gb1 = Beam(radius=10, angle=0.1,wavelength=1030E-3,pos=(0,0,0))
# gb1.normal = (-1,-1,0)
# gb1.make_circular_distribution(ring_number=2)
# ray1 = Ray(pos=(0,0,100))
# ray1.length=600
# Radius = 600
StripeM = Cylindrical_Mirror(radius = Radius,pos=(0,0,100))
p0=p1=(-100,0,100)
StripeM.set_normal_with_2_points(p0, p1)
StripeM.normal=-StripeM.normal
StripeM.aperture=75
StripeM.draw_dict["height"]=9
StripeM.draw_dict["thickness"]=25
StripeM.draw_dict["model_type"]="Stripe"
StripeM.draw()
StripeM.draw_mount()

# Concav1 = Cylindrical_Mirror(radius=Radius, name="Concav_Mirror")
# Concav1.pos = [-277.74575141,  146.94631307,  100.        ]
# Concav1.aperture = Aperture_concav
# # Concav1.normal = [-0.96430279,  0.21589063,  0.15333415]
# Concav1.draw_dict["height"]=6
# Concav1.draw_dict["thickness"]=25
# point0 = [202.25425, 146.94631, 100.     ]
# point1 = [ 22.25424859, 146.94631307, 110.        ]
# Concav1.set_normal_with_2_points(point0, point1)
# Concav1.draw_dict["mount_type"] = "dont_draw"
# Concav1.draw()
# ray1 = Ray(pos=[1159.95883,  961.53726,  -11.58567],normal=[-0.80703,  0.59051, -0.     ])
# ray1.draw()
# ray2.draw()
if freecad_da:
  setview()
