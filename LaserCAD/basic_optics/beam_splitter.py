# -*- coding: utf-8 -*-
"""
Created on Wed Jul 23 10:53:41 2025

@author: mens
"""

from .mirror import Mirror
from .refractive_plane import Refractive_plane
from .mount import Unit_Mount, Composed_Mount, Post
from .beam import Beam
from ..freecad_models.utils import thisfolder
import numpy as np
from copy import deepcopy


class ThinBeamsplitter(Mirror):
  def __init__(self, angle_of_incidence=45, transmission=True,
               name="BeamSplitter", **kwargs):
    super().__init__(phi=180-2*angle_of_incidence, name=name, **kwargs)
    self.transmission = transmission
    self.thickness = 3
    self.draw_dict["color"] = (0.8, 0.1, 0.5) #cosmetic

    self._output_beam = Beam()
    self._input_beam = Beam()
    self._alternative_beam = Beam()

  def next_ray(self, ray):
    if self.transmission:
      return self.just_pass_through(ray)
    return self.reflection(ray)
  
  def next_beam(self, beam):
    self._input_beam = deepcopy(beam)
    output_beam = super().next_beam(beam)
    self._output_beam = output_beam
    self.transmission = not self.transmission
    self._alternative_beam = super().next_beam(beam)
    self.transmission = not self.transmission
    return output_beam
    
  def get_input_beam(self):
    return deepcopy(self._input_beam)
  
  def get_output_beam(self):
    return deepcopy(self._output_beam)

  def get_alternative_beam(self):
    return deepcopy(self._alternative_beam)

  # def _pos_changed(self, old_pos, new_pos):
    # """
    # wird aufgerufen, wen die Position von <self> verändert wird
    # ändert die Position aller __rays mit
    # """
    # super()._pos_changed(old_pos, new_pos)
    # self._rearange_subobjects_pos(old_pos, new_pos, self._input_beam)
    # self._rearange_subobjects_pos(old_pos, new_pos, self._output_beam) #sonst wird ls doppelt geshifted
    # self._rearange_subobjects_pos(old_pos, new_pos, self._alternative_beam)
  
  # def _axes_changed(self, old_axes, new_axes):
  #   """
  #   wird aufgerufen, wen die axese von <self> verändert wird
  #   dreht die axese aller __rays mit
  
  #   dreht außerdem das eigene Koordiantensystem
  #   """
  #   super()._axes_changed(old_axes, new_axes)
  #   self._rearange_subobjects_axes(old_axes, new_axes, self._input_beam)
  #   self._rearange_subobjects_axes(old_axes, new_axes, self._output_beam)
  #   self._rearange_subobjects_axes(old_axes, new_axes, self._alternative_beam)


class ThickBeamsplitter(ThinBeamsplitter):
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



class TFP56(ThickBeamsplitter):
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
    m56 = TFP56_Mount()
    cm = Composed_Mount()
    cm.add(m56)
    if self.flip_mount:
      m56.rotate(vec=m56.normal, phi=np.pi)
    cm.add(Unit_Mount("POLARIS-K1"))
    cm.add(Post())
    self.set_mount(cm)
    if self.revers_mount:
      cm.reverse()


class TFP56_Mount(Unit_Mount):
  def __init__(self, name="TFP56_Mount_Head", **kwargs):
    super().__init__(name=name)
    self.angle_of_incidence = 56
    self.model = "56_degree_mounts"
    self.path = thisfolder + "mount_meshes/special_mount/"
    self.docking_obj.pos += (21.20, 24.85, 0)
    self.docking_obj.rotate(vec=(0,0,1), phi=self.angle_of_incidence*np.pi/180)
    self.is_horizontal = False
    self.draw_dict["color"] = (45/255, 45/255, 45/255)
