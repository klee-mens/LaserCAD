# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 12:39:52 2024

@author: 12816
"""

##################################
UseNormalDesign = True
UseCompactDesign = not UseNormalDesign

UsePolRotator = False
##################################

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
from LaserCAD.basic_optics import Composed_Mount,Unit_Mount,Lens,Post
from copy import deepcopy

if freecad_da:
  clear_doc()

def rad(angle):
    return np.pi/180*angle

def dont():
    return None

def get_TFP_distances(TFP_ydist, TFP_angle):
    TFP_xdist = TFP_ydist*np.tan(rad(2*TFP_angle-90))
    TFP_dist = np.sqrt(TFP_ydist**2 + TFP_xdist**2)
    TFP_delta = TFP_dist - TFP_ydist - TFP_xdist
    
    TFP_Lam = 0.2*TFP_dist
    Lam_PC = 0.6*TFP_dist
    PC_TFP = TFP_dist - TFP_Lam - Lam_PC
    
    return TFP_dist, TFP_xdist, TFP_delta, TFP_Lam, Lam_PC, PC_TFP
    
rotate_axis = np.pi
offset_axis = (-250,-300,0)

pockels_cell = Component()
pockels_cell.draw_dict["stl_file"]= thisfolder+"\mount_meshes\A2_mounts\Pockels_cell.stl"
pockels_cell.freecad_model = load_STL

vacuum_tube = Component()
vacuum_tube.draw_dict["stl_file"]= thisfolder+"\mount_meshes\special_mount\Vacuum_Tube.stl"
vacuum_tube.freecad_model = load_STL


"""
Polarisationsdreher
"""

sep = 28.3
PD_theta = 45*np.pi/180
L = 80.3
start_length = 14.496
PD_length = sep + 2*start_length
length_diff = 192.066 - PD_length

Housing = Unit_Mount("Polarization_rotator-Fusion")
#stl_file=thisfolder+"mount_meshes\special_mount\Polarization_rotator-Fusion.stl"
#Housing.draw_dict["stl_file"]=stl_file
Housing.draw_dict["color"]=(239/255, 239/255, 239/255)
Housing.docking_obj.pos += (28.65,38.89, -41.89)
Housing.docking_obj.normal = (0,0,1)
#Housing.freecad_model = load_STL


Rotator_box = Composed_Mount()
Rotator_box.add(Housing)
Rotator_box.add(Post())
Pol_Rotator_elm=Component()
Pol_Rotator_elm.draw_dict["stl_file"]="dont_draw"
Pol_Rotator_elm.freecad_model = load_STL
Pol_Rotator_elm.Mount = Rotator_box

PDM1 = Mirror()
PDM2 = Mirror()
PDM3 = Mirror()
PDM2.pos += (start_length + sep/2, L*np.cos(PD_theta), L*np.sin(PD_theta))
PDM3.pos += (start_length + sep,0,0)
Pol_Rotater = Composition(name="Polarisationsdreher")
Pol_Rotater.add_on_axis(Pol_Rotator_elm)
Pol_Rotater.propagate(start_length)
Pol_Rotater.add_on_axis(PDM1)
PDM1.set_normal_with_2_points(Pol_Rotater.pos-(1,0,0), PDM2.pos)
Pol_Rotater.add_fixed_elm(PDM2)
PDM2.set_normal_with_2_points(PDM1.pos, PDM3.pos)
Pol_Rotater.add_fixed_elm(PDM3)
PDM3.set_normal_with_2_points(PDM2.pos, PDM3.pos + (1,0,0))
Pol_Rotater.propagate(start_length)

"""
Simulation of the amplifier cavity
"""

r1 = 2000 
r2 = 2500

f1 = r1/2
f2 = r2/2

beam = Beam(radius=5, angle=0)
beam.pos=[0,0,0]

if UsePolRotator:
    g = 350 # object distance
    length_diff = 192.066 - PD_length
    if UseNormalDesign: g -= 20
else: 
    g = 450
    length_diff = 0
    if UseNormalDesign: g-=100

b = ((f1-g)*f2**2 + f1**2 * f2) / (f1**2)

tele_angle1 = 8   # opening angle for coupling into telescope
tele_angle2 = 3   # opening angle for couling into telescope
tele_cut_d1 = 150 # cut mirror x-distance from spherical mirrors
tele_cut_d2 = 400 # cut mirror y-distance from spherical mirrors

tele_cut_dist1 = tele_cut_d1 / np.cos(rad(tele_angle1)) # propagation distance to first spherical mirror
tele_cut_dist2 = tele_cut_d2 / np.cos(rad(tele_angle2)) # propagation distance to first spherical mirror

tele_cut_y1 = np.sqrt(tele_cut_dist1**2 - tele_cut_d1**2);
tele_cut_y2 = np.sqrt(tele_cut_dist2**2 - tele_cut_d2**2);

TFP_angle = 66
alpha = rad(2*TFP_angle - 90)
delta = 100 - length_diff # propagation difference to ideal imaging (after roundtrip)

col_len = g + b + delta

if UseNormalDesign:
    TFP_ydist = 175
    TFP_dist, TFP_xdist, TFP_delta, TFP_Lam, Lam_PC, PC_TFP = get_TFP_distances(TFP_ydist, TFP_angle)
    
    xdist = f1 + f2 - tele_cut_d1 - tele_cut_d2
    ydist = 0.5*(col_len - TFP_delta - xdist - (tele_cut_dist1 + tele_cut_dist2 + tele_cut_y1 + tele_cut_y2))
    M2 = Mirror(phi=-90-tele_angle2) # cut mirror 2
    M3 = Mirror(phi=90) # mirror to TFP1
    
elif UseCompactDesign:
    y = 100 
    xdist = f1 + f2 + tele_cut_y2 - tele_cut_dist2 - tele_cut_d1
    TFP_ydist = (col_len - xdist - (tele_cut_y1 + tele_cut_dist1) - tele_cut_d2) / (1 + 1/np.cos(alpha)- np.tan(alpha))
    TFP_dist, TFP_xdist, TFP_delta, TFP_Lam, Lam_PC, PC_TFP = get_TFP_distances(TFP_ydist, TFP_angle)
    
    ydist = TFP_ydist + y
    M2 = Mirror(phi=90-tele_angle2) # cut mirror 2
    M3 = Mirror(phi=-90) # mirror to TFP1
    print(TFP_xdist)


pump_dist = 100                         # length of pump section
d1 = g-tele_cut_dist1-pump_dist/2       # distance from DM to cut mirror
d2 = 50                                 # x-distance from M3 to TFP1
if UseCompactDesign: d2 *= 4
d3 = xdist - TFP_xdist - pump_dist - d2 # TFP2 to M4
d4 = ydist - d1 + tele_cut_y1           # M4 to PM1

P1 = Mirror(phi=-90)
P2 = Mirror(phi=90)
PM1 = Mirror()  # pump mirror
PM2 = Mirror()  # pump mirror 2
M1 = Mirror(phi=-90-tele_angle1) # cut mirror 1

M4 = Mirror(phi=90) # mirror after TFP2
R1 = Curved_Mirror(phi=-180+tele_angle1, radius=r1)
R2 = Curved_Mirror(phi=-180+tele_angle2, radius=r2)
TFP1 = Mirror(phi=-180+2*TFP_angle)
TFP2 = Mirror(phi=180-2*TFP_angle)


Setup = Composition()
Setup.set_light_source(beam)
Setup.pos += offset_axis
Setup.propagate(pump_dist/2)
Setup.add_on_axis(P2)
Setup.propagate(d1)
Setup.add_on_axis(M1)
Setup.propagate(tele_cut_dist1)
Setup.add_on_axis(R1)
Setup.propagate(250)
Setup.add_on_axis(vacuum_tube)

if UseNormalDesign:    
    Setup.propagate(f1+f2-250)
    Setup.add_on_axis(R2)
    Setup.propagate(tele_cut_dist2)
    Setup.add_on_axis(M2)
    Setup.propagate(tele_cut_y2+ydist-TFP_ydist)
    print(f"Image Distance = {tele_cut_dist2+tele_cut_y2+ydist-TFP_ydist + d2 + TFP_dist + d3+ d4 + pump_dist/2 - delta} = {b}")
    

elif UseCompactDesign: 
    Setup.propagate(f1+f2-250-tele_cut_dist2)
    Setup.add_on_axis(M2)
    Setup.propagate(tele_cut_dist2)
    Setup.add_on_axis(R2)
    Setup.propagate(tele_cut_d2-y)
    print(f"Image Distance = {tele_cut_d2-y+d2+TFP_dist+d3+d4+pump_dist/2 - delta} = {b}")
    # Setup.propagate(tele_cut_d2-ydist+TFP_ydist)

    
Setup.add_on_axis(M3)
Setup.propagate(d2)
Setup.add_on_axis(TFP1)
Setup.propagate(TFP_Lam)
# Polarisationsdreher %%%%%%%%%%%
if UsePolRotator:
    Setup.add_supcomposition_on_axis(Pol_Rotater)
else:
    Setup.add_on_axis(Lambda_Plate())
# Polarisationsdreher Ende
Setup.propagate(Lam_PC)
Setup.add_on_axis(pockels_cell)
pockels_cell.rotate((0,0,1), np.pi)
Setup.propagate(PC_TFP)
Setup.add_on_axis(TFP2)
Setup.propagate(d3)
Setup.add_on_axis(M4)
Setup.propagate(d4)
Setup.add_on_axis(P1)
Setup.propagate(pump_dist/2)

P1.aperture = P2.aperture = TFP1.aperture = TFP2.aperture = 25.4*2
for elements in Setup._elements:
  elements.set_mount_to_default()
M2.Mount.mount_list[0].flip(90)

PDM1.set_mount(Unit_Mount())
PDM2.set_mount(Unit_Mount())
PDM3.set_mount(Unit_Mount())
Setup.draw()

"""
Pump Setup
"""

focal_length1 = 125
focal_length2 = 175

beam1 = Beam(radius=7.5,angle=2.08*np.pi/180,wavelength=960E-6)
beam1.draw_dict["color"] = (255/256,255/256,0.0)

beam2 = Beam(radius=7.5,angle=2.08*np.pi/180,wavelength=960E-6)
beam2.draw_dict["color"] = (255/256,255/256,0.0)

Comp = Composition()
Comp.set_light_source(beam1)
Comp.pos -= (75+focal_length1,0,0)

Comp2 = Composition()
Comp2.set_light_source(beam2)
Comp2.pos -= (75+focal_length1,250,0)

Laser_Head_in = Component()
stl_file = thisfolder+"\misc_meshes\PM19_2.stl"
Laser_Head_in.draw_dict["stl_file"]=stl_file
Laser_Head_in.freecad_model = load_STL

Laser_Head_out = Component()
stl_file = thisfolder+"\misc_meshes\PM19_2.stl"
Laser_Head_out.draw_dict["stl_file"]=stl_file
Laser_Head_out.freecad_model = load_STL

lens1 = Lens(f=focal_length1)
lens1.aperture = 25.4*2
lens1.set_mount_to_default()
lens2 = Lens(f=focal_length2)
lens2.aperture = 25.4*2
lens2.set_mount_to_default()
lens3 = deepcopy(lens2)
lens4 = deepcopy(lens1)

M1 = Mirror(phi=90)
M1.aperture = 25.4*3
M1.set_mount_to_default()
M2 = deepcopy(M1)


# Comp.rotate((0,0,1), rotate_axis)
Comp.pos += offset_axis
Comp.add_on_axis(Laser_Head_in)
Comp.propagate(75)
Comp.add_on_axis(lens1)
Comp.propagate(focal_length1)

Comp2.pos += offset_axis
Comp2.add_on_axis(Laser_Head_out)
Comp2.propagate(75)
Comp2.add_on_axis(lens4)
Comp2.propagate(300)
Comp2.add_on_axis(lens3)
Comp2.propagate(50)
Comp2.add_on_axis(M2)
Comp2.propagate(250)
Comp2.add_on_axis(M1)
Comp2.propagate(50)
Comp2.add_on_axis(lens2)
Comp2.propagate(focal_length2)
# Laser_Head_out.normal = -Laser_Head_out.normal


Comp.draw()
Comp2.draw()

