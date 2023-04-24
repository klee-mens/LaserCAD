# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 13:57:20 2023
hi
i@author: mens
"""


import sys
import os

pfad = __file__
pfad = pfad.replace("\\", "/") #just in case
ind = pfad.rfind("/")
pfad = pfad[0:ind+1]
sys.path.append(pfad)

from basic_optics import Mirror,Lens,Gaussian_Beam,Beam,Cylindrical_Mirror

from basic_optics.freecad_models import clear_doc, setview, freecad_da, freecad_model_lens, model_table

from basic_optics import Beam, Mirror, Opt_Element, Geom_Object, Curved_Mirror,Thick_Lens, Cylindrical_Mirror
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
# # ip.spot_diagram(cavset._beams[-1])
# cavset.draw()

# table= model_table()

# result = all_moduls_test()

# iris_test()


# from basic_optics.tests import Intersection_plane_spot_diagram_test

Radius = 600 #Radius des großen Konkavspiegels
Aperture_concav = 100
h_StripeM = 10 #Höhe des Streifenspiegels
gamma = 33.4906043205826 /180 *np.pi # Seperationswinkel zwischen einfallenden und Mittelpunktsstrahl; Alpha = Gamma + Beta
grat_const = 1/1480 # Gitterkonstante in 1/mm
seperation = 120 # Differenz zwischen Gratingposition und Radius
lam_mid = 1030e-9 * 1e3 # Zentralwellenlänge in mm
delta_lamda = 50e-9*1e3 # Bandbreite in mm
number_of_rays = 20
safety_to_StripeM = 5 #Abstand der eingehenden Strahlen zum Concav Spiegel in mm
periscope_distance = 10

# abgeleitete Parameter
v = lam_mid/grat_const
s = np.sin(gamma)
c = np.cos(gamma)
a = v/2
b = np.sqrt(a**2 - (v**2 - s**2)/(2*(1+c)))
sinB = a - b
print(np.arcsin(sinB)*180/np.pi)

Concav1 = Cylindrical_Mirror(radius=Radius, name="Concav_Mirror")
Concav1.pos = (0,0,-h_StripeM/2 - safety_to_StripeM)
Concav1.aperture = Aperture_concav
Concav1.normal = (-1,0,0)
Concav1.draw_dict["height"]=6
Concav1.draw_dict["thickness"]=25
point0 = (Radius-seperation, 0, -h_StripeM/2 - safety_to_StripeM)
point1 = (Radius/2, 0, 0)
Concav1.set_normal_with_2_points(point0, point1)
Concav1.draw_dict["mount_type"] = "dont_draw"

StripeM = Cylindrical_Mirror(radius= -Radius/2, name="Stripe_Mirror")
StripeM.pos = (Radius/2, 0, 0)
#Cosmetics
StripeM.aperture=50
StripeM.draw_dict["height"]=9
StripeM.draw_dict["thickness"]=25
StripeM.draw_dict["model_type"]="Stripe"

Grat = Grating(grat_const=grat_const, name="Gitter")
Grat.pos = (Radius-seperation, 0, 0)
Grat.normal = (np.sqrt(1-sinB**2), -sinB, 0)

Concav2 = Cylindrical_Mirror(radius=Radius, name="Concav_Mirror")
Concav2.pos = (0, 0, h_StripeM/2 + safety_to_StripeM)
Concav2.aperture = Aperture_concav
Concav2.normal = (-1,0,0)
Concav2.draw_dict["height"]=6
Concav2.draw_dict["thickness"]=25
point0 = (Radius-seperation, 0, h_StripeM/2 + safety_to_StripeM)
point1 = (Radius/2, 0, 0)
Concav2.set_normal_with_2_points(point0, point1)
Concav2.draw_dict["mount_type"] = "dont_draw"

Concav3 = Cylindrical_Mirror(radius=Radius, name="Concav_Mirror")
Concav3.pos = (0, 0, h_StripeM/2 + safety_to_StripeM + periscope_distance)
Concav3.aperture = Aperture_concav
Concav3.normal = (-1,0,0)
Concav3.draw_dict["height"]=6
Concav3.draw_dict["thickness"]=25
point0 = (Radius-seperation, 0, h_StripeM/2 + safety_to_StripeM + periscope_distance)
point1 = (Radius/2, 0, 0)
Concav3.set_normal_with_2_points(point0, point1)
Concav3.draw_dict["mount_type"] = "dont_draw"

Concav4 = Cylindrical_Mirror(radius=Radius, name="Concav_Mirror")
Concav4.pos = (0, 0, -h_StripeM/2 - safety_to_StripeM - periscope_distance)
Concav4.aperture = Aperture_concav
Concav4.normal = (-1,0,0)
Concav4.draw_dict["height"]=6
Concav4.draw_dict["thickness"]=25
point0 = (Radius-seperation, 0, -h_StripeM/2 - safety_to_StripeM - periscope_distance)
point1 = (Radius/2, 0, 0)
Concav4.set_normal_with_2_points(point0, point1)
Concav4.draw_dict["mount_type"] = "dont_draw"

ray0 = Ray()
p_grat = np.array((Radius-seperation, 0, -h_StripeM/2 - safety_to_StripeM))
vec = np.array((c, s, 0))
pos0 = p_grat - 250 * vec
ray0.normal = vec
ray0.pos = pos0
ray0.wavelength = lam_mid

lightsource = Beam(radius=0, angle=0)
wavels = np.linspace(lam_mid-delta_lamda/2, lam_mid+delta_lamda/2, number_of_rays)
rays = []
cmap = plt.cm.gist_rainbow
for wavel in wavels:
  rn = Ray()
  # rn.normal = vec
  # rn.pos = pos0
  rn.wavelength = wavel
  x = (wavel - lam_mid + delta_lamda/2) / delta_lamda
  rn.draw_dict["color"] = cmap( x )
  rays.append(rn)
lightsource.override_rays(rays)

nfm1 = - ray0.normal
pfm1 = Grat.pos + 400 * nfm1 + (0,0,h_StripeM/2 + safety_to_StripeM + periscope_distance)
# subperis = Periscope(length=8, theta=-90, dist1=0, dist2=0)
# subperis.pos = pfm1
# subperis.normal = nfm1
flip_mirror1 = Mirror()
flip_mirror1.pos = pfm1
flip_mirror1.normal = nfm1 - np.array((0,0,-1))
def useless():
  return None
flip_mirror1.draw = useless
flip_mirror1.draw_dict["mount_type"] = "dont_draw"

flip_mirror2 = Mirror()
flip_mirror2.pos = pfm1 - np.array((0,0,periscope_distance))
flip_mirror2.normal = nfm1 - np.array((0,0,1))
flip_mirror2.draw = useless
flip_mirror2.draw_dict["mount_type"] = "dont_draw"

pure_cosmetic = Mirror(name="RoofTop_Mirror")
pure_cosmetic.draw_dict["model_type"]="Rooftop"
pure_cosmetic.draw_dict["mount_type"] = "rooftop_mirror"
pure_cosmetic.pos = (flip_mirror1.pos + flip_mirror2.pos ) / 2
pure_cosmetic.normal = (flip_mirror1.normal + flip_mirror2.normal ) / 2
pure_cosmetic.aperture = periscope_distance

M1 = Mirror()
M1.aperture = 25.4/2
M1.pos = pos0 - (0,0,periscope_distance)
point0 = p_grat - (0,0,periscope_distance)
point1 = M1.pos + (100,0,0)
M1.set_normal_with_2_points([point0], point1)

M3 = Mirror()
M3.aperture = 25.4/2
M3.pos = p_grat - 300 * vec
point0 = p_grat - (0,0,periscope_distance)
M3.normal = -vec

# M2 = Curved_Mirror(radius=1000, name="Concav_Mirror")
M2 = Mirror()
M2.aperture = 25.4*2
M2.pos = M1.pos + (250,0,0)
M2.normal = (1,0,0)
# point0 = M1.pos
# point1 = p_grat - (-100,0,periscope_distance)
# M2.set_normal_with_2_points([point0], point1)

Cavity1 = Curved_Mirror(radius=500, name="Concav_Mirror")
Cavity1.pos = point1
Cavity1.aperture = 25.4*2
# Concav1.normal = (-1,0,0)
point0 = M2.pos
point1 = Cavity1.pos + (100,0,0)
Cavity1.set_normal_with_2_points(point0, point1)

Cavity2 = Curved_Mirror(radius=500, name="Concav_Mirror")
Cavity2.pos = Concav1.pos + (500,0,0)
Cavity2.aperture = 25.4*2
Cavity2.normal = (1,0,0)


# pure_cosmetic.draw = useless

Stretcher = Composition(name="Strecker", pos=pos0, normal=vec)

Stretcher.set_light_source(lightsource)
Stretcher.add_fixed_elm(Grat)
Stretcher.add_fixed_elm(Concav1)
Stretcher.add_fixed_elm(StripeM)
Stretcher.add_fixed_elm(Concav2)
Stretcher.add_fixed_elm(flip_mirror2)
Stretcher.add_fixed_elm(flip_mirror1)
Stretcher.add_fixed_elm(Concav3)
Stretcher.add_fixed_elm(Concav4)
Stretcher.add_fixed_elm(M1)
Stretcher.add_fixed_elm(M2)
# Stretcher.add_fixed_elm(Concav1)
# Stretcher.add_fixed_elm(Concav2)
Stretcher.add_fixed_elm(M3)

Stretcher.add_fixed_elm(pure_cosmetic)

# for item in subperis._elements:
#   Stretcher.add_fixed_elm(item)


seq = [0,1,2,3,0,4,5,0,6,2,7,0,8,9,8,0,7,2,6,0,5,4,0,3,2,1,0,10]
# seq = [0,1,2,1,0, 3]
# seq = [0,1,2,3,0, 4, 5, 6, 2, 7, 0]

roundtrip_sequence = seq
roundtrip=1
for n in range(roundtrip-1):
  seq.extend(roundtrip_sequence)
Stretcher.set_sequence(seq)
Stretcher.propagate(1000)
Stretcher.pos = (0,0,100)
Stretcher.draw_elements()
# Stretcher.draw_mounts()
Stretcher.draw_rays()


# results = all_moduls_test()



if freecad_da:

  setview()