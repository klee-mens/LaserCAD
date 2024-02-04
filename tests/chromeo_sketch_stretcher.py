# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 10:41:34 2023

@author: 12816
"""

import numpy as np
import sys

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
from LaserCAD.basic_optics.mirror import Rooftop_mirror,Stripe_mirror
from LaserCAD.basic_optics import LinearResonator, Lens
from LaserCAD.basic_optics import Grating, Crystal, Intersection_plane
import matplotlib.pyplot as plt
from LaserCAD.freecad_models.utils import thisfolder, load_STL
from LaserCAD.non_interactings import Faraday_Isolator, Pockels_Cell, Lambda_Plate
from LaserCAD.basic_optics.mount import Unit_Mount

if freecad_da:
  clear_doc()

c0 = 299792458*1000 #mm/s

def dont():
  return None


# def Make_Stretcher_chromeo():
"""
constructs an Offner Stretcher with an on axis helper composition
Note: When drawing a rooftop mirror, we will draw apure_cosmetic mirror to
confirm the position of the mount. The mirror's geom is the average of two
flip mirror. And its aperture is the periscope_height.
Returns
-------
TYPE Composition
  den gesamten, geraytracten Strecker...
"""
# defining parameters
radius_concave = 1000 #radius of the big concave sphere
aperture_concave = 6 * inch
height_stripe_mirror = 10 #height of the stripe mirror in mm
width_stripe_mirror = 75 # in mm
seperation_angle = 10 /180 *np.pi # sep between in and outgoing middle ray
# incident_angle = seperation_angle + reflection_angle
grating_const = 1/450 # in 1/mm
seperation = 100 # difference grating position und radius_concave
lambda_mid = 2400e-9 * 1e3 # central wave length in mm
delta_lamda = 200e-9*1e3 # full bandwith in mm
number_of_rays = 20
safety_to_stripe_mirror = 5 #distance first incomming ray to stripe_mirror in mm
periscope_height = 15
first_propagation = 20 # legnth of the first ray_bundle to flip mirror1 mm
distance_flip_mirror1_grating = 300
distance_roof_top_grating = 600

# calculated parameters according to the grating equation
v = lambda_mid/grating_const
s = np.sin(seperation_angle)
c = np.cos(seperation_angle)
a = v/2
b = np.sqrt(a**2 - (v**2 - s**2)/(2*(1+c)))
sinB = a - b
grating_normal = (np.sqrt(1-sinB**2), sinB, 0)
# print(np.arcsin(sinB)*180/np.pi)

Concav = Curved_Mirror(radius=radius_concave, name="Concav_Mirror")
Concav.aperture = aperture_concave

StripeM = Stripe_mirror(radius= -radius_concave/2, name="Stripe_Mirror")
#Cosmetics
StripeM.aperture = width_stripe_mirror
StripeM.draw_dict["height"] = height_stripe_mirror
# StripeM.draw_dict["thickness"] = 25 # arbitrary
StripeM.thickness = 25
StripeM.draw_dict["model_type"] = "Stripe"

Grat = Grating(grat_const=grating_const, name="Gitter", order=-1)

Grat.normal = grating_normal

helper = Composition()
helper_light_source = Beam(angle=0, wavelength=lambda_mid)
helper.set_light_source(helper_light_source)
#to adjust the wavelength of the oA
helper.redefine_optical_axis(helper_light_source.inner_ray())
helper.add_fixed_elm(Grat)
helper.recompute_optical_axis()
helper.propagate(radius_concave - seperation)
helper.add_on_axis(Concav)
helper.propagate(radius_concave/2)
helper.add_on_axis(StripeM)

# setting the lightsource as an bundle of different coulered rays
lightsource = Beam(radius=0, angle=0)
wavels = np.linspace(lambda_mid-delta_lamda/2, lambda_mid+delta_lamda/2, number_of_rays)
rays = []
cmap = plt.cm.gist_rainbow
for wavel in wavels:
  rn = Ray()
  # rn.normal = vec
  # rn.pos = pos0
  rn.wavelength = wavel
  x = 1-(wavel - lambda_mid + delta_lamda/2) / delta_lamda
  rn.draw_dict["color"] = cmap( x )
  rays.append(rn)
lightsource.override_rays(rays)
lightsource.draw_dict['model'] = "ray_group"

# starting the real stretcher
Stretcher = Composition(name="DerStrecker")
Stretcher.set_light_source(lightsource)
Stretcher.redefine_optical_axis(helper_light_source.inner_ray())

Stretcher.propagate(first_propagation)
FlipMirror_In_Out = Mirror(phi=-90, name="FlipMirrorInOut")
Stretcher.add_on_axis(FlipMirror_In_Out)
FlipMirror_In_Out.pos += (0,0,-periscope_height/2)
Stretcher.propagate(distance_flip_mirror1_grating)

#adding the helper
helper.set_geom(Stretcher.last_geom())
helper.pos += (0,0, height_stripe_mirror/2 + safety_to_stripe_mirror)
for element in helper._elements:
  Stretcher.add_fixed_elm(element)

Stretcher.set_sequence([0,1,2,3,2,1])
Stretcher.recompute_optical_axis()

# adding the rooftop mirror and it's cosmetics
Stretcher.propagate(distance_roof_top_grating)
RoofTop1 = Mirror(phi=0, theta=90)
Stretcher.add_on_axis(RoofTop1)
Stretcher.propagate(periscope_height)
RoofTop2 = Mirror(phi=0, theta=90)
Stretcher.add_on_axis(RoofTop2)

RoofTop1.draw = dont
# RoofTop1.draw_dict["mount_type"] = "dont_draw"
RoofTop1.Mount = Unit_Mount("dont_draw")
RoofTop2.draw = dont
RoofTop2.Mount = Unit_Mount("dont_draw")

pure_cosmetic = Rooftop_mirror(name="RoofTop_Mirror")
pure_cosmetic.draw_dict["mount_type"] = "rooftop_mirror_mount"
pure_cosmetic.pos = (RoofTop1.pos + RoofTop2.pos ) / 2
pure_cosmetic.normal = (RoofTop1.normal + RoofTop2.normal ) / 2
# pure_cosmetic.draw = dont
pure_cosmetic.aperture = periscope_height
pure_cosmetic.draw_dict["model_type"] = "Rooftop"
ip_s = Intersection_plane()
ip_s.pos -=(0,0,periscope_height) 

SinS = np.sin(10/180*np.pi)
CosS = np.cos(10/180*np.pi)
Grat1 = Grating(grat_const=grating_const, order=-1)
Grat1.pos -=(500,0,periscope_height)
Grat1.normal = grating_normal
Grat1.normal = -Grat1.normal
Grat2 = Grating(grat_const=grating_const, order=-1)
propagation_length = 200
Grat2.pos -= (500-propagation_length*CosS,SinS*propagation_length,periscope_height)
Grat2.normal = grating_normal

C_RoofTop1 = Mirror()
C_RoofTop1.pos -= (700,SinS*propagation_length,periscope_height)
C_RoofTop1.normal = (-1,0,-1)
C_RoofTop2 = Mirror()
C_RoofTop2.pos -= (700,SinS*propagation_length,0)
C_RoofTop2.normal = (-1,0,1)

C_RoofTop1.draw = dont
C_RoofTop1.Mount = Unit_Mount("dont_draw")
C_RoofTop2.draw = dont
C_RoofTop2.Mount = Unit_Mount("dont_draw")
pure_cosmetic1 = Rooftop_mirror(name="RoofTop_Mirror")
pure_cosmetic1.draw_dict["mount_type"] = "rooftop_mirror_mount"
pure_cosmetic1.pos = (C_RoofTop1.pos + C_RoofTop2.pos ) / 2
pure_cosmetic1.normal = (C_RoofTop1.normal + C_RoofTop2.normal ) / 2
pure_cosmetic1.draw_dict["model_type"] = "Rooftop"
pure_cosmetic1.aperture = periscope_height

# ip = Intersection_plane()
# ip.pos -= (100,0,0)
Stretcher.add_fixed_elm(Grat1)
Stretcher.add_fixed_elm(Grat2)
Stretcher.add_fixed_elm(C_RoofTop1)
Stretcher.add_fixed_elm(C_RoofTop2)

Stretcher.add_fixed_elm(ip_s)
Stretcher.add_fixed_elm(pure_cosmetic)
Stretcher.add_fixed_elm(pure_cosmetic1)

# setting the final sequence and the last propagation for visualization
# note that pure cosmetic (pos6) is not in the sequence
Stretcher.set_sequence([0, 1,2,3,2,1, 4,5, 1,2,3,2,1, 0,6,7,8,9,7,6,10])
# Stretcher.set_sequence([0, 1,2,3,2,1, 4,5, 1,2,3,2,1, 0])
Stretcher.recompute_optical_axis()

Stretcher.draw()


# =============================================================================
# Optical path length and spot diagrams
# =============================================================================
ip_s.spot_diagram(Stretcher._beams[-1])
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
plt.figure()
ax1=plt.subplot(1,2,1)
plt.plot(ray_lam,path)
plt.ylabel("pathlength (mm)")
plt.xlabel("wavelength (mm)")
plt.title("Pathlength at different wavelength")
plt.axhline(path[int(len(path)/2)], color = 'black', linewidth = 1)
ax2=plt.subplot(1,2,2)
plt.plot(ray_lam,delay)
plt.ylabel("delay (ns)")
plt.xlabel("wavelength (mm)")
plt.title("Delay at different wavelength")
plt.axhline(0, color = 'black', linewidth = 1)
plt.show()



if freecad_da:
  setview()