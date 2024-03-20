# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 13:57:20 2023
hi
i@author: mens
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

from LaserCAD.freecad_models import clear_doc, setview, freecad_da
from LaserCAD.basic_optics import Mirror, Beam, Composition, inch
from LaserCAD.basic_optics import Curved_Mirror, Ray, Component
from LaserCAD.basic_optics import LinearResonator, Lens
from LaserCAD.basic_optics import Grating, Crystal,Intersection_plane
import matplotlib.pyplot as plt
from LaserCAD.freecad_models.utils import thisfolder, load_STL
from LaserCAD.non_interactings import Faraday_Isolator, Pockels_Cell, Lambda_Plate
from LaserCAD.basic_optics.mirror import Stripe_mirror
from LaserCAD.basic_optics.mount import Composed_Mount,Rooftop_Mirror_Mount
# from LaserCAD.non_interactings.table import Table
from LaserCAD.moduls import Make_RoofTop_Mirror

if freecad_da:
  clear_doc()

import numpy as np

# result = all_moduls_test()

# iris_test()

# from basic_optics.tests import Intersection_plane_spot_diagram_test

Radius = 600 #Radius des großen Konkavspiegels
Aperture_concav = 100
h_StripeM = 5 #Höhe des Streifenspiegels
# gamma = 33.4906043205826 /180 *np.pi # Seperationswinkel zwischen einfallenden und Mittelpunktsstrahl; Alpha = Gamma + Beta
gamma = 18.8239722389914963 /180 *np.pi #AOI = 60
# gamma = 8.3254033412311523321136 /180 *np.pi #AOI = 54
# grat_const = 1/1480 # Gitterkonstante in 1/mm
grat_const = 1/1400 # Gitterkonstante in 1/mm
seperation = 80 # Differenz zwischen Gratingposition und Radius
lam_mid = 1030e-9 * 1e3 # Zentralwellenlänge in mm
delta_lamda = 60e-9*1e3 # Bandbreite in mm
number_of_rays = 9
safety_to_StripeM = 2.5 #Abstand der eingehenden Strahlen zum Concav Spiegel in mm
periscope_distance = 10
c0 = 299792458*1000 #mm/s

# abgeleitete Parameter
v = lam_mid/grat_const
s = np.sin(gamma)
c = np.cos(gamma)
a = v/2
b = np.sqrt(a**2 - (v**2 - s**2)/(2*(1+c)))
sinB = a - b
# print("angle=",(gamma+np.arcsin(sinB))*180/np.pi)

Concav = Curved_Mirror(radius=Radius, name="Concav_Mirror")
Concav.pos = (0,0,0)
Concav.aperture = Aperture_concav
Concav.normal = (-1,0,0)
Concav.set_mount_to_default()

StripeM = Stripe_mirror(radius= -Radius/2, name="Stripe_Mirror")
# StripeM.pos = (Radius/2-0.125, 0, 0)
StripeM.pos = (Radius/2, 0, 0)
# StripeM.pos = (Radius/2, 0, 0)
StripeM.aperture=75
StripeM.height=h_StripeM
# StripeM.draw_dict["thickness"]=25
# StripeM.draw_dict["model_type"]="Stripe"

Grat = Grating(grat_const=grat_const, name="Gitter")
Grat.pos = (Radius-seperation, 0, 0)
Grat.normal = (np.sqrt(1-sinB**2), -sinB, 0)

ray0 = Ray()
p_grat = np.array((Radius-seperation, 0, h_StripeM/2 + safety_to_StripeM + periscope_distance))
vec = np.array((c, s, 0))
pos0 = p_grat - 250 * vec
ray0.normal = vec
ray0.pos = pos0
ray0.wavelength = lam_mid


wavels = np.linspace(lam_mid-delta_lamda/2, lam_mid+delta_lamda/2, number_of_rays)
cmap = plt.cm.gist_rainbow
Ring_number = 1
Beam_radius = 1
beam_number = 0
lightsource = []
rays=[]
for wavel in wavels:
  lightsource=Beam(radius=Beam_radius, angle=0,wavelength=wavel)
  lightsource.make_circular_distribution(ring_number=Ring_number)
  for ray_number in range(0,lightsource._ray_count):
    rn = lightsource.get_all_rays()[ray_number]
    x = (wavel - lam_mid + delta_lamda/2) / delta_lamda
    rn.draw_dict["color"] = cmap( 1 - x )
    rays.append(rn)
  beam_number+=1
  
newlightsource = Beam(radius=0, angle=0)
  
newlightsource.override_rays(rays)
newlightsource.draw_dict['model'] = "ray_group"

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
  rn.draw_dict["color"] = cmap( 1-x )
  rays.append(rn)
lightsource.override_rays(rays)
lightsource.draw_dict['model'] = "ray_group"

nfm1 = - ray0.normal
# pfm1 = Grat.pos + 450 * nfm1 + (0,0,-h_StripeM/2 - safety_to_StripeM - periscope_distance)
pfm1 = Grat.pos + 300 * nfm1 + (0,0,-h_StripeM/2 - safety_to_StripeM - periscope_distance)
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
flip_mirror2.pos = pfm1 + np.array((0,0,periscope_distance))
flip_mirror2.normal = nfm1 - np.array((0,0,1))
flip_mirror2.draw = useless
flip_mirror2.draw_dict["mount_type"] = "dont_draw"

pure_cosmetic = Mirror(name="RoofTop_Mirror")
pure_cosmetic.Mount = Rooftop_Mirror_Mount()
pure_cosmetic.draw_dict["model_type"]="Rooftop"
pure_cosmetic.draw_dict["mount_type"] = "rooftop_mirror_mount"
pure_cosmetic.pos = (flip_mirror1.pos + flip_mirror2.pos ) / 2
pure_cosmetic.normal = (flip_mirror1.normal + flip_mirror2.normal ) / 2
pure_cosmetic.aperture = periscope_distance

roof = Make_RoofTop_Mirror(height=periscope_distance,up=True)
roof.pos = pfm1
roof.normal = nfm1

# M1=Mirror()
# M1.pos = p_grat - vec*840 + (0,0,periscope_distance)
# p0 = p_grat + (0,0,periscope_distance)
# p1 = M1.pos - (0,0,50)
# M1.set_normal_with_2_points(p0, p1)

# M2=Mirror()
# M2.pos = p1
# p0 = M1.pos
# p1 = M2.pos + (932.85969667,0,0)
# M2.set_normal_with_2_points(p0, p1)
# M1.draw_dict["mount_type"]=M2.draw_dict["mount_type"]="dont_draw"

# ip = Intersection_plane(dia=100)
# ip.pos = (1000,p1[1],p1[2])
# ip.normal= (1,0,0)
ip = Intersection_plane(dia=100)
ip.pos = p_grat - vec*300 - (0,0,periscope_distance) + (0,0,0.022)
ip.normal = vec

Stretcher = Composition(name="Strecker")
Stretcher.pos = pos0
Stretcher.normal = vec
opt_ax = Ray()
opt_ax.pos=pos0
opt_ax.normal=vec
opt_ax.wavelength = lam_mid
Stretcher.redefine_optical_axis(opt_ax)


Stretcher.set_light_source(lightsource)
Stretcher.add_fixed_elm(Grat)
Stretcher.add_fixed_elm(Concav)
Stretcher.add_fixed_elm(StripeM)
# Stretcher.add_fixed_elm(Concav2)
# Stretcher.add_fixed_elm(flip_mirror1)
# Stretcher.add_fixed_elm(flip_mirror2)
Stretcher.add_supcomposition_fixed(roof)
# Stretcher.add_fixed_elm(M1)
# Stretcher.add_fixed_elm(M2)
# Stretcher.add_fixed_elm(Concav3)
# Stretcher.add_fixed_elm(Concav4)
Stretcher.add_fixed_elm(ip)

# Stretcher.add_fixed_elm(pure_cosmetic)

# for item in subperis._elements:
#   Stretcher.add_fixed_elm(item)
# seq = np.array([0,1,2,3,0,4,5,0,6,2,7,0])
seq = np.array([0,1,2,1,0,3,4,0,1,2,1,0,5])
roundtrip_sequence = list(seq)

# if freecad_da:
#   obj = model_table()

roundtrip=1
# seq = np.repeat(roundtrip_sequence, roundtrip)

# for n in range(roundtrip-1):
#   # print("step ", n, "of", roundtrip)
#   seq = np.append(seq,roundtrip_sequence)
  
# seq=np.append(seq, [5])

Stretcher.set_sequence(seq)
Stretcher.propagate(50)
Stretcher.pos = (0,0,120)

Stretcher.draw_mounts()
Stretcher.draw_elements()
# Stretcher.compute_beams()
# container = []
# for n in range(-32,1):
#   beam = Stretcher._beams[n]
#   beam.draw_dict["model"] = "ray_group"
#   obj = beam.draw()
#   container.append(obj)
# if freecad_da:
#   part = add_to_composition(Stretcher._beams_part, container)
# else:
#   for x in container:
#     Stretcher._beams_part.append(x)
"""
Calculate the pathlength, phase shift and GVD
"""
Stretcher.draw_beams()
pathlength = {}
for ii in range(Stretcher._beams[0]._ray_count):
  wavelength = Stretcher._beams[0].get_all_rays()[ii].wavelength
  pathlength[wavelength] = 0
for jj in range(len(Stretcher._beams)-1):
  for ii in Stretcher._beams[jj].get_all_rays():
    a=pathlength[ii.wavelength]
    pathlength[ii.wavelength] = a +ii.length
ray_lam = [ray.wavelength for ray in Stretcher._beams[0].get_all_rays()]
path = [pathlength[ii] for ii in ray_lam]

path_diff = [ii-path[int(len(path)/2)] for ii in path]
fai = [path_diff[ii]/ray_lam[ii]*2*np.pi for ii in range(len(path))]
omega = [c0/ii*2*np.pi for ii in ray_lam]
para = np.polyfit(omega, fai, 5)
fai2 = [20*para[0]*ii**3+12*para[1]*ii**2+6*para[2]*ii+2*para[3] for ii in omega]
# fai2 = [para[0]*ii**5+para[1]*ii**4+para[2]*ii**3+para[3]*ii**2+para[4]*ii+para[5] for ii in omega]
delay_mid = path[int(len(path)/2)]/c0
delay = [(pa/c0-delay_mid)*1E9 for pa in path]
# plt.close("all")
ip.spot_diagram(Stretcher._beams[-1],aberration_analysis=False)
# plt.figure()
# ax1=plt.subplot(1,2,1)
# plt.plot(ray_lam,path)
# plt.ylabel("pathlength (mm)")
# plt.xlabel("wavelength (mm)")
# plt.title("Pathlength at different wavelength")
# plt.axhline(path[int(len(path)/2)], color = 'black', linewidth = 1)
# ax1=plt.subplot(1,2,2)
# plt.plot(ray_lam,delay)
# plt.ylabel("delay (ns)")
# plt.xlabel("wavelength (mm)")
# plt.title("Delay at different wavelength")
# plt.axhline(0, color = 'black', linewidth = 1)
# plt.figure()

# plt.plot(omega,fai)
# plt.axhline(0, color = 'black', linewidth = 1)
# plt.ylabel("φ(ω) (1/s)")
# plt.xlabel("angular frequency (1/s)")
# plt.figure()
# fai2 = [ii*10E30 for ii in fai2]
# plt.plot(omega,fai2)
# plt.ylabel("GVD (fs^2)")
# plt.xlabel("angular frequency (1/s)")
# fai2 = [para[0]*ii**5+para[1]*ii**4+para[2]*ii**3+para[3]*ii**2+para[4]*ii+para[5] for ii in omega]
# plt.figure()
# plt.scatter(omega,fai,s=5)
# plt.plot(omega,fai2)
# plt.axhline(0, color = 'black', linewidth = 1)
# plt.ylabel("φ(ω) (1/s)")
# plt.xlabel("angular frequency (1/s)")
# plt.show()
if freecad_da:
  setview()