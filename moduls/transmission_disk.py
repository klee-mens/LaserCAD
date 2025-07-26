# -*- coding: utf-8 -*-
"""
Created on Tue Jul 22 09:47:13 2025

@author: mens
"""

from ..basic_optics import Composition, Refractive_plane, inch, Component, Composed_Mount, Mirror
from ..freecad_models import model_mirror
import numpy as np

class Transmission_Disk(Composition):
  def __init__(self, name="NewExtended_TFP", refractive_index=1.5, AOI=56,
               thickness=5, aperture = 2*inch, mount_reversed=False,
               mount_flipped=False, **kwargs):
    super().__init__(name=name, **kwargs)
    self.thickness = thickness
    self.aperture = aperture
    self.refractive_index = refractive_index
    self.__angle_of_incidence = AOI*np.pi/180
    self.AOI = AOI
    inside_angel = np.arcsin(np.sin(self.__angle_of_incidence) / self.refractive_index)
    self.lateral = self.thickness * (np.tan(self.__angle_of_incidence) - np.tan(inside_angel))

    ref1 = Refractive_plane(relative_refractive_index=self.refractive_index)
    ref1.invisible = True
    ref2 = Refractive_plane(relative_refractive_index=1/self.refractive_index)
    ref2.invisible = True
    cosmetic = Component(name="ShapeObject")
    cosmetic.freecad_model = model_mirror
    cosmetic.thickness = self.thickness
    cosmetic.aperture = self.aperture
    cosmetic.set_mount(Composed_Mount(unit_model_list=["KS2", "1inch_post"]))
    cosmetic.draw_dict["color"] = (1.0, 0.0, 2.0)
    self.add_on_axis(ref1)
    self.add_on_axis(cosmetic)
    self.propagate(self.thickness/np.cos(self.__angle_of_incidence))
    self.add_on_axis(ref2)

    ref1.rotate((0,0,1), self.__angle_of_incidence)
    ref2.rotate((0,0,1), self.__angle_of_incidence)
    cosmetic.rotate((0,0,1), self.__angle_of_incidence)
    cosmetic.pos += - cosmetic.get_coordinate_system()[1]*self.lateral/2

    if mount_reversed:
      cosmetic.Mount.reverse()
    if mount_flipped:
      cosmetic.Mount.flip()

  def reflected_beam(self, beam):
    mir = Mirror()
    mir.set_geom(self._elements[0].get_geom())
    return mir.next_beam(beam)