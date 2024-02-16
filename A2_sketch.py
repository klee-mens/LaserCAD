# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 10:47:53 2023

@author: Martin
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


from LaserCAD.freecad_models import clear_doc, setview, freecad_da,add_to_composition
from LaserCAD.basic_optics import Mirror, Beam, Composition, Component, inch, Curved_Mirror, Ray, Geom_Object
from LaserCAD.basic_optics import Grating, Opt_Element
import matplotlib.pyplot as plt
from LaserCAD.freecad_models.utils import thisfolder, load_STL
from LaserCAD.non_interactings import Faraday_Isolator, Pockels_Cell, Lambda_Plate
from LaserCAD.basic_optics import Composed_Mount,Unit_Mount

if freecad_da:
  clear_doc()
  
def dont():
    return None

"""
from LaserCAD.basic_optics.mount import MIRROR_LIST

MIRROR_LIST
"""

beam = Beam(radius=1, angle=0)
from LaserCAD.basic_optics import Gaussian_Beam


# define angles and components
tele_angle1 = 5
M1_angle = 1
PM_angle = 2
TFP_angle = 66
Glan_angle = 68
# -----------------------------------------------------------------------------
roundtrip = 2
# Now the glan_taylor_in and glan_taylor_out will no longer be drawn due to the
# "dont_draw" definition. I copied the "Glan_Taylor_reverced.stl" file into the
# special mount folder and defined its docking_position so that I could easily 
# draw its connected posts.
glan_taylor_in = Component()
# stl_file = thisfolder+"\mount_meshes\A2_mounts\Glan_Taylor_reverced.stl"
glan_taylor_in.draw_dict["stl_file"]="dont_draw"
glan_taylor_in.freecad_model = load_STL

glan_taylor_out = Component()
# stl_file = thisfolder+"\mount_meshes\A2_mounts\Glan_Taylor_reverced.stl"
glan_taylor_out.draw_dict["stl_file"]="dont_draw"
glan_taylor_out.freecad_model = load_STL

glan_taylor_in.Mount = Composed_Mount(unit_model_list=["Glan_Taylor","1inch_post"])
glan_taylor_out.Mount = Composed_Mount(unit_model_list=["Glan_Taylor","1inch_post"])

# -----------------------------------------------------------------------------
pockels_cell = Component()
pockels_cell.draw_dict["stl_file"]= thisfolder+"\mount_meshes\A2_mounts\Pockels_cell.stl"
pockels_cell.freecad_model = load_STL


# Prepare the setup

R1 = Curved_Mirror(phi=-180-tele_angle1, radius=2000)
TFP1 = Mirror(phi=-180-2*TFP_angle)
# TFP2 = Mirror(phi=180+2*TFP_angle)    # unused in this setup
M1 = Mirror(phi=-90+M1_angle)           # 2" mirror with two reflections per roundtrip
M2 = Mirror(phi=25)                     # 1" mirror in the small mount next to the Pockels cell
M3 = Mirror(phi=180+2*56)               # mirror before Glan_in
# -----------------------------------------------------------------------------
# redefine M2 Mount
# -----------------------------------------------------------------------------
M2.Mount = Composed_Mount(unit_model_list=["Newport-9771-M","1inch_post"])
M2.Mount.set_geom(M2.get_geom())
# -----------------------------------------------------------------------------
Glan_in = Mirror(phi=180-Glan_angle)    # input coupling Glan polarizer             
Glan_out = Mirror(phi=180+Glan_angle)   # output coupling Glan polarizer
# -----------------------------------------------------------------------------
# hide the Mounts. Their Mounts has already been drawn.
# -----------------------------------------------------------------------------
Glan_in.Mount.invisible = True
Glan_out.Mount.invisible = True
# -----------------------------------------------------------------------------
PM1 = Mirror(phi=-180+PM_angle)         # pump mirror

M1.aperture = 2 * inch
TFP1.aperture = 2 * inch 
# -----------------------------------------------------------------------------
# After the update, elements need to set mount to default when the aperture 
# changed.
# -----------------------------------------------------------------------------
M1.set_mount_to_default()
TFP1.set_mount_to_default()
# -----------------------------------------------------------------------------

# M2.mount_dict["model"] = "Newport-9771-M"


## Make the setup
Setup = Composition()
Setup.set_light_source(beam)

# We start at the position of the Glan_in
# Setup.propagate(10)
Setup.add_on_axis(glan_taylor_in)
Setup.propagate(185+80)
Setup.add_on_axis(pockels_cell)
pockels_cell.rotate(pockels_cell.get_axes()[2], phi=np.pi)
Setup.propagate(115)
Setup.add_on_axis(TFP1) #0
Setup.propagate(390)
Setup.add_on_axis(R1) #1
Setup.propagate(635)
Setup.add_on_axis(glan_taylor_out)
Setup.add_on_axis(Glan_out) #2
Setup.propagate(105)
Setup.add_on_axis(M2) #3
Setup.propagate(280)
Setup.add_on_axis(M1) #4
M1.pos += M1.get_coordinate_system()[1] * 10
Setup.propagate(575)
Setup.add_on_axis(PM1) #5
Setup.set_sequence([0,1,2,3,4,5,4])
Setup.recompute_optical_axis()  
p0=Setup.last_geom()[0]
Setup.propagate(105)
Setup.add_on_axis(M3) #6
# Setup.propagate(45)
# Setup.add_on_axis(Glan_in) #7
# -----------------------------------------------------------------------------
# Since there are some errors in the resonator. The following code is used to 
# correct these errors.
# -----------------------------------------------------------------------------
# M3.pos = (16.07335963622269,39.782961125846896,80)
# Setup.add_fixed_elm(M3) #6
Glan_in.pos = (0,0,80)
Setup.add_fixed_elm(Glan_in) #7
p1 = (0,0,80)
M3.set_normal_with_2_points(p0, p1)
p0 = M3.pos
p1 = TFP1.pos
Glan_in.set_normal_with_2_points(p0, p1)
print(Glan_in.phi)
print(180-Glan_angle)
Glan_in_pos = Glan_in.pos
glan_taylor_in.pos = Glan_in_pos

# -----------------------------------------------------------------------------
# The following code is designed to enable light to circulate in the resonator.
# -----------------------------------------------------------------------------
seq = np.array([0,1,2,3,4,5,4,6,7])
sequence_loop = list(np.array([0,1,2,3,4,5,4,6,7]))
for loop_i in range(roundtrip-1):
  seq = np.append(seq,sequence_loop)
seq=np.append(seq, [0,1])

Setup.set_sequence(seq)
Setup.propagate(750)
# -----------------------------------------------------------------------------


# glan_taylor_out.rotate(glan_taylor_out.get_axes()[0], phi=np.pi)
glan_taylor_in.rotate(glan_taylor_in.get_axes()[2], phi=np.pi)

# Doesnt work anymore since newest pull
# Glan_in.draw = dont
# Glan_in.mount.elm_type = "dont_draw"
# Glan_out.draw = dont
# Glan_out.mount.elm_type = "dont_draw"

# Setup.draw()
Setup.draw_elements()
Setup.draw_mounts()

# -----------------------------------------------------------------------------
# Since modeling multiple loops takes too long, the following code is used to 
# implement raytracing that only shows the last loop. Please note to comment 
# out the draw_beams function when using it.
# -----------------------------------------------------------------------------
# Setup.compute_beams()
# container = []
# for last_loop in range(-12,0):
#   beam = Setup._beams[last_loop]
#   obj = beam.draw()
#   container.append(obj)
# if freecad_da:
#   part = add_to_composition(Setup._beams_part, container)
# else:
#   for x in container:
#     Setup._beams_part.append(x)
Setup.draw_beams()
# -----------------------------------------------------------------------------
if freecad_da:
  setview()