# -*- coding: utf-8 -*-
"""
Created on Thu May  2 15:50:29 2024

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

vertical_mat = True

centerlamda =1030e-9*1e3
vertical_mat = True
s_shift = 0
ls="CB"
Plane_height = 150 # The height of the second floor.
# focal_length = 428.0733746200338 # The focal length of the telescope
angle =1
para_d = 10
seperation = 71
Concav_shift = [0,0,0,0]
# Concav_shift = [0.2, 0.2, 0.2, 0.2]
# Concav_shift = [-0.05, -0.05, -0.05, -0.05]

Radius = 600 #Radius des großen Konkavspiegels
Aperture_concav = 100
h_StripeM = 10 #Höhe des Streifenspiegels
# gamma = 33.4906043205826 /180 *np.pi
# gamma = 18.8239722389914963 /180 *np.pi #AOI = 60
gamma = 8.3254033412311523321136 /180 *np.pi #AOI = 54
grat_const = 1/1480 # Gitterkonstante in 1/mm
# seperation = 203 # Differenz zwischen Gratingposition und Radius
focal_length = (12*300-4*seperation*(1-np.cos(54/180*np.pi)**2/np.cos(54/180*np.pi-gamma)**2))/8
lam_mid = centerlamda # Zentralwellenlänge in mm
lam_mid_grating = 1030E-6 # Zentralwellenlänge in mm
delta_lamda = 60e-9*1e3 # Bandbreite in mm
number_of_rays = 15
# safety_to_StripeM = 5 
periscope_distance = 12
c0 = 299792458*1000 #mm/s

half_height_middle = 10

v = lam_mid_grating/grat_const
s = np.sin(gamma)
c = np.cos(gamma)
a = v/2
b = np.sqrt(a**2 - (v**2 - s**2)/(2*(1+c)))
sinB = a - b
print("angle=",(gamma+np.arcsin(sinB))*180/np.pi)

Ring_number = 2
Beam_radius = 1
lightsource = Beam(radius=0, angle=0)
wavels = np.linspace(lam_mid-delta_lamda/2, lam_mid+delta_lamda/2, 
                     number_of_rays)
rays = []
cmap = plt.cm.gist_rainbow
for wavel in wavels:
  rn = Ray()
  # rn.normal = vec
  # rn.pos = pos0
  rn.wavelength = wavel
  x = 1-(wavel - lam_mid + delta_lamda/2) / delta_lamda
  rn.draw_dict["color"] = cmap( x )
  rg = Beam(radius=Beam_radius, angle=0,wavelength=wavel)
  rg.make_circular_distribution(ring_number=Ring_number)
  for ray_number in range(0,rg._ray_count):
    rn = rg.get_all_rays()[ray_number]
    rn.draw_dict["color"] = cmap( x )
    rays.append(rn)
lightsource.override_rays(rays)
lightsource.draw_dict['model'] = "ray_group"
centerlightsource = Beam(radius=0, angle=0)
wavels = np.linspace(lam_mid-delta_lamda/2, lam_mid+delta_lamda/2, 
                     number_of_rays)
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

centerray = Beam(radius=0.5, angle=0,wavelength=centerlamda)
centerray.make_cone_distribution(ray_count=13)
for ray1 in centerray.get_all_rays():
  ray1.wavelength = centerlamda
ray1 = Ray()
ray1.wavelength = centerlamda#lam_mid - 15e-9*1e3
ray1.draw_dict["color"] = cmap( 0.5 )
rays = []
rays.append(ray1)

if vertical_mat:
  Concav1 = Cylindrical_Mirror1(radius=Radius,name="Concav_Mirror")
  Concav2 = Cylindrical_Mirror1(radius=Radius,name="Concav_Mirror")
  Concav3 = Cylindrical_Mirror1(radius=Radius,name="Concav_Mirror")
  Concav4 = Cylindrical_Mirror1(radius=Radius,name="Concav_Mirror")
  StripeM1 = Cylindrical_Mirror1(radius= -Radius/2, name="Stripe_Mirror")
  StripeM2 = Cylindrical_Mirror1(radius= -Radius/2, name="Stripe_Mirror")
else:
  Concav1 = Cylindrical_Mirror(radius=Radius,name="Concav_Mirror")
  Concav2 = Cylindrical_Mirror(radius=Radius,name="Concav_Mirror")
  Concav3 = Cylindrical_Mirror(radius=Radius,name="Concav_Mirror")
  Concav4 = Cylindrical_Mirror(radius=Radius,name="Concav_Mirror")
  StripeM1 = Cylindrical_Mirror(radius= -Radius/2, name="Stripe_Mirror")
  StripeM2 = Cylindrical_Mirror(radius= -Radius/2, name="Stripe_Mirror")

StripeM1.pos = (Radius/2+s_shift, 0, -half_height_middle-periscope_distance/2)
StripeM1.aperture=50
StripeM1.draw_dict["height"]=9
StripeM1.draw_dict["thickness"]=25
# StripeM1.Mount = Composed_Mount(unit_model_list=["Stripe_mirror_mount",
#                                                 "POLARIS-K2","1inch_post"])
# StripeM1.Mount.set_geom(StripeM1.get_geom())
# StripeM1.Mount.pos += StripeM1.normal*25

StripeM2.pos = (Radius/2+s_shift, 0, half_height_middle+periscope_distance/2)
StripeM2.aperture=50
StripeM2.draw_dict["height"]=9
StripeM2.draw_dict["thickness"]=25
# StripeM2.Mount = Composed_Mount(unit_model_list=["Stripe_mirror_mount",
#                                                 "POLARIS-K2","1inch_post"])
# StripeM2.Mount.set_geom(StripeM2.get_geom())
# StripeM2.Mount.pos += StripeM2.normal*25

Grat = Grating(grat_const=grat_const,order=1, name="Gitter")
Grat.pos = (Radius-seperation, 0, 0)
Grat.normal = (np.sqrt(1-sinB**2), -sinB, 0)


Concav1.pos = (Radius/2-np.sqrt(((Radius/2+Concav_shift[0])**2)-(periscope_distance/2)**2),
               0,-half_height_middle)
# Concav1.pos = (0,0,-half_height_middle)
Concav1.aperture = Aperture_concav
Concav1.normal = (-1,0,0)
Concav1.draw_dict["height"]=10
Concav1.draw_dict["thickness"]=25
point0 = (Radius-seperation, 0, -half_height_middle)
point1 = (Radius/2, 0, -half_height_middle-periscope_distance/2)
Concav1.set_normal_with_2_points(point0, point1)
Concav1.draw_dict["mount_type"] = "dont_draw"

Concav2.pos = (Radius/2-np.sqrt(((Radius/2+Concav_shift[1])**2)-(periscope_distance/2)**2), 
               0, half_height_middle)
Concav2.aperture = Aperture_concav
Concav2.normal = (-1,0,0)
Concav2.draw_dict["height"]=10
Concav2.draw_dict["thickness"]=25
point0 = (Radius-seperation, 0, half_height_middle)
point1 = (Radius/2, 0, half_height_middle+periscope_distance/2)
Concav2.set_normal_with_2_points(point0, point1)
Concav2.draw_dict["mount_type"] = "dont_draw"
Concav3.pos = (Radius/2-np.sqrt(((Radius/2+Concav_shift[2])**2)-(periscope_distance/2)**2), 
               0, half_height_middle + periscope_distance)
Concav3.aperture = Aperture_concav
Concav3.normal = (-1,0,0)
Concav3.draw_dict["height"]=10
Concav3.draw_dict["thickness"]=25
point0 = (Radius-seperation, 0, half_height_middle + periscope_distance)
point1 = (Radius/2, 0, half_height_middle+periscope_distance/2)
Concav3.set_normal_with_2_points(point0, point1)
Concav3.draw_dict["mount_type"] = "dont_draw"
Concav4.pos = (Radius/2-np.sqrt(((Radius/2+Concav_shift[3])**2)-(periscope_distance/2)**2), 
               0, -half_height_middle - periscope_distance)
Concav4.aperture = Aperture_concav
Concav4.normal = (-1,0,0)
Concav4.draw_dict["height"]=10
Concav4.draw_dict["thickness"]=25
point0 = (Radius-seperation, 0, -half_height_middle - periscope_distance)
point1 = (Radius/2, 0, -half_height_middle-periscope_distance/2)
Concav4.set_normal_with_2_points(point0, point1)
Concav4.draw_dict["mount_type"] = "dont_draw"
ray0 = Ray()
p_grat = np.array((Radius-seperation, 0, -half_height_middle - periscope_distance))
vec = np.array((c, s, 0))
pos0 = p_grat - 250 * vec
ray0.normal = vec
ray0.pos = pos0
ray0.wavelength = lam_mid

nfm1 = - ray0.normal
pfm1 = Grat.pos + 300 * nfm1 + (0,0,-half_height_middle)

# roof = Make_RoofTop_Mirror(height=periscope_distance,up=False)
roof = Make_Periscope(height=half_height_middle*2, up=True, backwards=True)
roof.height = half_height_middle*2 # just for the records
m1, m2 = roof._elements
m1.invisible = True
m2.invisible = True
roof.pos = pfm1
roof.normal = nfm1
pure_cosmetic = Rooftop_Mirror_Component(name="RoofTop_Mirror",aperture=half_height_middle*2)
pure_cosmetic.pos = (m1.pos+m2.pos)/2
pure_cosmetic.normal = (m1.normal+m2.normal)/2
pure_cosmetic.draw_dict["model_type"] = "Rooftop"
pure_cosmetic.Mount= Unit_Mount("dont_draw")
pure_cosmetic.draw_dict["length"] = 25
pure_cosmetic.draw_dict["l_height"] = 25


Stretcher = Composition()
Stretcher.pos = pos0
Stretcher.normal = -nfm1
if ls == "CB":
  Stretcher.set_light_source(centerlightsource)
elif ls == "CR":
  Stretcher.set_light_source(centerray)
else:
  Stretcher.set_light_source(lightsource)

Stretcher.add_fixed_elm(Grat)#0
Stretcher.add_fixed_elm(Concav4)#1
Stretcher.add_fixed_elm(StripeM1)#2
Stretcher.add_fixed_elm(Concav1)#3
Stretcher.add_supcomposition_fixed(roof) #4,5
Stretcher.add_fixed_elm(Concav2)#6
Stretcher.add_fixed_elm(StripeM2)#7
Stretcher.add_fixed_elm(Concav3)#8
Stretcher.add_fixed_elm(pure_cosmetic)#9
seq = [0,1,2,3,0,4,5,0,6,7,8,0]
Stretcher.set_sequence(seq)
Stretcher.recompute_optical_axis()
Stretcher.propagate(250+44)
Stretcher.pos += (0,0,100)
Stretcher.draw()
ip = Intersection_plane()
ip.set_geom(Stretcher.last_geom())
ip.pos+=(0,0,7)
ip.spot_diagram(Stretcher._beams[-1],aberration_analysis=True)
ip.draw()
# print(Stretcher.Kostenbauder_matrix())