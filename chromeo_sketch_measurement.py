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
# Seed.propagate(distance_seed_laser_stretcher-distance_6_mm_faraday-distance_faraday_mirror)
Seed.propagate(150)
Seed_M0 = Mirror(phi=90)
Seed_M1 = Mirror(phi=-90)
Seed.add_on_axis(Seed_M0)
Seed.propagate(750)
Seed.add_on_axis(Seed_M1)
Seed.propagate(1000)
Seed_AC = Component()
Seed_AC.draw_dict["stl_file"]=thisfolder+"\other_elements\APE.stl"
Seed_AC.draw_dict["color"]=(100/255, 100/255, 100/255)
Seed_AC.freecad_model = load_STL
Seed.add_on_axis(Seed_AC)
# seed_end_geom = Seed.last_geom()
# print(faraday_isolator_6mm.pos)

Alignment_M0 = Mirror(phi=-90)

Alignment = Composition()
ls = Beam(angle=0, radius=2,wavelength=532E-6)
ls.draw_dict["color"] = (0/255,255/255,0/255)
Alignment.set_light_source(ls)
Alignment.pos = (145-50,-150-750,104)
Alignment.normal = (0,1,0)
Alignment.propagate(750)
Alignment.add_on_axis(Alignment_M0)
Alignment.propagate(50+750)
Alignment.add_on_axis(Seed_M1)
Alignment.propagate(1000)

def dont():
  return None




# =============================================================================
# Draw Selection
# =============================================================================

Seed.draw()
Alignment.draw()


if freecad_da:
  setview()