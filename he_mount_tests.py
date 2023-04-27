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
# ===========================================================
# rg=Beam(radius=2.5,angle=0.1,pos=(-100,0,100))
# rg.normal = (1,0,0)
# rg.make_square_distribution(5)
# m = Cylindrical_Mirror(name="Standard_Mirror",radius=-200, pos=(100,0,100))
# m.normal = (1,1,0)
# # m.draw_dict["model_type"]="Rooftop"
# #m.normal = (1,0,0)
# # m.draw_dict["mount_type"] = "rooftop_mirror"
# m.aperture = 25.4*4
# # print(m.pos,m.normal,m.get_coordinate_system())
# m.rotate((1,1,0), np.pi/2)
# # print(m.pos,m.normal,m.get_coordinate_system())
# # m._axes = np.array([[1,0,0],[0,0,1],[0,-1,0]])
# m.draw()
# # m.draw_mount()
# rg1 = m.next_beam(rg)
# # print(m._axes)
# # rg1.length = 2000
# rg.draw()
# rg1.draw()
# ==========================================================
# ray0 = Ray(pos=[208.49408, 137.95006, 100.     ],normal=[-0.83397755, -0.55179838,  0.        ])
# ray0 = Ray(pos=[0,0,0],normal=[1,1,0])
gb1 = Beam(radius=10, angle=0.1,wavelength=1030E-3,pos=(0,0,0))
gb1.normal = (-1,-1,0)
gb1.make_circular_distribution(ring_number=2)
M3 = Curved_Mirror( name="Concav_Mirror")
M3.aperture = 25.4*2
# gamma = 33.4906043205826 /180 *np.pi
# Radius = 600
# seperation = 120
# h_StripeM = 10 
# safety_to_StripeM = 5
# s = np.sin(gamma)
# c = np.cos(gamma)
# vec = np.array((c, s, 0))
# p_grat = np.array((Radius-seperation, 0, -h_StripeM/2 - safety_to_StripeM))
M3.pos = (0,0,0)
# M3.normal =(-1,-1,0)
point0 = (100,0,0)
point1 = (0,100,0)
M3.set_normal_with_2_points(point0, point1)
gb2 = M3.next_beam(gb1)
# gb1.draw()
print(M3.normal)
# gb2.draw()
M3.normal *=-1
print(M3.normal)
# ray2 = M3.next_ray(ray0)
# ray0.draw()

# ray2.draw()
if freecad_da:
  setview()
