# -*- coding: utf-8 -*-
"""
Created on Thu Mar 20 09:51:43 2025

@author: mens
"""

from .. basic_optics import Beam, Composition, RainbowBeam
from .. basic_optics import Grating
from .periscope import Make_RoofTop_Mirror
import numpy as np


def Make_Compressor(seperation_angle = 20 /180 *np.pi, # sep between in and outgoing middle ray
    grating_const = 1/1000, # in 1/mm
    seperation = 200, # difference grating position und radius_concave
    lambda_mid = 800e-9 * 1e3, # central wave length in mm
    band_width = 100e-9*1e3, # full bandwith in mm
    number_of_rays = 20,
    height_seperation = 16, # seperation between incomming and outgoing beam,
    first_propagation = 120, # legnth of the first ray_bundle to grating 1 mm
    distance_roof_top_grating = 600,
    grating1_dimensions = (25, 25, 5),
    grating2_dimensions = (50, 50, 5)):

  # calculated parameters according to the grating equation and set the grating
  v = lambda_mid/grating_const
  s = np.sin(seperation_angle)
  c = np.cos(seperation_angle)
  a = v/2
  b = np.sqrt(a**2 - (v**2 - s**2)/(2*(1+c)))
  sinB = a - b
  grating_normal = (np.sqrt(1-sinB**2), sinB, 0)
  Grat1 = Grating(grat_const=grating_const, name="Gitter1", order=-1)
  Grat1.normal = grating_normal
  Grat1.width, Grat1.height, Grat1.thickness = grating1_dimensions

  Grat2 = Grating(grat_const=grating_const, name="Gitter2", order=-1)
  Grat2.width, Grat2.height, Grat2.thickness = grating2_dimensions

  # prepare the helper Composition
  helper = Composition()
  helper_light_source = Beam(angle=0, wavelength=lambda_mid)
  helper.set_light_source(helper_light_source)
  #to adjust the wavelength of the oA and set everything on axis
  helper.redefine_optical_axis(helper_light_source.inner_ray())
  helper.add_fixed_elm(Grat1)
  helper.recompute_optical_axis()
  helper.propagate(seperation)
  helper.add_on_axis(Grat2)
  Grat2.normal = - Grat1.normal

  lightsource = RainbowBeam(wavelength=lambda_mid, bandwith=band_width, ray_count=number_of_rays)

  # starting the real Compressor
  Compressor = Composition(name="DerKompressor")
  Compressor.set_light_source(lightsource)
  Compressor.redefine_optical_axis(helper_light_source.inner_ray())

  Compressor.propagate(first_propagation)
  #adding the helper
  helper.set_geom(Compressor.last_geom())
  helper.pos += (0,0, +height_seperation/2)
  Compressor.add_supcomposition_fixed(helper)

  # Compressor.set_sequence([0,1,2,1,0])
  Compressor.recompute_optical_axis()
  # Compressor.draw()

  # adding the rooftop mirror and it's cosmetics
  Compressor.propagate(distance_roof_top_grating)
  RoofTopMirror = Make_RoofTop_Mirror(height=height_seperation, up=True)

  Compressor.add_supcomposition_on_axis(RoofTopMirror)
  Compressor.set_sequence([0,1,2,3,1,0]) # believe me :)
  # Ok, for real: 0: Grat1, 1: Grat2, 2,3: RoofTopMirror, 1: Grat2, 0: Grat1
  Compressor.recompute_optical_axis()
  Compressor.propagate(100)

  # =============================================================================
  # GDD, TOD computation
  # =============================================================================
  lam0 = lambda_mid * 1e-3 # m
  d0 = grating_const * 1e-3 # m
  c0 = 299792458 # m/s
  sep = seperation * 1e-3
  diffray = Compressor._optical_axis[1]
  theta = diffray.angle_to(Grat1)

  GDD = -lam0**3 / np.pi / (c0 * d0 * np.cos(theta))**2 * sep # s^2
  TOD = GDD * 3*lam0/(2*np.pi*c0) * (1 + lam0/d0 * np.tan(theta)/np.cos(theta))
  Compressor.GDD = GDD
  Compressor.TOD = TOD

  return Compressor