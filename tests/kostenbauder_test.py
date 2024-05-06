# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 13:42:19 2024

@author: mens
"""

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
from LaserCAD.basic_optics import Curved_Mirror, Ray
from LaserCAD.basic_optics import Grating
from LaserCAD.basic_optics.mirror import Stripe_mirror
from LaserCAD.moduls import Make_RoofTop_Mirror
from LaserCAD.basic_optics.mount import Unit_Mount, Composed_Mount
import numpy as np
import matplotlib.pyplot as plt


if freecad_da:
  clear_doc()

# =============================================================================
# Stretcher parameter
# =============================================================================

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
grating_const = 1/450 # in mm (450 lines per mm)
seperation = 135 # difference grating position und radius_concave
lambda_mid = 2400e-9 * 1e3 # central wave length in mm
delta_lamda = 200e-9*1e3 # full bandwith in mm
number_of_rays = 20
safety_to_stripe_mirror = 5 #distance first incomming ray to stripe_mirror in mm
periscope_height = 15
periscope_height = 0
first_propagation = 20 # legnth of the first ray_bundle to flip mirror1 mm
distance_flip_mirror1_grating = 300-85
distance_roof_top_grating = 600

# calculated parameters according to the grating equation
v = lambda_mid/grating_const
s = np.sin(seperation_angle)
c = np.cos(seperation_angle)
a = v/2
b = np.sqrt(a**2 - (v**2 - s**2)/(2*(1+c)))
sinB = a - b
print(sinB)
grating_normal = (np.sqrt(1-sinB**2), sinB, 0)

Concav = Curved_Mirror(radius=radius_concave, name="Big_Concav_Mirror")
Concav.aperture = aperture_concave
Concav.set_mount_to_default()

StripeM = Stripe_mirror(radius= -radius_concave/2,thickness=25,  name="Stripe_Mirror")
#Cosmetics
StripeM.aperture = width_stripe_mirror
StripeM.draw_dict["height"] = height_stripe_mirror
StripeM.draw_dict["thickness"] = 25 # arbitrary
# StripeM.thickness = 25
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
mid_ray = Ray() # add additionally the 2400 nm mid lambda beam to be the inner ray, just cause
mid_ray.wavelength = lambda_mid
rays = [mid_ray] + rays
lightsource.override_rays(rays)
lightsource.draw_dict['model'] = "ray_group"

# starting the real stretcher
Stretcher = Composition(name="DerStrecker")
Stretcher.set_light_source(lightsource)
Stretcher.redefine_optical_axis(helper_light_source.inner_ray())

Stretcher.propagate(first_propagation)
FlipMirror_In_Out = Mirror(phi=100, name="FlipMirrorInOut")
FlipMirror_In_Out.set_mount(Composed_Mount(unit_model_list = ["MH25_KMSS","1inch_post"]))

mount=Composed_Mount()
Mount1=Unit_Mount(model="MH25")
Mount1.docking_obj.pos = Mount1.pos+(6.3,0,0)
Mount1.docking_obj.normal = Mount1.normal
Mount2=Unit_Mount(model="KMSS")
mount.add(Mount1)
mount.add(Mount2)
FlipMirror_In_Out.mount = mount
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
Stretcher.add_supcomposition_on_axis(Make_RoofTop_Mirror(height=periscope_height, up=False))

# setting the final sequence and the last propagation for visualization
# note that pure cosmetic (pos6) is not in the sequence
Stretcher.set_sequence([0, 1,2,3,2,1, 4,5, 1,2,3,2,1, 0])
Stretcher.recompute_optical_axis()
Stretcher.propagate(120)


# last small flip mirror from stretcher with cosmetics
FlipMirror_pp = Mirror(phi=-90, name="Small_Output_Flip")
FlipMirror_pp.set_mount(Composed_Mount(unit_model_list = ["MH25_KMSS","1inch_post"]))
flip_mirror_push_down = - 5 # distance to push the first mirror out ouf the seed beam
Stretcher.add_on_axis(FlipMirror_pp)
FlipMirror_pp.pos += (0,0,flip_mirror_push_down)
Stretcher.propagate(13)


# =============================================================================
# so far for the chromeo stretcher, now comes the calculation
# =============================================================================

from scipy.constants import speed_of_light as c

lam0 = lambda_mid * 1e-3
d0 = grating_const * 1e-3
beams = Stretcher.compute_beams()
b2 = beams[2]
theta = b2.angle_to(Grat)
sep = seperation * 1e-3

GDD = lam0**3 * sep / (np.pi * c**2 * d0**2 * np.cos(theta)**2) * 1e30 * 2

kb = Stretcher.kostenbauder()

print()
print("GDD to Srpinger in fs^2", np.round(GDD))

GDDTill = 4290465 #fs^2

print()
print("GDD to Till App in fs^2", GDDTill)

print()
print("My GDD: ", kb[2,3]/2/np.pi * 1e30)

print()
print("My Kostenbauder Stretcher:")
print(kb)











if freecad_da:
  setview()