# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 15:36:30 2023

@author: 12816
"""

from ..basic_optics import Geom_Object
from ..freecad_models.freecad_model_mounts import model_table

class Table(Geom_Object):
  def __init__(self, name="BreadBoard",length=4000,width=1500,height=10, **kwargs):
    super().__init__(name, **kwargs)
    # stl_file=thisfolder+"\post\optical_breadboard.stl"
    # self.draw_dict["stl_file"]=stl_file
    # self.freecad_model = load_STL
    self.pos = (-1500,-800,0)
    self.length=length
    self.width=width
    self.height = height
    # self.Xdimension = 1500
    # self.Ydimension = 800
    self.freecad_model = model_table
  
  def update_draw_dict(self):
    super().update_draw_dict()
    self.draw_dict["length"] = self.length
    self.draw_dict["width"] = self.width
    self.draw_dict["height"] = self.height
  
  def draw_fc(self):
    self.update_draw_dict()
    obj=model_table(**self.draw_dict)
    return obj