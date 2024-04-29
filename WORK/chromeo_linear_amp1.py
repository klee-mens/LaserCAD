# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 12:54:40 2024

@author: mens
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
from LaserCAD.basic_optics import LinearResonator, Lens
from LaserCAD.basic_optics import Grating, Crystal
import matplotlib.pyplot as plt
from LaserCAD.freecad_models.utils import thisfolder, load_STL
from LaserCAD.non_interactings import Faraday_Isolator, Pockels_Cell, Lambda_Plate
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

stretcher_out_obj = Lens()
stretcher_out_obj.pos = POS_STRETCHER_END_MIRROR
stretcher_out_obj.draw()

tm_big_obj = Lens()
tm_big_obj.pos = POS_THULIUM_BIG_OUT
tm_big_obj.draw()


tm_small_obj = Lens()
tm_small_obj.pos = POS_THULIUM_SMALL_OUT
tm_small_obj.draw()

X_ADDITIONAL = 80
Y_ADDITIONAL = 80



# =============================================================================
# Pump Amp1
# =============================================================================
f1 = -100
f2 = 300

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

Pump.add_on_axis(Lens(f=f1))
Pump.propagate(f1+f2*0.5)
Pump.propagate(f1+f2*0.5)
Pump.add_on_axis(Lens(f=f2))
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

# optics

cm0 = Curved_Mirror(radius=focal*2, phi = 180, name="Curved_Far")
mir1 = Mirror(phi=180 + 10, name="Dichroit")
mir1.aperture = 0.5 * inch
mir1.set_mount_to_default()

TFP_Amp1 = Mirror(phi= 180 - 2*tfp_angle, name="TFP_Amp1")
TFP_Amp1.draw_dict["color"] = (1.0, 0.0, 2.0)
TFP_Amp1.aperture = tfp_aperture
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




# print()
# print("TFP Position", TFP_Amp1.pos)
# print()


# =============================================================================
# The pulse picker
# =============================================================================


tfp_angle = 65 #tfp angle of incidence in degree
flip_mirror_push_down = 8 # distance to push the first mirror out ouf the seed beam
tfp_push_aside = 5 # distance in mm to push the TFP aside, so that the beam can pass through


PulsePicker = Composition(name="PulsePicker")
PulsePicker.pos = POS_STRETCHER_END_MIRROR + (0, 7, 0)
PulsePicker.normal = (0, -1, 0)
PulsePicker.propagate(7)

# lightsource_pp = Beam(angle=0, radius=seed_beam_radius)
# PulsePicker.set_light_source(lightsource_pp)
# PulsePicker.propagate(distance_seed_laser_stretcher*0.2)

# first small flip mirror from stretcher with cosmetics
FlipMirror_pp = Mirror(phi=90, name="Small_Flip")
FlipMirror_pp_mount=Composed_Mount()
FlipMirror_pp.Mount = Composed_Mount(unit_model_list = ["MH25_KMSS","1inch_post"])
FlipMirror_pp.Mount.set_geom(FlipMirror_pp.get_geom())
PulsePicker.add_on_axis(FlipMirror_pp)
FlipMirror_pp.pos += (0,0,flip_mirror_push_down)

# polarisation optics upt to pockels cell
PulsePicker.propagate(90)
Lambda2 = Lambda_Plate()
PulsePicker.add_on_axis(Lambda2)
PulsePicker.propagate(390)
Back_Mirror_PP = Mirror(name="Back_Mirror")
PulsePicker.add_on_axis(Back_Mirror_PP)
PulsePicker.propagate(30)
Lambda4 = Lambda_Plate(name="Compensation_for_PZ")
PulsePicker.add_on_axis(Lambda4)
PulsePicker.propagate(30)
pockelscell = Pockels_Cell()
PulsePicker.add_on_axis( pockelscell)
pockelscell.rotate(vec=pockelscell.normal,phi=np.pi*0)
PulsePicker.propagate(210)

# Splitting TFP
TFP_pp = Mirror(phi = 180-2*tfp_angle, name="TPF_to_Regen")
TFP_pp.draw_dict["color"] = (1.0, 0.0, 2.0)
TFP_pp.draw_dict["thickness"] = 4
TFP_pp.aperture = 2*inch
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
TFP_out.set_mount_to_default()
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
Lambda2_2_pp = Lambda_Plate(name="Compensation_for_FR")
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
b5 = bs[5]
b4 = bs[4]
Out_Beam0 = Beam(radius=2)
Out_Beam0.draw_dict["color"] = (1.0, 0.5, 0.5)
Out_Beam0.pos = b5.pos
Out_Beam0.normal = -b4.normal
helper_mirror = Mirror()
helper_mirror.set_geom(TFP_out.get_geom())
Out_Beam1 = helper_mirror.next_beam(Out_Beam0)

Out_Beam0.draw()
Out_Beam1.draw()

# =============================================================================
# Last Minute Cosmetics
# =============================================================================
# x,y,z = TFP_Amp1.get_coordinate_system()
# TFP_Amp1.pos += -y * tfp_push_aside

# =============================================================================
# Draw Section and Selection
# =============================================================================

Amplifier_I.draw()
PulsePicker.draw()
Pump.draw()

if freecad_da:
  setview()
