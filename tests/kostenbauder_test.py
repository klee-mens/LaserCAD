# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 13:42:19 2024

@author: mens
"""
from LaserCAD.freecad_models import clear_doc, setview, freecad_da
from LaserCAD.basic_optics import Mirror, Beam, Composition, inch, Lens
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
# lens test
# =============================================================================
lens_comp = Composition()
lens_comp.propagate(200)
lens_comp.add_on_axis(Lens())
lens_comp.propagate(200)



# =============================================================================
# grating Test
# =============================================================================
grat_comp = Composition()
grat_comp.propagate(1e-6)
test_grating = Grating(order=-1)

test_grating.normal = (1,1,0)

grat_comp.add_fixed_elm(test_grating)
grat_comp.recompute_optical_axis()
grat_comp.propagate(1e-6)

grat_comp.compute_beams()

r0 = grat_comp._optical_axis[0]
r1 = grat_comp._optical_axis[1]
ew = r0.angle_to(test_grating)
aw = r1.angle_to(test_grating)
A = - np.cos(aw) / np.cos(ew)
D = 1/A
F = r0.wavelength*1e-3 * (np.sin(aw) - np.sin(ew))/3e8/np.cos(aw)
G = (np.sin(ew) - np.sin(aw)) / 3e8 / np.cos(ew) * 1e15 / 1e3

df_dlam = -3e8 / (r0.wavelength *1e-3)**2
F *= df_dlam / 1e9

print()
print()
print()
print()
print()

kb, tx = grat_comp.Kostenbauder_matrix(reference_axis="y", text_explanation=True)
print(tx)

print()
print("A:", A)
print("D:", D)
print("F:", F)
print("G:", G)


print()
print()
print()
print()
print()




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

  plane_stretch.pos += (0, 200, 0)
  # plane_stretch.draw()

  # comp.draw()

  cpa_composition.draw()
  # cpa_composition.draw_beams()
  # cpa_composition.draw_elements()
if freecad_da:
  setview()