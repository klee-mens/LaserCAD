#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 26 10:11:15 2025

@author: mens
"""

from ..basic_optics import Component, Unit_Mount, Composed_Mount, Post
from ..freecad_models.utils import thisfolder, load_STL

class Detector(Component):
  def __init__(self, name="Det_PDA10A2", **kwargs):
    super().__init__(name, **kwargs)
    stl_file = thisfolder+"misc_meshes/Diode.stl"
    self.draw_dict["stl_file"]=stl_file
    self.draw_dict["color"]=(0.1, 0.1, 0.1)
    self.freecad_model = load_STL
    self.set_mount_to_default()

  def set_mount_to_default(self):
    invis_adapter = Unit_Mount()
    invis_adapter.docking_obj.pos += (10.5, 0, -25)
    comp = Composed_Mount(name=self.name + "_mount")
    comp.add(invis_adapter)
    comp.add(Post(model="0.5inch_post"))
    # comp.add(Post())
    comp.set_geom(self.get_geom())
    self.Mount = comp