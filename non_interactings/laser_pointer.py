# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 11:57:49 2024

@author: mens
"""

from ..freecad_models.utils import load_STL, thisfolder, inch
from ..basic_optics import Component, Composed_Mount


class LaserPointer(Component):

  def __init__(self, name = "New_LaserPointer", **kwargs):
    super().__init__(name, **kwargs)
    stl_file=thisfolder+"misc_meshes/LaserPointer.stl"
    self.draw_dict["stl_file"]=stl_file
    self.draw_dict["color"]=(33/255, 33/255, 33/255)
    self.freecad_model = load_STL
    self.set_mount(Composed_Mount(unit_model_list=["0.5inch_post"]))
    self.Mount.pos += (-39, 0, -inch)