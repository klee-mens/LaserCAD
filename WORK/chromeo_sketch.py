# -*- coding: utf-8 -*-
"""
Created on Tue Jun 27 22:34:31 2023

@author: mens
"""

import numpy as np
from LaserCAD.freecad_models import clear_doc, setview, freecad_da
from LaserCAD.basic_optics import Mirror, Beam, Composition, inch, RainbowBeam
from LaserCAD.basic_optics import Curved_Mirror, Ray, Component
from LaserCAD.basic_optics import LinearResonator, Lens
from LaserCAD.basic_optics import Grating
import matplotlib.pyplot as plt
from LaserCAD.freecad_models.utils import thisfolder, load_STL
from LaserCAD.non_interactings import Faraday_Isolator, Pockels_Cell, Lambda_Plate, Crystal, Iris
from LaserCAD.basic_optics.mirror import Stripe_mirror
from LaserCAD.moduls import Make_RoofTop_Mirror
from LaserCAD.basic_optics.mount import Unit_Mount, Composed_Mount
from LaserCAD.non_interactings.table import Table

if freecad_da:
  clear_doc()

# a1=0.314258136824135*1000
# b1=1.65864036470845*1000

# =============================================================================
# Measured Coordinates on the Table (approx to unity m6 holes)
# =============================================================================
POS_SEED = np.array((25, 59-8, 0)) * 25  + np.array((0,0,100))
POS_STRETCHER_END_MIRROR = np.array((33, 59-15, 0)) * 25  + np.array((0,0,100))
POS_THULIUM_BIG_OUT = np.array((96, 59-11, 0)) * 25  + np.array((0,0,100))
POS_THULIUM_SMALL_OUT = np.array((104, 59-49, 0)) * 25 + np.array((0,0,100))

TABLE_MAX_COORDINATES = np.array((158, 58)) * 25

stretcher_out_obj = Lens(name="Stretcher_Output")
stretcher_out_obj.pos = POS_STRETCHER_END_MIRROR

tm_big_obj = Lens(name="TmLaser_Big_Output")
tm_big_obj.pos = POS_THULIUM_BIG_OUT

tm_small_obj = Lens(name="TmOszillator_Output")
tm_small_obj.pos = POS_THULIUM_SMALL_OUT

# =============================================================================
# Draw the seed laser and seed beam
# =============================================================================
start_point = np.array((0,0,4)) + POS_SEED #see CLPF-2400-10-60-0_8 sn2111348_Manual
seed_beam_radius = 2.5/2 #see CLPF-2400-10-60-0_8 sn2111348_Manual
distance_6_mm_faraday = 45 + 55
distance_faraday_mirror = 100

seed_laser = Component(name="IPG_Seed_Laser")

stl_file=thisfolder+"\misc_meshes\Laser_Head-Body.stl"
seed_laser.draw_dict["stl_file"]=stl_file
color = (170/255, 170/255, 127/255)
seed_laser.draw_dict["color"]=color
seed_laser.freecad_model = load_STL

faraday_isolator_6mm = Faraday_Isolator()

Seed = Composition(name="Seed")
# Seed.normal = (1,2,0)
Seed.pos = start_point
Seed.set_light_source(Beam(angle=0, radius=seed_beam_radius))
Seed.add_on_axis(seed_laser)
Seed.propagate(distance_6_mm_faraday)
Seed.add_on_axis(faraday_isolator_6mm)
Flip0 = Mirror(phi=-90)
Seed.propagate(distance_faraday_mirror)
Seed.add_on_axis(Flip0)
Seed.propagate(50)
Seed.add_on_axis(Lambda_Plate())
Seed.propagate(223)
# seed_end_geom = Seed.last_geom()
# print(faraday_isolator_6mm.pos)
# =============================================================================
# Create and draw the stretcher
# =============================================================================


# def dont():
#   return None

# =============================================================================
# Stretcher parameter
# =============================================================================

## def Make_Stretcher_chromeo():
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

Stretcher.set_geom(Seed.last_geom())



# =============================================================================
# folded Resonator
# =============================================================================
# calculus
# A_target = 4.908738521234052 #from gain simlutation area in mm^2
focal = 2500
lam_mid = 2.4e-3
# A_natural = lam_mid * focal
# geometrie_factor = A_target / A_natural
regen_helf_length = focal / 2
tfp_push_aside = 5 # distance in mm to push the TFP aside, so that the beam can pass through

# design params
width_pz = 80
dist_mir_pz = 20 + width_pz
dist_pz_lambda = 115 - width_pz
dist_lambda_tfp = 70
dist_tfp_fold1 = 65
# dist_fold1_fold2 = 300
dist_crystal_end = 20
last = regen_helf_length - dist_mir_pz - dist_pz_lambda - dist_lambda_tfp -dist_tfp_fold1
tfp_aperture = 2*inch
tfp_angle = 65
tfp_thickness = 6.35
regen_dist_end_mir_to_flip1 = 550
regen_dist_flip1_flip2 = 150


# optics

cm0 = Curved_Mirror(radius=focal*2, phi = 180, name="Curved_Far")
mir1 = Mirror(phi=-90, name="Dichroit")
mir1.draw_dict["color"] = (0.8, 0.6, 0.1)

regen_flip1 = Mirror(name="Flip1", phi=-90)
regen_flip2 = Mirror(name="Flip2", phi=-90)


TFP_Amp1 = Mirror(phi= 180 - 2*tfp_angle, name="TFP_Amp1")
TFP_Amp1.draw_dict["color"] = (1.0, 0.0, 2.0)
TFP_Amp1.aperture = tfp_aperture
TFP_Amp1.thickness = tfp_thickness
TFP_Amp1.set_mount_to_default()
pol_mount = TFP_Amp1.Mount.mount_list[0]
pol_mount.flip()
# TFP_Amp1.mount_dict["Flip90"]=True

cm = Curved_Mirror(radius=focal*2, phi = 180, name="Curved_PZ")
PockelsCell = Pockels_Cell(name="PockelZelleRes1")
Lambda_Regen = Lambda_Plate()
fold1 = Mirror(phi=90)

regen_laser_crys = Crystal(width=6, thickness=10, n=2.45)

simres = LinearResonator(name="Regen")
simres.set_wavelength(lam_mid)
simres.add_on_axis(cm0)
simres.propagate(regen_helf_length-regen_dist_end_mir_to_flip1-regen_dist_flip1_flip2)
simres.add_on_axis(regen_flip1)
simres.propagate(regen_dist_end_mir_to_flip1)
simres.add_on_axis(regen_flip2)
simres.propagate(regen_dist_flip1_flip2)
simres.add_on_axis(mir1)
simres.propagate(dist_crystal_end)
simres.add_on_axis(regen_laser_crys)
simres.propagate(last-dist_crystal_end)
simres.add_on_axis(fold1)
simres.propagate(dist_tfp_fold1)
simres.add_on_axis(TFP_Amp1)
simres.propagate(dist_lambda_tfp)
simres.add_on_axis(Lambda_Regen)
simres.propagate(dist_pz_lambda)
simres.add_on_axis(PockelsCell)
simres.propagate(dist_mir_pz)
simres.add_on_axis(cm)
simres.compute_eigenmode()

# Amplifier_I = Make_Amplifier_I()
Amplifier_I = simres
# Amplifier_I.set_input_coupler_index(1, False)
# ppos, paxes = Pump.last_geom()

Amplifier_I.set_input_coupler_index(5)
# Amplifier_I.set_geom(Pump.last_geom())
# Amplifier_I.pos = ppos


# =============================================================================
# Amp1 Mode
# =============================================================================
amp_len = [x.length  for x in Amplifier_I._optical_axis]
s1 = amp_len[Amplifier_I._input_coupler_index+1]
s2 = sum(amp_len[0:Amplifier_I._input_coupler_index+1])


def MatProp(x):
  mat = np.eye(2)
  mat[0,1] = x
  return mat

def MatCm(R):
  mat = np.eye(2)
  mat[1,0] = -2/R
  return mat

MatRes = MatProp(s2) @ MatCm(2*focal) @ MatProp(s2) @ MatProp(s1) @ MatCm(2*focal) @ MatProp(s1)

[[A,B], [C,D]] = MatRes

z2 = (A-D) / 2 / C
r2 = abs(1/2/C) * np.sqrt(4 - (A+D)**2)



# =============================================================================
# complicated calculation for compensation
# =============================================================================
# PropA = 1695.724204685186
adapt_a2b2 = 220
adapt_a1 = 70
adapt_out_mirror_diff = - 64
adapt_last_prop = 130
PropA = Seed.optical_path_length() + Stretcher.matrix()[0,1] + adapt_a1 + adapt_a2b2

adapt_focal = 479.3

a = PropA
f = adapt_focal
r1 = 2.5**2 * np.pi / 4 / 2.4e-3

v = r1/r2
al = 1 - a/f
ph = 1/f

p = al / (al**2 + ph**2 * r1**2)
q = (1-v) / (al**2 + ph**2 * r1**2)

x1 = -p + np.sqrt(p**2 - q)
x2 = -p - np.sqrt(p**2 - q)
x = x1

def bet(x):
  nen = (1 + al*x)**2 + (ph*x*r1)**2
  return (z2*nen +f*al*(1+al*x) + ph*x*r1**2) / ((1+al*x)**2*f + ph*x**2*r1**2 ) * -1

delta = x*f
beta = bet(x)
b = f*(1-beta )
PropB = b

# Test
L = 2*f + delta

def Kogel(mat, q):
  return (mat[0,0]*q + mat[0,1]) / (mat[1,0]*q + mat[1,1])

q1 = 0 + 1j*r1
q2 = z2 + 1j*r2

mattele = MatProp(b) @ MatCm(2*f) @ MatProp(2*f+delta) @MatCm(2*f) @ MatProp(a)

# print("q1", q1)
# print("q2", q2)
# print("Kogelnik", Kogel(mattele, q1))

# print()
# print("delta:", delta)
# print("b:", b)
 

def complete_solver_del_b(a=1695.7, f=1029, r1=2045.3, r2=2165, z2=1045):
  v = r1/r2
  al = 1 - a/f
  ph = 1/f
  
  p = al / (al**2 + ph**2 * r1**2)
  q = (1-v) / (al**2 + ph**2 * r1**2)
  
  x1 = -p + np.sqrt(p**2 - q)
  x2 = -p - np.sqrt(p**2 - q)
  x = x1
  
  bet1 = (z2*v +f*al*(1+al*x) + ph*x*r1**2) / ((1+al*x)**2*f + ph*x**2*r1**2 ) * -1
  
  x = x2
  bet2 = (z2*v +f*al*(1+al*x) + ph*x*r1**2) / ((1+al*x)**2*f + ph*x**2*r1**2 ) * -1
  
  delta1 = x1*f
  delta2 = x2*f
  b1 = f*(1-bet1)
  b2 = f*(1-bet2)
  return [(delta1, b1), (delta2, b2)]

a = np.linspace(PropA*0.9, PropA*1.5, 2000)

[(delta1, b1), (delta2, b2)] = complete_solver_del_b(a=a)


# import matplotlib.pyplot as plt
# plt.figure()
# plt.plot(a, b1)
# plt.plot(PropA, complete_solver_del_b(a=PropA)[0][1], "-xk" )


# =============================================================================
# AdaptTeles
# =============================================================================



AdaptTeles = Composition(name="ModeAdaptionTelescope")

AdaptTeles.propagate(adapt_a1)
AdaptTeles.add_on_axis(Mirror(phi=90))
AdaptTeles.propagate(adapt_a2b2)

L1 = Lens(f=adapt_focal)
AdaptTeles.add_on_axis(L1)
L1.pos += L1.get_coordinate_system()[1]*5.1
AdaptTeles.recompute_optical_axis()
AdaptTeles.propagate(adapt_focal + delta/2)

M_tele = Mirror()
AdaptTeles.add_on_axis(M_tele)
M_tele.normal = L1.normal

AdaptTeles.set_sequence([0,1,2,1])
AdaptTeles.recompute_optical_axis()
AdaptTeles.propagate(adapt_a2b2 + adapt_out_mirror_diff)
M_tele2 = Mirror(phi = 90)
M_tele2.set_mount(Composed_Mount(unit_model_list=["MH25_KMSS", "1inch_post"]))
AdaptTeles.add_on_axis(M_tele2)
M_tele2.pos += M_tele2.get_coordinate_system()[1] * -6.2
AdaptTeles.propagate(adapt_last_prop)

AdaptTeles.set_geom(Stretcher.last_geom())
AdaptTeles._lightsource.draw_dict["model"] = "ray_group"





# =============================================================================
# The pulse picker
# =============================================================================

class K1_Mirror(Mirror):
  def __init__(self, phi=180, theta=0, **kwargs):
    super().__init__(phi=phi, theta=theta, **kwargs)
    self.set_mount(Composed_Mount(["KS1", "1inch_post"]))
    
tfp_angle = 65 #tfp angle of incidence in degree
flip_mirror_push_down = 8 # distance to push the first mirror out ouf the seed beam
tfp_push_aside = 5 # distance in mm to push the TFP aside, so that the beam can pass through

PulsePicker = Composition(name="PulsePicker")
# PulsePicker.set_geom(Stretcher.last_geom())
PulsePicker.set_geom(AdaptTeles.last_geom())

# polarisation optics up to pockels cell
PulsePicker.propagate(136-12.5)
Lambda2 = Lambda_Plate()
PulsePicker.add_on_axis(Lambda2)
PulsePicker.propagate(330)
Back_Mirror_PP = Mirror()
PulsePicker.add_on_axis(Back_Mirror_PP)
PulsePicker.propagate(30)
Lambda4 = Lambda_Plate()
PulsePicker.add_on_axis(Lambda4)
PulsePicker.propagate(30)
pockelscell = Pockels_Cell()
PulsePicker.add_on_axis( pockelscell)
pockelscell.rotate(vec=pockelscell.normal,phi=np.pi*-0.5)
PulsePicker.propagate(150)

# Splitting TFP
TFP_pp = Mirror(phi = 180-2*tfp_angle, name="TFP_p")
TFP_pp.draw_dict["color"] = (1.0, 0.0, 2.0)
TFP_pp.draw_dict["thickness"] = 4
TFP_pp.aperture = 2*inch
# TFP_pp.thickness = tfp_thickness
TFP_pp.set_mount_to_default()
# TFP_out.mount_dict["Flip90"]=True
PulsePicker.add_on_axis(TFP_pp)
x,y,z = TFP_pp.get_coordinate_system()
TFP_pp.pos += y * tfp_push_aside


# Spacer Stage for adapting the real part of the beam to the regen
PulsePicker.propagate(70)
PulsePicker.add_on_axis(Iris())
PulsePicker.propagate(70)
FlipMirror2_pp = K1_Mirror(phi=90)
PulsePicker.add_on_axis(FlipMirror2_pp)

# delay stage
pp_delay_stage_length = 540
PulsePicker.propagate(pp_delay_stage_length)
PulsePicker.add_on_axis(K1_Mirror(phi=-90))
PulsePicker.propagate(60)
PulsePicker.add_on_axis(K1_Mirror(phi=-90))
PulsePicker.propagate(pp_delay_stage_length-60)
PulsePicker.add_on_axis(K1_Mirror(phi=90))


# PulsePicker.propagate(385)

# Output Stage bevore the RegenAmp
pp_dist_last_flip_mirror_to_lambda3 = 40
pp_dist_lambda3_to_tfp_out = 100
pp_dist_tfp_out_to_lambda4 = 70
pp_dist_lambda4_to_faraday_rot = 50
pp_dist_faraday_rot_to_regen_in = 150

pp_last_prop = PropB - PulsePicker.optical_path_length() -adapt_a2b2 - pp_dist_last_flip_mirror_to_lambda3 - adapt_last_prop -pp_dist_lambda3_to_tfp_out - pp_dist_tfp_out_to_lambda4 - pp_dist_lambda4_to_faraday_rot - pp_dist_faraday_rot_to_regen_in
PulsePicker.propagate(pp_last_prop)

last_flip_pp = K1_Mirror(phi=90)
PulsePicker.add_on_axis(last_flip_pp)
PulsePicker.propagate(pp_dist_last_flip_mirror_to_lambda3)

PulsePicker.add_on_axis(Lambda_Plate())
PulsePicker.propagate(pp_dist_lambda3_to_tfp_out)

# Output TFP to send the beam to Amp2
TFP_out = Mirror(phi = -180+2*tfp_angle, name="Output_to_Amp2")
TFP_out.draw_dict["color"] = (1.0, 0.0, 2.0)
TFP_out.draw_dict["thickness"] = 4
TFP_out.aperture = 2*inch
TFP_out.thickness = tfp_thickness
TFP_out_Mount = Composed_Mount(["KS2", "1inch_post"])
TFP_out.set_mount(TFP_out_Mount)
TFP_out.Mount.mount_list[0].flip()
TFP_out.next_ray = TFP_out.just_pass_through
PulsePicker.add_on_axis(TFP_out)
TFP_out.normal = TFP_pp.normal
TFP_out.rotate((0,0,1), phi=np.pi/2)
x,y,z = TFP_out.get_coordinate_system()
TFP_out.pos += - y * tfp_push_aside
PulsePicker.propagate(pp_dist_tfp_out_to_lambda4) # maybe just use the thickness of the energy detector everytime instead ...

Lambda2_2_pp = Lambda_Plate()
PulsePicker.add_on_axis(Lambda2_2_pp)
PulsePicker.propagate(pp_dist_lambda4_to_faraday_rot)
FaradPP = Faraday_Isolator()
PulsePicker.add_on_axis(FaradPP)
PulsePicker.propagate(pp_dist_faraday_rot_to_regen_in)


PulsePicker._lightsource.draw_dict["model"] = "ray_group"


Amplifier_I.set_geom(PulsePicker.last_geom())




# =============================================================================
# Output Beam to Amp2
# =============================================================================
bs = PulsePicker.compute_beams()
b_pp_end = bs[-1]
r_pp_end = b_pp_end.inner_ray()
Out_Beam0 = Beam(radius=2, name="Beam_to_Amp2")
Out_Beam0.draw_dict["color"] = (1.0, 0.5, 0.5)
Out_Beam0.pos = r_pp_end.endpoint()
Out_Beam0.normal = -b_pp_end.normal
helper_mirror = Mirror()
helper_mirror.set_geom(TFP_out.get_geom())
Out_Beam1 = helper_mirror.next_beam(Out_Beam0)








# =============================================================================
# 4pass Relay Imaging Amp2
# =============================================================================

focal = 300
sep_angle_A2 = -5
bigcrys = Crystal(width=20, thickness=15, n=2.45)
source = Beam(radius=1.4, angle=0)
telesf1 = -75
telesf2 = 270
knee_shift_amp2 = -220
# knee_shift_amp2 = 150

#Telescope for beam widening
Amp2 = Composition(name="RelayTyp2")
Amp2.set_light_source(source)

Amp2.propagate(257)
Amp2.add_on_axis(Mirror(phi=-90))

Amp2.propagate(200)
teles_lens1 = Lens(f=telesf1)
Amp2.add_on_axis(teles_lens1)
Amp2.propagate(telesf1 + telesf2)
teles_lens2 = Lens(f=telesf2)
Amp2.add_on_axis(teles_lens2)


# # Knee for adjustments
# Amp2.propagate(90)
# Amp2.add_on_axis(Mirror(phi=90*np.sign(knee_shift_amp2)))
# Amp2.propagate(np.abs(knee_shift_amp2))
# Amp2.add_on_axis(Mirror(phi=-90*np.sign(knee_shift_amp2)))
Amp2.propagate(680)

# AmpTyp2 with for passes, that will definitely fail
Amp2.add_on_axis(bigcrys)
Amp2.propagate(20)
active_mir = Mirror(phi=180-sep_angle_A2)
Amp2.add_on_axis(active_mir)
Amp2.propagate(focal*2)
concave1 = Curved_Mirror(radius=focal*2, phi=180+sep_angle_A2)
# concave1 = Mirror(phi=180+sep_angle_A2)
Amp2.add_on_axis(concave1)
Amp2.propagate(2*focal)
end_concave= Curved_Mirror(radius=focal, phi=180-sep_angle_A2)
# end_concave= Mirror(phi=180-sep_angle_A2)
Amp2.add_on_axis(end_concave)
Amp2.propagate(2*focal)
concave2 = Curved_Mirror(radius=focal*2, phi=180+sep_angle_A2)
# concave2 = Mirror(phi=180+sep_angle_A2)
Amp2.add_on_axis(concave2)
concave2.set_normal_with_2_points(end_concave.pos, active_mir.pos)

# Amp2.set_sequence([0,1,2,3, 4,5,6,7,4   ])
# Amp2.set_sequence([0,1,2,3,4, 5,6,7,8,5   ])
Amp2.set_sequence([0,1,2, 3,4,5,6,3   ])
Amp2.recompute_optical_axis()

a2_safe_angle_for_non_colliding_with_crystal = 2
Amp2.propagate(580)
Amp2.add_on_axis(Mirror(phi=180 - sep_angle_A2 + a2_safe_angle_for_non_colliding_with_crystal-3))
Amp2.propagate(580)

Amp2.add_on_axis(Mirror(phi=90 - a2_safe_angle_for_non_colliding_with_crystal+3))
Amp2.propagate(400)
Beam_Splitter = Mirror(phi=90, name="BeamSplitter")
Beam_Splitter.aperture= 2*inch
Beam_Splitter.set_mount_to_default() # should really automatize this...
Beam_Splitter.draw_dict["color"] = (100/255, 200/255, 240/255)
Amp2.add_on_axis(Beam_Splitter)
Amp2.propagate(20)

Amp2.set_geom(Out_Beam1.get_geom())







# =============================================================================
# breadboards
# =============================================================================
# from LaserCAD.non_interactings import Breadboard
# StartPos = (-700, -450, 0)
# b1 = Breadboard()
# b1.pos += StartPos
# b1.draw()
# b2= Breadboard()
# b2.pos += b1.pos + (b2.Xdimension, 0, 0)
# b2.draw()
# b3= Breadboard()
# b3.pos += b1.pos + (0, b2.Ydimension, 0)
# b3.draw()
# b4= Breadboard()
# b4.pos += b1.pos + (b2.Xdimension, b2.Ydimension, 0)
# b4.draw()
# b5= Breadboard()
# b5.pos += b1.pos + (0, -b2.Ydimension, 0)
# b5.draw()
# b6= Breadboard()
# b6.pos += b1.pos + (b2.Xdimension, -b2.Ydimension, 0)
# b6.draw()



# =============================================================================
# Pump Amp1
# =============================================================================

Pump = Composition(name="JuergenTmPump1")
Pump.pos = regen_laser_crys.pos

pump_bema = Beam(radius=1.7)
pump_bema.draw_dict["color"] = (1.0, 1.0, 0.0)
Pump.set_light_source(pump_bema)

Pump.propagate(240)
Pump.add_on_axis(Mirror(phi=-90))
ep = Pump.last_geom()[0]
Pump.propagate(abs(ep[1] - tm_small_obj.pos[1]))
Pump.add_on_axis(Mirror(phi=90))
Pump.propagate(abs(ep[0] - tm_small_obj.pos[0]))




# =============================================================================
# big_pump
# =============================================================================
big_pump_ls = Beam(radius=6, angle=0)
big_pump_ls.draw_dict["color"] = (1.0,1.0,0.0)
BigPump = Composition("Big_Pump")
BigPump.set_light_source(big_pump_ls)
BigPump.pos = bigcrys.pos

dx, dy, dz = POS_THULIUM_BIG_OUT - bigcrys.pos

BigPump.propagate(dx - 50)
BigPump.add_on_axis(Mirror(phi=90))
BigPump.propagate(dy)
BigPump.add_on_axis(Mirror(phi=-90))
BigPump.propagate(50)




# =============================================================================
# Compressor
# =============================================================================

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

Compressor= Composition()
Compressor.set_light_source(lightsource)
angle = 10
SinS = np.sin(angle/180*np.pi)
CosS = np.cos(angle/180*np.pi)

v = lambda_mid/grating_const
a = v/2
B = np.sqrt(a**2 - (v**2 - SinS**2)/(2*(1+CosS)))
sinB_new = a - B
Grating_normal = (np.sqrt(1-sinB_new**2), sinB_new, 0)

Grat1 = Grating(grat_const=grating_const, order=-1)
Grat1.pos -=(500-10,0,0)
Grat1.normal = Grating_normal
Grat1.normal = -Grat1.normal
Plane_height = 23+25.4
Grat2 = Grating(grat_const=grating_const, order=-1)
# propagation_length = 99.9995
# propagation_length = seperation*2-0.0078
propagation_length = seperation*2-0.008

# propagation_length = 99.9949
Grat2.pos -= (500-10-propagation_length*CosS,SinS*propagation_length,0)
Grat2.normal = Grating_normal

shift_direction = np.cross((0,0,1),Grat1.normal)
Grat1.pos += shift_direction * -15
Grat2.pos += shift_direction * 1

Grat1.pos += (1000,0,0)
Grat2.pos += (1000,0,0)





# =============================================================================
# Four Gratings Compressor
# =============================================================================
Grat3 =Grating(grat_const=grating_const,order=-1)
Grat3.pos = (Grat1.pos[0]-Grat2.pos[0]+Grat1.pos[0]-45-2*35*abs(Grat1.normal[0]),Grat2.pos[1],Grat2.pos[2])
Grat3.normal = (Grat1.normal[0],-Grat1.normal[1],Grat1.normal[2])
Grat4 =Grating(grat_const=grating_const,order=-1)

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
Grat3.Mount.mount_list[-1]._lower_limit = Plane_height-23+25
Grat2.Mount.mount_list[-1]._lower_limit = Plane_height-23+25
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
# PM1=Post_Marker()
# PM2=Post_Marker()
# Grat2.Mount.add(PM1)
# Grat3.Mount.add(PM2)

# print("setting pos=",(Grat1.pos+Grat2.pos+Grat3.pos+Grat4.pos)/4)
# ip = Intersection_plane()
# ip.pos -= (100,0,0)
Compressor.add_fixed_elm(Grat4)
Compressor.add_fixed_elm(Grat3)
Compressor.add_fixed_elm(Grat2)
Compressor.add_fixed_elm(Grat1)
Compressor.propagate(300)
Compressor.set_geom(Amp2.last_geom())




# =============================================================================
# KLT Tm-Pumplaser
# =============================================================================
klt_laser = Component(name="KLT Tm-Pumplaser")
stl_file=thisfolder+"\misc_meshes\Pump_laser.stl"
klt_laser.draw_dict["stl_file"]=stl_file
color = (130/255, 130/255, 230/255)
klt_laser.draw_dict["color"]=color
klt_laser.freecad_model = load_STL

klt_beam = Beam()
klt_beam.draw_dict["color"] = (1.0,0.9,0.0)

klt_pump = Composition(name="klt_pump")
klt_pump.set_light_source(klt_beam)

klt_pump.propagate(130)
klt_pump.add_on_axis(Mirror(phi=-90))
klt_pump.propagate(290)
klt_pump.add_on_axis(Mirror(phi=-90))
klt_pump.propagate(100)
klt_pump.add_on_axis(klt_laser)
klt_laser.rotate((0,0,1), np.pi)

klt_pump.pos = regen_laser_crys.pos



# =============================================================================
# Draw Selection
# =============================================================================

Seed.draw()
Stretcher.draw()
AdaptTeles.draw()
PulsePicker.draw()
# Amplifier_I.draw()
# klt_pump.draw()

# Out_Beam0.draw()
# Out_Beam1.draw()

# Amp2.draw()

# Pump.draw()
# BigPump.draw()
# Table().draw()
# Compressor.draw()

# # PulsePicker.draw_alignment_posts()


# stretcher_out_obj.draw()
# tm_big_obj.draw()
# tm_small_obj.draw()

#PulsePicker.draw_alignment_posts()




# from LaserCAD.basic_optics import Gaussian_Beam
# from copy import deepcopy

# gb = Gaussian_Beam()
# gb.wavelength = 2.4E-3
# gb.q_para =  2045.3077171808552j
# gb.draw_dict["model"]= "cone"
# Seed.set_light_source(gb)

# Seed.compute_beams()
# last_gb1 = Seed._beams[-1]

# def next_gaussian_beam(last_gb=Gaussian_Beam()):
#   next_gb = deepcopy(last_gb)
#   next_gb.q_para += last_gb.length
#   next_gb.pos = last_gb.endpoint()
#   return next_gb

# Stretcher.set_light_source(next_gaussian_beam(last_gb1))
# Stretcher.compute_beams()
# last_gb2 = Stretcher._beams[-1]
# PulsePicker.set_light_source(next_gaussian_beam(last_gb2))
# # PulsePicker.compute_beams()
# # last_gb3 = PulsePicker._beams[-1]
# # Amplifier_I.set_light_source(next_gaussian_beam(last_gb3))

# amp1_lengths = [r.length for r in Amplifier_I._optical_axis]
# s2 = sum(amp1_lengths[0:4])
# s1 = amp1_lengths[4]

# def PropMat(s):
#   mat = np.eye(2)
#   mat[0,1] = s
#   return mat

# def Curved(R):
#   mat = np.eye(2)
#   mat[1,0] = -2/R
#   return mat

# ResonMat = PropMat(s2) @ Curved(5000) @ PropMat(s2) @ PropMat(s1) @ Curved(5000) @ PropMat(s1)

# def Kogel(Mat ,q):
#   return (Mat[0,0] *q + Mat[0,1]) / ( Mat[1,0] *q + Mat[1,1] )


# [[A,B], [C,D]] = ResonMat

# zamp = (A-D) / 2 / C

# zrayamp = np.sqrt(4-(A+D)**2) / 2 / C
# zrayamp = np.abs(zrayamp)



# resonator_overlay_beams = []
# b0 = deepcopy(PulsePicker._beams[-1])
# b0.draw_dict["color"] = (0.2,0.2,0.8)

# resonator_overlay_beams.append(b0)

# b1 = Amplifier_I._elements[-1].next_beam(b0)
# resonator_overlay_beams.append(b1)

# b2 = Amplifier_I._elements[-2].next_beam(b1)
# resonator_overlay_beams.append(b2)

# b3 = Amplifier_I._elements[-3].next_beam(b2)
# resonator_overlay_beams.append(b3)

# b4 = Amplifier_I._elements[-4].next_beam(b3)
# resonator_overlay_beams.append(b4)

# for beeem in resonator_overlay_beams:
#   beeem.draw()


if freecad_da:
  setview()