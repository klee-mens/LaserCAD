# -*- coding: utf-8 -*-
"""
Created on Tue Jun 27 22:34:31 2023

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
from LaserCAD.basic_optics.mirror import Rooftop_mirror,Stripe_mirror
from LaserCAD.basic_optics.mount import Mount,Composed_Mount,Special_mount
from LaserCAD.non_interactings.table import Table
if freecad_da:
  clear_doc()

# =============================================================================
# Draw the seed laser and seed beam
# =============================================================================
start_point = (0,0,104) #see CLPF-2400-10-60-0_8 sn2111348_Manual
seed_beam_radius = 2.5/2 #see CLPF-2400-10-60-0_8 sn2111348_Manual
distance_seed_laser_stretcher = 400 #the complete distance
distance_6_mm_faraday = 45
distance_faraday_mirror = 100

seed_laser = Component(name="IPG_Seed_Laser")

stl_file=thisfolder+"\mount_meshes\special mount\Laser_Head-Body.stl"
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
Seed.propagate(distance_seed_laser_stretcher-distance_6_mm_faraday-distance_faraday_mirror)
seed_end_geom = Seed.last_geom()
# print(faraday_isolator_6mm.pos)
# =============================================================================
# Create and draw the stretcher
# =============================================================================


def dont():
  return None


def Make_Stretcher_chromeo():
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
  seperation = 50 # difference grating position und radius_concave
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
  print(sinB)
  grating_normal = (np.sqrt(1-sinB**2), sinB, 0)

  Concav = Curved_Mirror(radius=radius_concave, name="Concav_Mirror")
  Concav.aperture = aperture_concave

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
  lightsource.override_rays(rays)
  lightsource.draw_dict['model'] = "ray_group"

  # starting the real stretcher
  Stretcher = Composition(name="DerStrecker")
  Stretcher.set_light_source(lightsource)
  Stretcher.redefine_optical_axis(helper_light_source.inner_ray())

  Stretcher.propagate(first_propagation)
  FlipMirror_In_Out = Mirror(phi=90, name="FlipMirrorInOut")
  
  mount=Composed_Mount()
  Mount1=Special_mount(model="MH25",drawing_post=False)
  Mount1.docking_obj.pos = Mount1.pos+(6.3,0,0)
  Mount1.docking_obj.normal = Mount1.normal
  Mount2=Mount(model="KMSS")
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
  RoofTop1 = Mirror(phi=0, theta=90)
  Stretcher.add_on_axis(RoofTop1)
  Stretcher.propagate(periscope_height)
  RoofTop2 = Mirror(phi=0, theta=90)
  Stretcher.add_on_axis(RoofTop2)

  RoofTop1.draw = dont
  RoofTop1.mount.elm_type = "dont_draw"
  RoofTop2.draw = dont
  RoofTop2.mount.elm_type = "dont_draw"

  pure_cosmetic = Rooftop_mirror(name="RoofTop_Mirror")
  pure_cosmetic.draw_dict["mount_type"] = "rooftop_mirror_mount"
  pure_cosmetic.pos = (RoofTop1.pos + RoofTop2.pos ) / 2
  pure_cosmetic.normal = (RoofTop1.normal + RoofTop2.normal ) / 2
  pure_cosmetic.aperture = periscope_height
  pure_cosmetic.draw_dict["model_type"] = "Rooftop"
  # pure_cosmetic.draw = dont
  Stretcher.add_fixed_elm(pure_cosmetic)

  # setting the final sequence and the last propagation for visualization
  # note that pure cosmetic (pos6) is not in the sequence
  Stretcher.set_sequence([0, 1,2,3,2,1, 4,5, 1,2,3,2,1, 0])
  Stretcher.recompute_optical_axis()
  Stretcher.propagate(100)

  return Stretcher

Stretcher = Make_Stretcher_chromeo()
Stretcher.set_geom(seed_end_geom)



# =============================================================================
# The pulse picker
# =============================================================================
# from LaserCAD.basic_optics.mirror import Lam_Plane

tfp_angle = 65 #tfp angle of incidence in degree
flip_mirror_push_down = 8 # distance to push the first mirror out ouf the seed beam
tfp_push_forward = 1 # distance to push the TFP forward, so that the beam can pass through

PulsePicker = Composition(name="PulsePicker")
lightsource_pp = Beam(angle=0, radius=seed_beam_radius)
PulsePicker.set_light_source(lightsource_pp)
PulsePicker.propagate(distance_seed_laser_stretcher*0.2)
FlipMirror_pp = Mirror(phi=90)
FlipMirror_pp_mount=Composed_Mount()
FlipMirror_pp_mount_Mount1=Special_mount(model="MH25",drawing_post=False)
FlipMirror_pp_mount_Mount1.docking_obj.pos = FlipMirror_pp_mount_Mount1.pos+(6.3,0,0)
FlipMirror_pp_mount_Mount1.docking_obj.normal = FlipMirror_pp_mount_Mount1.normal
FlipMirror_pp_mount_Mount2=Mount(model="KMSS")
FlipMirror_pp_mount.add(FlipMirror_pp_mount_Mount1)
FlipMirror_pp_mount.add(FlipMirror_pp_mount_Mount2)
FlipMirror_pp.mount = FlipMirror_pp_mount
# FlipMirror_pp.mount_dict["Flip90"]=False
PulsePicker.add_on_axis(FlipMirror_pp)
FlipMirror_pp.pos += (0,0,flip_mirror_push_down)
PulsePicker.propagate(100)
Lambda2 = Lambda_Plate()
PulsePicker.add_on_axis(Lambda2)
PulsePicker.propagate(390)
Back_Mirror_PP = Mirror()
PulsePicker.add_on_axis(Back_Mirror_PP)
PulsePicker.propagate(30)
Lambda4 = Lambda_Plate()
PulsePicker.add_on_axis(Lambda4)
PulsePicker.propagate(30)
pockelscell =Pockels_Cell()
PulsePicker.add_on_axis( pockelscell)
pockelscell.rotate(vec=pockelscell.normal,phi=np.pi)
PulsePicker.propagate(210)
TFP_pp = Mirror(phi = 180-2*tfp_angle)
TFP_pp.draw_dict["color"] = (1.0, 0.0, 2.0)
TFP_pp.draw_dict["thickness"] = 4
TFP_pp.aperture = 2*inch
# TFP_pp.mount_dict["Flip90"]=True
PulsePicker.add_on_axis(TFP_pp)
TFP_pp.pos += -1 * TFP_pp.normal * tfp_push_forward
PulsePicker.recompute_optical_axis()
PulsePicker.propagate(250)
FlipMirror2_pp = Mirror(phi=90)
PulsePicker.add_on_axis(FlipMirror2_pp)
PulsePicker.propagate(100)
FaradPP = Faraday_Isolator()
PulsePicker.add_on_axis(FaradPP)
PulsePicker.propagate(200)
Lambda2_2_pp = Lambda_Plate()
PulsePicker.add_on_axis(Lambda2_2_pp)
PulsePicker.propagate(200)

PulsePicker.set_geom(Stretcher.last_geom())



# =============================================================================
# simple Amp1
# =============================================================================
# calculus
A_target = 4.908738521234052 #from gain simlutation area in mm^2
focal = 2500
lam_mid = 2.4e-3
A_natural = lam_mid * focal
geometrie_factor = A_target / A_natural
total_length = focal * (1 - np.sqrt(1 - geometrie_factor**2))

# design params
dist_mir_pz = 20
dist_pz_lambda = 115
dist_lambda_tfp = 70
dist_tfp_fold1 = 65
dist_fold1_fold2 = 300
dist_crystal_end = 20
last = total_length - dist_mir_pz - dist_pz_lambda - dist_lambda_tfp -dist_tfp_fold1 -dist_fold1_fold2
tfp_aperture = 2*inch
tfp_angle = 65

# optics

mir1 = Mirror(phi=180)
TFP1 = Mirror(phi= 180 - 2*tfp_angle, name="TFP1")
TFP1.draw_dict["color"] = (1.0, 0.0, 2.0)
TFP1.aperture = tfp_aperture
TFP1.mount_dict["Flip90"]=True

cm = Curved_Mirror(radius=focal*2, phi = 180)
PockelsCell = Pockels_Cell(name="PockelZelleRes1")
Lambda_Regen = Lambda_Plate()
fold1 = Mirror(phi=90)
fold2 = Mirror(phi=90)

simres = LinearResonator(name="simple_Resonator1")
simres.set_wavelength(lam_mid)
simres.add_on_axis(mir1)
simres.propagate(dist_mir_pz)
simres.add_on_axis(PockelsCell)
simres.propagate(dist_pz_lambda)
simres.add_on_axis(Lambda_Regen)
simres.propagate(dist_lambda_tfp)
simres.add_on_axis(TFP1)
simres.propagate(dist_tfp_fold1)
simres.add_on_axis(fold1)
simres.propagate(dist_fold1_fold2)
simres.add_on_axis(fold2)
simres.propagate(last-dist_crystal_end)

laser_crys = Crystal(width=6, thickness=10, n=2.45)

simres.add_on_axis(laser_crys)
simres.propagate(dist_crystal_end)

simres.add_on_axis(cm)

simres.compute_eigenmode()

# PockelsCell.rotate(PockelsCell.normal, np.pi/2)


# Amplifier_I = Make_Amplifier_I()
Amplifier_I = simres
Amplifier_I.set_input_coupler_index(1, False)
Amplifier_I.set_geom(PulsePicker.last_geom())



# =============================================================================
# Pump Amp1
# =============================================================================
f1 = -100
f2 = 300

# pump_geom = Amplifier_I._elements[-2].get_geom()
pump_geom = Amplifier_I._elements[-1].get_geom()
Pump = Composition(name="Pump")
Pump.set_geom(pump_geom)
pump_light = Beam(radius=1.5, angle=0)
pump_light.draw_dict["color"] = (1.0, 1.0, 0.0)
Pump.set_light_source(pump_light)

Pump.propagate(100)
Pump.add_on_axis(Lens(f=f1))
Pump.propagate(f1+f2*0.5)
Pump.add_on_axis(Mirror(phi=90))
Pump.propagate(f1+f2*0.5)
Pump.add_on_axis(Lens(f=f2))
Pump.propagate(190)

# =============================================================================
# simple AMP2
# =============================================================================


focal = 300
sep_angle = 5
bigcrys = Crystal(width=20, thickness=15, n=2.45)
source = Beam(radius=1.4, angle=0)
telesf1 = -75
telesf2 = 270

amp2 = Composition(name="herbert")
amp2.set_light_source(source)
amp2.propagate(100)
teles_lens1 = Lens(f=telesf1)
amp2.add_on_axis(teles_lens1)
amp2.propagate(telesf1 + telesf2)
teles_lens2 = Lens(f=telesf2)
amp2.add_on_axis(teles_lens2)
amp2.propagate(800)
amp2.add_on_axis(bigcrys)
amp2.propagate(20)
active_mir = Mirror(phi=180-sep_angle)
amp2.add_on_axis(active_mir)
amp2.propagate(focal*2)
concave1 = Curved_Mirror(radius=focal*2, phi=180+sep_angle)
amp2.add_on_axis(concave1)
amp2.propagate(2*focal)
end_concave= Curved_Mirror(radius=focal, phi=180-sep_angle)
amp2.add_on_axis(end_concave)
amp2.propagate(2*focal)
concave2 = Curved_Mirror(radius=focal*2, phi=180+sep_angle)
amp2.add_on_axis(concave2)
concave2.set_normal_with_2_points(end_concave.pos, active_mir.pos)
# amp2.set_sequence([0,1,2,3,4,5,2])
amp2.set_sequence([0,1,2,3,2,4,5,6,2,3,2])
amp2.recompute_optical_axis()
amp2.propagate(650)
amp2.add_on_axis(Mirror(phi=90))
amp2.propagate(600)
# amp2.set_sequence([0,1,2,3,4,5,2,6])
# amp2.set_sequence([0,1,2,3,2,4,5,6,5,4,2,3,7])





back_beam = PulsePicker.compute_beams()[3]
back_pos = back_beam.pos
back_normal = back_beam.normal * -1
amp2.pos = back_pos
amp2.normal = back_normal

# =============================================================================
# big_pump
# =============================================================================
big_pump_ls = Beam(radius=6, angle=0)
big_pump_ls.draw_dict["color"] = (1.0,1.0,0.0)
BigPump = Composition("Big_Pump")
BigPump.set_light_source(big_pump_ls)
BigPump.propagate(200)

BigPump.set_geom(amp2._elements[2].get_geom())
# BigPump.set_geom(amp2.non_opticals[-1].get_geom())




# =============================================================================
# Draw Selection
# =============================================================================

Seed.draw()
Stretcher.draw()
PulsePicker.draw()
Amplifier_I.draw()
Pump.draw()
amp2.draw()
# BigPump.draw()
t=Table()
t.draw()

# =============================================================================
# breadboards
# =============================================================================
from LaserCAD.non_interactings import Breadboard
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