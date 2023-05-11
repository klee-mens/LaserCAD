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

from basic_optics import Mirror,Lens,Gaussian_Beam,Beam,Cylindrical_Mirror,Intersection_plane

from basic_optics.freecad_models import clear_doc, setview, freecad_da, freecad_model_lens, model_table

from basic_optics import Opt_Element, Geom_Object, Curved_Mirror,Thick_Lens
from basic_optics import Ray, Composition, Grating, Propagation
from basic_optics import Refractive_plane
from basic_optics.freecad_models import add_to_composition

# from basic_optics.mirror import curved_mirror_test
from basic_optics.tests import all_moduls_test
from basic_optics.moduls import Make_White_Cell
import matplotlib.pyplot as plt

import numpy as np
from copy import deepcopy

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
# gamma = 33.4906043205826 /180 *np.pi # Seperationswinkel zwischen einfallenden und Mittelpunktsstrahl; Alpha = Gamma + Beta
gamma = 36 /180 *np.pi
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

newlightsource0 = Beam(radius=0.5, angle=0,wavelength=lam_mid)
newlightsource0.make_circular_distribution(ring_number=2)

newlightsource1 = Beam(radius=0.5, angle=0,wavelength=lam_mid+delta_lamda/2)
newlightsource1.make_circular_distribution(ring_number=2)
  
newlightsource2 = Beam(radius=0.5, angle=0,wavelength=lam_mid-delta_lamda/2)
newlightsource2.make_circular_distribution(ring_number=2)
  
newlightsource = Beam(radius=0, angle=0)
r=Ray()
r.wavelength=lam_mid
r.draw_dict["color"] = cmap( 0.4 )
rays = []
for wavel in range(0,newlightsource0._ray_count):
  rn = newlightsource0.get_all_rays()[wavel]
  rn.draw_dict["color"] = cmap( 0.4 )
  rays.append(rn)
for wavel in range(0,newlightsource1._ray_count):
  rn = newlightsource1.get_all_rays()[wavel]
  rn.draw_dict["color"] = cmap( 0.8 )
  rays.append(rn)
for wavel in range(0,newlightsource2._ray_count):
  rn = newlightsource2.get_all_rays()[wavel]
  rn.draw_dict["color"] = cmap( 0 )
  rays.append(rn)
newlightsource.override_rays(rays)

nfm1 = - ray0.normal
pfm1 = Grat.pos + 600 * nfm1 + (0,0,h_StripeM/2 + safety_to_StripeM + periscope_distance)
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
pure_cosmetic.draw_dict["mount_type"] = "rooftop_mirror_mount"
pure_cosmetic.pos = (flip_mirror1.pos + flip_mirror2.pos ) / 2
pure_cosmetic.normal = (flip_mirror1.normal + flip_mirror2.normal ) / 2
pure_cosmetic.aperture = periscope_distance

M1 = Mirror()
M1.aperture = 25.4/2
M1.pos = pos0 - (0,0,periscope_distance)
point0 = p_grat - (0,0,periscope_distance)
point1 = M1.pos + (100,0,0)
M1.set_normal_with_2_points([point0], point1)

# M3 = Curved_Mirror(radius=2500, name="Concav_Mirror")
M3 = Mirror()
M3.aperture = 25.4/2
M3.pos = p_grat - 400 * vec
# M3.normal = -vec
point0 = p_grat
point1 = M3.pos + (-100,0,0)
M3.set_normal_with_2_points(point0, point1)

Curved_Mirror2 = Curved_Mirror(radius=5000, name="Concav_Mirror")
Curved_Mirror2.aperture = 25.4*2
Curved_Mirror2.pos = M3.pos + (-100,0,0)
Curved_Mirror2.normal = (-1,0,0)

fixlens1 = Lens(f=100)
fixlens1.aperture = 25.4/2
fixlens1.pos = p_grat - 445 * vec
fixlens1.normal = vec

fixlens2 = Lens(f=25)
fixlens2.aperture = 25.4/2
fixlens2.pos = p_grat - 425 * vec
fixlens2.normal = vec

Curved_Mirror1 = Curved_Mirror(radius=5000, name="Concav_Mirror")
Curved_Mirror1.aperture = 25.4*2
Curved_Mirror1.pos = M1.pos + (250,0,0)
Curved_Mirror1.normal = (1,0,0)
# point0 = M1.pos
# point1 = p_grat - (-100,0,periscope_distance)
# M2.set_normal_with_2_points([point0], point1)

Cavity1 = Curved_Mirror(radius=500, name="Concav_Mirror")
Cavity1.pos = point1
Cavity1.aperture = 25.4*2
# Concav1.normal = (-1,0,0)
point0 = Curved_Mirror1.pos
point1 = Cavity1.pos + (100,0,0)
Cavity1.set_normal_with_2_points(point0, point1)

Cavity2 = Curved_Mirror(radius=500, name="Concav_Mirror")
Cavity2.pos = Concav1.pos + (500,0,0)
Cavity2.aperture = 25.4*2
Cavity2.normal = (1,0,0)

ip = Intersection_plane(dia=100)
ip.pos = p_grat + vec*250
ip.normal = vec
# ip.pos = StripeM.pos
# ip.normal = StripeM.normal

# pure_cosmetic.draw = useless
M1.pos = M1.pos-(0,0,4)


Stretcher = Composition(name="Strecker", pos=pos0, normal=vec)
opt_ax = Ray(pos=pos0, normal=vec)
opt_ax.wavelength = lam_mid
Stretcher.redefine_optical_axis(opt_ax)

Stretcher.set_light_source(newlightsource)
Stretcher.add_fixed_elm(Grat)
Stretcher.add_fixed_elm(Concav1)
Stretcher.add_fixed_elm(StripeM)
Stretcher.add_fixed_elm(Concav2)
Stretcher.add_fixed_elm(flip_mirror2)
Stretcher.add_fixed_elm(flip_mirror1)
Stretcher.add_fixed_elm(Concav3)
Stretcher.add_fixed_elm(Concav4)
Stretcher.add_fixed_elm(M1)
Stretcher.add_fixed_elm(Curved_Mirror1)
# Stretcher.add_fixed_elm(Concav1)
# Stretcher.add_fixed_elm(Concav2)
Stretcher.add_fixed_elm(M3)
Stretcher.add_fixed_elm(Curved_Mirror2)
Stretcher.add_fixed_elm(ip)
# Stretcher.add_fixed_elm(fixlens1)
# Stretcher.add_fixed_elm(fixlens2)

Stretcher.add_fixed_elm(pure_cosmetic)

# for item in subperis._elements:
#   Stretcher.add_fixed_elm(item)

# seq = [0,1,2,3,0,4,5,0,6,2,7,0,8,9,8,0,7,2,6,0,5,4,0,3,2,1,0,10,11,10]
# seq = [0,1,2,1,0, 3]

# seq = [0,1,2,3,0, 4, 5, 6, 2, 7, 0]

# from collections import deque

seq = np.array([0,1,2,3,0,4,5,0,6,2,7,0,8,9,8,0,7,2,6,0,5,4,0,3,2,1,0,10,11,10])
roundtrip_sequence = list(seq)
# seq = np.array([0,1,2,12])
# Concav1.draw()
# Grat.draw()

# if freecad_da:
#   obj = model_table()

roundtrip=11
# seq = np.repeat(roundtrip_sequence, roundtrip)

for n in range(roundtrip-1):
  # print("step ", n, "of", roundtrip)
  seq = np.append(seq,roundtrip_sequence)
  
seq=np.append(seq, [12])

Stretcher.set_sequence(seq)
Stretcher.propagate(100)
Stretcher.pos = (0,0,100)

Stretcher.draw_mounts()
Stretcher.draw_elements()
Stretcher.compute_beams()

container = []
for n in range(-32,1):
  beam = Stretcher._beams[n]
  beam.draw_dict["model"] = "ray_group"
  obj = beam.draw()
  container.append(obj)
if freecad_da:
  part = add_to_composition(Stretcher._beams_part, container)
else:
  for x in container:
    Stretcher._beams_part.append(x)
# Stretcher.draw_beams(style="ray_group")
ip.spot_diagram(Stretcher._beams[-1])


# for n in range(roundtrip-1):
#   rays = Stretcher._beams[-1].get_all_rays()
#   for ii in rays:
#     ii.name = str(n+1) +" "+ ii.name[-16:]
#   newlightsource = Beam(radius=0, angle=0)
#   newlightsource.override_rays(rays)
#   Stretcher = Composition(name="Strecker", pos=pos0, normal=vec)
#   opt_ax = Ray(pos=pos0, normal=vec)
#   opt_ax.wavelength = lam_mid
#   Stretcher.redefine_optical_axis(opt_ax)
  
#   # Stretcher.set_light_source(newlightsource)
  
#   Stretcher._lightsource = newlightsource
#   newlightsource.name = Stretcher.name + "_Lightsource"
#   Stretcher._beams = [Stretcher._lightsource]
#   group_ls = Stretcher._lightsource.get_all_rays()
#   counter = 0
#   for ray in group_ls:
#     ray.name = Stretcher._lightsource.name + "_" + str(counter)
#     counter += 1
#   Stretcher._ray_groups = [group_ls]
  
#   Stretcher.add_fixed_elm(Grat)
#   Stretcher.add_fixed_elm(Concav1)
#   Stretcher.add_fixed_elm(StripeM)
#   Stretcher.add_fixed_elm(Concav2)
#   Stretcher.add_fixed_elm(flip_mirror2)
#   Stretcher.add_fixed_elm(flip_mirror1)
#   Stretcher.add_fixed_elm(Concav3)
#   Stretcher.add_fixed_elm(Concav4)
#   Stretcher.add_fixed_elm(M1)
#   Stretcher.add_fixed_elm(Curved_Mirror1)
#   Stretcher.add_fixed_elm(M3)
#   Stretcher.add_fixed_elm(Curved_Mirror2)
#   Stretcher.add_fixed_elm(ip)
#   Stretcher.add_fixed_elm(pure_cosmetic)
  
#   if n<roundtrip-2:
#     Stretcher.set_sequence(seq)
#     Stretcher.compute_beams()
#   else:
#     seq.extend([12])
#     Stretcher.set_sequence(seq)
#     Stretcher.draw_elements()
#     Stretcher.draw_beams(style="ray_group")
#     ip.spot_diagram(Stretcher._beams[-1])



# results = all_moduls_test()



if freecad_da:

  setview()