# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 13:17:07 2023

@author: He
"""

import numpy as np
from copy import deepcopy
from .optical_element import Opt_Element
from ..freecad_models import model_intersection_plane



class Refractive_plane(Opt_Element):
  """
  The class of Refractive_plane.
  """
  def __init__(self, relative_refractive_index = 1.5, 
               name="NewRefractiuveSurface", **kwargs):
    super().__init__(name=name, **kwargs)

    self.relative_refractive_index = relative_refractive_index # n2/n1
    self.draw_dict["Radius"] = 50
    self.draw_dict["color"] = (0/255, 100/255, 100/255)
    self.freecad_model = model_intersection_plane
    
  def next_ray(self, ray):
    # See Springer Handbook of Lasers and Optics page 68
    ray2 = deepcopy(ray)
    ray2.pos = self.intersection(ray)
    N = self.normal
    a1 = ray.normal
    n1n2 = 1/self.relative_refractive_index
    a2 = n1n2* a1 - n1n2*np.sum(a1*N)* N + np.sqrt(1 - n1n2**2*(1 - np.sum(a1*N)**2))* N
    if np.sign(np.sum(a1*N)) != np.sign(np.sum(a2*N)):
      a2 = n1n2* a1 - n1n2*np.sum(a1*N)* N - np.sqrt(1 - n1n2**2*(1 - np.sum(a1*N)**2))* N
    ray2.normal = a2
    return ray2

  # def next_ray(self, ray):
  #     ray2 = deepcopy(ray)
  #     ray2.pos = self.intersection(ray) #dadruch wird ray.length verändert(!)
  #     # print("ray2.pos =",ray2.pos)
  #     # radial_vec = ray2.pos - self.pos
  #     # ray2 = ray
  #     norm = ray2.normal
  #     ea = self.normal
  #     ref = 1/self.relative_refractive_index
  #     muti = norm[0]*ea[0]+norm[1]*ea[1]+norm[2]*ea[2]
  #     norm2 = ref * norm - ref*(muti)*ea + pow(1-ref**2*(1-muti**2),0.5)*ea
  #     muti2 = norm2[0]*ea[0]+norm2[1]*ea[1]+norm2[2]*ea[2]
  #     if muti2 < 0 :
  #         norm2 = ref * norm - ref*(muti)*ea - pow(1-ref**2*(1-muti**2),0.5)*ea
  #     ray2.normal = norm2
  #     return ray2
  
