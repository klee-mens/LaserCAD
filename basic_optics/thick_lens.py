# -*- coding: utf-8 -*-
"""
Created on Wed Apr 12 09:05:00 2023

@author: HE
"""

# from basic_optics import Opt_Element
# from .basic_optics.freecad_models import model_lens
from .freecad_models import model_lens, lens_mount
from .optical_element import Opt_Element
from .geom_object import TOLERANCE

class Thick_Lens(Opt_Element):
  def __init__(self, radius1 = 300, radius2= 250,thickness = 10, n = 1.5, name="NewLens", **kwargs):
    super().__init__(name=name, **kwargs)
    # self.focal_length = f
    self.draw_dict["thickness"] = thickness #sieht schöner aus
    self.draw_dict["Radius1"] = radius1
    self.draw_dict["Radius2"] = radius2
    self.draw_dict["Refractive_index"] = n
    if abs(radius1) < TOLERANCE:
      if abs(radius2) < TOLERANCE:
        self.focal_length = 0
        print("infinite focal length")
      else:
        self.focal_length = float(1 / ((n-1)*(1/radius2)))
    else:
      if abs(radius2) < TOLERANCE:
        self.focal_length = float(1 / ((n-1)*(1/radius1)))
      else:
        self.focal_length = float(1 / ((n-1)*(1/radius1+1/radius2)-(n-1)*(n-1)*thickness/(n*radius1*radius2)))
  @property
  def focal_length(self):
    return self.__f
  @focal_length.setter
  def focal_length(self, x):
    self.__f = x
    if x == 0:
      self._matrix[1,0] = 0
    else:
      self._matrix[1,0] = -1/x

  def next_ray(self, ray):
    return self.refraction(ray)

  def draw_fc(self):
    self.update_draw_dict()
    self.draw_dict["dia"]=self.aperture
    # model_lens(self.name, dia=self.aperture, geom_info=self.get_geom())
    return model_lens(**self.draw_dict)

  def draw_mount_fc(self):
    return lens_mount(**self.draw_dict)

  def __repr__(self):
    n = len(self.class_name())
    txt = 'Thick Lens(f=' + repr(self.focal_length)
    txt += ', ' + super().__repr__()[n+1::]
    return txt

  def from_dict(dc):
    oe = Opt_Element()
    oe.name = dc["name"]
    oe.pos = dc["pos"]
    oe.normal = dc["normal"]
    oe._axes = dc["axes"]
    oe._matrix = dc["matrix"]
    oe.aperture = dc["aperture"]
    oe.group = dc["group"]
    return oe