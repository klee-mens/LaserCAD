# -*- coding: utf-8 -*-
"""
Created on Tue Jun 27 22:34:31 2023

@author: mens
"""

import numpy as np
from LaserCAD.freecad_models import clear_doc, setview, freecad_da
from LaserCAD.basic_optics import Mirror, Beam, Composition, inch
from LaserCAD.basic_optics import Curved_Mirror, Ray, Component
from LaserCAD.basic_optics import LinearResonator, Lens
from LaserCAD.basic_optics import Grating
import matplotlib.pyplot as plt
from LaserCAD.freecad_models.utils import thisfolder, load_STL
from LaserCAD.non_interactings import Faraday_Isolator, Pockels_Cell, Lambda_Plate, Crystal
from LaserCAD.basic_optics.mirror import Stripe_mirror
from LaserCAD.moduls import Make_RoofTop_Mirror
from LaserCAD.basic_optics.mount import Unit_Mount, Composed_Mount
from LaserCAD.non_interactings.table import Table

if freecad_da:
  clear_doc()

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
stretcher_out_obj.draw()

tm_big_obj = Lens(name="TmLaser_Big_Output")
tm_big_obj.pos = POS_THULIUM_BIG_OUT
tm_big_obj.draw()


tm_small_obj = Lens(name="TmOszillator_Output")
tm_small_obj.pos = POS_THULIUM_SMALL_OUT
tm_small_obj.draw()

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
Seed.propagate(75)
Seed.add_on_axis(Lambda_Plate())
Seed.propagate(200)
seed_end_geom = Seed.last_geom()
# print(faraday_isolator_6mm.pos)
# =============================================================================
# Create and draw the stretcher
# =============================================================================


# def dont():
#   return None

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

Stretcher.set_geom(seed_end_geom)



# =============================================================================
# Pump Amp1
# =============================================================================

X_ADDITIONAL = 0
Y_ADDITIONAL = 80
f1 = -100
f2 = 150

pump_first_prop = 100 + X_ADDITIONAL #in -x
pump_second_prop = 100 + Y_ADDITIONAL # in +y
pump_third_prop = 100 # in -x

# pump_geom = Amplifier_I._elements[-2].get_geom()
Pump = Composition(name="Pump")
Pump.pos = POS_THULIUM_SMALL_OUT
Pump.normal = (-1,0,0)

pump_light = Beam(radius=1.5, angle=0)
pump_light.draw_dict["color"] = (1.0, 1.0, 0.0)
Pump.set_light_source(pump_light)


Pump.propagate(pump_first_prop)
Pump.add_on_axis(Mirror(phi=-90))
Pump.propagate(pump_second_prop)
Pump.add_on_axis(Mirror(phi=+90))
Pump.propagate(pump_third_prop)

# Pump.add_on_axis(Lens(f=f1))
Pump.propagate(f1+f2*0.5)
Pump.propagate(f1+f2*0.5)
# Pump.add_on_axis(Lens(f=f2))
Pump.propagate(190)


# =============================================================================
# even simpler Res
# =============================================================================
# calculus
# A_target = 4.908738521234052 #from gain simlutation area in mm^2
focal = 2500
lam_mid = 2.4e-3
# A_natural = lam_mid * focal
# geometrie_factor = A_target / A_natural
total_length = focal / 2
tfp_push_aside = 5 # distance in mm to push the TFP aside, so that the beam can pass through

# design params
width_pz = 80
dist_mir_pz = 20 + width_pz
dist_pz_lambda = 115 - width_pz
dist_lambda_tfp = 70
dist_tfp_fold1 = 65
# dist_fold1_fold2 = 300
dist_crystal_end = 20
last = total_length - dist_mir_pz - dist_pz_lambda - dist_lambda_tfp -dist_tfp_fold1
tfp_aperture = 2*inch
tfp_angle = 65
tfp_thickness = 6.35


# optics

cm0 = Curved_Mirror(radius=focal*2, phi = 180, name="Curved_Far")
mir1 = Mirror(phi=180 + 7, name="Dichroit")
mir1.aperture = 0.5 * inch
mir1.set_mount_to_default()

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


simres = LinearResonator(name="Regen")
simres.set_wavelength(lam_mid)

simres.add_on_axis(cm0)
simres.propagate(total_length)

simres.add_on_axis(mir1)

simres.propagate(dist_crystal_end)
laser_crys = Crystal(width=6, thickness=10, n=2.45)
simres.add_on_axis(laser_crys)

simres.propagate(last-dist_crystal_end)

simres.add_on_axis(fold1)

simres.propagate(dist_tfp_fold1)

simres.add_on_axis(TFP_Amp1)
# x,y,z = TFP_Amp1.get_coordinate_system()
# TFP_Amp1.pos += y * tfp_push_aside

simres.propagate(dist_lambda_tfp)

simres.add_on_axis(Lambda_Regen)

simres.propagate(dist_pz_lambda)

simres.add_on_axis(PockelsCell)

simres.propagate(dist_mir_pz)

simres.add_on_axis(cm)

simres.compute_eigenmode()

# PockelsCell.rotate(PockelsCell.normal, np.pi/2)


# Amplifier_I = Make_Amplifier_I()
Amplifier_I = simres
# Amplifier_I.set_input_coupler_index(1, False)
ppos, paxes = Pump.last_geom()

Amplifier_I.set_input_coupler_index(1)
Amplifier_I.set_geom(Pump.last_geom())
# Amplifier_I.pos = ppos


# =============================================================================
# The pulse picker
# =============================================================================


tfp_angle = 65 #tfp angle of incidence in degree
flip_mirror_push_down = 8 # distance to push the first mirror out ouf the seed beam
tfp_push_aside = 5 # distance in mm to push the TFP aside, so that the beam can pass through

PulsePicker = Composition(name="PulsePicker")
PulsePicker.set_geom(Stretcher.last_geom())

# PulsePicker.pos = POS_STRETCHER_END_MIRROR - (0, 12, 0)
# PulsePicker.normal = (0, 1, 0)
# PulsePicker.propagate(12)

# lightsource_pp = Beam(angle=0, radius=seed_beam_radius)
# PulsePicker.set_light_source(lightsource_pp)
# PulsePicker.propagate(distance_seed_laser_stretcher*0.2)

# first small flip mirror from stretcher with cosmetics
# FlipMirror_pp = Mirror(phi=-90)
# FlipMirror_pp_mount=Composed_Mount()
# FlipMirror_pp.set_mount(Composed_Mount(unit_model_list = ["MH25_KMSS","1inch_post"]))
# FlipMirror_pp.Mount.set_geom(FlipMirror_pp.get_geom())
# PulsePicker.add_on_axis(FlipMirror_pp)
# FlipMirror_pp.pos += (0,0,flip_mirror_push_down)

# polarisation optics upt to pockels cell
PulsePicker.propagate(320)
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
TFP_pp = Mirror(phi = 180-2*tfp_angle)
TFP_pp.draw_dict["color"] = (1.0, 0.0, 2.0)
TFP_pp.draw_dict["thickness"] = 4
TFP_pp.aperture = 2*inch
# TFP_pp.thickness = tfp_thickness
TFP_pp.set_mount_to_default()
# TFP_out.mount_dict["Flip90"]=True
PulsePicker.add_on_axis(TFP_pp)
x,y,z = TFP_pp.get_coordinate_system()
TFP_pp.pos += y * tfp_push_aside


PulsePicker.propagate(80)
PulsePicker.add_on_axis(Lambda_Plate())
PulsePicker.propagate(100)

# Output TFP to sedn the beam to Amp2
TFP_out = Mirror(phi = 180-2*tfp_angle, name="Output_to_Amp2")
TFP_out.draw_dict["color"] = (1.0, 0.0, 2.0)
TFP_out.draw_dict["thickness"] = 4
TFP_out.aperture = 2*inch
TFP_out.thickness = tfp_thickness
# TFP_out.set_mount_to_default()
TFP_out_Mount = Composed_Mount(["KS2", "1inch_post"])
TFP_out.set_mount(TFP_out_Mount)
TFP_out.Mount.mount_list[0].flip()
TFP_out.next_ray = TFP_out.just_pass_through
PulsePicker.add_on_axis(TFP_out)
TFP_out.normal = TFP_pp.normal
x,y,z = TFP_out.get_coordinate_system()
TFP_out.pos += - y * tfp_push_aside
PulsePicker.propagate(90) # maybe just use the thickness of the energy detector everytime instead ...

# zick zack beam line to adjust the beam into Amp1
FlipMirror2_pp = Mirror(phi=90)
PulsePicker.add_on_axis(FlipMirror2_pp)
PulsePicker.propagate(80)
FaradPP = Faraday_Isolator()
PulsePicker.add_on_axis(FaradPP)
PulsePicker.propagate(120)
Lambda2_2_pp = Lambda_Plate()
PulsePicker.add_on_axis(Lambda2_2_pp)
#last knee for adjustment
PulsePicker.propagate(80)

second_last_flip_pp = Mirror(phi=-90)
PulsePicker.add_on_axis(second_last_flip_pp)

#geometrical considerations regarding 2 perpendicular rays that should
#zick zack meet in Regen TFP
p,a = PulsePicker.last_geom()
n1 = a[:,0]
Lslfp = np.sum(TFP_Amp1.pos*n1) - np.sum(second_last_flip_pp.pos*n1)

PulsePicker.propagate(Lslfp)
last_flip_pp = Mirror(phi=90)
PulsePicker.add_on_axis(last_flip_pp)
PulsePicker.propagate(np.linalg.norm(last_flip_pp.pos - TFP_Amp1.pos))


# =============================================================================
# Output Beam to Amp2
# =============================================================================
bs = PulsePicker.compute_beams()
b4 = bs[4]
b3 = bs[3]
Out_Beam0 = Beam(radius=2, name="Beam_to_Amp2")
Out_Beam0.draw_dict["color"] = (1.0, 0.5, 0.5)
Out_Beam0.pos = b4.pos
Out_Beam0.normal = -b3.normal
helper_mirror = Mirror()
helper_mirror.set_geom(TFP_out.get_geom())
Out_Beam1 = helper_mirror.next_beam(Out_Beam0)

Out_Beam0.draw()
Out_Beam1.draw()





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
Amp2.propagate(100)
teles_lens1 = Lens(f=telesf1)
Amp2.add_on_axis(teles_lens1)
Amp2.propagate(telesf1 + telesf2)
teles_lens2 = Lens(f=telesf2)
Amp2.add_on_axis(teles_lens2)

# Knee for adjustments
Amp2.propagate(90)
Amp2.add_on_axis(Mirror(phi=90*np.sign(knee_shift_amp2)))
Amp2.propagate(np.abs(knee_shift_amp2))
Amp2.add_on_axis(Mirror(phi=-90*np.sign(knee_shift_amp2)))
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
Amp2.set_sequence([0, 1, 2, 3, 4, 5, 4, 6, 7, 8, 4, 5, 4])
# Amp2.recompute_optical_axis()

a2_safe_angle_for_non_colliding_with_crystal = 2
Amp2.propagate(580)
Amp2.add_on_axis(Mirror(phi=180 - sep_angle_A2 + a2_safe_angle_for_non_colliding_with_crystal))
Amp2.propagate(580)

Amp2.add_on_axis(Mirror(phi=90 - a2_safe_angle_for_non_colliding_with_crystal))
Amp2.propagate(500)
Beam_Splitter = Mirror(phi=90, name="BeamSplitter")
Beam_Splitter.aperture= 2*inch
Beam_Splitter.set_mount_to_default() # should really automatize this...
Beam_Splitter.draw_dict["color"] = (100/255, 200/255, 240/255)
Amp2.add_on_axis(Beam_Splitter)
Amp2.propagate(20)

Amp2.set_geom(Out_Beam1.get_geom())




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


t=Table()
# =============================================================================
# Draw Selection
# =============================================================================

Seed.draw()
Stretcher.draw()
PulsePicker.draw()
Amplifier_I.draw()
# Pump.draw()
# Amp2.draw()
# BigPump.draw()
t.draw()
# Compressor.draw()
# PulsePicker.draw_alignment_posts()




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

if freecad_da:
  setview()