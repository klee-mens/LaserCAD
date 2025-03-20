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
print()
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
print("dz2_dlam: ", dz2_dlam, "mm/nm | Spatial chirp z-lambda around 0")


print()


dalpha2_dz = kb6[1,0] * 1e-3 # 1/mm
print("dalpha2_dz: ", dalpha2_dz, "1/mm | Focal power alpha-z, around 0")

dalpha2_dalpha = kb6[1,1] # mm
print("dalpha2_dalpha: ", dalpha2_dalpha, "| Angular magnification alpha-alpha, around 1")

dalpha2_dy = kb6[1,2] * 1e-3
print("dalpha2_dy: ", dalpha2_dy, "1/mm | Twisting focal power alpha-y, around 0")

dalpha2_dbeta = kb6[1,3]
print("dalpha2_dbeta: ", dalpha2_dbeta, "| Twisting angular magnification alpha-beta, around 0")

dalpha2_dt = kb6[1,4]
print("dalpha2_dt: ", dalpha2_dt, "rad/s | Time dependence alpha-t, by definition 0")

dalpha2_dlam = kb6[1,5] * -speed_of_light / lam0**2 / 1e9
print("dalpha2_dlam: ", dalpha2_dlam, "rad/nm | Angular chirp alpha-lambda around 0")


print()


dy2_dz = kb6[2,0]
print("dy2_dz: ", dy2_dz, "| Twisting magnification y-z, around 0")

dy2_dalpha = kb6[2,1] * 1e3 # mm
print("dy2_dalpha: ", dy2_dalpha, "mm | Twisting propagation y-alpha, around 0")

dy2_dy = kb6[2,2]
print("dy2_dy: ", dy2_dy, "| Magnification y-y, around 1")

dy2_dbeta = kb6[2,3] * 1e3
print("dy2_dbeta: ", dy2_dbeta, "mm | Propagation y-beta, some hundred mm")

dy2_dt = kb6[2,4] * 1e3
print("dy2_dt: ", dy2_dt, "mm/s | Time dependence y-t, by definition 0")

dy2_dlam = kb6[2,5] * - speed_of_light / lam0**2 * 1e3 / (1e9)
print("dy2_dlam: ", dy2_dlam, "mm/nm | Spatial chirp y-lambda around 0")


print()


dbeta2_dz = kb6[3,0] * 1e-3 # 1/mm
print("dbeta2_dz: ", dbeta2_dz, "1/mm | Focal power beta-z, around 0")

dbeta2_dalpha = kb6[3,1] # mm
print("dbeta2_dalpha: ", dbeta2_dalpha, "| Twisting angular magnification beta-alpha, around 0")

dbeta2_dy = kb6[3,2] * 1e-3
print("dbeta2_dy: ", dbeta2_dy, "1/mm | Focal power beta-y, around 0")

dbeta2_dbeta = kb6[3,3]
print("dbeta2_dbeta: ", dbeta2_dbeta, "| Angular magnification beta-beta, around 1")

dbeta2_dt = kb6[3,4]
print("dbeta2_dt: ", dbeta2_dt, "rad/s | Time dependence beta-t, by definition 0")

dbeta2_dlam = kb6[3,5] * -speed_of_light / lam0**2 / 1e9
print("dbeta2_dlam: ", dbeta2_dlam, "rad/nm | Angular chirp beta-lambda around 0")


print()


dt2_dz = kb6[4,0] * 1e15/1e3 # fs/mm
print("dt2_dz: ", dt2_dz, "fs/mm | Spatial pulse front tilt t-z, around 0")

dt2_dalpha = kb6[4,1] * 1e15/1e3 # fs/mrad
print("dt2_dalpha: ", dt2_dalpha, "fs/mrad | Angular pulse front tilt t-alpha, around 0")

dt2_dy = kb6[4,2] * 1e15/1e3 # fs/mm
print("dt2_dy: ", dt2_dy, "fs/mm | Spatial pulse front tilt t-y, around 0")

dt2_dbeta = kb6[4,3] * 1e15/1e3 # fs/mrad
print("dt2_dbeta: ", dt2_dbeta, "fs/mrad | Angular pulse front tilt t-beta, around 0")

dt2_dt = kb6[4,4]
print("dt2_dt: ", dt2_dt, "Time dependence t-t, by definition 1")

dt2_dlam = kb6[4,5] / (2*np.pi) * 1e30 # fs^2
print("dt2_dlam: ", dt2_dlam, "fs^2 | Group delay dispersion about 6 orders fs^2")


print()


df2_dz = kb6[5,0]
print("df2_dz: ", df2_dz, "f-z, by definition 0")

df2_dalpha = kb6[5,1]
print("df2_dalpha: ", df2_dalpha, "f-alpha, by definition 0")

df2_dy = kb6[5,2]
print("df2_dy: ", df2_dy, "f-y, by definition 0")

df2_dbeta = kb6[5,3]
print("df2_dbeta: ", df2_dbeta, "f-beta, by definition 0")

df2_dt = kb6[5,4]
print("df2_dt: ", df2_dt, "f-t, by definition 0")

df2_dlam = kb6[5,5]
print("df2_dlam: ", df2_dlam, "f-f, by definition 1")



# =============================================================================
# jetzt wäre es noch cool einen mathematischen beispielstrecker zu konstruieren und daran spatial chirp in y und pulse front zeug auszuprobieren...
# =============================================================================
from LaserCAD.moduls import Make_Stretcher


# plane_stretch = Make_Stretcher(seperation_angle=0,
#                                height_stripe_mirror=0,
#                                safety_to_stripe_mirror=0,
#                                seperation=50)
plane_stretch = Make_Stretcher(radius_concave = 1000, #radius of the big concave sphere
    aperture_concave = 6 * inch,
    height_stripe_mirror = 10, #height of the stripe mirror in mm
    seperation_angle = 20 /180 *np.pi, # sep between in and outgoing middle ray
    # incident_angle = seperation_angle + reflection_angle
    grating_const = 1/1000, # in 1/mm
    seperation = 100, # difference grating position und radius_concave
    lambda_mid = 800e-9 * 1e3, # central wave length in mm
    band_width = 20e-9*1e3, # full bandwith in mm
    number_of_rays = 20,
    safety_to_stripe_mirror = 5, #distance first incomming ray to stripe_mirror in mm
    periscope_height = 10,
    first_propagation = 120, # legnth of the first ray_bundle to flip mirror1 mm
    distance_roof_top_grating = 600)

grat_ps = plane_stretch._elements[0]


kbps, txtps = plane_stretch.Kostenbauder_matrix(dimension=6, text_explanation=True)


print()
print("GDD plane stretcher:", np.round(plane_stretch.GDD*1e30), "fs^2")
print()
print(txtps)


from LaserCAD.moduls import Make_Compressor

# comp = Make_Compressor(seperation=100, seperation_angle=0, height_seperation=0)
comp = Make_Compressor(seperation_angle = 20 /180 *np.pi, # sep between in and outgoing middle ray
    grating_const = 1/1000, # in 1/mm
    seperation = 200, # difference grating position und radius_concave
    lambda_mid = 800e-9 * 1e3, # central wave length in mm
    band_width = 20e-9*1e3, # full bandwith in mm
    number_of_rays = 20,
    height_seperation = 16, # seperation between incomming and outgoing beam,
    first_propagation = 120, # legnth of the first ray_bundle to grating 1 mm
    distance_roof_top_grating = 600,
    grating1_dimensions = (25, 25, 5),
    grating2_dimensions = (50, 50, 5))
kbcomp, txtcomp = comp.Kostenbauder_matrix(dimension=6, text_explanation=True)

print()
print("GDD plane stretcher:", np.round(comp.GDD*1e30), "fs^2")
print()
print(txtcomp)


print()
print()

kbps4 = plane_stretch.Kostenbauder_matrix(reference_axis="y")
kbcomp4 = comp.Kostenbauder_matrix(reference_axis="y")

print(kbps4)
print()
print(kbcomp4)
print()
print(np.matmul(kbcomp4, kbps4))

from copy import deepcopy
cpa_composition = deepcopy(plane_stretch)
cpa_composition.propagate(1000)
old_sequence = cpa_composition.get_sequence()
cpa_composition.add_supcomposition_on_axis(comp)
comp.rotate(vec=(1,0,0), phi=np.pi)
cpa_composition.recompute_optical_axis()
cpa_composition.set_sequence(old_sequence + [5, 6, 7, 8, 6, 5]) # trust me, im an engineer ;)
cpa_composition.propagate(100)


cpaK, cpaT = cpa_composition.Kostenbauder_matrix(reference_axis="y", text_explanation=True)
print()
print()
print(cpaT)


# =============================================================================
# Draw section just for fun
# =============================================================================
if freecad_da:
  clear_doc()
  Stretcher.normal = (0,1,0)
  # Stretcher.draw()

  plane_stretch.pos += (0, 200, 0)
  # plane_stretch.draw()

  # comp.draw()

  cpa_composition.draw()
  # cpa_composition.draw_beams()
  # cpa_composition.draw_elements()
if freecad_da:
  setview()