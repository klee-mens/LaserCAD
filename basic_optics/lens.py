#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 21 20:28:02 2022

@author: mens
"""

from ..freecad_models import model_lens, model_stripe_mirror
from .optical_element import Opt_Element
from .mount import Unit_Mount, KM100C
from copy import deepcopy
import numpy as np
from .geom_object import TOLERANCE

class Lens(Opt_Element):
  def __init__(self, f=100, name="NewLens", **kwargs):
    super().__init__(name=name, **kwargs)
    self.focal_length = f
    self.thickness = 4
    self.freecad_model = model_lens

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
    return self.ABCD_refraction(ray)

  def update_draw_dict(self):
    super().update_draw_dict()
    self.draw_dict["Radius1"] = 400
    self.draw_dict["Radius2"] = 0

  def __repr__(self):
    n = len(self.class_name())
    txt = 'Lens(f=' + repr(self.focal_length)
    txt += ', ' + super().__repr__()[n+1::]
    return txt


class Cylindrical_Lens(Opt_Element):
  """
  The class of Cylindrical mirror.
  Cylindrical mirror have those parameters:
    radius: The curvature of the mirror
    height: The vertical thickness of the mirror
    thickness: The horizontal thickness of the mirror
  The default mirror is placed horizontally, which means the cylinder_center
  points tp the z-axis. Use rotate function if you want to rotate the mirror.
  """
  def __init__(self, f=100, height=30, thickness=10, **kwargs):
    super().__init__(**kwargs)
    self.focal_length = f
    # self.draw_dict["Radius"] = radius
    self.height=height
    self.thickness=thickness
    # self.draw_dict["model_type"]="Stripe"
    self.freecad_model = model_stripe_mirror
    # self.set_mount(KM100C(height=self.height, width=self.aperture, post="0.5inch_post"))

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

  def update_draw_dict(self):
    super().update_draw_dict()
    self.draw_dict["dia"]=self.aperture
    self.draw_dict["Radius"] = - 300
    self.draw_dict["height"]=self.height
    self.draw_dict["thickness"]=self.thickness
    DEFAULT_COLOR_LENS = (0/255,170/255,124/255)
    self.draw_dict["color"] = DEFAULT_COLOR_LENS

  def next_ray(self, ray):
    """
    lskdfölkadfmaöof

    """
    ray2 = deepcopy(ray)
    ray2.pos = self.intersection(ray)

    ex, ey, ez = self.get_coordinate_system()
    radius = np.dot(ray2.pos - self.pos, ey) # abstand zu achse in y richtung
    cn = np.dot(ex, ray2.normal) # normal compopent

    if np.sum(cn) < 0:
      ex *= -1#gibt sonst hässliche Ergebnisse, wenn die Linse falsch rum steht
    if np.abs(radius) > TOLERANCE:
      cm = np.dot(ey, ray2.normal) # meridonial
      cs = np.dot(ez, ray2.normal) # sagital

      alpha = np.arctan(cm/cn)
      vm = np.sqrt(cm**2 + cn**2) #length of the raz.normal projected in the meridional plane
      parax1 = np.array((radius, alpha)) #classic matrix optics
      rad2, alpha2 = np.matmul(self._matrix, parax1) #classic matrix optics
      norm2 = vm*np.cos(alpha2)*ex + vm*np.sin(alpha2)*ey + cs*ez # neue normale
      ray2.normal = norm2
      return ray2
    else:
      # mittelpunktstrahl
      return ray2

  # def set_mount_to_default(self):
  #   x,y,z = self.get_coordinate_system()
  #   if np.abs(np.dot(y, (0,1,0))) > 0.9:
  #     self.set_mount(KM100C(height=self.height, width=self.aperture, post="0.5inch_post"))
  #   else:
  #     self.set_mount(KM100C(height=self.aperture, width=self.height, post="0.5inch_post"))
  #   self.Mount.pos = self.pos








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