# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 10:56:05 2023

@author: 12816
"""

from .. basic_optics import Mirror, Beam, Composition, inch, Curved_Mirror, RainbowBeam
from .. basic_optics import Grating, Unit_Mount, Composed_Mount
from ..basic_optics.mirror import Stripe_mirror
from .periscope import Make_RoofTop_Mirror
import numpy as np


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
  Stretcher.propagate(120)


  # last small flip mirror from stretcher with cosmetics
  FlipMirror_pp = Mirror(phi=-90, name="Small_Output_Flip")
  FlipMirror_pp.set_mount(Composed_Mount(unit_model_list = ["MH25_KMSS","1inch_post"]))
  flip_mirror_push_down = - 5 # distance to push the first mirror out ouf the seed beam
  Stretcher.add_on_axis(FlipMirror_pp)
  FlipMirror_pp.pos += (0,0,flip_mirror_push_down)
  Stretcher.propagate(13)

  # =============================================================================
  # GDD, TOD computation
  # =============================================================================
  lam0 = lambda_mid * 1e-3 # m
  d0 = grating_const * 1e-3 # m
  c0 = 299792458 # m/s
  sep = seperation * 1e-3
  diffray = Stretcher._optical_axis[2]
  theta = diffray.angle_to(Grat)

  GDD = -lam0**3 / np.pi / (c0 * d0 * np.cos(theta))**2 * (-2 * sep) # s^2
  TOD = GDD * 3*lam0/(2*np.pi*c0) * (1 + lam0/d0 * np.tan(theta)/np.cos(theta))
  Stretcher.GDD = GDD
  Stretcher.TOD = TOD
  return Stretcher




def Make_Stretcher(radius_concave = 1000, #radius of the big concave sphere
    aperture_concave = 6 * inch,
    height_stripe_mirror = 10, #height of the stripe mirror in mm
    seperation_angle = 10 /180 *np.pi, # sep between in and outgoing middle ray
    grating_const = 1/1000, # in 1/mm
    seperation = 50, # difference grating position und radius_concave
    lambda_mid = 800e-9 * 1e3, # central wave length in mm
    band_width = 100e-9*1e3, # full bandwith in mm
    number_of_rays = 20,
    safety_to_stripe_mirror = 5, #distance first incomming ray to stripe_mirror in mm
    periscope_height = 10,
    first_propagation = 120, # legnth of the first ray_bundle to flip mirror1 mm
    distance_roof_top_grating = 600):

  # calculated parameters according to the grating equation and set the grating
  v = lambda_mid/grating_const
  s = np.sin(seperation_angle)
  c = np.cos(seperation_angle)
  a = v/2
  b = np.sqrt(a**2 - (v**2 - s**2)/(2*(1+c)))
  sinB = a - b
  grating_normal = (np.sqrt(1-sinB**2), sinB, 0)
  Grat = Grating(grat_const=grating_const, name="Gitter", order=-1)
  Grat.normal = grating_normal

  #set the big sphere
  Concav = Curved_Mirror(radius=radius_concave,name="Concav_Mirror")
  Concav.aperture = aperture_concave
  Concav.set_mount_to_default()

  # set the convex stripe mirror and its cosmetics
  StripeM = Stripe_mirror(radius= -radius_concave/2)

  # prepare the helper Composition
  helper = Composition()
  helper_light_source = Beam(angle=0, wavelength=lambda_mid)
  helper.set_light_source(helper_light_source)
  #to adjust the wavelength of the oA and set everything on axis
  helper.redefine_optical_axis(helper_light_source.inner_ray())
  helper.add_fixed_elm(Grat)
  helper.recompute_optical_axis()
  helper.propagate(radius_concave - seperation)
  helper.add_on_axis(Concav)
  helper.propagate(radius_concave/2)
  helper.add_on_axis(StripeM)

  lightsource = RainbowBeam(wavelength=lambda_mid, bandwith=band_width, ray_count=number_of_rays)

  # starting the real stretcher
  Stretcher = Composition(name="DerStrecker")
  Stretcher.set_light_source(lightsource)
  Stretcher.redefine_optical_axis(helper_light_source.inner_ray())

  Stretcher.propagate(first_propagation)
  #adding the helper
  helper.set_geom(Stretcher.last_geom())
  helper.pos += (0,0, height_stripe_mirror/2 + safety_to_stripe_mirror)
  Stretcher.add_supcomposition_fixed(helper)

  Stretcher.set_sequence([0,1,2,1,0])
  Stretcher.recompute_optical_axis()
  # Stretcher.draw()

  # adding the rooftop mirror and it's cosmetics
  Stretcher.propagate(distance_roof_top_grating)
  RoofTopMirror = Make_RoofTop_Mirror(height=periscope_height, up=False)

  Stretcher.add_supcomposition_on_axis(RoofTopMirror)
  Stretcher.set_sequence([0,1,2,1,0, 3,4, 0,1,2,1,0]) # believe me :)
  Stretcher.recompute_optical_axis()
  Stretcher.propagate(100)

  # =============================================================================
  # GDD, TOD computation
  # =============================================================================
  lam0 = lambda_mid * 1e-3 # m
  d0 = grating_const * 1e-3 # m
  c0 = 299792458 # m/s
  sep = seperation * 1e-3
  diffray = Stretcher._optical_axis[1]
  theta = diffray.angle_to(Grat)

  GDD = -lam0**3 / np.pi / (c0 * d0 * np.cos(theta))**2 * (-2 * sep) # s^2
  TOD = GDD * 3*lam0/(2*np.pi*c0) * (1 + lam0/d0 * np.tan(theta)/np.cos(theta))
  Stretcher.GDD = GDD
  Stretcher.TOD = TOD
  return Stretcher