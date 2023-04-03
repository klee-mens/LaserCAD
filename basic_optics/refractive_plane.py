# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 13:17:07 2023

@author: He
"""

from .geom_object import TOLERANCE, NORM0
from .ray import Ray
from .freecad_models import model_mirror, mirror_mount, model_stripe_mirror
from .optical_element import Opt_Element
import numpy as np
from copy import deepcopy
from .freecad_models import model_intersection_plane



class Refractive_plane(Opt_Element):

  def __init__(self, r_ref_index = 1.5, **kwargs):
    super().__init__(**kwargs)

    self.relative_refractive_index = r_ref_index
    self.draw_dict["Radius"] = 50
    self.draw_dict["color"] = (0/255, 100/255, 100/255)
    
  def next_ray(self, ray):
      ray2 = deepcopy(ray)
      ray2.pos = ray.intersect_with(self) #dadruch wird ray.length verändert(!)
      # print("ray2.pos =",ray2.pos)
      # radial_vec = ray2.pos - self.pos
      # ray2 = ray
      norm = ray2.normal
      ea = self.normal
      ref = 1/self.relative_refractive_index
      muti = norm[0]*ea[0]+norm[1]*ea[1]+norm[2]*ea[2]
      norm2 = ref * norm - ref*(muti)*ea + pow(1-ref**2*(1-muti**2),0.5)*ea
      muti2 = norm2[0]*ea[0]+norm2[1]*ea[1]+norm2[2]*ea[2]
      if muti2 < 0 :
          norm2 = ref * norm - ref*(muti)*ea - pow(1-ref**2*(1-muti**2),0.5)*ea
      ray2.normal = norm2
      return ray2
  
  def draw_fc(self):
    self.update_draw_dict()
    return model_intersection_plane(**self.draw_dict)