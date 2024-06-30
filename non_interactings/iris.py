# -*- coding: utf-8 -*-
"""
Created on Sat Aug 19 13:12:01 2023

@author: mens
"""

from ..freecad_models import model_iris_diaphragms,iris_post
# from ..basic_optics import Component
from ..basic_optics.component import Component


class Iris(Component):

  def __init__(self, dia = 20, name = "New_iris_diaphragms",**kwargs):
    super().__init__(name=name, **kwargs)
    self.aperture = dia
    self.draw_dict["thickness"] = 5
    self.draw_dict["Radius1"] = dia/2
    self.draw_dict["Radius2"] = 25
    self.draw_dict["height"] = dia/2 + 10


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

