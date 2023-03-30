# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 12:12:58 2023

@author: He
Ignore this part. Itsd not finished yet.
"""

from .freecad_models import model_iris_diaphragms,iris_post
from .optical_element import Opt_Element

class Iris(Opt_Element):
  def __init__(self, dia = 20, name = "New_iris_diaphragms",**kwargs):
    super().__init__(name=name, **kwargs)
    self.aperture = dia
    self.draw_dict["thickness"] = 3 #sieht schöner aus
    self.draw_dict["Radius1"] = dia/2
    self.draw_dict["Radius2"] = 25
    
  def next_ray(self, ray):
    return None
  
  def draw_fc(self):
    self.update_draw_dict()
    return model_iris_diaphragms(**self.draw_dict)
  
  def draw_mount_fc(self):
    return iris_post(**self.draw_dict)
  
  def __repr__(self):
    n = len(self.Klassenname())
    txt = 'Iris(dia=' + repr(self.aperture)
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