# -*- coding: utf-8 -*-
"""
Created on Sat Aug 19 13:13:11 2023

@author: mens
"""

# from ..basic_optics import Component
# from .component import Component
from ..freecad_models.utils import thisfolder, load_STL, freecad_da, update_geom_info, get_DOC
from ..freecad_models.freecad_model_composition import initialize_composition_old, add_to_composition
from ..freecad_models import model_crystal
from LaserCAD.basic_optics.component import Component
import numpy as np

import csv
# if freecad_da:
#   from FreeCAD import Vector, Placement, Rotation
#   import Mesh
#   import ImportGui
#   import Part
#   import Sketcher
#   from math import pi

DEFALUT_HOLDER_COLOR = (0.2,0.2,0.2)

class Faraday_Isolator(Component):
  def __init__(self, name="Faraday_Isolator", **kwargs):
    super().__init__(name, **kwargs)
    stl_file=thisfolder+"\mount_meshes\special mount\Faraday-Isolatoren-Body.stl"
    self.draw_dict["stl_file"]=stl_file
    self.draw_dict["color"]=(10/255, 20/255, 230/255)
    # self.draw_dict["color"]=(84/255, 84/255, 84/255)
    self.freecad_model = load_STL
    self.freecad_model = load_STL
    
  def draw_mount_fc(self):
    new_pos = self.pos
    new_pos[2] = new_pos[2]/2-8
    obj = model_crystal(width=40,height=new_pos[2]*2,thickness=65,color=DEFALUT_HOLDER_COLOR,Transparency=0,geom=(new_pos,self.normal))
    return obj
