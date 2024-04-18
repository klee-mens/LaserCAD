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





# =============================================================================
# Pump Amp1
# =============================================================================
f1 = -100
f2 = 300

pump_first_prop = 150 #in -x 
pump_second_prop = 300 # in +y
pump_third_prop = 300 # in -x

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

Pump.draw()

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

mir1 = Mirror(phi=180)
mir1.aperture = 0.5 * inch
mir1.set_mount_to_default()

TFP1 = Mirror(phi= 180 - 2*tfp_angle, name="TFP1")
TFP1.draw_dict["color"] = (1.0, 0.0, 2.0)
TFP1.aperture = tfp_aperture
TFP1.set_mount_to_default()
pol_mount = TFP1.Mount.mount_list[0]
pol_mount.flip()
# TFP1.mount_dict["Flip90"]=True

cm = Curved_Mirror(radius=focal*2, phi = 180)
PockelsCell = Pockels_Cell(name="PockelZelleRes1")
Lambda_Regen = Lambda_Plate()
fold1 = Mirror(phi=90)


simres = LinearResonator(name="simple_Resonator1")
simres.set_wavelength(lam_mid)

simres.add_on_axis(mir1)

simres.propagate(dist_crystal_end)
laser_crys = Crystal(width=6, thickness=10, n=2.45)
simres.add_on_axis(laser_crys)

simres.propagate(last-dist_crystal_end)

simres.add_on_axis(fold1)

simres.propagate(dist_tfp_fold1)

simres.add_on_axis(TFP1)

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
Amplifier_I.pos = ppos

Amplifier_I.draw()




if freecad_da:
  setview()
