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
from LaserCAD.non_interactings import Crystal, LaserPointer, Camera
from LaserCAD.basic_optics import Composed_Mount,Unit_Mount,Lens,Post, export_to_TikZ, print_post_positions, ThinBeamsplitter
from copy import deepcopy
from LaserCAD.moduls import Polarization_Rotator

from A3_sketch_generalized import Newport_Mirror, Newport_Curved_Mirror, Table, Cylindric_Crystal, rad, deg


rotate_axis = np.pi
offset_axis = (950+110-15,500,20)

class Adapter_1inch(Composed_Mount):
  def __init__(self, angle=0):
    super().__init__()
    um = Unit_Mount()
    um.model = "1inch_adapter"
    um.path = thisfolder + "misc_meshes/"
    um.docking_obj.pos += (6,38,0) # from manual adjustments in FreeCAD
    um.is_horizontal = False
    um.draw_dict["color"] = (0.3,0.3,0.3)
    self.add(um)
    um.rotate(vec=um.normal, phi=angle*np.pi/180)
    self.add(Unit_Mount(model="Newport-9771-M"))
    self.add(Post())



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

Comp = Composition(name="PM19 top")
Comp.set_light_source(beam1)
Comp.pos -= (pump_module_xoffset,0,0)


Comp2 = Composition(name="PM19 bot")
Comp2.set_light_source(beam2)
Comp2.pos -= (pump_module_xoffset,pump_module_separation,0)

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

# Comp.rotate((0,0,1), rotate_axis)
Comp.pos += offset_axis
print(f"PM19 top position = ({Comp.pos[0]/10:.1f}cm, {Comp.pos[1]/10:.1f}cm, {Comp.pos[2]/10:.1f}cm)")
Comp.add_on_axis(Laser_Head_in)
# Comp.propagate(pump_module_lens_dist)
# Comp.add_on_axis(lens1)
# Comp.propagate(image_distance)

Comp2.pos += offset_axis
print(f"PM19 bot position = ({Comp2.pos[0]/10:.1f}cm, {Comp2.pos[1]/10:.1f}cm, {Comp2.pos[2]/10:.1f}cm)")
Comp2.add_on_axis(Laser_Head_out)
Comp2.propagate(pump_module_lens_dist)
Comp2.add_on_axis(lens4)
# Comp2.propagate(focal_length1+focal_length2)
Comp2.propagate(image_distance+focal_length2)
Comp2.add_on_axis(lens3)
Comp2.propagate(distance_lens_to_mirror)
Comp2.add_on_axis(M3_2)
Comp2.propagate(pump_module_separation)
Comp2.add_on_axis(M3_1)
Comp2.propagate(distance_lens_to_mirror)
Comp2.add_on_axis(lens2)
Comp2.propagate(focal_length2)

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


"""
#####################################
Mach Zehnder Setup
#####################################
"""
focal_length_tele1 = -30
focal_length_tele2 = 400
x_deviation = -950
y_deviation = 180
total_deviation = np.sqrt(x_deviation**2 + y_deviation**2)
angle_of_incidence = np.arctan(y_deviation/x_deviation) * 180 / np.pi
angle_mach_zehnder = 35

beam = Beam(radius=0.8, angle=0)
beam.draw_dict["color"] = (0.0,1.0,0.0)
# beam.pos=[0,0,0]

Laser = LaserPointer(name="Laser Pointer 1")
Camera1 = Camera(name="Camera 1")
M1 = Newport_Mirror(name="pump mirror 1", phi=180+50, aperture=25.4) # pump mirror 1
M1.set_mount(Adapter_1inch(angle=180))
M2 = Newport_Mirror(name="M2", phi=180-50-angle_of_incidence, aperture=2*25.4)
M3 = Newport_Mirror(name="M3", phi=-90)
M4 = Newport_Mirror(name="M4", phi=-90)
M5 = Newport_Mirror(name="M5", phi=180-2*angle_mach_zehnder-angle_of_incidence, aperture=25.4)
TFP1 = ThinBeamsplitter(transmission=True, angle_of_incidence=-angle_mach_zehnder, name="TFP1")
TFP1.aperture = 25.4*2
TFP1.set_mount(Composed_Mount(unit_model_list=["U200-A2K", "1inch_post"]))
TFP1.Mount.flip()

TFP2 = ThinBeamsplitter(transmission=False, angle_of_incidence=25+angle_of_incidence/2, name="TFP2")
TFP2.aperture = 25.4*2
TFP2.set_mount(Composed_Mount(unit_model_list=["U200-A2K", "1inch_post"]))


telelens1 = Lens(f=focal_length_tele1, name=f"telescope lens 1, f={focal_length_tele1}mm")
telelens1.aperture = 25.4*1
telelens1.set_mount_to_default()
telelens2 = Lens(f=focal_length_tele2, name=f"telescope lens 2, f={focal_length_tele2}mm")
telelens2.aperture = 25.4*2
telelens2.set_mount_to_default()


Setup = Composition(name="Mach Zehnder")
Setup.set_light_source(beam)
Setup.normal = (-x_deviation, -y_deviation,0)
Setup.pos += offset_axis
Setup.pos += (x_deviation, y_deviation,0)
Setup.add_on_axis(Laser)
Setup.propagate(200)
Setup.add_on_axis(telelens1)
Setup.propagate(focal_length_tele1+focal_length_tele2)
Setup.add_on_axis(telelens2)
Setup.propagate(200)
Setup.add_on_axis(TFP1)
Setup.propagate(total_deviation-(200+200+focal_length_tele1+focal_length_tele2))
Setup.propagate(170)
Setup.add_on_axis(M1)
Setup.propagate(240)
Setup.add_on_axis(TFP2)
Setup.propagate(50)
Setup.add_on_axis(M3)
Setup.propagate(240)
Setup.add_on_axis(M4)
Setup.propagate(400)
Setup.add_on_axis(Camera1)

Setup.compute_beams()
arm2_lightsource = TFP1._alternative_beam
Setup2 = Composition(name="Mach Zehnder 2")
Setup2.set_geom(arm2_lightsource.get_geom())
Setup2.set_light_source(arm2_lightsource) 
Setup2.propagate(256)
Setup2.add_on_axis(M5)
Setup2.propagate(305)

# Setup2.propagate(100.1)
# rotator= Polarization_Rotator()
# Setup2.add_supcomposition_on_axis(rotator)
# Setup2._optical_axis[-1] = rotator._optical_axis[-1]
# Setup2.propagate(0)

if freecad_da:
    clear_doc()
    Comp.draw()
    Comp2.draw()
    Setup.draw()
    Setup2.draw()
    table.draw()
    table2.draw()
    Housing.draw()
    Housing2.draw()
    LiMgAS_crystal2.draw()
    LiMgAS_crystal1.draw()
    setview()

else:
    print_post_positions(Comp)
    print_post_positions(Comp2)
    print_post_positions(Setup)
    print_post_positions(Setup2)

    # export_to_TikZ(Comp, draw_beams=True, beam_color="optikzred")
    # export_to_TikZ(Comp2, draw_beams=True, beam_color="optikzred")
    # export_to_TikZ(Setup, draw_rays=True, beam_color="green")
