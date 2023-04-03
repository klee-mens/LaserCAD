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
    ray2=deepcopy(ray)
    ray2.pos = ray.intersect_with(self)
    return self.refraction(ray2,r_ref_index = self.relative_refractive_index)
  
  def draw_fc(self):
    self.update_draw_dict()
    return model_intersection_plane(**self.draw_dict)