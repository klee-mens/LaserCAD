#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 21 20:28:02 2022

@author: mens
"""

# from basic_optics import Opt_Element
# from .basic_optics.freecad_models import model_lens
from .freecad_models import model_lens, lens_mount
from .optical_element import Opt_Element

class Lens(Opt_Element):
  def __init__(self, f=100, name="NewLens", **kwargs):
    super().__init__(name=name, **kwargs)
    self.focal_length = f
    self.draw_dict["thickness"] = 3 #sieht schöner aus
    self.draw_dict["Radius1"] = 300

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
    txt = 'Lens(f=' + repr(self.focal_length)
    txt += ', ' + super().__repr__()[n+1::]
    return txt

#   def __repr__(self):
#     txt = 'Lens(f=' + repr(self.focal_length)
#     txt += ', name="' + self.name
#     txt += '", pos='+repr(self.pos)[6:-1]
#     txt += ', norm='+repr(self.normal)[6:-1]+")"
#     return txt

  # def to_dict(self):
  #   dc = super().to_dict()

  #   return dc

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

def tests():
  from basic_optics import Ray

  l1 = Lens(name="susanne")
  l2 = eval(repr(l1))
  print(l2)

  print()

  r = Ray(pos = (0,0,90))
  print(r)
  r2 = l1.next_ray(r)
  print(r2)
  s = l1.focal_length / r2.normal[0]
  h = r2.normal[2]*s
  print(h)
  print("sollte bei -10 liegen")


if __name__ == "__main__":
  tests()