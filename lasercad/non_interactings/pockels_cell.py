# -*- coding: utf-8 -*-
"""
Created on Sat Aug 19 13:11:23 2023

@author: mens
"""

# from ..basic_optics import Component
from ..basic_optics.component import Component
from ..freecad_models.utils import thisfolder, load_STL

class Pockels_Cell(Component):
  def __init__(self, name="Pockels_Cell", **kwargs):
    super().__init__(name, **kwargs)
    stl_file=thisfolder+"misc_meshes/pockels_cell_easy_steal-Body.stl"
    self.draw_dict["stl_file"]=stl_file
    self.draw_dict["color"]=(239/255, 239/255, 239/255)
    # self.draw_dict["color"]=(100/255, 100/255, 100/255)
    self.freecad_model = load_STL

