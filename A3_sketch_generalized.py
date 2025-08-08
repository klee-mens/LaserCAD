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
import matplotlib.pyplot as plt
import sys

from LaserCAD.freecad_models import clear_doc, setview, freecad_da, model_mirror, add_to_composition
from LaserCAD.basic_optics import Mirror, Beam, Ray_Distribution, Composition, Component, inch, Curved_Mirror, Ray, Geom_Object
from LaserCAD.basic_optics import Grating, Opt_Element
import matplotlib.pyplot as plt
from LaserCAD.freecad_models.utils import thisfolder, load_STL
from LaserCAD.non_interactings import Crystal, Lambda_Plate, Pockels_Cell
from LaserCAD.basic_optics import Composed_Mount,Unit_Mount,Lens,Post, export_to_TikZ, print_post_positions
from copy import deepcopy
from LaserCAD.moduls import Polarization_Rotator


def rad(angle):
    return np.pi/180*angle

def deg(angle):
    return 180/np.pi*angle

def get_TFP_distances(TFP_ydist, TFP_angle):
    TFP_xdist = TFP_ydist*np.tan(TFP_angle)
    TFP_dist = np.sqrt(TFP_ydist**2 + TFP_xdist**2)
    TFP_delta = TFP_dist - TFP_ydist - TFP_xdist
    
    TFP_Lam = 0.2*TFP_dist
    Lam_PC = 0.6*TFP_dist
    PC_TFP = TFP_dist - TFP_Lam - Lam_PC
    
    return TFP_dist, TFP_xdist, TFP_delta, TFP_Lam, Lam_PC, PC_TFP

rotate_axis = np.pi
offset_axis = (950+110-15,500,20)

class Newport_Mirror(Mirror):
    def __init__(self, name="Newport Mirror", aperture=25.4, **kwargs):
        super().__init__(name=name, aperture=aperture, **kwargs)
        self.aperture = aperture
        if self.aperture == 25.4:
            self.set_mount(Composed_Mount(unit_model_list=["U100-A2K", "1inch_post"]))
        elif self.aperture == 2*25.4:
            self.set_mount(Composed_Mount(unit_model_list=["U200-A2K", "1inch_post"]))
        elif self.aperture == 3*25.4:
            self.set_mount(Composed_Mount(unit_model_list=["U300-A2K", "1inch_post"]))

class Newport_Curved_Mirror(Curved_Mirror):
    def __init__(self, name="Newport Mirror", aperture=25.4, **kwargs):
        super().__init__(name=name, aperture=aperture, **kwargs)
        self.aperture = aperture
        if self.aperture == 25.4:
            self.set_mount(Composed_Mount(unit_model_list=["U100-A2K", "1inch_post"]))
        elif self.aperture == 2*25.4:
            self.set_mount(Composed_Mount(unit_model_list=["U200-A2K", "1inch_post"]))

class Table(Crystal):
    def __init__(self, name="Table", width=1000, height=10, thickness=1000, **kwargs):
        super().__init__(name=name, width=width, height=height, thickness=thickness, **kwargs)
        self.draw_dict["Transparency"] = 0
        self.draw_dict["color"] = (0.3, 0.3, 0.3)

class Adapter_2inch(Composed_Mount):
  def __init__(self, angle=0):
    super().__init__()
    um = Unit_Mount()
    um.model = "2inch_adapter"
    um.path = thisfolder + "misc_meshes/"
    um.docking_obj.pos += (14.3,64,0) # from manual adjustments in FreeCAD
    um.is_horizontal = False
    um.draw_dict["color"] = (0.3,0.3,0.3)
    self.add(um)
    um.rotate(vec=um.normal, phi=angle*np.pi/180)
    self.add(Unit_Mount(model="U200-A2K"))
    self.add(Post())

class Cylindric_Crystal(Component):
  def __init__(self, name="LaserCrystal", aperture=6, thickness=3, **kwargs):
    super().__init__(name=name, **kwargs)
    self.aperture = aperture
    self.thickness = thickness
    self.draw_dict["color"] = (0.8, 0.3, 0.1)
    self.freecad_model = model_mirror
    self.pos += offset_axis

# pockels_cell = Component(name="Pockels Cell")
# pockels_cell.draw_dict["stl_file"]= rf"{thisfolder}\mount_meshes\A2_mounts\Pockels_cell.stl"
# pockels_cell.freecad_model = load_STL

vacuum_tube = Component(name="Vacuum Tube")
vacuum_tube.draw_dict["stl_file"]= rf"{thisfolder}\mount_meshes\special_mount\Vacuum_Tube_1300mm.stl"
vacuum_tube.freecad_model = load_STL

"""
Simulation of the amplifier cavity
"""

Pol_Rotater = Polarization_Rotator()
r1 = 2000 
r2 = 2500

f1 = r1/2
f2 = r2/2

beam = Beam(radius=5, angle=0)
beam.pos=[0,0,0]

if UsePolRotator:
    g = 500 # object distance: distance between the pump region and the first curved mirror
    length_diff = Pol_Rotater.length_diff
    if UseNormalDesign: g -= 20
else: 
    g = 520#520
    length_diff = 0
    if UseNormalDesign: g = 490
    
    

# Calculation of the image distance
b = ((f1-g)*f2**2 + f1**2 * f2) / (f1**2)

pump_angle = 90   # input-output angle on the pump mirrors, standard: 90
tele_angle1 = 4   # opening angle for coupling into telescope
tele_angle2 = 4   # opening angle for couling into telescope

ydist_M2_M3 = 60 if UseCompactDesign else 0 # y-distance between M2 and M3, standard: 60mm

xdist_R1_M1 = 300-ydist_M2_M3/2 # cut mirror x-distance from spherical mirrors
ydist_R2_M2 = 300+ydist_M2_M3/2 # cut mirror y-distance from spherical mirrors

dist_R1_M1 = xdist_R1_M1 / np.cos(rad(tele_angle1)) # propagation distance to first spherical mirror
dist_R2_M2 = ydist_R2_M2 / np.cos(rad(tele_angle2)) # propagation distance to second spherical mirror

ydist_R1_M1 = np.sqrt(dist_R1_M1**2 - xdist_R1_M1**2)
xdist_R2_M2 = np.sqrt(dist_R2_M2**2 - ydist_R2_M2**2)


TFP_angle = 66
TFP_angle = rad(2*TFP_angle - 90)

difference_to_ideal_imaging = 100 - length_diff # propagation difference to ideal imaging (after roundtrip)
            
cavity_length = f1 + f2 + g + b + difference_to_ideal_imaging   # total cavity length, g-object distance, b-image distance
            
pump_dist = 125    # 150            # length of pump section
P2_shift = 5
dist_P2_M1 = g-dist_R1_M1-pump_dist/2       # distance from P2 to M1
xdist_M3_TFP1 = 130                            # x-distance from M3 to TFP1
dist_vacuum_tube = xdist_R1_M1 + 70


if UseNormalDesign:
    TFP_ydist = 170
    TFP_dist, TFP_xdist, TFP_delta, TFP_Lam, Lam_PC, PC_TFP = get_TFP_distances(TFP_ydist, TFP_angle)
    
    xdist_P1_TFP1 = f1 + f2 - xdist_R1_M1 - ydist_R2_M2 - xdist_M3_TFP1 - pump_dist
    ydist = 0.5*(cavity_length - f1 - f2 - TFP_delta - (xdist_P1_TFP1 + pump_dist + xdist_M3_TFP1) - (dist_R1_M1 + dist_R2_M2 + ydist_R1_M1 + xdist_R2_M2))
    M2 = Newport_Mirror(phi=-90-tele_angle2, name="M2") # cut mirror 2
    M3 = Newport_Mirror(phi=90, name="M3") # mirror to TFP1

else: # UseCompactDesign
    # ydist: difference between beam y-position at TFP2 and the vacuum tube
    # ydist_M2_M3: y-distance between M2 and M3
    # ydist_P2_TFP1: y-distance between pump mirror P2 and TFP1
    # xdist_P1_TFP1: x-distance between pump mirror P2 and TFP1

    pump_angle_rad = rad(180-pump_angle)
    
    # is 1 for a pump angle of 90°
    pump_angle_correction_factor = 1/np.tan(pump_angle_rad) + 1/np.sin(pump_angle_rad)
    x_correction_by_angled_pump = dist_P2_M1 * np.cos(rad(180-pump_angle))  
    
    ydist_P2_TFP1 = (dist_P2_M1 * np.sin(rad(180-pump_angle)) - ydist_R1_M1 - ydist_M2_M3) * pump_angle_correction_factor
    xdist_P1_TFP1 = f1 + f2 + xdist_R2_M2 - dist_R2_M2 - xdist_R1_M1 + x_correction_by_angled_pump - pump_dist - xdist_M3_TFP1
    
    distance_to_TFP1 = g + f1 + f2 + ydist_R2_M2 - ydist_M2_M3 + xdist_M3_TFP1

    TFP_ydist = (cavity_length - xdist_P1_TFP1 - distance_to_TFP1 - pump_dist/2 + ydist_P2_TFP1) / (1/np.cos(TFP_angle)- np.tan(TFP_angle) + pump_angle_correction_factor)
    TFP_dist, TFP_xdist, TFP_delta, TFP_Lam, Lam_PC, PC_TFP = get_TFP_distances(TFP_ydist, TFP_angle)
    ydist = TFP_ydist + ydist_M2_M3
    
    M2 = Newport_Mirror(phi=90-tele_angle2, name="M2, cut mirror 2") # cut mirror 2
    M3 = Newport_Mirror(phi=-90, name="M3, mirror towards tfp 1") # mirror to TFP1


dist_M4_P1 = (ydist - dist_P2_M1*np.sin(rad(180-pump_angle)) + ydist_R1_M1) / np.sin(rad(pump_angle))  # M4 to P1 (pump mirror 1)
dist_TFP2_M4 = xdist_P1_TFP1 - TFP_xdist + dist_M4_P1 * np.cos(rad(180-pump_angle)) # TFP2 to M4

print(f"g = {g}, b={b}, difference to ideal image={difference_to_ideal_imaging}")

P1 = Newport_Mirror(name="pump mirror 1", phi=-pump_angle, aperture=25.4*2) # pump mirror 1
P1.set_mount(Adapter_2inch(angle=90))
P2 = Newport_Mirror(name="pump mirror 2", phi=pump_angle, aperture=25.4*2)  # pump mirror 2
M1 = Newport_Mirror(name="M1, cut mirror 1", phi=-pump_angle-tele_angle1) # cut mirror 1

M4 = Newport_Mirror(name="M4, mirror after tfp 2", phi=pump_angle) # mirror after TFP2
R1 = Newport_Curved_Mirror(name=f"R1, f={f1:.0f}mm", phi=-180+tele_angle1, radius=r1)
R2 = Newport_Curved_Mirror(name=f"R1, f={f2:.0f}mm", phi=-180+tele_angle2, radius=r2)
TFP1 = Newport_Mirror(name="TFP1 (Input)", phi=-90+deg(TFP_angle), aperture=25.4*2)
TFP2 = Newport_Mirror(name="TFP2 (Output)", phi=90-deg(TFP_angle), aperture=25.4*2)
pockels_cell = Pockels_Cell(name="Pockels Cell", mount_name="Pockels_cell")

Setup = Composition(name="A3")
Setup.set_light_source(beam)
Setup.pos += offset_axis
Setup.propagate(pump_dist/2)
Setup.add_on_axis(P2)
Setup.propagate(dist_P2_M1)
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
    print(f"Image Distance = {dist_R2_M2+xdist_R2_M2+ydist-TFP_ydist + xdist_M3_TFP1 + TFP_dist + dist_TFP2_M4+ dist_M4_P1 + pump_dist/2 - difference_to_ideal_imaging} (adding all lengths) = {b} (b)")
    

elif UseCompactDesign: 
    Setup.propagate(f1+f2-dist_vacuum_tube-dist_R2_M2)
    Setup.add_on_axis(M2)
    Setup.propagate(dist_R2_M2)
    Setup.add_on_axis(R2)
    Setup.propagate(ydist_R2_M2-ydist_M2_M3)
    print(f"Image Distance = {ydist_R2_M2-ydist_M2_M3+xdist_M3_TFP1+TFP_dist+dist_TFP2_M4+dist_M4_P1+pump_dist/2 - difference_to_ideal_imaging} (adding all lengths) = {b} (b)")
    # Setup.propagate(ydist_R2_M2-ydist+TFP_ydist)

    
Setup.add_on_axis(M3)
Setup.propagate(xdist_M3_TFP1)
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
pockels_cell.rotate(pockels_cell.normal, np.pi)

Setup.propagate(PC_TFP)
Setup.add_on_axis(TFP2)
Setup.propagate(dist_TFP2_M4+P2_shift)
Setup.add_on_axis(M4)
Setup.propagate(dist_M4_P1)
Setup.add_on_axis(P1)
Setup.propagate(pump_dist/2-P2_shift)

print(f"optical path length = {Setup.optical_path_length():.2f}, cavity length = {cavity_length:.2f}\n")

M3.Mount.mount_list[0].flip(90)
# P1.Mount.mount_list[0].flip(90)


"""
#####################################
Pump Setup
#####################################
"""
pump_magnification = 0.45  
max_pump_power = 15.7 # kW
pump_spot_size = 15 # mm
final_pump_area = 1e-2*(pump_magnification*pump_spot_size)**2 # cm^2

focal_length1 = 75 # 125
focal_length2 = 200

object_distance = focal_length1 * (1 + 1/pump_magnification)
image_distance = focal_length1 * (1 + pump_magnification)

print(f"object distance = {object_distance:.1f}mm, image distance = {image_distance:.1f}mm")
print(f"pump magnification = {pump_magnification:.2f}, final spot size = {pump_magnification*pump_spot_size:.1f}mm, A = {final_pump_area:.2f}cm²")
print(f"pump intensity = {max_pump_power/final_pump_area:.1f}kW/cm²\n")
image_plane_to_pump_module_distance = 65

pump_module_separation = 300
pump_module_xoffset = object_distance + image_plane_to_pump_module_distance + image_distance
pump_module_lens_dist = object_distance + image_plane_to_pump_module_distance

distance_lens_to_mirror = (2*focal_length2-pump_module_separation)/2

beam1 = Ray_Distribution(radius=pump_spot_size/2,angle=0*2.08*np.pi/180,wavelength=940E-6, steps=3)
beam1.draw_dict["color"] = (255/256,255/256,0.0)

beam2 = Ray_Distribution(radius=pump_spot_size/2,angle=0*2.08*np.pi/180,wavelength=940E-6, steps=3)
beam2.draw_dict["color"] = (255/256,255/256,0.0)

Pump_top = Composition(name="PM19 top")
Pump_top.set_light_source(beam1)
Pump_top.pos -= (pump_module_xoffset,0,0)


Pump_bot = Composition(name="PM19 bot")
Pump_bot.set_light_source(beam2)
Pump_bot.pos -= (pump_module_xoffset,pump_module_separation,0)

Laser_Head_in = Component(name="Pump Module PM19 bot")
stl_file = rf"{thisfolder}\misc_meshes\PM19_2.stl"
Laser_Head_in.draw_dict["stl_file"]=stl_file
Laser_Head_in.freecad_model = load_STL

Laser_Head_out = Component(name="Pump Module PM19 top")
stl_file = rf"{thisfolder}\misc_meshes\PM19_2.stl"
Laser_Head_out.draw_dict["stl_file"]=stl_file
Laser_Head_out.freecad_model = load_STL

lens1 = Lens(f=focal_length1, name=f"Pump Lens 1, f={focal_length1}mm")
lens1.aperture = 25.4*2
lens1.set_mount_to_default()
lens2 = Lens(f=focal_length2, name=f"telescope lens 1, f={focal_length2}mm")
lens2.aperture = 25.4*3
lens2.set_mount_to_default()
lens3 = deepcopy(lens2)
lens4 = deepcopy(lens1)

lens3.name = f"telescope lens 2, f={focal_length2}mm"
lens4.name = f"Pump Lens 2, f={focal_length1}mm"

M3_1 = Newport_Mirror(phi=90, name="3inch mirror", aperture=25.4*3)
M3_2 = deepcopy(M3_1)
M3_2.name = "3inch mirror 2"

# Pump_top.rotate((0,0,1), rotate_axis)
Pump_top.pos += offset_axis
print(f"PM19 top position = ({Pump_top.pos[0]/10:.1f}cm, {Pump_top.pos[1]/10:.1f}cm, {Pump_top.pos[2]/10:.1f}cm)")
Pump_top.add_on_axis(Laser_Head_in)
Pump_top.propagate(pump_module_lens_dist)
Pump_top.add_on_axis(lens1)
Pump_top.propagate(image_distance)

Pump_bot.pos += offset_axis
print(f"PM19 bot position = ({Pump_bot.pos[0]/10:.1f}cm, {Pump_bot.pos[1]/10:.1f}cm, {Pump_bot.pos[2]/10:.1f}cm)\n")
Pump_bot.add_on_axis(Laser_Head_out)
Pump_bot.propagate(pump_module_lens_dist)
Pump_bot.add_on_axis(lens4)
# Pump_bot.propagate(focal_length1+focal_length2)
Pump_bot.propagate(image_distance+focal_length2)
Pump_bot.add_on_axis(lens3)
Pump_bot.propagate(distance_lens_to_mirror)
Pump_bot.add_on_axis(M3_2)
Pump_bot.propagate(pump_module_separation)
Pump_bot.add_on_axis(M3_1)
Pump_bot.propagate(distance_lens_to_mirror)
Pump_bot.add_on_axis(lens2)
Pump_bot.propagate(focal_length2)

table = Table(name="Right Table", width=900, height=10, thickness=1500)
table.pos = (0,450,-5)

table2 = Table(name="Left Table", width=750, height=10, thickness=900)
table2.pos = (-900,375,-5)

Housing = Table(name="Housing", width=40, height=40, thickness=15)
Housing.pos = offset_axis
Housing.pos += (-18, 0, 80)
Housing.draw_dict["color"] = (181/255, 166/255, 66/255)

Housing2 = Table(name="Housing", width=40, height=40, thickness=15)
Housing2.pos = offset_axis
Housing2.pos += (3, 0, 80)
Housing2.draw_dict["color"] = (181/255, 166/255, 66/255)

LiMgAS_crystal1 = Cylindric_Crystal(name="LiMgAs", aperture=15, thickness=11)
LiMgAS_crystal1.pos += (1,0,0)

LiMgAS_crystal2 = Cylindric_Crystal(name="LiMgAs2", aperture=15, thickness=11)
LiMgAS_crystal2.pos += (-12, 0, 0)

if freecad_da:
    clear_doc()
    Setup.draw()
    Pump_top.draw()
    Pump_bot.draw()
    table.draw()
    table2.draw()
    Housing.draw()
    Housing2.draw()
    LiMgAS_crystal2.draw()
    LiMgAS_crystal1.draw()
    # setview()

else:
    print_post_positions(Setup) 
    print_post_positions(Pump_top)
    print_post_positions(Pump_bot)

    # export_to_TikZ(Pump_top, draw_beams=True, beam_color="optikzred")
    # export_to_TikZ(Pump_bot, draw_beams=True, beam_color="optikzred")
    # export_to_TikZ(Setup, draw_rays=True)
