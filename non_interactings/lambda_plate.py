# -*- coding: utf-8 -*-
"""
Created on Sat Aug 19 13:11:01 2023

@author: mens
"""

from ..freecad_models import model_lamda_plane
from ..basic_optics import Component

class Lambda_Plate(Component):

  def __init__(self,thickness=1, **kwargs):
    super().__init__(**kwargs)
    self.aperture = 25.4/2
    self.draw_dict["thickness"]=thickness


  def draw_mount_fc(self):
    self.update_draw_dict()
    obj = model_lamda_plane(**self.draw_dict)
    return obj