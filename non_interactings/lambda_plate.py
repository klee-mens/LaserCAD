# -*- coding: utf-8 -*-
"""
Created on Sat Aug 19 13:11:01 2023

@author: mens
"""

from ..freecad_models import model_lambda_plate,model_mirror
# from ..basic_optics import Component
from LaserCAD.basic_optics.component import Component

class Lambda_Plate(Component):

  def __init__(self,thickness=2, **kwargs):
    super().__init__(**kwargs)
    self.aperture = 25.4/2
    self.draw_dict["thickness"]=thickness

  def draw_fc(self):
    self.update_draw_dict()
    self.draw_dict["dia"]=self.aperture
    obj = model_mirror(**self.draw_dict)
    return obj

  def draw_mount_fc(self):
    self.update_draw_dict()
    obj = model_lambda_plate(**self.draw_dict)
    return obj