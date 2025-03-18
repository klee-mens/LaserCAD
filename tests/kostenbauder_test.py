# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 13:42:19 2024

@author: mens
"""
from LaserCAD.freecad_models import clear_doc, setview, freecad_da
from LaserCAD.basic_optics import Mirror, Beam, Composition, inch
from LaserCAD.basic_optics import Curved_Mirror, RainbowBeam
from LaserCAD.basic_optics import Grating
from LaserCAD.basic_optics.mirror import Stripe_mirror
from LaserCAD.moduls import Make_RoofTop_Mirror
from LaserCAD.basic_optics.mount import Unit_Mount, Composed_Mount
from scipy.constants import speed_of_light
import numpy as np


# =============================================================================
# Pure Propagation test
# =============================================================================

translation_comp = Composition()
translation_comp.propagate(300)
print(translation_comp.Kostenbauder_matrix())
print(translation_comp.Kostenbauder_matrix(dimension=6))

output1 = """
[[1.  0.3 0.  0. ]
 [0.  1.  0.  0. ]
 [0.  0.  1.  0. ]
 [0.  0.  0.  1. ]]
[[1.  0.3 0.  0.  0.  0. ]
 [0.  1.  0.  0.  0.  0. ]
 [0.  0.  1.  0.3 0.  0. ]
 [0.  0.  0.  1.  0.  0. ]
 [0.  0.  0.  0.  1.  0. ]
 [0.  0.  0.  0.  0.  1. ]]"""

print()
print()

# =============================================================================
# Flip Mirror Test
# =============================================================================

flip_mirror_comp = Composition()
flip_mirror_comp.propagate(100)
flip_mirror_comp.add_on_axis(Mirror(phi=90))
flip_mirror_comp.propagate(200)
print(np.round(flip_mirror_comp.Kostenbauder_matrix(), decimals=2))
print(np.round(flip_mirror_comp.Kostenbauder_matrix(dimension=6), decimals=2))

output2 = """
[[1.  0.3 0.  0. ]
 [0.  1.  0.  0. ]
 [0.  0.  1.  0. ]
 [0.  0.  0.  1. ]]
[[ 1.   0.3  0.   0.   0.   0. ]
 [ 0.   1.   0.   0.   0.   0. ]
 [ 0.   0.  -1.  -0.3  0.   0. ]
 [ 0.  -0.   0.  -1.   0.   0. ]
 [ 0.   0.   0.   0.   1.   0. ]
 [ 0.   0.   0.   0.   0.   1. ]]"""

print()
print("The - sign in the y quarter is correct (to our definition), since the mirror flips the y axis")

print()
print()



# =============================================================================
# Stretcher parameter
# =============================================================================

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
lightsource = RainbowBeam(wavelength=lambda_mid, bandwith=delta_lamda, ray_count=number_of_rays)

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
Stretcher.propagate(185)


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


print(Stretcher.Kostenbauder_matrix())
print(Stretcher.Kostenbauder_matrix(dimension=6))

lam0 = lambda_mid * 1e-3
d0 = grating_const * 1e-3
sep = seperation * 1e-3
diffracted_ray = Stretcher._optical_axis[2]
grating = Stretcher._elements[1]
theta = diffracted_ray.angle_to(grating)

GDD = lam0**3 * sep / (np.pi * speed_of_light**2 * d0**2 * np.cos(theta)**2) * 1e30 * 2

kb4 = Stretcher.Kostenbauder_matrix()

print()
print("GDD to Srpinger in fs^2", np.round(GDD), "fs^2")

GDDTill = 4290465 #fs^2

print()
print("GDD to Till App in fs^2", GDDTill, "fs^2")

kostenbauder_gdd = kb4[2,3]
# kostenbauder_gdd *= - (lam0)**2 / (2*np.pi * speed_of_light)
kostenbauder_gdd *= 1 / (2*np.pi)

print()
print("My GDD: ",  np.round(kostenbauder_gdd * 1e30), "fs^2")

print()
print()
print("Now have a closer look on the 6x6 entries:")
print()

kb6 = Stretcher.Kostenbauder_matrix(dimension=6)
dz2_dz = kb6[0,0]
print("dz2_dz: ", dz2_dz, "| Magnification z-z, around 1")

dz2_dalpha = kb6[0,1] * 1e3 # mm
print("dz2_dalpha: ", dz2_dalpha, "mm | Propagation z-alpha, some hundred mm")

dz2_dy = kb6[0,2]
print("dz2_dy: ", dz2_dy, "| Twisting z-y, around 0")

dz2_dbeta = kb6[0,3] * 1e3
print("dz2_dbeta: ", dz2_dbeta, "mm | Twisting propagation z-beta, around 0")

dz2_dt = kb6[0,4] * 1e3
print("dz2_dt: ", dz2_dt, "mm/s | Time dependence z-t, by definition 0")

dz2_dlam = kb6[0,5] * - speed_of_light / lam0**2 * 1e3 / (1e9)
print("dz2_dlam: ", dz2_dlam, "mm/nm | Spatial chirp z-lambda")

# =============================================================================
# Draw section just for fun
# =============================================================================
if freecad_da:
  clear_doc()
  Stretcher.draw()

if freecad_da:
  setview()