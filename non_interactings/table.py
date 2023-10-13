# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 15:36:30 2023

@author: 12816
"""

from ..basic_optics import Geom_Object
from ..freecad_models.freecad_model_mounts import model_table

class Table(Geom_Object):
  def __init__(self, name="BreadBoard", pos=(0,0,0), **kwargs):
    super().__init__(name, pos, **kwargs)
    # stl_file=thisfolder+"\post\optical_breadboard.stl"
    # self.draw_dict["stl_file"]=stl_file
    # self.freecad_model = load_STL
    # self.Xdimension = 1500
    # self.Ydimension = 800
    
  def draw_fc(self):
    self.update_draw_dict()
    obj=model_table(**self.draw_dict)
    return obj