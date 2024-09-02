# -*- coding: utf-8 -*-
"""
Created on Mon Aug 19 09:21:01 2024

@author: 12816
"""

import sys
# import os

pfad = __file__
pfad = pfad.replace("\\","/") #folder conventions windows linux stuff
pfad = pfad.lower()
ind = pfad.rfind("lasercad")
pfad = pfad[0:ind-1]
if not pfad in sys.path:
  sys.path.append(pfad)
from copy import deepcopy

from LaserCAD.basic_optics import Mirror,Beam,Cylindrical_Mirror,Grating,Ray
from LaserCAD.basic_optics import Intersection_plane,Cylindrical_Mirror1
from LaserCAD.basic_optics import Curved_Mirror, Composition
from LaserCAD.basic_optics.beam import CircularRayBeam

from LaserCAD.basic_optics import Unit_Mount,Composed_Mount
from LaserCAD.non_interactings import Pockels_Cell
from LaserCAD.non_interactings import Lambda_Plate

from LaserCAD.freecad_models import clear_doc, setview, add_to_composition
from LaserCAD.freecad_models import freecad_da
from LaserCAD.moduls import Make_RoofTop_Mirror, Make_Periscope
from LaserCAD.moduls.periscope import Rooftop_Mirror_Component
from LaserCAD.basic_optics.refractive_plane import Refractive_plane

import matplotlib.pyplot as plt
import numpy as np

if freecad_da:
  clear_doc()

class Laser_bar(Beam):
  def __init__(self, radius=5, angle=0, name="NewBeam", wavelength=1030E-6, 
               ray_count = 11, **kwargs):
    super().__init__(radius=radius, angle=angle,name=name,wavelength=wavelength, **kwargs)
    self._ray_count = ray_count
    self._rays = [Ray() for n in range(self._ray_count)]
    self._angle = angle
    self._radius = radius
    self._Bwavelength = wavelength
    self._distribution = "ray_group"
    self.make_line_distribution(ray_count)
    self.draw_dict["model"] = "ray_group"
    
  def make_line_distribution(self, ray_count=2):
    self._ray_count = ray_count
    self._rays = [Ray() for n in range(self._ray_count)]
    mr = self._rays[0]
    mr.set_geom(self.get_geom())
    mr.name = self.name + "_inner_Ray"
    mr.wavelength = self._Bwavelength
    # thetas = np.linspace(0, 2*np.pi, self._ray_count)
    ray_number = 1
    for n in np.arange(-int(self._ray_count/2),round(self._ray_count/2)):
      if n != 0:
        our = self._rays[ray_number]
        if n< 0:
          our.from_h_alpha_theta(self._radius*abs(n)/int(self._ray_count/2), self._angle*abs(n)/int(self._ray_count/2),np.pi*3/2, self)
        else:
          our.from_h_alpha_theta(self._radius*abs(n)/int(self._ray_count/2), self._angle*abs(n)/int(self._ray_count/2),np.pi/2, self)
        our.name = self.name + "_outer_Ray" + str(ray_number)
        ray_number+=1
        our.wavelength = self._Bwavelength

Pump1 = Laser_bar(radius=5, angle=np.pi/180*1,wavelength=885E-6)
# for ray in Pump1._rays:
#   ray.draw_dict["color"]=(0.86,0.08,0.24)
# Pump2 = deepcopy(Pump1)

Pump4 = deepcopy(Pump1)
# Pump1.draw()
Laser_sourse = Laser_bar(radius=5, angle=0,wavelength=1064E-6)
for ray in Laser_sourse._rays:
  ray.draw_dict["color"]=(0.86,0.08,0.24)
Comp = Composition()
Comp.set_light_source(Laser_sourse)
# Comp.propagate(100)
r1 = Refractive_plane(r_ref_index=1.816)
r1.pos += (100,0,0)
r1.rotate((0,0,1), np.arctan(1/1.816))
Comp.add_fixed_elm(r1)
# Comp.propagate(100)
r2 = Refractive_plane(r_ref_index=1/1.816)
r2.pos += (150,0,0)
r2.rotate((0,0,1), np.arctan(1/1.816))
Comp.add_fixed_elm(r2)
Comp.recompute_optical_axis()
Comp.propagate(100)
Comp.draw()

r3 = Refractive_plane(r_ref_index=1.822)
r3.pos += (100,7,0)
r3.normal = (0.23236,-0.97263,0)
r4 = Refractive_plane(r_ref_index=1/1.822)
r4.pos += (120,-2,0)
r4.normal = (0.23236,-0.97263,0)
Pump1.rotate((0,0,1), -(np.arctan(1/1.822)+np.arcsin(np.sin(np.arctan(1/1.822))/1.822)))
Pump1.pos += (67,50,0)
Comp1= Composition()
Comp1.set_geom(Pump1.get_geom())
Comp1.set_light_source(Pump1)
Comp1.add_fixed_elm(r3)
Comp1.add_fixed_elm(r4)
Comp1.recompute_optical_axis()
Comp1.propagate(0.050)
Comp1.draw()

Pump2 = deepcopy(Pump1)
Pump2.pos += (20,0,0)
Comp2= Composition()
Comp2.set_geom(Pump2.get_geom())
Comp2.set_light_source(Pump1)
Comp2.add_fixed_elm(r3)
Comp2.add_fixed_elm(r4)
Comp2.recompute_optical_axis()
Comp2.propagate(0.050)
Comp2.draw_beams()

Pump3 = deepcopy(Pump1)
Pump3.normal = -Pump1.normal 
Pump3.pos += (70,-92,0)
Comp3= Composition()
Comp3.set_geom(Pump3.get_geom())
Comp3.set_light_source(Pump1)
r5= deepcopy(r3)
r5.relative_refractive_index = 1/1.822
r5.normal = -r5.normal
r6 = deepcopy(r4)
r6.relative_refractive_index = 1.822
r6.normal = -r6.normal 
Comp3.add_fixed_elm(r6)
Comp3.add_fixed_elm(r5)
Comp3.recompute_optical_axis()
Comp3.propagate(0.050)
Comp3.draw_beams()

Pump4 = deepcopy(Pump3)
Pump4.pos += (20,0,0)
Comp4= Composition()
Comp4.set_geom(Pump4.get_geom())
Comp4.set_light_source(Pump1)
Comp4.add_fixed_elm(r6)
Comp4.add_fixed_elm(r5)
Comp4.recompute_optical_axis()
Comp4.propagate(0.050)
Comp4.draw_beams()

if freecad_da:
  setview()