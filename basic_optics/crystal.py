#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 21 20:28:02 2022

@author: mens
"""

# from basic_optics import Opt_Element
# from .basic_optics.freecad_models import model_lens
from ..freecad_models import model_lens, lens_mount, model_crystal,model_crystal_mount
from .optical_element import Opt_Element
from copy import deepcopy
import numpy as np

class Crystal(Opt_Element):
  def __init__(self, width=10,model="cube",thickness=10,n=1.5, name="NewCrystal", **kwargs):
    super().__init__(name=name, **kwargs)
    self.draw_dict["width"]=width
    self.draw_dict["height"]=width
    self.draw_dict["model"]=model
    self._matrix[0,1] = thickness*(1/n-1)
    self.thickness=thickness
    self.draw_dict["thickness"]=self.thickness
    self.relative_refractive_index = n

  # @property
  # def focal_length(self):
  #   return self.__f
  # @focal_length.setter
  # def focal_length(self, x):
  #   self.__f = x
  #   if x == 0:
  #     self._matrix[1,0] = 0
  #   else:
      # self._matrix[1,0] = -1/x

  def next_ray(self, ray):
    ray2 = deepcopy(ray)
    ray2.pos = ray.intersect_with(self) #dadruch wird ray.length verändert(!)
    
    # print("ray2.pos =",ray2.pos)
    # radial_vec = ray2.pos - self.pos
    # ray2 = ray
    norm = ray2.normal
    ea = self.normal
    ref = 1/self.relative_refractive_index
    muti = norm[0]*ea[0]+norm[1]*ea[1]+norm[2]*ea[2]
    norm2 = ref * norm - ref*(muti)*ea + pow(1-ref**2*(1-muti**2),0.5)*ea
    muti2 = norm2[0]*ea[0]+norm2[1]*ea[1]+norm2[2]*ea[2]
    if muti2 < 0 :
        norm2 = ref * norm - ref*(muti)*ea - pow(1-ref**2*(1-muti**2),0.5)*ea
    ray2.normal = norm2
    ray3 = deepcopy(ray2)
    new_pos = self.pos+self.normal * self.thickness
    delta_p = new_pos - ray2.pos
    # print(delta_p)
    s = np.sum(delta_p*self.normal) / np.sum(ray2.normal * self.normal)
    ray2.length = s
    ray3.pos = ray2.endpoint()
    ray3.normal=ray.normal
    # print(ray.length)
    return ray3

  def draw_fc(self):
    self.update_draw_dict()
    return model_crystal(**self.draw_dict)

  def draw_mount_fc(self):
    self.update_draw_dict()
    return model_crystal_mount(**self.draw_dict)

  # def draw_mount_fc(self):
  #   obj = lens_mount(**self.draw_dict)
  #   # post_pos = xshift*self.normal+self.pos
  #   return lens_mount(**self.draw_dict)
  
  # def draw_mount_text(self):
  #   if self.draw_dict["mount_type"] == "dont_draw":
  #     txt = "<" + self.name + ">'s mount will not be drawn."
  #   elif self.draw_dict["mount_type"] == "default":
  #     txt = "<" + self.name + ">'s mount is the default mount."
  #   else:
  #     txt = "<" + self.name + ">'s mount is the " + self.draw_dict["mount_type"] + "."
  #   return txt
  
  def __repr__(self):
    n = len(self.class_name())
    txt = 'Crystal('
    
    # txt = 'Lens(f=' + repr(self.focal_length)
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

  l1 = Crystal(name="susanne")
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