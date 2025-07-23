# -*- coding: utf-8 -*-
"""
Created on Wed Jul 23 10:53:41 2025

@author: mens
"""

from .mirror import Mirror
from .refractive_plane import Refractive_plane
from .mount import Unit_Mount
from ..freecad_models.utils import thisfolder
import numpy as np


class ThinBeamsplitter(Mirror):
  def __init__(self, angle_of_incidence=45, transmission=True,
               name="BeamSplitter", **kwargs):
    super().__init__(phi=180-2*angle_of_incidence, name=name, **kwargs)
    self.transmission = transmission
    self.thickness = 3
    self.draw_dict["color"] = (0.8, 0.1, 0.5) #cosmetic

  def next_ray(self, ray):
    if self.transmission:
      return self.just_pass_through(ray)
    return self.reflection(ray)


class ThickBeamplitter(ThinBeamsplitter):
  def __init__(self, angle_of_incidence=45, thickness=5, transmission=True,
               refractive_index=1.45, name="ThickSplitter", **kwargs):
    super().__init__(angle_of_incidence=angle_of_incidence,
                     transmission=transmission, name=name, **kwargs)
    self.thickness = thickness
    self.refractive_index = refractive_index
    self.draw_dict["color"] = (0.2, 0.8, 0.5) #cosmetic

  def next_ray(self, ray):
    if self.transmission:
      surface = Refractive_plane(relative_refractive_index=self.refractive_index)
      surface.set_geom(self.get_geom())
      backside = Refractive_plane(relative_refractive_index=1/self.refractive_index)
      backside.set_axes(self.get_axes())
      backside.pos = self.pos + self.thickness*self.normal
      if np.dot(self.normal, ray.normal) > 0:
        first_ray = surface.next_ray(ray)
        second_ray = backside.next_ray(first_ray)
      else:
        first_ray = backside.next_ray(ray)
        second_ray = surface.next_ray(first_ray)
      return second_ray
    return self.reflection(ray)



class TFP56(ThickBeamplitter):
  def __init__(self, name="NewTFP56", **kwargs):
    super().__init__(name=name, angle_of_incidence=56, **kwargs)
    self.angle_of_incidence = 56
    self.refractive_index = 1.45
    self.thickness = 4

    self.angle_positiv = True
    self.transmission = True
    self.flip_mount = False
    self.revers_mount = False
    self.update_phi()
    self.update_mount()

  def update_phi(self):
    if self.angle_positiv:
      self.phi = 180 - 2*self.angle_of_incidence
    else:
      self.phi = 2*self.angle_of_incidence - 180

  def update_mount(self):
    self.set_mount(TFP56_Mount())
    if self.flip_mount:
     m = self.Mount
     m.rotate(vec=m.normal, phi=np.pi)
    if self.revers_mount:
      self.Mount.reverse()

  # def next_ray(self, ray):
  #   if self.transmission:
  #     surface = Refractive_plane(relative_refractive_index=self.refractive_index)
  #     surface.set_geom(self.get_geom())
  #     backside = Refractive_plane(relative_refractive_index=1/self.refractive_index)
  #     backside.set_axes(self.get_axes())
  #     backside.pos = self.pos + self.thickness*self.normal
  #     if np.dot(self.normal, ray.normal) > 0:
  #       first_ray = surface.next_ray(ray)
  #       second_ray = backside.next_ray(first_ray)
  #     else:
  #       first_ray = backside.next_ray(ray)
  #       second_ray = surface.next_ray(first_ray)
  #     return second_ray
  #   return self.reflection(ray)



class TFP56_Mount(Unit_Mount):
  def __init__(self, name="TFP56_Mount_Head", **kwargs):
    super().__init__(name=name)
    self.angle_of_incidence = 56
    self.model = "56_degree_mounts"
    self.path = thisfolder + "mount_meshes/special_mount/"
    self.docking_obj.pos += (21.20, 24.85, 0)
    self.docking_obj.rotate(vec=(0,0,1), phi=self.angle_of_incidence*np.pi/180)