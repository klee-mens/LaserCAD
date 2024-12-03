#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 11:46:23 2023

@author: mens
"""

from ..basic_optics import Component

from ..freecad_models import model_crystal

# class Crystal(Component):
#   def __init__(self, name="Crystal", diameter=6, length=10, **kwargs):
#     super().__init__(name, **kwargs)
#     self.draw_dict["color"]=(10/255, 20/255, 230/255)
#     self.draw_dict["dia"]=diameter
#     self.draw_dict["prop"]=length
#     self.draw_dict["f"] = 0
#     self.freecad_model = model_beam
    
    
#   def update_draw_dict(self):
#     self.draw_dict["geom_info"] = (self.pos, self.normal)


class Crystal(Component):
  def __init__(self, width=10,height=10,thickness=10,n=1.5, name="NewCrystal", **kwargs):
    super().__init__(name=name, **kwargs)
    self.thickness=thickness
    self.width = width
    self.height = height
    self.relative_refractive_index = n
    self.freecad_model = model_crystal

  def update_draw_dict(self):
    super().update_draw_dict()
    self.draw_dict["height"] = self.height
    self.draw_dict["width"] = self.width
    self.draw_dict["thickness"] = self.thickness

    # self.draw_dict["length"] = self.length
    # self.draw_dict["radius"] = radius
    # self.draw_dict["angle"] = angle

  # def draw_fc(self):
  #   self.update_draw_dict()
  #   return model_crystal(**self.draw_dict)