# -*- coding: utf-8 -*-
"""
Created on Tue Jun 27 22:34:31 2023

@author: mens
"""

import numpy as np
import sys

pfad = __file__
pfad = pfad.replace("\\","/") #folder conventions windows linux stuff
ind = pfad.rfind("/")
pfad = pfad[0:ind-1]
ind = pfad.rfind("/")
pfad = pfad[0:ind]
if not pfad in sys.path:
  sys.path.append(pfad)


from LaserCAD.freecad_models import clear_doc, setview, freecad_da
from LaserCAD.basic_optics import Mirror, Beam, Composition, inch, Curved_Mirror, Ray, Geom_Object, Component
from LaserCAD.basic_optics import Grating, Opt_Element
import matplotlib.pyplot as plt
from LaserCAD.freecad_models.utils import thisfolder, load_STL

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
# seed_laser.pos = start_point

stl_file=thisfolder+"\mount_meshes\special mount\Laser_Head-Body.stl"
seed_laser.draw_dict["stl_file"]=stl_file
color = (170/255, 170/255, 127/255)
seed_laser.draw_dict["color"]=color
seed_laser.freecad_model = load_STL

faraday_isolator_6mm = Opt_Element(name="Faraday_Isolator")
stl_file=thisfolder+"\mount_meshes\special mount\Faraday-Isolatoren-Body.stl"
faraday_isolator_6mm.draw_dict["stl_file"]=stl_file
color = (10/255, 20/255, 230/255)
faraday_isolator_6mm.draw_dict["color"]=color
faraday_isolator_6mm.freecad_model = load_STL

faraday_isolator_6mm.pos = start_point + np.array((45,0,0))

seed_beam = Beam(angle=0, radius=seed_beam_radius, pos=start_point)

Seed = Composition(name="Seed")
Seed.normal = (1,2,0)
Seed.pos = start_point
Seed.set_light_source(seed_beam)
Seed.add_on_axis(seed_laser)
Seed.propagate(distance_6_mm_faraday)
Seed.add_on_axis(faraday_isolator_6mm)
Flip0 = Mirror(phi=90)
Seed.propagate(distance_faraday_mirror)
Seed.add_on_axis(Flip0)
Seed.propagate(distance_seed_laser_stretcher-distance_6_mm_faraday-distance_faraday_mirror)
seed_end_geom = Seed.last_geom()

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
  periscope_height = 10
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
  grating_normal = (np.sqrt(1-sinB**2), sinB, 0)

  Concav = Curved_Mirror(radius=radius_concave, name="Concav_Mirror")
  Concav.aperture = aperture_concave

  StripeM = Curved_Mirror(radius= -radius_concave/2, name="Stripe_Mirror")
  #Cosmetics
  StripeM.aperture = width_stripe_mirror
  StripeM.draw_dict["height"] = height_stripe_mirror
  StripeM.draw_dict["thickness"] = 25 # arbitrary
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
  RoofTop1 = Mirror(phi=0, theta=90)
  Stretcher.add_on_axis(RoofTop1)
  Stretcher.propagate(periscope_height)
  RoofTop2 = Mirror(phi=0, theta=90)
  Stretcher.add_on_axis(RoofTop2)

  RoofTop1.draw = dont
  RoofTop1.draw_dict["mount_type"] = "dont_draw"
  RoofTop2.draw = dont
  RoofTop2.draw_dict["mount_type"] = "dont_draw"

  pure_cosmetic = Mirror(name="RoofTop_Mirror")
  pure_cosmetic.draw_dict["mount_type"] = "rooftop_mirror_mount"
  pure_cosmetic.pos = (RoofTop1.pos + RoofTop2.pos ) / 2
  pure_cosmetic.normal = (RoofTop1.normal + RoofTop2.normal ) / 2
  pure_cosmetic.draw = dont
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
from LaserCAD.basic_optics.mirror import Lam_Plane

tfp_angle = 65 #tfp angle of incidence in degree
flip_mirror_push_down = 8 # distance to push the first mirror out ouf the seed beam
tfp_push_forward = 1 # distance to push the TFP forward, so that the beam can pass through

PulsePicker = Composition(name="PulsePicker")
lightsource_pp = Beam(angle=0, radius=seed_beam_radius)
PulsePicker.set_light_source(lightsource_pp)
PulsePicker.propagate(distance_seed_laser_stretcher*0.2)
FlipMirror_pp = Mirror(phi=-90)
PulsePicker.add_on_axis(FlipMirror_pp)
FlipMirror_pp.pos += (0,0,flip_mirror_push_down)
PulsePicker.propagate(200)
Lambda2 = Lam_Plane()
PulsePicker.add_on_axis(Lambda2)
PulsePicker.propagate(310)
Back_Mirror_PP = Mirror()
PulsePicker.add_on_axis(Back_Mirror_PP)
PulsePicker.propagate(30)
Lambda4 = Lam_Plane()
PulsePicker.add_on_axis(Lambda4)
PulsePicker.propagate(30)

PockelsCell = Opt_Element(name="PockelZellePulsPicker")
# Pockels cell is pure cosmetics
stl_file=thisfolder+"\mount_meshes\special mount\pockels_cell_easy_steal-Body.stl"
PockelsCell.draw_dict["stl_file"]=stl_file
color = (239/255, 239/255, 239/255)
PockelsCell.draw_dict["color"]=color
PockelsCell.freecad_model = load_STL

PulsePicker.add_on_axis(PockelsCell)

PulsePicker.propagate(140)
TFP_pp = Mirror(phi = -180+2*tfp_angle)
TFP_pp.draw_dict["color"] = (1.0, 0.0, 2.0)
TFP_pp.draw_dict["thickness"] = 3
PulsePicker.add_on_axis(TFP_pp)
TFP_pp.pos += -1 * TFP_pp.normal * tfp_push_forward
PulsePicker.recompute_optical_axis()
PulsePicker.propagate(250)
FlipMirror2_pp = Mirror(phi=-90)
PulsePicker.add_on_axis(FlipMirror2_pp)
PulsePicker.propagate(200)
Lambda2_2_pp = Lam_Plane()
PulsePicker.add_on_axis(Lambda2_2_pp)
PulsePicker.propagate(400)

PulsePicker.set_geom(Stretcher.last_geom())


# =============================================================================
# Regen Amp1 Section
# =============================================================================
from LaserCAD.basic_optics import LinearResonator, Lens


def Make_Amplifier_I():

  tfp_angle = 65
  tfp_aperture = 2*inch
  angle_on_sphere = 10
  alpha = -0.8
  beta = -0.8
  print("g1*g2 = ", alpha*beta)
  focal = 500
  dist1 = (1-alpha)*focal
  dist2 = (1-beta)*focal
  wavelength = 2400*1e-6

  # geometric restrictions
  dist_tfp1_2 = 230
  dist_tfp1_pockels = 50
  dist_pockels_lambda = 115
  dist_tfp2_sphere = 400
  dist_m1_tfp1 = dist1 - dist_tfp1_2 - dist_tfp2_sphere
  dist_crystal_end = 15

  mir1 = Mirror(phi=180)
  TFP1 = Mirror(phi= 180 - 2*tfp_angle, name="TFP1")
  TFP1.draw_dict["color"] = (1.0, 0.0, 2.0)
  TFP1.aperture = tfp_aperture
  TFP2 = Mirror(phi= - 180 + 2*tfp_angle, name="TFP2")
  TFP2.draw_dict["color"] = (1.0, 0.0, 2.0)
  TFP2.aperture = tfp_aperture
  mir4 = Mirror(phi=180)
  cm = Curved_Mirror(radius=focal*2, phi = 180 - angle_on_sphere)

  PockelsCell = Opt_Element(name="PockelZellePulsPicker")
  # Pockels cell is pure cosmetics
  stl_file=thisfolder+"\mount_meshes\special mount\pockels_cell_easy_steal-Body.stl"
  PockelsCell.draw_dict["stl_file"]=stl_file
  color = (239/255, 239/255, 239/255)
  PockelsCell.draw_dict["color"]=color
  PockelsCell.freecad_model = load_STL

  Lambda2 = Lam_Plane()

  amp1 = LinearResonator(name="foldedRes")
  amp1.set_wavelength(wavelength)
  amp1.add_on_axis(mir1)
  amp1.propagate(dist_m1_tfp1)
  amp1.add_on_axis(TFP1)
  amp1.propagate(dist_tfp1_pockels)
  amp1.add_on_axis(PockelsCell)
  amp1.propagate(dist_pockels_lambda)
  amp1.add_on_axis(Lambda2)
  amp1.propagate(dist_tfp1_2-dist_tfp1_pockels-dist_pockels_lambda)
  amp1.add_on_axis(TFP2)
  amp1.propagate(dist_tfp2_sphere)
  amp1.add_on_axis(cm)
  amp1.propagate(dist2 - dist_crystal_end)


  crystal = Beam(radius=3, angle=0)
  crystal.draw_dict['color'] = (182/255, 109/255, 46/255)
  crystal.set_length(10)

  amp1.add_on_axis(crystal)
  amp1.propagate(dist_crystal_end)
  amp1.add_on_axis(mir4)

  amp1.compute_eigenmode()
  return amp1


pp_last_pos, pp_last_ax = PulsePicker.last_geom()
helper = Beam()
helper.set_geom(PulsePicker.last_geom())
h = helper.normal
h[2] = 0
helper.normal = h


Amplifier_I = Make_Amplifier_I()
Amplifier_I.set_input_coupler_index(1)
Amplifier_I.set_geom(PulsePicker.last_geom())


# =============================================================================
# Pump Amp1
# =============================================================================
pump_geom = Amplifier_I._elements[-1].get_geom()
Pump = Composition(name="Pump")
Pump.set_geom(pump_geom)
pump_light = Beam(radius=0.2, angle=0.03)
pump_light.draw_dict["color"] = (1.0, 1.0, 0.0)
Pump.set_light_source(pump_light)
Pump.propagate(120)
PumpMirror = Mirror(phi=90)
Pump.add_on_axis(PumpMirror)
Pump.propagate(90)
PumpLens = Lens(f=120+90)
Pump.add_on_axis(PumpLens)
Pump.propagate(190)




# out_beam = amp_beams[3]


# =============================================================================
# Draw Selection
# =============================================================================

Seed.draw()
Stretcher.draw()
PulsePicker.draw()
Amplifier_I.draw()
Pump.draw()
#Amplifier_I.pos += (0,0,300)
Amplifier_I.draw_dict["beam_model"] = "cone"
Amplifier_I.draw()

from LaserCAD.moduls.type_II_Amplifier import Make_Amplifier_Typ_II_Juergen
from LaserCAD.basic_optics.beam import Gaussian_Beam

#gb = Gaussian_Beam()
#gb.draw()
#gb.draw_dict["model"] = "cone"
#gb.pos += (0,50, 0)
#gb.draw()

# amp2 = Make_Amplifier_Typ_II_Juergen()
# amp2.draw()

if freecad_da:
  setview()