# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 15:21:13 2024

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

import numpy as np
# from copy import deepcopy

if freecad_da:
  clear_doc()

centerlamda =1030e-9*1e3
vertical_mat = True
s_shift = 0
ls="CB"
Plane_height = 150

Radius = 600 #Radius des großen Konkavspiegels
Aperture_concav = 100
h_StripeM = 10 #Höhe des Streifenspiegels
# gamma = 33.4906043205826 /180 *np.pi # Seperationswinkel zwischen einfallenden und Mittelpunktsstrahl; Alpha = Gamma + Beta
# gamma = 18.8239722389914963 /180 *np.pi #AOI = 60
gamma = 8.3254033412311523321136 /180 *np.pi #AOI = 54
grat_const = 1/1480 # Gitterkonstante in 1/mm
seperation = 75 # Differenz zwischen Gratingposition und Radius
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
print("angle=",np.arcsin(np.sin(gamma+np.arcsin(sinB)))*180/np.pi)

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
Concav1.pos = (Radius/2-np.sqrt((Radius**2)/4-(h_StripeM/2 + safety_to_StripeM)**2),0,-h_StripeM/2 - safety_to_StripeM)
# Concav1.pos = (0,0,-h_StripeM/2 - safety_to_StripeM)
Concav1.aperture = Aperture_concav
Concav1.normal = (-1,0,0)
Concav1.draw_dict["height"]=10
Concav1.draw_dict["thickness"]=25
point0 = (Radius-seperation, 0, -h_StripeM/2 - safety_to_StripeM)
point1 = (Radius/2, 0, 0)
Concav1.set_normal_with_2_points(point0, point1)
Concav1.draw_dict["mount_type"] = "dont_draw"

StripeM.pos = (Radius/2+s_shift, 0, 0)
StripeM.aperture=50
StripeM.draw_dict["height"]=9
StripeM.draw_dict["thickness"]=25
StripeM.Mount = Composed_Mount(unit_model_list=["Stripe_mirror_mount","POLARIS-K2","1inch_post"])
StripeM.Mount.set_geom(StripeM.get_geom())
StripeM.Mount.pos += StripeM.normal*25

Grat = Grating(grat_const=grat_const, name="Gitter")
Grat.pos = (Radius-seperation, 0, 0)
Grat.normal = (np.sqrt(1-sinB**2), -sinB, 0)

Concav2.pos = (Radius/2-np.sqrt((Radius**2)/4-(h_StripeM/2 + safety_to_StripeM)**2), 0, h_StripeM/2 + safety_to_StripeM)
Concav2.aperture = Aperture_concav
Concav2.normal = (-1,0,0)
Concav2.draw_dict["height"]=10
Concav2.draw_dict["thickness"]=25
point0 = (Radius-seperation, 0, h_StripeM/2 + safety_to_StripeM)
point1 = (Radius/2, 0, 0)
Concav2.set_normal_with_2_points(point0, point1)
Concav2.draw_dict["mount_type"] = "dont_draw"

Concav3.pos = (Radius/2-np.sqrt((Radius**2)/4-(h_StripeM/2 + safety_to_StripeM+periscope_distance)**2), 0, h_StripeM/2 + safety_to_StripeM + periscope_distance)
Concav3.aperture = Aperture_concav
Concav3.normal = (-1,0,0)
Concav3.draw_dict["height"]=10
Concav3.draw_dict["thickness"]=25
point0 = (Radius-seperation, 0, h_StripeM/2 + safety_to_StripeM + periscope_distance)
point1 = (Radius/2, 0, 0)
Concav3.set_normal_with_2_points(point0, point1)
Concav3.draw_dict["mount_type"] = "dont_draw"

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

Ring_number = 2
Beam_radius = 0.5
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
  rg = Beam(radius=Beam_radius, angle=0,wavelength=wavel)
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

centerray = Beam(radius=0.5, angle=0,wavelength=centerlamda)
centerray.make_cone_distribution(ray_count=13)
for ray1 in centerray.get_all_rays():
  ray1.wavelength = centerlamda
ray1 = Ray()
ray1.wavelength = centerlamda#lam_mid - 15e-9*1e3
ray1.draw_dict["color"] = cmap( 0.5 )
rays = []
rays.append(ray1)

nfm1 = - ray0.normal
pfm1 = Grat.pos + 300 * nfm1 + (0,0,h_StripeM/2 + safety_to_StripeM + periscope_distance)

# roof = Make_RoofTop_Mirror(height=periscope_distance,up=False)
roof = Make_Periscope(height=periscope_distance, up=False, backwards=True)
roof.height = periscope_distance # just for the records
m1, m2 = roof._elements
m1.invisible = True
m2.invisible = True
roof.pos = pfm1
roof.normal = nfm1
pure_cosmetic = Rooftop_Mirror_Component(name="RoofTop_Mirror",aperture=periscope_distance)
pure_cosmetic.pos = (m1.pos+m2.pos)/2
pure_cosmetic.normal = (m1.normal+m2.normal)/2
pure_cosmetic.draw_dict["model_type"] = "Rooftop"
pure_cosmetic.Mount= Unit_Mount("dont_draw")
pure_cosmetic.draw_dict["length"] = 24
pure_cosmetic.draw_dict["l_height"] = 15


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
Stretcher.add_fixed_elm(StripeM)#2
Stretcher.add_fixed_elm(Concav3)#3
Stretcher.add_supcomposition_fixed(roof) #4,5
Stretcher.add_fixed_elm(Concav2)#6
Stretcher.add_fixed_elm(Concav1)#7
Stretcher.add_fixed_elm(pure_cosmetic)#8
seq = [0,1,2,3,0,4,5,0,6,2,7,0]
Stretcher.set_sequence(seq)
Stretcher.recompute_optical_axis()
Stretcher.propagate(250+44)

Stretcher.pos += (0,0,Plane_height+100)
for ii in Stretcher._elements:
  print(ii)
  if type(ii.Mount) != Unit_Mount:
    ii.Mount.mount_list[-1]._lower_limit = Plane_height

# Amplifler--------------------------------------------------------------------
d_TFP1_Lam1 = 200
d_lam1_PC =50
d_PC_TFP2 = 150
a_TFP = 65
d_TFP2_M1 = 150
d_M1_CM = 450
R_CM = 7000
d_CM_M2 = 300
d_M2_M3 = 544
d_M2_p = 250
d_p = d_M2_M3-d_M2_p*2
d_M3_Crys = 300

Amp = Composition()
Amp.set_light_source(Beam())
Amp.propagate(100)
TFP1= Mirror(phi=a_TFP)
TFP1.pos = (50,0,80)
TFP1.normal = -TFP1.normal
Amp.propagate(d_TFP1_Lam1)
Lam1 = Lambda_Plate()
Amp.add_on_axis(Lam1)
Amp.propagate(d_lam1_PC)
PC = Pockels_Cell()
Amp.add_on_axis(PC)
PC.rotate(vec=PC.normal, phi=np.pi)
Amp.propagate(d_PC_TFP2)
TFP2 = Mirror(phi=-a_TFP)
Amp.add_on_axis(TFP2) #0
Amp.propagate(d_TFP2_M1)
M1 = Mirror(phi=-50)
Amp.add_on_axis(M1) #1
Amp.propagate(d_M1_CM)
CM = Curved_Mirror(phi=178,radius=R_CM)
Amp.add_on_axis(CM) #2
Amp.propagate(d_CM_M2)
M2 = Mirror(phi = 92)
Amp.add_on_axis(M2) #3
Amp.propagate(d_M2_p)
Amp.recompute_optical_axis()
print(Amp.last_geom())
peri_geom = Amp.last_geom()
peri1 = Mirror()
peri1.set_geom(peri_geom)
# peri1 = Make_Periscope()
# Amp.add_supcomposition_on_axis(peri1)

Amp.propagate(d_p)
Amp.recompute_optical_axis()
print(Amp.last_geom())
peri4 = Mirror()
peri4.set_geom(Amp.last_geom())
# peri2 = Make_Periscope(up=False)
# Amp.add_supcomposition_on_axis(peri2)

# M_peri1 = Mirror(theta=90)
# Amp.add_on_axis(M_peri1) #4
# Amp.propagate(Plane_height-2)

# M_peri2 = Mirror()
# M_peri2.set_geom(M_peri1.get_geom())
# M_peri2.pos += (0, 0, Plane_height-2)
# M_peri2.normal = -M_peri1.normal
# Amp.add_fixed_elm(M_peri2) #5
# Amp.propagate(d_p/2)
# Amp.recompute_optical_axis()
# M_peri3 = Mirror(theta=-90)
# Amp.add_on_axis(M_peri3) #6

# Amp.propagate(Plane_height-2)
# M_peri4 = Mirror(theta=-90)
# Amp.add_on_axis(M_peri4) #7
# M_peri1.Mount = M_peri2.Mount = M_peri3.Mount = M_peri4.Mount = Unit_Mount("dont_draw")

Amp.propagate(d_M2_p)
M3 = Mirror(phi = 92)
Amp.add_on_axis(M3) #8
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

Stretcher.set_geom(peri_geom)
Stretcher.pos += (0,0,Plane_height)
Stretcher.normal = -Stretcher.normal

Amp.draw()
Stretcher.draw()

peri2 = Mirror()
peri2.aperture = 25.4/2
peri2.set_geom(Stretcher.get_geom())
peri3 = Mirror()
peri3.pos = peri4.pos +(0,0,Plane_height+10)


p0=M2.pos
p1=peri2.pos
peri1.set_normal_with_2_points(p0, p1)
p0=peri1.pos 
p1=Grat.pos
peri2.set_normal_with_2_points(p0, p1)
p0 = Grat.pos + (0,0,periscope_distance)
p1 = peri4.pos
peri3.set_normal_with_2_points(p0, p1)
p0 = peri3.pos
p1 = M3.pos
peri4.set_normal_with_2_points(p0, p1)
peri1.draw()
peri2.draw()
peri3.draw()
peri4.draw()
