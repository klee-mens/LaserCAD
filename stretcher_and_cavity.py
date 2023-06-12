# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 09:43:43 2023

@author: He
"""

import sys
import os

pfad = __file__
pfad = pfad.replace("\\", "/") #just in case
ind = pfad.rfind("/")
pfad = pfad[0:ind+1]
sys.path.append(pfad)

from basic_optics import Mirror,Lens,Gaussian_Beam,Beam,Cylindrical_Mirror,Intersection_plane,Cylindrical_Mirror1

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


# peris, teles, amp, stretch, wcell = all_moduls_test()

from basic_optics.moduls import Make_Telescope,Make_Stretcher
# from basic_optics.moduls import diaphragms_test

from basic_optics.tests import iris_test

# result = all_moduls_test()

# iris_test()

# from basic_optics.tests import Intersection_plane_spot_diagram_test

Radius = 600 #Radius des großen Konkavspiegels
Aperture_concav = 6*25.4
h_StripeM = 10 #Höhe des Streifenspiegels
# gamma = 33.4906043205826 /180 *np.pi # Seperationswinkel zwischen einfallenden und Mittelpunktsstrahl; Alpha = Gamma + Beta
gamma = 18.8239722389914963 /180 *np.pi #AOI = 60
# gamma = 8.3254033412311523321136 /180 *np.pi #AOI = 54
grat_const = 1/1480 # Gitterkonstante in 1/mm
seperation = 50 # Differenz zwischen Gratingposition und Radius
lam_mid = 1030e-9 * 1e3 # Zentralwellenlänge in mm
delta_lamda = 60e-9*1e3 # Bandbreite in mm
number_of_rays = 15
safety_to_StripeM = 5 #Abstand der eingehenden Strahlen zum Concav Spiegel in mm
periscope_distance = 12

# abgeleitete Parameter
v = lam_mid/grat_const
s = np.sin(gamma)
c = np.cos(gamma)
a = v/2
b = np.sqrt(a**2 - (v**2 - s**2)/(2*(1+c)))
sinB = a - b
# print("angle=",(gamma+np.arcsin(sinB))*180/np.pi)
 
Concav1 = Cylindrical_Mirror1(radius=Radius, name="Concav_Mirror")
Concav1.pos = (Radius/2-np.sqrt((Radius**2)/4-(h_StripeM/2 + safety_to_StripeM)**2),0,-h_StripeM/2 - safety_to_StripeM)
Concav1.aperture = Aperture_concav
Concav1.normal = (-1,0,0)
Concav1.draw_dict["height"]=10
Concav1.draw_dict["thickness"]=25
point0 = (Radius-seperation, 0, -h_StripeM/2 - safety_to_StripeM)
point1 = (Radius/2, 0, 0)
Concav1.set_normal_with_2_points(point0, point1)
Concav1.draw_dict["mount_type"] = "dont_draw"

StripeM = Cylindrical_Mirror1(radius= -Radius/2, name="Stripe_Mirror")
StripeM.pos = (Radius/2+0.1185, 0, 0)
# StripeM.pos = (Radius/2, 0, 0)
StripeM.aperture=50
StripeM.draw_dict["height"]=9
StripeM.draw_dict["thickness"]=25
StripeM.draw_dict["model_type"]="Stripe"

Grat = Grating(grat_const=grat_const, name="Gitter")
Grat.pos = (Radius-seperation, 0, 0)
Grat.normal = (np.sqrt(1-sinB**2), -sinB, 0)

Concav2 = Cylindrical_Mirror1(radius=Radius, name="Concav_Mirror")
Concav2.pos = (Radius/2-np.sqrt((Radius**2)/4-(h_StripeM/2 + safety_to_StripeM)**2), 0, h_StripeM/2 + safety_to_StripeM)
Concav2.aperture = Aperture_concav
Concav2.normal = (-1,0,0)
Concav2.draw_dict["height"]=10
Concav2.draw_dict["thickness"]=25
point0 = (Radius-seperation, 0, h_StripeM/2 + safety_to_StripeM)
point1 = (Radius/2, 0, 0)
Concav2.set_normal_with_2_points(point0, point1)
Concav2.draw_dict["mount_type"] = "dont_draw"

Concav3 = Cylindrical_Mirror1(radius=Radius, name="Concav_Mirror")
Concav3.pos = (Radius/2-np.sqrt((Radius**2)/4-(h_StripeM/2 + safety_to_StripeM+periscope_distance)**2), 0, h_StripeM/2 + safety_to_StripeM + periscope_distance)
Concav3.aperture = Aperture_concav
Concav3.normal = (-1,0,0)
Concav3.draw_dict["height"]=10
Concav3.draw_dict["thickness"]=25
point0 = (Radius-seperation, 0, h_StripeM/2 + safety_to_StripeM + periscope_distance)
point1 = (Radius/2, 0, 0)
Concav3.set_normal_with_2_points(point0, point1)
Concav3.draw_dict["mount_type"] = "dont_draw"

Concav4 = Cylindrical_Mirror1(radius=Radius, name="Concav_Mirror")
Concav4.pos = (Radius/2-np.sqrt((Radius**2)/4-(h_StripeM/2 + safety_to_StripeM+periscope_distance)**2), 0, -h_StripeM/2 - safety_to_StripeM - periscope_distance)
Concav4.aperture = Aperture_concav
Concav4.normal = (-1,0,0)
Concav4.draw_dict["height"]=10
Concav4.draw_dict["thickness"]=25
point0 = (Radius-seperation, 0, -h_StripeM/2 - safety_to_StripeM - periscope_distance)
point1 = (Radius/2, 0, 0)
Concav4.set_normal_with_2_points(point0, point1)
Concav4.draw_dict["mount_type"] = "dont_draw"

ray0 = Ray()
p_grat = np.array((Radius-seperation, 0, -h_StripeM/2 - safety_to_StripeM - periscope_distance))
vec = np.array((c, s, 0))
pos0 = p_grat - 250 * vec
ray0.normal = vec
ray0.pos = pos0
ray0.wavelength = lam_mid

Ring_number = 1
Beam_radius = 3.5
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
  rg = Beam(radius=Beam_radius, angle=0,wavelength=wavel)
  rg.make_circular_distribution(ring_number=Ring_number)
  for ray_number in range(0,rg._ray_count):
    rn = rg.get_all_rays()[ray_number]
    rn.draw_dict["color"] = cmap( x )
    rays.append(rn)
lightsource.override_rays(rays)
lightsource.draw_dict['model'] = "ray_group"

newlightsource = Beam(radius=0, angle=0)
wavels = np.linspace(lam_mid-delta_lamda/2, lam_mid+delta_lamda/2, number_of_rays)
rays = []
cmap = plt.cm.gist_rainbow
for wavel in wavels:
  rn = Ray()
  rn.wavelength = wavel
  x = (wavel - lam_mid + delta_lamda/2) / delta_lamda
  rn.draw_dict["color"] = cmap( x )
  rays.append(rn)
newlightsource.override_rays(rays)
newlightsource.draw_dict['model'] = "ray_group"

nfm1 = - ray0.normal
pfm1 = Grat.pos + 600 * nfm1 + (0,0,h_StripeM/2 + safety_to_StripeM + periscope_distance)
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

Stretcher_M1 = Mirror(pos = pos0)
p0 = Stretcher_M1.pos - (500,0,0)
point0 = p0
p1 = p_grat
Stretcher_M1.set_normal_with_2_points(p0, p1)
Stretcher_M1.aperture = 25.4/2
Stretcher_M0 = Mirror()
Stretcher_M0.pos = (-150, Stretcher_M1.pos[1],Stretcher_M1.pos[2])
# Stretcher_M0.pos[1]=119.3345650361552
p0 = Stretcher_M1.pos
p1 = Stretcher_M0.pos - (0,200,0)
Stretcher_M0.set_normal_with_2_points(p0, p1)
TFP2 = Mirror()
TFP2.draw_dict["model_type"] = "45_polarizer"
TFP2.pos = (-150,-300,Stretcher_M1.pos[2])
p0 = Stretcher_M0.pos
p1 = TFP2.pos - (100,0,0)
point1 =p1
TFP2.set_normal_with_2_points(p0, p1)

Stretcher_M2 = Mirror(pos = p_grat - vec*500 + (0,0,periscope_distance))
p0 = Stretcher_M2.pos + (250,0,0)
p1 = p_grat + (0,0,periscope_distance)
Stretcher_M2.aperture = 25.4/2
Stretcher_M2.set_normal_with_2_points(p0, p1)

TFP1 = Mirror(pos=p0)
TFP1.normal = (-1,1,0)
TFP1.draw_dict["model_type"] = "45_polarizer"
TFP1.draw_dict["thickness"] = 2
Matrix_fixing_Mirror1 = Cylindrical_Mirror(radius=Radius*3/2,pos=p0+(600,0,-10))
Matrix_fixing_Mirror1.normal=(1,0,0)
Matrix_fixing_Mirror1.rotate((1,0,0), np.pi/2)
# Matrix_fixing_Mirror2 = Mirror(pos=Matrix_fixing_Mirror1.pos-(Radius*3/4-0.083,0,11))
Matrix_fixing_Mirror2 = Mirror(pos=Matrix_fixing_Mirror1.pos-(Radius*3/4,0,10))
Matrix_fixing_Mirror2.normal=(-1,0,0)

cavity_mirror1 = Mirror()
cavity_mirror1.pos = TFP1.pos -(0,50,0)
p0 = TFP1.pos
p1 = TFP2.pos+(100,0,0)
cavity_mirror1.set_normal_with_2_points(p0, p1)
cavity_mirror2 = Mirror(pos=p1)
p0 = cavity_mirror1.pos
p1 = TFP2.pos
cavity_mirror2.set_normal_with_2_points(p0, p1)
Cavity_mirror = Curved_Mirror(radius=6000)
Cavity_mirror.aperture = 2*25.4
Cavity_mirror.pos = point1
Cavity_mirror.normal = (-1,0,0)

ip = Intersection_plane(dia=100)
# ip.pos = p_grat - vec*1000 + (0,0,periscope_distance)
ip.pos = TFP2.pos
ip.normal = (-1,0,0)

Comp = Composition(name="Strecker", pos=point1, normal=(1,0,0))
opt_ax = Ray(pos=point1, normal=(1,0,0))
opt_ax.wavelength = lam_mid
Comp.redefine_optical_axis(opt_ax)

Comp.set_light_source(newlightsource)
Comp.add_fixed_elm(TFP2)
Comp.add_fixed_elm(Stretcher_M0)
Comp.add_fixed_elm(Stretcher_M1)
Comp.add_fixed_elm(Grat)
Comp.add_fixed_elm(Concav4)
Comp.add_fixed_elm(StripeM)
Comp.add_fixed_elm(Concav3)
Comp.add_fixed_elm(flip_mirror1)
Comp.add_fixed_elm(flip_mirror2)
Comp.add_fixed_elm(Concav2)
Comp.add_fixed_elm(Concav1)
Comp.add_fixed_elm(Stretcher_M2)
Comp.add_fixed_elm(Matrix_fixing_Mirror1)
Comp.add_fixed_elm(Matrix_fixing_Mirror2)
Comp.add_fixed_elm(TFP1)
Comp.add_fixed_elm(cavity_mirror1)
Comp.add_fixed_elm(cavity_mirror2)
Comp.add_fixed_elm(Cavity_mirror)

Comp.add_fixed_elm(ip)


Comp.add_fixed_elm(pure_cosmetic)

seq = np.array([0,1,2,3,4,5,6,3,7,8,3,9,5,10,3,11,12,13,12,13,12,13,12,14,15,16,17])

roundtrip_sequence = list(seq)
# if freecad_da:
#   obj = model_table()

roundtrip=75
# seq = np.repeat(roundtrip_sequence, roundtrip)
for n in range(roundtrip-1):
  # print("step ", n, "of", roundtrip)
  seq = np.append(seq,roundtrip_sequence)
  
seq=np.append(seq, [18])

Comp.set_sequence(seq)
Comp.propagate(100)
Comp.pos = (0,0,100)

Comp.draw_mounts()
Comp.draw_elements()
Comp.compute_beams()

container = []
for n in range(-29,1):
  beam = Comp._beams[n]
  beam.draw_dict["model"] = "ray_group"
  obj = beam.draw()
  container.append(obj)
if freecad_da:
  part = add_to_composition(Comp._beams_part, container)
else:
  for x in container:
    Comp._beams_part.append(x)

# plt.close("all")
ip.spot_diagram(Comp._beams[-1],aberration_analysis=True)



if freecad_da:

  setview()