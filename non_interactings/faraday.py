# -*- coding: utf-8 -*-
"""
Created on Sat Aug 19 13:13:11 2023

@author: mens
"""

from ..basic_optics import Component
from ..freecad_models.utils import thisfolder, load_STL

class Faraday_Isolator(Component):
  def __init__(self, name="Faraday_Isolator", **kwargs):
    super().__init__(name, **kwargs)
    stl_file=thisfolder+"\mount_meshes\special mount\Faraday-Isolatoren-Body.stl"
    self.draw_dict["stl_file"]=stl_file
    self.draw_dict["color"]=(10/255, 20/255, 230/255)
    self.freecad_model = load_STL