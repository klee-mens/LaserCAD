# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 10:41:34 2023

@author: 12816
"""

import numpy as np
from scipy.interpolate import interp1d
import scipy
from scipy.misc import derivative
from copy import deepcopy

from LaserCAD.freecad_models import clear_doc, freecad_da
from LaserCAD.basic_optics import Mirror, Beam, Composition, inch
from LaserCAD.basic_optics import Curved_Mirror, Ray, Lens
from LaserCAD.basic_optics.mirror import Stripe_mirror
# from LaserCAD.basic_optics import LinearResonator, Lens
from LaserCAD.moduls import Make_RoofTop_Mirror
from LaserCAD.basic_optics import Grating, Intersection_plane
import matplotlib.pyplot as plt
from LaserCAD.freecad_models.utils import thisfolder, load_STL
from LaserCAD.non_interactings import Faraday_Isolator, Pockels_Cell, Lambda_Plate,Table
from LaserCAD.basic_optics.mount import Unit_Mount, Post_Marker

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
seperation = 135 # difference grating position und radius_concave
lambda_mid = 2400e-9 * 1e3 # central wave length in mm
delta_lamda = 200e-9*1e3 # full bandwith in mm
number_of_rays = 31
safety_to_stripe_mirror = 5 #distance first incomming ray to stripe_mirror in mm
periscope_height = 15
first_propagation = 20 # legnth of the first ray_bundle to flip mirror1 mm
distance_flip_mirror1_grating = 300
distance_roof_top_grating = 600

input_radius = 1.25
C1 = np.pi/2 # assume input_radius*input_angle = lambda/pi*C1, C1 is a const. C1=1 if the input beam is a Gaussian beam
C1 = 1 # assume input_radius*input_angle = lambda/pi*C1, C1 is a const. C1=1 if the input beam is a Gaussian beam
input_angle = (lambda_mid+delta_lamda/2)/np.pi*C1/input_radius
# input_angle = 0

# calculated parameters according to the grating equation
v = lambda_mid/grating_const
s = np.sin(seperation_angle)
c = np.cos(seperation_angle)
a = v/2
b = np.sqrt(a**2 - (v**2 - s**2)/(2*(1+c)))
sinB = a - b
sinAOI = np.sin(seperation_angle+np.arcsin(sinB))
f = radius_concave

GDD = 2*lambda_mid**3*(seperation)/(np.pi*c0**2*grating_const**2*(1-(lambda_mid/grating_const-sinAOI)**2))


print("sin(angle)=",np.sin(seperation_angle+np.arcsin(sinB)))
grating_normal = (np.sqrt(1-sinB**2), sinB, 0)

Concav = Curved_Mirror(radius=radius_concave, name="Concav_Mirror")
Concav.aperture = aperture_concave
Concav.set_mount_to_default()
# Concav.mount.model = "default"

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
helper.propagate(radius_concave/2+20)
helper.add_on_axis(StripeM)


# -----------------------------------------------------------------------------
# setting the lightsource as a beam of different coulered rays
lightsource = Beam(radius=0, angle=0)
wavels = np.linspace(lambda_mid-delta_lamda/2, lambda_mid+delta_lamda/2, number_of_rays)
rays = []
cmap = plt.cm.gist_rainbow
for wavel in wavels:
    # B_test = Beam(radius=input_radius,angle=input_angle)
    # B_test.make_cone_distribution(ray_count=9)
    # ray_group =B_test.get_all_rays()
    # for rn in ray_group:
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
# RoofTop1 = Mirror(phi=0, theta=90)
# Stretcher.add_on_axis(RoofTop1)
# Stretcher.propagate(periscope_height)
# RoofTop2 = Mirror(phi=0, theta=90)
# Stretcher.add_on_axis(RoofTop2)

# RoofTop1.draw = dont
# # RoofTop1.draw_dict["mount_type"] = "dont_draw"
# # RoofTop1.Mount = Unit_Mount("dont_draw")
# RoofTop2.draw = dont
# # RoofTop2.Mount = Unit_Mount("dont_draw")
# RoofTop1.Mount.draw =dont
# RoofTop2.Mount.draw =dont

# pure_cosmetic = Rooftop_mirror(name="RoofTop_Mirror")
# pure_cosmetic.draw_dict["mount_type"] = "rooftop_mirror_mount"
# pure_cosmetic.pos = (RoofTop1.pos + RoofTop2.pos ) / 2
# pure_cosmetic.normal = (RoofTop1.normal + RoofTop2.normal ) / 2
# # pure_cosmetic.draw = dont
# pure_cosmetic.aperture = periscope_height
# pure_cosmetic.draw_dict["model_type"] = "Rooftop"
# pure_cosmetic.set_mount_to_default()

Stretcher.add_supcomposition_on_axis(Make_RoofTop_Mirror(height=periscope_height,up=False))

# le1 = Lens(f=-75)
# le1.pos -= (0,0,periscope_height)
# le2 = Lens(f=100)
# le2.pos -= (25,0,periscope_height)
# Stretcher.add_fixed_elm(le1)
# Stretcher.add_fixed_elm(le2)

# angle = 10.00134
# angle = 10.001
angle = 10
SinS = np.sin(angle/180*np.pi)
CosS = np.cos(angle/180*np.pi)

v = lambda_mid/grating_const
a = v/2
B = np.sqrt(a**2 - (v**2 - SinS**2)/(2*(1+CosS)))
sinB_new = a - B
Grating_normal = (np.sqrt(1-sinB_new**2), sinB_new, 0)

Grat1 = Grating(grat_const=grating_const, order=-1)
Grat1.pos -=(500-10,0,periscope_height)
Grat1.normal = Grating_normal
Grat1.normal = -Grat1.normal
Plane_height = 23+25.4
Grat2 = Grating(grat_const=grating_const, order=-1)
# propagation_length = 99.9995
# propagation_length = seperation*2-0.0078
# propagation_length = seperation*2-0.008
propagation_length = seperation*2-0.085

# propagation_length = 99.9949
Grat2.pos -= (500-10-propagation_length*CosS,SinS*propagation_length,periscope_height)
Grat2.normal = Grating_normal

shift_direction = np.cross((0,0,1),Grat1.normal)
Grat1.pos += shift_direction * -15
Grat2.pos += shift_direction * 1

"""
# =============================================================================
# Two Gratings Compressor
# =============================================================================
C_RoofTop1 = Mirror()
C_RoofTop1.pos -= (700,SinS*propagation_length,periscope_height)
C_RoofTop1.normal = (-1,0,-1)
C_RoofTop2 = Mirror()
C_RoofTop2.pos -= (700,SinS*propagation_length,0)
C_RoofTop2.normal = (-1,0,1)

C_RoofTop1.draw = dont
C_RoofTop1.mount.elm_type = "dont_draw"
C_RoofTop2.draw = dont
C_RoofTop2.mount.elm_type = "dont_draw"
pure_cosmetic1 = Rooftop_mirror(name="RoofTop_Mirror")
pure_cosmetic1.draw_dict["mount_type"] = "rooftop_mirror_mount"
pure_cosmetic1.pos = (C_RoofTop1.pos + C_RoofTop2.pos ) / 2
pure_cosmetic1.normal = (C_RoofTop1.normal + C_RoofTop2.normal ) / 2
pure_cosmetic1.draw_dict["model_type"] = "Rooftop"
pure_cosmetic1.aperture = periscope_height
"""
# =============================================================================
# Four Gratings Compressor
# =============================================================================
Grat3 =Grating(grat_const=grating_const,order=1)
Grat3.pos = (Grat1.pos[0]-Grat2.pos[0]+Grat1.pos[0]-45-2*35*abs(Grat1.normal[0]),Grat2.pos[1],Grat2.pos[2])
Grat3.normal = (Grat1.normal[0],-Grat1.normal[1],Grat1.normal[2])
Grat4 =Grating(grat_const=grating_const,order=1)
Grat4.pos = (Grat2.pos[0]-Grat2.pos[0]+Grat1.pos[0]-45-2*35*abs(Grat1.normal[0]),Grat1.pos[1],Grat2.pos[2])
Grat4.normal = (Grat2.normal[0],-Grat2.normal[1],Grat2.normal[2])
# Grat3.pos += (1,0,0)
# Grat4.pos -= (1,0,0)

# Grat3.rotate((0,0,1), 0.01)
# Grat4.rotate((0,0,1), 0.01)

Grat1.height=Grat2.height=Grat3.height=Grat4.height=25
Grat1.thickness=Grat2.thickness=Grat3.thickness=Grat4.thickness=9.5
Grat1.set_mount_to_default()
Grat2.set_mount_to_default()
Grat3.set_mount_to_default()
Grat4.set_mount_to_default()
Grat1.Mount.mount_list[1].flip(-90)
Grat2.Mount.mount_list[1].flip(-90)
Grat4.Mount.mount_list[-1]._lower_limit = Plane_height
Grat1.Mount.mount_list[-1]._lower_limit = Plane_height
Grat3.Mount.mount_list[-1]._lower_limit = Plane_height-23
Grat2.Mount.mount_list[-1]._lower_limit = Plane_height-23
Grat1.Mount.mount_list[1].model = "POLARIS-K1E3"
Grat2.Mount.mount_list[1].model = "POLARIS-K1E3"
Grat3.Mount.mount_list[1].model = "POLARIS-K1E3"
Grat4.Mount.mount_list[1].model = "POLARIS-K1E3"
Grat1.Mount.mount_list[1].docking_obj.pos = Grat1.Mount.mount_list[1].pos + Grat1.Mount.mount_list[1].normal*17.1-np.array((0,0,1))*25.4
Grat1.Mount.mount_list[2].set_geom(Grat1.Mount.mount_list[1].docking_obj.get_geom())
Grat2.Mount.mount_list[1].docking_obj.pos = Grat2.Mount.mount_list[1].pos + Grat2.Mount.mount_list[1].normal*17.1-np.array((0,0,1))*25.4
Grat2.Mount.mount_list[2].set_geom(Grat2.Mount.mount_list[1].docking_obj.get_geom())
Grat3.Mount.mount_list[1].docking_obj.pos = Grat3.Mount.mount_list[1].pos + Grat3.Mount.mount_list[1].normal*17.1-np.array((0,0,1))*25.4
Grat3.Mount.mount_list[2].set_geom(Grat3.Mount.mount_list[1].docking_obj.get_geom())
Grat4.Mount.mount_list[1].docking_obj.pos = Grat4.Mount.mount_list[1].pos + Grat4.Mount.mount_list[1].normal*17.1-np.array((0,0,1))*25.4
Grat4.Mount.mount_list[2].set_geom(Grat4.Mount.mount_list[1].docking_obj.get_geom())
PM1=Post_Marker()
PM2=Post_Marker()
Grat2.Mount.add(PM1)
Grat3.Mount.add(PM2)

# print("setting pos=",(Grat1.pos+Grat2.pos+Grat3.pos+Grat4.pos)/4)
ip = Intersection_plane()
ip.pos -= (100,0,0)
# Stretcher.add_fixed_elm(Grat1)
# Stretcher.add_fixed_elm(Grat2)
# Stretcher.add_fixed_elm(Grat3)
# Stretcher.add_fixed_elm(Grat4)
"""
Stretcher.add_fixed_elm(C_RoofTop1)
Stretcher.add_fixed_elm(C_RoofTop2)
"""
# Stretcher.add_fixed_elm(ip_s)
# Stretcher.add_fixed_elm(pure_cosmetic)
# Stretcher.add_fixed_elm(pure_cosmetic1)

# setting the final sequence and the last propagation for visualization
# note that pure cosmetic (pos6) is not in the sequence
# Stretcher.set_sequence([0, 1,2,3,2,1, 4,5, 1,2,3,2,1, 0,6,7,8,9,7,6,10]) #two Gratings Compressor
# Stretcher.set_sequence([0, 1,2,3,2,1, 4,5, 1,2,3,2,1, 0,6,7,8,9])#8,9,10,11]) #four Gratings Compressor
Stretcher.set_sequence([0, 1,2,3,2,1, 4,5, 1,2,3,2,1, 0]) #no compressor
Stretcher.recompute_optical_axis()
Stretcher.pos += (0,0,24)
Stretcher.propagate(500)
# ip=Intersection_plane()
# ip.set_geom(Stretcher.last_geom())
# ip.spot_diagram(Stretcher._beams[-1],aberration_analysis=True)
# ip.draw()

