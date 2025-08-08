#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 11:46:23 2023

@author: mens
"""

from ..basic_optics import Component

from ..freecad_models import model_crystal, model_mirror

class Cylindric_Crystal(Component):
  def __init__(self, name="LaserCrystal", aperture=6, thickness=3, **kwargs):
    super().__init__(name=name, **kwargs)
    self.aperture = aperture
    self.thickness = thickness
    self.draw_dict["color"] = (0.8, 0.3, 0.1)
    self.freecad_model = model_mirror


class Crystal(Component):
  def __init__(self, width=10,height=10,thickness=10,n=1.5, name="NewCrystal", **kwargs):
    super().__init__(name=name, **kwargs)
    self.thickness=thickness
    self.width = width
    self.height = height
    self.relative_refractive_index = n
    self.freecad_model = model_crystal
    self.draw_dict["color"] = (131/255,27/255,44/255)

  def update_draw_dict(self):
    super().update_draw_dict()
    self.draw_dict["height"] = self.height
    self.draw_dict["width"] = self.width
    self.draw_dict["thickness"] = self.thickness

