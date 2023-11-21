# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 11:33:16 2023

@author: 12816
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

Radius = 1000 #Radius des großen Konkavspiegels
Aperture_concav = 6 * inch
h_StripeM = 10 #Höhe des Streifenspiegels
gamma = 10 /180 *np.pi # Seperationswinkel zwischen einfallenden und Mittelpunktsstrahl; Alpha = Gamma + Beta
grat_const = 1/450 # Gitterkonstante in 1/mm
seperation = 50 # Differenz zwischen Gratingposition und Radius
lam_mid = 2400e-9 * 1e3 # Zentralwellenlänge in mm
delta_lamda = 200e-9*1e3 # Bandbreite in mm
number_of_rays = 20
safety_to_StripeM = 5 #Abstand der eingehenden Strahlen zum Concav Spiegel in mm
periscope_distance = 15
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
  # definierende Parameter
  # Radius = 1000 #Radius des großen Konkavspiegels
  # Aperture_concav = 6 * inch
  # h_StripeM = 10 #Höhe des Streifenspiegels
  # gamma = 5 /180 *np.pi # Seperationswinkel zwischen einfallenden und Mittelpunktsstrahl; Alpha = Gamma + Beta
  # grat_const = 1/450 # Gitterkonstante in 1/mm
  # seperation = 100 # Differenz zwischen Gratingposition und Radius
  # lam_mid = 2400e-9 * 1e3 # Zentralwellenlänge in mm
  # delta_lamda = 250e-9*1e3 # Bandbreite in mm
  # number_of_rays = 20
  # safety_to_StripeM = 5 #Abstand der eingehenden Strahlen zum Concav Spiegel in mm
  # periscope_distance = 8
  
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

StripeM = Stripe_mirror(radius= -Radius/2,thickness=25, name="Stripe_Mirror")
StripeM.pos = (Radius/2+50, 0, 0)
#Cosmetics
StripeM.aperture=75
StripeM.draw_dict["height"]=10
StripeM.draw_dict["thickness"]=25
StripeM.draw_dict["model_type"] = "Stripe"

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
    # rn.normal = vec
    # rn.pos = pos0
    rn.wavelength = wavel
    x = (wavel - lam_mid + delta_lamda/2) / delta_lamda
    rn.draw_dict["color"] = cmap( x )
    rays.append(rn)
lightsource.override_rays(rays)
lightsource.draw_dict['model'] = "ray_group"
  
nfm1 = - ray0.normal
pfm1 = Grat.pos + 600 * nfm1 + (0,0,-h_StripeM/2 - safety_to_StripeM)
# subperis = Periscope(length=8, theta=-90, dist1=0, dist2=0)
# subperis.pos = pfm1
# subperis.normal = nfm1
# flip_mirror1 = Mirror()
# flip_mirror1.pos = pfm1
# flip_mirror1.normal = nfm1 - np.array((0,0,-1))
# def useless():
#        return None
# flip_mirror1.draw = useless
# flip_mirror1.draw_dict["mount_type"] = "dont_draw"

# flip_mirror2 = Mirror()
# flip_mirror2.pos = pfm1 - np.array((0,0,periscope_distance))
# flip_mirror2.normal = nfm1 - np.array((0,0,1))
# flip_mirror2.draw = useless
# flip_mirror2.draw_dict["mount_type"] = "dont_draw"

# pure_cosmetic = Mirror(name="RoofTop_Mirror")
# pure_cosmetic.draw_dict["mount_type"] = "rooftop_mirror_mount"
# pure_cosmetic.pos = (flip_mirror1.pos + flip_mirror2.pos ) / 2
# pure_cosmetic.normal = (flip_mirror1.normal + flip_mirror2.normal ) / 2
# pure_cosmetic.aperture = periscope_distance

# pure_cosmetic.draw = useless

Stretcher = Composition(name="Strecker")
Stretcher.pos = pos0
Stretcher.normal = vec
def dont():
  return None
RoofTop1 = Mirror()
RoofTop1.pos = pfm1
RoofTop1.normal = nfm1 - np.array((0,0,-1))
RoofTop2 = Mirror()
RoofTop2.pos = pfm1 - np.array((0,0,periscope_distance))
RoofTop2.normal = nfm1 - np.array((0,0,1))


RoofTop1.draw = dont
RoofTop1.mount.elm_type = "dont_draw"
RoofTop2.draw = dont
RoofTop2.mount.elm_type = "dont_draw"

pure_cosmetic = Rooftop_mirror(name="RoofTop_Mirror")
pure_cosmetic.draw_dict["mount_type"] = "rooftop_mirror_mount"
pure_cosmetic.pos = (RoofTop1.pos + RoofTop2.pos ) / 2
pure_cosmetic.normal = (RoofTop1.normal + RoofTop2.normal ) / 2
pure_cosmetic.aperture = periscope_distance
pure_cosmetic.draw_dict["model_type"] = "Rooftop"
# pure_cosmetic.draw = dont


Stretcher.set_light_source(lightsource)
Stretcher.add_fixed_elm(Grat)
Stretcher.add_fixed_elm(Concav)
Stretcher.add_fixed_elm(StripeM)
Stretcher.add_fixed_elm(RoofTop1)
Stretcher.add_fixed_elm(RoofTop2)
Stretcher.add_fixed_elm(pure_cosmetic)
  
  # for item in subperis._elements:
  #   Stretcher.add_fixed_elm(item)
  
  
  # seq = [0,1,2,1,0]
  # seq = [0,1,2,1,0, 3]
  # seq = [0,1,2,1,0, 3,4]
seq = [0,1,2,1,0, 3,4, 0, 1, 2, 1, 0]
Stretcher.set_sequence(seq)
Stretcher.propagate(300)
Stretcher.draw()