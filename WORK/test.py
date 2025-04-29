# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 14:01:12 2024

@author: 12816
"""
from LaserCAD.basic_optics import Beam, Refractive_plane
from LaserCAD.freecad_models import freecad_da, clear_doc, setview
import numpy as np
from LaserCAD.non_interactings import Faraday_Isolator

if freecad_da:
  clear_doc()

farad = Faraday_Isolator()
farad.draw()
farad.draw_mount()

# THICKNESS = 42

# ref = Refractive_plane()

# b0 = Beam(radius=1.5)

# ref.pos += (60, 0 , 0)
# ref.normal = (1,1,0)
# # ref.normal = (0.1+np.random.rand(), np.random.rand(), np.random.rand())

# b1 =  ref.next_beam(b0)

# ref2 = Refractive_plane(relative_refractive_index=1/1.5)

# # ref2.pos += (2*60, 0 , 0)
# # ref2.normal = ref.normal
# ref2.set_geom(ref.get_geom())
# ref2.pos += ref.normal * THICKNESS

# b2 = ref2.next_beam(b1)



# from LaserCAD.basic_optics import Opt_Element, Composition, inch, Mirror
# from LaserCAD.freecad_models import model_lens
# from LaserCAD.basic_optics import TOLERANCE
# from copy import deepcopy

# class Transmission_Optic(Opt_Element):
#   def __init__(self, name="NewTransmissionOptic", refractive_index=1.5,
#                thickness=5, **kwargs):
#     super().__init__(name=name, **kwargs)
#     self.thickness = thickness
#     self.refractive_index = refractive_index
#     self.freecad_model = model_lens

#   def update_draw_dict(self):
#     super().update_draw_dict()
#     self.draw_dict["Radius1"] = 0
#     self.draw_dict["Radius2"] = 0

#   def next_ray(self, ray):
#     ray2 = deepcopy(ray)
#     ray2.pos = self.intersection(ray)
#     alpha = ray.angle_to(self)
#     if np.abs(alpha) < TOLERANCE:
#       return ray2
#     beta = np.arcsin(np.sin(alpha)/self.refractive_index)
#     shift = self.thickness*(np.tan(alpha) - np.tan(beta))
#     surface_vec = ray.normal -np.sum(ray.normal*self.normal)* self.normal
#     surface_vec *= 1/np.linalg.norm(surface_vec)
#     ray2.pos += - surface_vec*shift*np.sign(alpha)
#     return ray2

# tro = Transmission_Optic(thickness=60/2**0.5)
# tro.aperture = 100
# tro.set_geom(ref.get_geom())
# b3 = tro.next_beam(b0)
# b3.set_length(410)

# from LaserCAD.freecad_models import model_mirror
# from LaserCAD.basic_optics import Composed_Mount, Component


# class Transmission_Disk(Composition):
#   def __init__(self, name="NewExtended_TFP", refractive_index=1.5, AOI=56,
#                thickness=5, aperture = 2*inch, **kwargs):
#     super().__init__(name=name, **kwargs)
#     self.thickness = thickness
#     self.aperture = aperture
#     self.refractive_index = refractive_index
#     self.angle_of_incidence = AOI

#     ref1 = Refractive_plane(relative_refractive_index=self.refractive_index)
#     ref1.invisible = True
#     ref2 = Refractive_plane(relative_refractive_index=1/self.refractive_index)
#     ref2.invisible = True
#     cosmetic = Component(name="ShapeObject")
#     cosmetic.freecad_model = model_mirror
#     cosmetic.thickness = self.thickness
#     cosmetic.aperture = self.aperture
#     cosmetic.set_mount(Composed_Mount(unit_model_list=["KS2", "1inch_post"]))
#     cosmetic.draw_dict["color"] = (1.0, 0.0, 2.0)
#     self.add_on_axis(ref1)
#     self.add_on_axis(cosmetic)
#     self.propagate(self.thickness/np.cos(self.angle_of_incidence*np.pi/180))
#     self.add_on_axis(ref2)

#     ref1.rotate((0,0,1), self.angle_of_incidence*np.pi/180)
#     ref2.rotate((0,0,1), self.angle_of_incidence*np.pi/180)
#     cosmetic.rotate((0,0,1), self.angle_of_incidence*np.pi/180)
#     # self.set_sequence([0,1])



# # =============================================================================
# # drawing
# # =============================================================================
# b0.draw()
# ref.draw()
# b1.draw()
# ref2.draw()
# b2.draw()

# tro.draw()
# b3.draw()


# tfp = Transmission_Disk(thickness=THICKNESS)
# # tfp = Transmission_Disk(thickness=7)
# tfp.set_geom(tro.get_geom())
# tfp._lightsource = b0
# tfp.propagate(300)
# tfp.draw()

# comp = Composition()
# comp.propagate(100)
# comp.add_on_axis(Mirror(phi=90))
# comp.propagate(200)
# tfp = Transmission_Disk(AOI=-56, thickness=8)
# comp.add_supcomposition_on_axis(tfp)
# # tfp.rotate((0,0,1), -45*np.pi/180)
# comp.recompute_optical_axis()
# comp.propagate(400)
# comp.add_on_axis(Mirror(phi=90))
# comp.propagate(100)

# tfp_shape = comp.non_opticals[0]
# tfp_shape.Mount.reverse()

# comp.draw()

# for ray in comp._optical_axis:
#   ray.draw()


from LaserCAD.non_interactings import LaserPointer

las = LaserPointer()
las.draw()
las.draw_mount()
b = Beam()
b.draw()

if freecad_da:
  setview()