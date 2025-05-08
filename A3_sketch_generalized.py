# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 12:39:52 2024

@author: 12816
"""

##################################
UseNormalDesign = False
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
  print(pfad)
  sys.path.append(pfad)

from LaserCAD.freecad_models import clear_doc, setview, freecad_da,add_to_composition
from LaserCAD.basic_optics import Mirror, Beam, Composition, Component, inch, Curved_Mirror, Ray, Geom_Object
from LaserCAD.basic_optics import Grating, Opt_Element
import matplotlib.pyplot as plt
from LaserCAD.freecad_models.utils import thisfolder, load_STL
from LaserCAD.non_interactings import Faraday_Isolator, Pockels_Cell, Lambda_Plate
from LaserCAD.basic_optics import Composed_Mount,Unit_Mount,Lens,Post
from copy import deepcopy


def rad(angle):
    return np.pi/180*angle

def deg(angle):
    return 180/np.pi*angle

def dont():
    return None

def get_TFP_distances(TFP_ydist, TFP_angle):
    TFP_xdist = TFP_ydist*np.tan(TFP_angle)
    TFP_dist = np.sqrt(TFP_ydist**2 + TFP_xdist**2)
    TFP_delta = TFP_dist - TFP_ydist - TFP_xdist
    
    TFP_Lam = 0.2*TFP_dist
    Lam_PC = 0.6*TFP_dist
    PC_TFP = TFP_dist - TFP_Lam - Lam_PC
    
    return TFP_dist, TFP_xdist, TFP_delta, TFP_Lam, Lam_PC, PC_TFP
    
rotate_axis = np.pi
offset_axis = (950,500,20+100)

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

PDM1 = Mirror(name="Polarisationsdreher M1")
PDM2 = Mirror(name="Polarisationsdreher M2")
PDM3 = Mirror(name="Polarisationsdreher M3")
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
    g = 350 # object distance: distance between the pump region and the first curved mirror
    length_diff = 192.066 - PD_length
    if UseNormalDesign: g -= 20
else: 
    g = 520
    length_diff = 0
    if UseNormalDesign: g-=100

# Calculation of the image distance
b = ((f1-g)*f2**2 + f1**2 * f2) / (f1**2)


pump_angle = 90   # input-output angle on the pump mirrors, standard: 90
tele_angle1 = 5   # opening angle for coupling into telescope
tele_angle2 = 5   # opening angle for couling into telescope

xdist_R2_M1 = 300 # cut mirror x-distance from spherical mirrors
ydist_R2_M2 = 300 # cut mirror y-distance from spherical mirrors

dist_R1_M1 = xdist_R2_M1 / np.cos(rad(tele_angle1)) # propagation distance to first spherical mirror
dist_R2_M2 = ydist_R2_M2 / np.cos(rad(tele_angle2)) # propagation distance to second spherical mirror

ydist_R1_M1 = np.sqrt(dist_R1_M1**2 - xdist_R2_M1**2)
xdist_R2_M2 = np.sqrt(dist_R2_M2**2 - ydist_R2_M2**2)

TFP_angle = 66
TFP_angle = rad(2*TFP_angle - 90)

difference_to_ideal_imaging = 100 - length_diff # propagation difference to ideal imaging (after roundtrip)
            
cavity_length = f1 + f2 + g + b + difference_to_ideal_imaging           # total cavity length, g-object distance, b-image distance
            
pump_dist = 125    # 150            # length of pump section
d1 = g-dist_R1_M1-pump_dist/2       # distance from P2 to M1
d2 = 200                            # x-distance from M3 to TFP1
dist_vacuum_tube = xdist_R2_M1 + 70

x_correction_by_angled_pump = d1 * np.cos(rad(180-pump_angle))  

if UseNormalDesign:
    d2 /= 4
    TFP_ydist = 175
    TFP_dist, TFP_xdist, TFP_delta, TFP_Lam, Lam_PC, PC_TFP = get_TFP_distances(TFP_ydist, TFP_angle)
    
    xdist_P2_TFP1 = f1 + f2 - xdist_R2_M1 - ydist_R2_M2
    ydist = 0.5*(cavity_length - TFP_delta - xdist_P2_TFP1 - (dist_R1_M1 + dist_R2_M2 + ydist_R1_M1 + xdist_R2_M2))
    M2 = Mirror(phi=-90-tele_angle2, name="M2") # cut mirror 2
    M3 = Mirror(phi=90, name="M3") # mirror to TFP1
    
elif UseCompactDesign:
    # ydist: difference between beam y-position at the pump medium vs entrance TFP
    # ydist_M2_M3: y-distance between M2 and M3
    # ydist_P2_TFP1: y-distance between pump mirror P2 and TFP1
    # xdist_P2_TFP1: x-distance between pump mirror P2 and TFP1
    ydist_M2_M3 = 120
    pump_angle_rad = rad(180-pump_angle)
    
    # is 1 for a pump angle of 90°
    pump_angle_correction_factor = 1/np.tan(pump_angle_rad) + 1/np.sin(pump_angle_rad)
    
    
    ydist_P2_TFP1 = (d1 * np.sin(rad(180-pump_angle)) - ydist_R1_M1 - ydist_M2_M3) * pump_angle_correction_factor
    xdist_P2_TFP1 = f1 + f2 + xdist_R2_M2 - dist_R2_M2 - xdist_R2_M1 + x_correction_by_angled_pump - pump_dist - d2
    
    distance_to_TFP1 = g + f1 + f2 + ydist_R2_M2 - ydist_M2_M3 + d2

    TFP_ydist = (cavity_length - xdist_P2_TFP1 - distance_to_TFP1 - pump_dist/2 + ydist_P2_TFP1) / (1/np.cos(TFP_angle)- np.tan(TFP_angle) + pump_angle_correction_factor)
    TFP_dist, TFP_xdist, TFP_delta, TFP_Lam, Lam_PC, PC_TFP = get_TFP_distances(TFP_ydist, TFP_angle)
    print(f"TFP_ydist = {TFP_ydist}")
    ydist = TFP_ydist + ydist_M2_M3
    
    M2 = Mirror(phi=90-tele_angle2, name="M2") # cut mirror 2
    M3 = Mirror(phi=-90, name="M3") # mirror to TFP1


d4 = (ydist - d1*np.sin(rad(180-pump_angle)) + ydist_R1_M1) / np.sin(rad(pump_angle))  # M4 to P1 (pump mirror 1)
d3 = xdist_P2_TFP1 - TFP_xdist + d4 * np.cos(rad(180-pump_angle)) # TFP2 to M4

print(f"total length = {cavity_length}, distance_to_TFP1 = {distance_to_TFP1}, remainder = {cavity_length-distance_to_TFP1}, b = {b}, g={g}, Delta={difference_to_ideal_imaging}")
print(f"TFP_dist = {TFP_dist}, TFP_xdist = {TFP_xdist}, xdist_P2_TFP1 = {xdist_P2_TFP1}, d3 = {d3}, d4={d4}")
P1 = Mirror(name="pump mirror 1", phi=-pump_angle) # pump mirror 1
P2 = Mirror(name="pump mirror 2", phi=pump_angle)  # pump mirror 2
M1 = Mirror(name="M1", phi=-pump_angle-tele_angle1) # cut mirror 1

M4 = Mirror(name="M4", phi=pump_angle) # mirror after TFP2
R1 = Curved_Mirror(name=f"R1, f={f1}", phi=-180+tele_angle1, radius=r1)
R2 = Curved_Mirror(name=f"R1, f={f2}", phi=-180+tele_angle2, radius=r2)
TFP1 = Mirror(name="TFP1 (Input)", phi=-90+deg(TFP_angle))
TFP2 = Mirror(name="TFP2 (Outpu)", phi=90-deg(TFP_angle))


Setup = Composition()
Setup.set_light_source(beam)
Setup.pos += offset_axis
Setup.propagate(pump_dist/2)
Setup.add_on_axis(P2)
Setup.propagate(d1)
Setup.add_on_axis(M1)
Setup.propagate(dist_R1_M1)
Setup.add_on_axis(R1)
Setup.propagate(dist_vacuum_tube)
Setup.add_on_axis(vacuum_tube)

if UseNormalDesign:    
    Setup.propagate(f1+f2-dist_vacuum_tube)
    Setup.add_on_axis(R2)
    Setup.propagate(dist_R2_M2)
    Setup.add_on_axis(M2)
    Setup.propagate(xdist_R2_M2+ydist-TFP_ydist)
    print(f"Image Distance = {dist_R2_M2+xdist_R2_M2+ydist-TFP_ydist + d2 + TFP_dist + d3+ d4 + pump_dist/2 - difference_to_ideal_imaging} = {b}")
    

elif UseCompactDesign: 
    Setup.propagate(f1+f2-dist_vacuum_tube-dist_R2_M2)
    Setup.add_on_axis(M2)
    Setup.propagate(dist_R2_M2)
    Setup.add_on_axis(R2)
    Setup.propagate(ydist_R2_M2-ydist_M2_M3)
    print(f"Image Distance = {ydist_R2_M2-ydist_M2_M3+d2+TFP_dist+d3+d4+pump_dist/2 - difference_to_ideal_imaging} = {b}")
    # Setup.propagate(ydist_R2_M2-ydist+TFP_ydist)

    
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


print(f"optical path length = {Setup.optical_path_length()}, cavity length = {cavity_length}")

P1.aperture = P2.aperture = TFP1.aperture = TFP2.aperture = 25.4*2
for elements in Setup._elements:
  elements.set_mount_to_default()
M2.Mount.mount_list[0].flip(90)

PDM1.set_mount(Unit_Mount())
PDM2.set_mount(Unit_Mount())
PDM3.set_mount(Unit_Mount())


"""
Pump Setup
"""

focal_length1 = 125
focal_length2 = 250

pump_module_separation = 300
pump_module_xoffset = focal_length1
pump_module_lens_dist = focal_length1

distance_lens_to_mirror = (2*focal_length2-pump_module_separation)/2

beam1 = Beam(radius=7.5,angle=2.08*np.pi/180,wavelength=940E-6)
beam1.draw_dict["color"] = (255/256,255/256,0.0)

beam2 = Beam(radius=7.5,angle=2.08*np.pi/180,wavelength=940E-6)
beam2.draw_dict["color"] = (255/256,255/256,0.0)

Comp = Composition()
Comp.set_light_source(beam1)
Comp.pos -= (pump_module_xoffset+focal_length1,0,0)

Comp2 = Composition()
Comp2.set_light_source(beam2)
Comp2.pos -= (pump_module_xoffset+focal_length1,pump_module_separation,0)

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
Comp.propagate(pump_module_lens_dist)
Comp.add_on_axis(lens1)
Comp.propagate(focal_length1)

Comp2.pos += offset_axis
Comp2.add_on_axis(Laser_Head_out)
Comp2.propagate(pump_module_lens_dist)
Comp2.add_on_axis(lens4)
Comp2.propagate(focal_length1+focal_length2)
Comp2.add_on_axis(lens3)
Comp2.propagate(distance_lens_to_mirror)
Comp2.add_on_axis(M2)
Comp2.propagate(pump_module_separation)
Comp2.add_on_axis(M1)
Comp2.propagate(distance_lens_to_mirror)
Comp2.add_on_axis(lens2)
Comp2.propagate(focal_length2)
# Laser_Head_out.normal = -Laser_Head_out.normal


from LaserCAD.non_interactings import Breadboard, Crystal 

# breadboard = Breadboard()
# breadboard.pos = (0,0,0)
# breadboard.draw()

table = Crystal(width=900,height=10,thickness=1500)
table.pos = (0,450,-5)
table.draw_dict["Transparency"] = 0
table.draw_dict["color"] = (0.3,0.3,0.3)
table.draw()


table2 = Crystal(width=750,height=10,thickness=900)
table2.pos = (-900,375,-5)
table2.draw_dict["Transparency"] = 0
table2.draw_dict["color"] = (0.3,0.3,0.3)



if freecad_da:
    clear_doc()
    Setup.draw()
    Comp.draw()
    Comp2.draw()
    table.draw()
    table2.draw()
    setview()

Setup.post_positions(verbose=True)
print(Laser_Head_in.pos)