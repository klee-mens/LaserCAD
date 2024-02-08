# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 10:56:05 2023

@author: 12816
"""

from .. basic_optics import Mirror, Beam, Composition, inch, Curved_Mirror, Ray
from .. basic_optics import Grating, Unit_Mount, Composed_Mount, Post
from ..basic_optics.mirror import Stripe_mirror
from .periscope import Make_RoofTop_Mirror
import matplotlib.pyplot as plt
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

  # setting the lightsource as an bundle of different coulered rays
  lightsource = Beam(radius=0, angle=0)
  wavels = np.linspace(lambda_mid-delta_lamda/2, lambda_mid+delta_lamda/2, number_of_rays)
  rays = []
  cmap = plt.cm.gist_rainbow
  for wavel in wavels:
    rn = Ray()
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
  FlipMirror_In_Out.Mount = Composed_Mount()
  FlipMirror_In_Out.Mount.add(Unit_Mount("MH25_KMSS"))
  FlipMirror_In_Out.Mount.add(Post())
  FlipMirror_In_Out.Mount.set_geom(FlipMirror_In_Out.get_geom())
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


  RoofTopMirror = Make_RoofTop_Mirror(height=periscope_height, up=False)

  Stretcher.add_supcomposition_on_axis(RoofTopMirror)
  Stretcher.set_sequence([0, 1,2,3,2,1, 4,5, 1,2,3,2,1, 0]) # believe me :)
  Stretcher.recompute_optical_axis()
  Stretcher.propagate(100)

  return Stretcher




def Make_Stretcher(
        Radius = 1000, #Radius des großen Konkavspiegels
        Aperture_concav = 6 * inch,
        h_StripeM = 10, #Höhe des Streifenspiegels
        gamma = 5 /180 *np.pi, # Seperationswinkel zwischen einfallenden und Mittelpunktsstrahl; Alpha = Gamma + Beta
        grat_const = 1/450, # Gitterkonstante in 1/mm
        seperation = 100, # Differenz zwischen Gratingposition und Radius
        lam_mid = 2400e-9 * 1e3, # Zentralwellenlänge in mm
        delta_lamda = 250e-9*1e3, # Bandbreite in mm
        number_of_rays = 20,
        safety_to_StripeM = 5, #Abstand der eingehenden Strahlen zum Concav Spiegel in mm
        periscope_distance = 8,
        distance_rooftop_gratig = 600):
  """
  tja, versuchen wir mal einen Offner Strecker...
  Note: When drawing a rooftop mirror, we will draw apure_cosmetic mirror to
  confirm the position of the mount. The mirror's geom is the average of two
  flip mirror. And its aperture is the periscope_distance.

  Returns
  -------
  TYPE Composition
    den gesamten, geraytracten Strecker...

  """

  # abgeleitete Parameter
  v = lam_mid/grat_const
  s = np.sin(gamma)
  c = np.cos(gamma)
  a = v/2
  b = np.sqrt(a**2 - (v**2 - s**2)/(2*(1+c)))
  sinB = a - b

  Concav = Curved_Mirror(radius=Radius, name="Concav_Mirror")
  Concav.pos = (0,0,0)
  Concav.aperture = Aperture_concav
  Concav.normal = (-1,0,0)

  StripeM = Curved_Mirror(radius= -Radius/2, name="Stripe_Mirror")
  StripeM.pos = (Radius/2-5, 0, 0)
  #Cosmetics
  StripeM.aperture=75
  StripeM.draw_dict["height"]=10
  StripeM.draw_dict["thickness"]=25
  StripeM.draw_dict["model_type"]="Stripe"

  Grat = Grating(grat_const=grat_const, name="Gitter")
  Grat.pos = (Radius-seperation, 0, 0)
  Grat.normal = (np.sqrt(1-sinB**2), -sinB, 0)

  ray0 = Ray()
  p_grat = np.array((Radius-seperation, 0, h_StripeM/2 + safety_to_StripeM))
  vec = np.array((c, s, 0))
  pos0 = p_grat - 250 * vec
  ray0.normal = vec
  ray0.pos = pos0
  ray0.wavelength = lam_mid

  lightsource = Beam(radius=0, angle=0)
  wavels = np.linspace(lam_mid-delta_lamda/2, lam_mid+delta_lamda/2, number_of_rays)
  rays = []
  cmap = plt.cm.gist_rainbow
  for wavel in wavels:
    rn = Ray()
    rn.wavelength = wavel
    x = (wavel - lam_mid + delta_lamda/2) / delta_lamda
    rn.draw_dict["color"] = cmap( x )
    rays.append(rn)
  lightsource.override_rays(rays)
  lightsource.draw_dict['model'] = "ray_group"

  nfm1 = - ray0.normal
  pfm1 = Grat.pos + distance_rooftop_gratig * nfm1 + (0,0,-h_StripeM/2 - safety_to_StripeM)
  # subperis = Periscope(length=8, theta=-90, dist1=0, dist2=0)
  # subperis.pos = pfm1
  # subperis.normal = nfm1
  flip_mirror1 = Mirror()
  flip_mirror1.pos = pfm1
  flip_mirror1.normal = nfm1 - np.array((0,0,-1))
  def useless():
    return None
  flip_mirror1.draw = useless
  flip_mirror1.draw_dict["mount_type"] = "dont_draw"

  flip_mirror2 = Mirror()
  flip_mirror2.pos = pfm1 - np.array((0,0,periscope_distance))
  flip_mirror2.normal = nfm1 - np.array((0,0,1))
  flip_mirror2.draw = useless
  flip_mirror2.draw_dict["mount_type"] = "dont_draw"

  pure_cosmetic = Mirror(name="RoofTop_Mirror")
  pure_cosmetic.draw_dict["mount_type"] = "rooftop_mirror_mount"
  pure_cosmetic.pos = (flip_mirror1.pos + flip_mirror2.pos ) / 2
  pure_cosmetic.normal = (flip_mirror1.normal + flip_mirror2.normal ) / 2
  pure_cosmetic.aperture = periscope_distance

  pure_cosmetic.draw = useless

  Stretcher = Composition(name="Strecker")
  Stretcher.pos=pos0
  Stretcher.normal=vec

  Stretcher.set_light_source(lightsource)
  Stretcher.add_fixed_elm(Grat)
  Stretcher.add_fixed_elm(Concav)
  Stretcher.add_fixed_elm(StripeM)
  Stretcher.add_fixed_elm(flip_mirror1)
  Stretcher.add_fixed_elm(flip_mirror2)
  Stretcher.add_fixed_elm(pure_cosmetic)

  seq = [0,1,2,1,0, 3,4, 0, 1, 2, 1, 0]
  Stretcher.set_sequence(seq)
  Stretcher.propagate(300)
  return Stretcher