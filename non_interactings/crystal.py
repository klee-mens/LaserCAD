#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 11:46:23 2023

@author: mens
"""

from ..basic_optics import Component
from ..freecad_models import model_beam

class Crystal(Component):
  def __init__(self, name="Crystal", diameter=6, length=10, **kwargs):
    super().__init__(name, **kwargs)
    self.draw_dict["color"]=(10/255, 20/255, 230/255)
    self.draw_dict["dia"]=diameter
    self.draw_dict["prop"]=length
    self.draw_dict["f"] = 0
    self.freecad_model = model_beam
    
    
  def update_draw_dict(self):
    self.draw_dict["geom_info"] = (self.pos, self.normal)


