# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 14:00:59 2023

@author: He
"""

from .freecad_models import model_diaphragms,iris_post
from .optical_element import Opt_Element

from copy import deepcopy

class Barriers(Opt_Element):
  """
    The class of diaphragms.
    Just a block. Nothing special.
  """
  def __init__(self, dia = 50, name = "New_diaphragms",**kwargs):
    super().__init__(name=name, **kwargs)
    self.aperture = dia
    self.draw_dict["thickness"] = 5 #sieht schöner aus
    self.draw_dict["Radius"] = dia/2
    
  def next_ray(self, ray):
    ray2=deepcopy(ray)
    ray2.pos = ray.intersect_with(self)
    ray2.length=1
    return ray2
  
  def draw_fc(self):
    self.update_draw_dict()
    return model_diaphragms(**self.draw_dict)
  
  def draw_mount_fc(self):
    return iris_post(**self.draw_dict)
  
  def __repr__(self):
    n = len(self.Klassenname())
    txt = 'Diaphragms(dia=' + repr(self.aperture)
    txt += ', ' + super().__repr__()[n+1::]
    return txt
  

  
  def from_dict(dc):
    oe = Opt_Element()
    oe.name = dc["name"]
    oe.pos = dc["pos"]
    oe.normal = dc["normal"]
    oe._axes = dc["axes"]
    oe.aperture = dc["aperture"]
    oe.group = dc["group"]
    return oe