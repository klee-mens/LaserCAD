# -*- coding: utf-8 -*-
"""
Created on Sat Aug 19 13:11:01 2023

@author: mens
"""

from ..freecad_models import model_mirror
from ..basic_optics import Component
from ..basic_optics.mount import Unit_Mount,Composed_Mount,Post

DEFAULT_LAMBDA_PLATE_COLOR = (255/255,255/255,0/255)

class Lambda_Plate(Component):

  def __init__(self, name="LambdaPlate", **kwargs):
    super().__init__(name=name, **kwargs)
    self.aperture = 25.4/2
    self.thickness = 2
    self.freecad_model = model_mirror
    self.set_mount_to_default()
    self.draw_dict["Radius"] = 0
    self.draw_dict["color"] = DEFAULT_LAMBDA_PLATE_COLOR    
    
  def set_mount_to_default(self):
    self.Mount = Composed_Mount()
    self.Mount.add(Unit_Mount("lambda_mirror_mount"))
    self.Mount.add(Post(model="0.5inch_post"))
    self.Mount.set_geom(self.get_geom())
