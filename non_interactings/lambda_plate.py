# -*- coding: utf-8 -*-
"""
Created on Sat Aug 19 13:11:01 2023

@author: mens
"""

from ..freecad_models import model_lambda_plate,model_mirror
# from ..basic_optics import Component
# from ..basic_optics.mount import Special_mount
from ..basic_optics.mount2 import Unit_Mount,Composed_Mount,Post
from LaserCAD.basic_optics.component import Component

class Lambda_Plate(Component):

  def __init__(self,thickness=2, **kwargs):
    super().__init__(**kwargs)
    self.aperture = 25.4/2
    self.draw_dict["thickness"]=thickness
    # self._update_mount_dict()
    self.mount = Composed_Mount()
    self.mount.add(Unit_Mount("lambda_mirror_mount"))
    self.mount.add(Post())
    
  # def _update_mount_dict(self):
  #   super()._update_mount_dict()
  #   self.mount_dict["elm_type"] = "mirror"
  #   self.mount_dict["name"] = self.name + "_mount"
  #   self.mount_dict["model"] = "lamuda_mirror_mount"
  #   self.mount_dict["docking_pos"] = (6,0,-33.35)
  #   self.mount_dict["drawing_post"] = True

  def draw_fc(self):
    self.update_draw_dict()
    self.draw_dict["dia"]=self.aperture
    obj = model_mirror(**self.draw_dict)
    return obj

  # def draw_mount_fc(self):
  #   self.update_draw_dict()
  #   obj = model_lambda_plate(**self.draw_dict)
  #   return obj