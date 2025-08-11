# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 11:57:49 2024

@author: mens
"""

from ..freecad_models.utils import load_STL, thisfolder, inch
from ..basic_optics import Component, Composed_Mount


class Camera(Component):

  def __init__(self, name = "New_Camera", mesh_name="Manta_allied_vision_camera", **kwargs):
    super().__init__(name, **kwargs)
    stl_file=thisfolder+f"misc_meshes/{mesh_name}.stl"
    self.draw_dict["stl_file"]=stl_file
    self.draw_dict["color"]=(0.8*176/255, 0.8*46/255, 0.8*54/255)
    self.freecad_model = load_STL
    self.set_mount(Composed_Mount(unit_model_list=["0.5inch_post"]))
    self.Mount.pos += (35.5, 0, -14.5)