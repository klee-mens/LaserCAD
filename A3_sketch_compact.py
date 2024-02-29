# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 12:39:52 2024

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


from LaserCAD.freecad_models import clear_doc, setview, freecad_da,add_to_composition
from LaserCAD.basic_optics import Mirror, Beam, Composition, Component, inch, Curved_Mirror, Ray, Geom_Object
from LaserCAD.basic_optics import Grating, Opt_Element
import matplotlib.pyplot as plt
from LaserCAD.freecad_models.utils import thisfolder, load_STL
from LaserCAD.non_interactings import Faraday_Isolator, Pockels_Cell, Lambda_Plate
from LaserCAD.basic_optics import Composed_Mount,Unit_Mount,Lens
from copy import deepcopy

if freecad_da:
  clear_doc()
  
def conv_to_rad(angle):
    return np.pi/180*angle
    
def dont():
    return None

rotate_axis = np.pi
offset_axis = (-250,-590,0)

pockels_cell = Component()
pockels_cell.draw_dict["stl_file"]= thisfolder+"\mount_meshes\A2_mounts\Pockels_cell.stl"
pockels_cell.freecad_model = load_STL

focal_length = 125

beam = Beam(radius=5,angle=0,wavelength=600E-6)
beam.draw_dict["color"] = (255/256,255/256,0.0)
Comp = Composition()
Comp.set_light_source(beam)
Comp.pos -= (75+focal_length,0,0)

Laser_Head_in = Component()
stl_file = thisfolder+"\misc_meshes\PM19_2.stl"
Laser_Head_in.draw_dict["stl_file"]=stl_file
Laser_Head_in.freecad_model = load_STL

Laser_Head_out = Component()
stl_file = thisfolder+"\misc_meshes\PM19_2.stl"
Laser_Head_out.draw_dict["stl_file"]=stl_file
Laser_Head_out.freecad_model = load_STL

lens1 = Lens(f=focal_length)
lens1.aperture = 25.4*2
lens1.set_mount_to_default()
lens2 = Lens(f=focal_length)
lens2.aperture = 25.4*2
lens2.set_mount_to_default()
lens3 = deepcopy(lens2)
lens4 = deepcopy(lens1)

M1 = Mirror(phi=-90)
M1.aperture = 25.4*3
M1.set_mount_to_default()
M2 = deepcopy(M1)


# Comp.rotate((0,0,1), rotate_axis)
Comp.pos += offset_axis
Comp.add_on_axis(Laser_Head_in)
Comp.propagate(75)
Comp.add_on_axis(lens1)
Comp.propagate(310)
Comp.add_on_axis(lens2)
Comp.propagate(50)
Comp.add_on_axis(M1)
Comp.propagate(250)
Comp.add_on_axis(M2)
Comp.propagate(50)
Comp.add_on_axis(lens3)
Comp.propagate(310)
Comp.add_on_axis(lens4)
Comp.propagate(75)
Comp.add_on_axis(Laser_Head_out)
Laser_Head_out.normal = -Laser_Head_out.normal

Comp.draw()

"""
Amplifier cavity
"""

r1 = 2000 
r2 = 2500

f1 = r1/2
f2 = r2/2

beam = Beam(radius=5, angle=0)
beam.pos=[0,0,0]

g = 350 # object distance
b = ((f1-g)*f2**2 + f1**2 * f2) / (f1**2)

tele_angle1 = 8 #opening angle for couling intot telescope
tele_cut_d1 = 150 # cut mirror distance from spherical mirrors
tele_angle2 = 3 # opening angle for couling intot telescope
tele_cut_d2 = 400 # cut mirror distance from spherical mirrors

tele_cut_dist1 = tele_cut_d1 / np.cos(conv_to_rad(tele_angle1)) # propagation distance to first spherical mirror
tele_cut_dist2 = tele_cut_d2 / np.cos(conv_to_rad(tele_angle2)) # propagation distance to first spherical mirror

tele_cut_y1 = np.sqrt(tele_cut_dist1**2 - tele_cut_d1**2);
tele_cut_y2 = np.sqrt(tele_cut_dist2**2 - tele_cut_d2**2);

TFP_angle = 66
TFP_ydist = 200
TFP_xdist = TFP_ydist*np.tan((2*TFP_angle-90)*np.pi/180)
TFP_dist = np.sqrt(TFP_ydist**2 + TFP_xdist**2)
TFP_Lambda_Plate = 60
Lam_Pockscell = 150
Last_dist = TFP_dist - TFP_Lambda_Plate - Lam_Pockscell
TFP_delta = TFP_dist - TFP_ydist - TFP_xdist

delta = 100 # propagation difference to ideal imaging (after roundtrip)

col_len = g + b + delta - TFP_delta
xdist = f1 + f2 + tele_cut_y2 - tele_cut_dist2
ydist = 0.5*(col_len - xdist - tele_cut_y1 - tele_cut_d2)

pump_dist = 100 # length of pump section
d1 = g-tele_cut_dist1-pump_dist/2 # distance from DM to cut mirror
d2 = 200 # x-distance from M3 to TFP1
d3 = xdist - tele_cut_d1 - TFP_xdist - pump_dist - d2 # TFP2 to M4
d4 = ydist - d1 + tele_cut_y1

P1 = Mirror(phi=-90)
P2 = Mirror(phi=90)
PM1 = Mirror()  # pump mirror
PM2 = Mirror()  # pump mirror 2
M1 = Mirror(phi=-90-tele_angle1)
M2 = Mirror(phi=-90+tele_angle2)
M3 = Mirror(phi=90)
M4 = Mirror(phi=90)
R1 = Curved_Mirror(phi=-180+tele_angle1, radius=r1)
R2 = Curved_Mirror(phi=-180-tele_angle2, radius=r2)
TFP1 = Mirror(phi=-180+2*66)
TFP2 = Mirror(phi=180-2*66)

Setup = Composition()
Setup.set_light_source(beam)


# Setup.rotate((0,0,1), rotate_axis)
Setup.pos += offset_axis


Setup.propagate(pump_dist/2)
Setup.add_on_axis(P2)
Setup.propagate(d1)
Setup.add_on_axis(M1)
Setup.propagate(tele_cut_dist1)
Setup.add_on_axis(R1)
Setup.propagate(f1+f2-tele_cut_dist2)
Setup.add_on_axis(M2)
Setup.propagate(tele_cut_dist2)
Setup.add_on_axis(R2)
Setup.propagate(tele_cut_d2+ydist-TFP_ydist)
Setup.add_on_axis(M3)
Setup.propagate(d2)
Setup.add_on_axis(TFP1)
Setup.propagate(TFP_Lambda_Plate)
Setup.add_on_axis(Lambda_Plate())
Setup.propagate(Lam_Pockscell)
Setup.add_on_axis(pockels_cell)
pockels_cell.rotate((0,0,1), np.pi)
Setup.propagate(Last_dist)
Setup.add_on_axis(TFP2)
Setup.propagate(d3)
Setup.add_on_axis(M4)
Setup.propagate(d4)
Setup.add_on_axis(P1)
Setup.propagate(pump_dist/2)

# Setup.propagate(pump_dist/2)
# Setup.add_on_axis(P2)
# Setup.propagate(d1)
# Setup.add_on_axis(M1)
# Setup.propagate(tele_cut_dist1)
# Setup.add_on_axis(R1)
# Setup.propagate(f1+f2-400*(1+np.tan(conv_to_rad(tele_angle2))))
# Setup.add_on_axis(M2)
# Setup.propagate(400*(1+np.tan(conv_to_rad(tele_angle2))))
# Setup.add_on_axis(R2)
# Setup.propagate(75+400*(1+np.tan(conv_to_rad(tele_angle2)))/(np.cos(conv_to_rad(tele_angle2))))
# Setup.add_on_axis(M3)
# Setup.propagate(200)
# Setup.add_on_axis(TFP1)
# Setup.propagate(TFP_Lambda_Plate)
# Setup.add_on_axis(Lambda_Plate())
# Setup.propagate(Lam_Pockscell)
# Setup.add_on_axis(pockels_cell)
# pockels_cell.rotate((0,0,1), np.pi)
# Setup.propagate(Last_dist)
# Setup.add_on_axis(TFP2)
# Setup.propagate(1370-126)
# Setup.add_on_axis(M4)
# Setup.propagate(40)
# Setup.add_on_axis(P1)
# Setup.propagate(pump_dist/2)

P1.aperture = P2.aperture = M1.aperture = M3.aperture = M4.aperture = TFP1.aperture = TFP2.aperture = 25.4*2
for elements in Setup._elements:
  elements.set_mount_to_default()
M2.Mount.mount_list[0].flip(90)
Setup.draw()

print(tele_cut_d2+ydist-TFP_ydist+d2+TFP_dist+d3+d4+pump_dist/2)