# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 10:56:05 2023

@author: 12816
"""

import sys
pfad = __file__
pfad = pfad.replace("\\","/") #folder conventions windows linux stuff
pfad = pfad.lower()
ind = pfad.rfind("lasercad")
pfad = pfad[0:ind-1]
if not pfad in sys.path:
  sys.path.append(pfad)

from LaserCAD.basic_optics import Beam, Composition, inch, Curved_Mirror, Ray, Grating
from LaserCAD.basic_optics.mirror import Stripe_mirror
from LaserCAD.moduls.periscope import Make_RoofTop_Mirror
import matplotlib.pyplot as plt
import numpy as np
from LaserCAD.freecad_models.utils import freecad_da, clear_doc, setview

if freecad_da:
  clear_doc()

radius_concave = 1000 #radius of the big concave sphere
aperture_concave = 6 * inch
height_stripe_mirror = 10 #height of the stripe mirror in mm
seperation_angle = 10 /180 *np.pi # sep between in and outgoing middle ray
# incident_angle = seperation_angle + reflection_angle
grating_const = 1/1000 # in 1/mm
seperation = 50 # difference grating position und radius_concave
lambda_mid = 800e-9 * 1e3 # central wave length in mm
band_width = 100e-9*1e3 # full bandwith in mm
number_of_rays = 20
safety_to_stripe_mirror = 5 #distance first incomming ray to stripe_mirror in mm
periscope_height = 10
first_propagation = 120 # legnth of the first ray_bundle to flip mirror1 mm
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

# incident = Ray()
# incident.wavelength = 800e-6
# incident.pos += (-80,0,0)
# outgoing = Grat.next_ray(incident)

# Grat.draw()
# incident.draw()
# outgoing.draw()

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

# helper.draw()

# setting the lightsource as an bundle of different coulered rays
lightsource = Beam(radius=0, angle=0)
wavels = np.linspace(lambda_mid-band_width/2, lambda_mid+band_width/2, number_of_rays)
rays = []
cmap = plt.cm.gist_rainbow
for wavel in wavels:
  rn = Ray()
  rn.wavelength = wavel
  x = 1-(wavel - lambda_mid + band_width/2) / band_width
  rn.draw_dict["color"] = cmap( x )
  rays.append(rn)
lightsource.override_rays(rays)
lightsource.draw_dict['model'] = "ray_group"

# lightsource.pos += (-80,0,0)
# outgoing = Grat.next_beam(lightsource)

# Grat.draw()
# lightsource.draw()
# outgoing.draw()

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

Stretcher.draw()

if freecad_da:
  setview()