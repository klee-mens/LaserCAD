# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 09:31:20 2024

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

from LaserCAD.basic_optics import Mirror,Beam,Cylindrical_Mirror,Intersection_plane
from LaserCAD.basic_optics import Cylindrical_Mirror1,Curved_Mirror,Ray, Composition, Grating
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
  
Radius = 600 #Radius des großen Konkavspiegels
Aperture_concav = 100
h_StripeM = 10 #Höhe des Streifenspiegels
# gamma = 33.4906043205826 /180 *np.pi # Seperationswinkel zwischen einfallenden und Mittelpunktsstrahl; Alpha = Gamma + Beta
gamma = 18.8239722389914963 /180 *np.pi #AOI = 60
# gamma = 8.3254033412311523321136 /180 *np.pi #AOI = 54
grat_const = 1/1480 # Gitterkonstante in 1/mm
seperation = 150 # Differenz zwischen Gratingposition und Radius
lam_mid = 1030e-9 * 1e3 # Zentralwellenlänge in mm
# lam_mid = centerlamda # Zentralwellenlänge in mm
delta_lamda = 60e-9*1e3 # Bandbreite in mm
number_of_rays = 3
safety_to_StripeM = 5 #Abstand der eingehenden Strahlen zum Concav Spiegel in mm
periscope_distance = 12
c0 = 299792458*1000 #mm/s
# plt.close("all")
# abgeleitete Parameter
v = lam_mid/grat_const
s = np.sin(gamma)
c = np.cos(gamma)
a = v/2
b = np.sqrt(a**2 - (v**2 - s**2)/(2*(1+c)))
sinB = a - b

vertical_mat = True
s_shift = 0
C_radius = 8000
roundtrip = 1

if vertical_mat:
  Concav1 = Cylindrical_Mirror1(radius=Radius,name="Concav_Mirror")
  Concav2 = Cylindrical_Mirror1(radius=Radius,name="Concav_Mirror")
  Concav3 = Cylindrical_Mirror1(radius=Radius,name="Concav_Mirror")
  Concav4 = Cylindrical_Mirror1(radius=Radius,name="Concav_Mirror")
  StripeM = Cylindrical_Mirror1(radius= -Radius/2, name="Stripe_Mirror")
else:
  Concav1 = Cylindrical_Mirror(radius=Radius,name="Concav_Mirror")
  Concav2 = Cylindrical_Mirror(radius=Radius,name="Concav_Mirror")
  Concav3 = Cylindrical_Mirror(radius=Radius,name="Concav_Mirror")
  Concav4 = Cylindrical_Mirror(radius=Radius,name="Concav_Mirror")
  StripeM = Cylindrical_Mirror(radius= -Radius/2, name="Stripe_Mirror")
Concav1.aperture= Concav2.aperture = Concav3.aperture = Concav4.aperture = Aperture_concav
Concav1.normal = Concav2.normal = Concav3.normal = Concav4.normal = (-1,0,0)
Concav1.height = Concav2.height = Concav3.height = Concav4.height =10

Concav1.pos = (Radius/2-np.sqrt((Radius**2)/4-(h_StripeM/2 + safety_to_StripeM)**2), 0 ,-h_StripeM/2 - safety_to_StripeM)
Concav2.pos = (Radius/2-np.sqrt((Radius**2)/4-(h_StripeM/2 + safety_to_StripeM)**2), 0 , h_StripeM/2 + safety_to_StripeM)
Concav3.pos = (Radius/2-np.sqrt((Radius**2)/4-(h_StripeM/2 + safety_to_StripeM+periscope_distance)**2),
               0, h_StripeM/2 + safety_to_StripeM + periscope_distance)
Concav4.pos = (Radius/2-np.sqrt((Radius**2)/4-(h_StripeM/2 + safety_to_StripeM+periscope_distance)**2),
               0, -h_StripeM/2 - safety_to_StripeM - periscope_distance)

point0 = (Radius-seperation, 0, -h_StripeM/2 - safety_to_StripeM)
point1 = (Radius/2, 0, 0)
Concav1.set_normal_with_2_points(point0, point1)
point0 = (Radius-seperation, 0, h_StripeM/2 + safety_to_StripeM)
Concav2.set_normal_with_2_points(point0, point1)
point0 = (Radius-seperation, 0, h_StripeM/2 + safety_to_StripeM + periscope_distance)
Concav3.set_normal_with_2_points(point0, point1)
point0 = (Radius-seperation, 0, -h_StripeM/2 - safety_to_StripeM - periscope_distance)
Concav4.set_normal_with_2_points(point0, point1)

StripeM.pos = (Radius/2+s_shift, 0, 0)
StripeM.aperture=50
StripeM.draw_dict["height"]=9
StripeM.draw_dict["thickness"]=25
# StripeM.draw_dict["model_type"]="Stripe"
StripeM.Mount = Composed_Mount(unit_model_list=["Stripe_mirror_mount","POLARIS-K2","1inch_post"])
StripeM.Mount.set_geom(StripeM.get_geom())
StripeM.Mount.pos += StripeM.normal*25
Grat = Grating(grat_const=grat_const, name="Gitter")
Grat.pos = (Radius-seperation, 0, 0)
Grat.normal = (np.sqrt(1-sinB**2), -sinB, 0)

ray0 = Ray()
p_grat = np.array((Radius-seperation, 0, -h_StripeM/2 - safety_to_StripeM - periscope_distance))
vec = np.array((c, s, 0))
pos0 = p_grat - 250 * vec
ray0.normal = vec
ray0.pos = pos0
ray0.wavelength = lam_mid

Ring_number = 2
Beam_radius = 0.5
C1 = 1 # assume input_radius*input_angle = lambda/pi*C1, C1 is a const. C1=1 if the input beam is a Gaussian beam
input_angle = (lam_mid+delta_lamda/2)/np.pi*C1/Beam_radius
lightsource = Beam(radius=0, angle=0)
wavels = np.linspace(lam_mid-delta_lamda/2, lam_mid+delta_lamda/2, number_of_rays)
rays = []
cmap = plt.cm.gist_rainbow
for wavel in wavels:
  rn = Ray()
  # rn.normal = vec
  # rn.pos = pos0
  rn.wavelength = wavel
  x = 1-(wavel - lam_mid + delta_lamda/2) / delta_lamda
  rn.draw_dict["color"] = cmap( x )
  rg = Beam(radius=Beam_radius, angle=input_angle,wavelength=wavel)
  rg.make_circular_distribution(ring_number=Ring_number)
  for ray_number in range(0,rg._ray_count):
    rn = rg.get_all_rays()[ray_number]
    rn.draw_dict["color"] = cmap( x )
    rays.append(rn)
lightsource.override_rays(rays)
lightsource.draw_dict['model'] = "ray_group"

centerlightsource = Beam(radius=0, angle=0)
wavels = np.linspace(lam_mid-delta_lamda/2, lam_mid+delta_lamda/2, number_of_rays)
rays = []
cmap = plt.cm.gist_rainbow
for wavel in wavels:
  rn = Ray()
  rn.wavelength = wavel
  x = 1-(wavel - lam_mid + delta_lamda/2) / delta_lamda
  rn.draw_dict["color"] = cmap( x )
  # print(wavel,x,cmap( x ))
  rays.append(rn)
centerlightsource.override_rays(rays)
centerlightsource.draw_dict['model'] = "ray_group"

nfm1 = - ray0.normal
pfm1 = Grat.pos + 600 * nfm1 + (0,0,h_StripeM/2 + safety_to_StripeM + periscope_distance)

roof = Make_RoofTop_Mirror(height=periscope_distance,up=False)
roof.pos = pfm1
roof.normal = nfm1

Stretcher_M1 = Mirror()
Stretcher_M1.pos = pos0
p0 = Stretcher_M1.pos - (500,0,0)
point0 = p0
p1 = p_grat
Stretcher_M1.set_normal_with_2_points(p0, p1)
# Stretcher_M1.aperture = 25.4/2
Stretcher_M1.Mount = Composed_Mount(unit_model_list=["MH25_KMSS","1inch_post"])
Stretcher_M1.Mount.set_geom(Stretcher_M1.get_geom())
# Stretcher_M1.set_mount_to_default()
Stretcher_M0 = Mirror()
Stretcher_M0.Mount = Composed_Mount(unit_model_list=["H45","POLARIS-K1","1inch_post"])
Stretcher_M0.pos = (-150, Stretcher_M1.pos[1],Stretcher_M1.pos[2])
p0 = Stretcher_M1.pos
p1 = Stretcher_M0.pos - (0,200,0)
Stretcher_M0.set_normal_with_2_points(p0, p1)
TFP2 = Mirror()
# TFP2.draw_dict["model_type"] = "45_polarizer"
TFP2.Mount = Composed_Mount(unit_model_list=["H45","POLARIS-K1","1inch_post"])
TFP2.pos = (-150,-300,Stretcher_M1.pos[2])
p0 = Stretcher_M0.pos
p1 = TFP2.pos - (100,0,0)
point1 =p1
TFP2.set_normal_with_2_points(p0, p1)
Lam_Plane2=Lambda_Plate()
Lam_Plane2.pos=TFP2.pos-(50,0,0)
Stretcher_M2 = Mirror()
Stretcher_M2.pos = p_grat - vec*500 + (0,0,periscope_distance)

p0 = Stretcher_M2.pos + (250,0,0)
p1 = p_grat + (0,0,periscope_distance)
Stretcher_M2.Mount = Composed_Mount(unit_model_list=["MH25_KMSS","1inch_post"])
Stretcher_M2.Mount.set_geom(Stretcher_M2.get_geom())
# Stretcher_M2.aperture = 25.4/2
# Stretcher_M2.set_mount_to_default()
Stretcher_M2.set_normal_with_2_points(p0, p1)

TFP1 = Mirror()
TFP1.Mount = Composed_Mount(unit_model_list=["H45","POLARIS-K1","1inch_post"])
TFP1.pos=p0
TFP1.normal = (-1,1,0)
# TFP1.draw_dict["model_type"] = "45_polarizer"
TFP1.draw_dict["thickness"] = 2
Lam_Plane1=Lambda_Plate()
Lam_Plane1.pos=TFP1.pos+(50,0,0)
if vertical_mat:
  Matrix_fixing_Mirror1 = Cylindrical_Mirror(radius=Radius*3/2)
  Matrix_fixing_Mirror1.pos=p0+(600,0,-10)
else:
  Matrix_fixing_Mirror1 = Cylindrical_Mirror1(radius=Radius*3/2)
  Matrix_fixing_Mirror1.pos=p0+(600,0,-10)
# Matrix_fixing_Mirror1.normal=(1,0,0)
Matrix_fixing_Mirror1.rotate((1,0,0), np.pi/2)
# Matrix_fixing_Mirror2 = Mirror(pos=Matrix_fixing_Mirror1.pos-(Radius*3/4-0.083,0,11))
Matrix_fixing_Mirror2 = Mirror()
Matrix_fixing_Mirror2.Mount = Composed_Mount(unit_model_list=["MH25_KMSS","1inch_post"])
Matrix_fixing_Mirror2.pos=Matrix_fixing_Mirror1.pos-(Radius*3/4,0,10)
Matrix_fixing_Mirror2.normal=(-1,0,0)
cavity_mirror1 = Mirror()
cavity_mirror1.pos = TFP1.pos -(0,50,0)
p0 = TFP1.pos
p1 = TFP2.pos+(200,0,0)
cavity_mirror1.set_normal_with_2_points(p0, p1)
cavity_mirror2 = Mirror()
cavity_mirror2.pos=p1
cavity_mirror2.aperture = 25.4*2
p0 = cavity_mirror1.pos
p1 = TFP2.pos
cavity_mirror2.set_normal_with_2_points(p0, p1)
Cavity_mirror = Curved_Mirror(radius=C_radius)
Cavity_mirror.aperture = 2*25.4
Cavity_mirror.pos = point1
Cavity_mirror.normal = (-1,0,0)
Cavity_mirror.set_mount_to_default()
# ---------------------------------------------------------------------------
# p0=p_grat + (0,0,periscope_distance)
# p1=cavity_mirror2.pos
# Stretcher_M2.set_normal_with_2_points(p0,p1)
# p0=Stretcher_M2.pos
# p1=Cavity_mirror.pos
# cavity_mirror2.set_normal_with_2_points(p0,p1)
# ---------------------------------------------------------------------------
cavity_mirror2.set_mount_to_default()
ip = Intersection_plane(dia=100)
# ip.pos = p_grat - vec*1000 + (0,0,periscope_distance)
# ip.pos = TFP2.pos
# ip.pos = Matrix_fixing_Mirror2.pos + (0,0,0.51)
ip.pos = Stretcher_M0.pos + (0,100,0)
ip.normal = (0,1,0)

Comp = Composition(name="Strecker")#pos=TFP2.pos - (0,100,0), normal=(0,1,0))
Comp.pos=TFP2.pos- (0,100,0)
Comp.normal=(0,1,0)
opt_ax = Ray()
opt_ax.set_geom(Comp.get_geom())

opt_ax.wavelength = lam_mid
Comp.redefine_optical_axis(opt_ax)
# Comp.set_light_source(centerlightsource)
Comp.set_light_source(lightsource)
Comp.add_fixed_elm(TFP2)#0
Comp.add_fixed_elm(Stretcher_M0)#1
Comp.add_fixed_elm(Stretcher_M1)#2
Comp.add_fixed_elm(Grat)#3
Comp.add_fixed_elm(Concav4)#4
Comp.add_fixed_elm(StripeM)#5
Comp.add_fixed_elm(Concav3)#6
Comp.add_supcomposition_fixed(roof) #7,8
# Comp.add_fixed_elm(flip_mirror1)#7
# Comp.add_fixed_elm(flip_mirror2)#8
Comp.add_fixed_elm(Concav2)#9
Comp.add_fixed_elm(Concav1)#10
Comp.add_fixed_elm(Stretcher_M2)#11
Comp.add_fixed_elm(Matrix_fixing_Mirror1)#12
Comp.add_fixed_elm(Matrix_fixing_Mirror2)#13
Comp.add_fixed_elm(TFP1)#14
Comp.add_fixed_elm(cavity_mirror1)#15
Comp.add_fixed_elm(cavity_mirror2)#16
Comp.add_fixed_elm(Cavity_mirror)#17

Comp.add_fixed_elm(ip)#18
# Comp.add_fixed_elm(pure_cosmetic)
Comp.add_fixed_elm(Lam_Plane1)
Comp.add_fixed_elm(Lam_Plane2)
seq = np.array([1,2,3,4,5,6,3,7,8,3,9,5,10,3,11,12,13,12,13,12,13,12,14,15,16,17])
seq1 = np.array([0,1,2,3,4,5,6,3,7,8,3,9,5,10,3,11,12,13,12,13,12,13,12,14,15,16,17])

# seq = np.array([1,2,3,4,5,6,3,7,8,3,9,5,10,3,11,16,17])
# seq1 = np.array([0,1,2,3,4,5,6,3,7,8,3,9,5,10,3,11,16,17])

roundtrip_sequence = list(seq1)
# if freecad_da:
#   obj = model_table()

# roundtrip=1
# seq = np.repeat(roundtrip_sequence, roundtrip)
for n in range(roundtrip-1):
  seq = np.append(seq,roundtrip_sequence)
  
seq=np.append(seq, [0,18])
Comp.set_sequence(seq)
Comp.propagate(0.1)
Comp.pos = (0,0,100)
Comp.draw()
# Comp.compute_beams()