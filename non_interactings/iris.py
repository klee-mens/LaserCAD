# -*- coding: utf-8 -*-
"""
Created on Sat Aug 19 13:12:01 2023

@author: mens
"""

from ..freecad_models.utils import load_STL, thisfolder
from ..basic_optics import Component, Composed_Mount


class Iris(Component):

  def __init__(self, name = "New_iris", **kwargs):
    super().__init__(name, **kwargs)
    stl_file=thisfolder+"misc_meshes/Iris_ID12M.stl"
    self.draw_dict["stl_file"]=stl_file
    self.draw_dict["color"]=(33/255, 33/255, 33/255)
    self.freecad_model = load_STL
    self.distance_to_post = 12.8
    self.set_mount(Composed_Mount(unit_model_list=["0.5inch_post"]))
    self.Mount.pos += (-2, 0, -self.distance_to_post)


