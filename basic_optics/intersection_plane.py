# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 16:06:17 2023

@author: 12816
"""
from .ray import Ray
from .freecad_models import model_mirror, mirror_mount, model_stripe_mirror
from .optical_element import Opt_Element
import numpy as np
from copy import deepcopy
import matplotlib.pyplot as plt


class Intersection_plane(Opt_Element):
  def __init__(self, f=100, name="NewLens", **kwargs):
  
  def spot_diagram(self, rays):
    point_x = []
    point_y = []
    # for point_i in rays:
    #   pos_diff = point_i.pos- self.pos
    #   print(pos_diff)
    #   point_x.append(pos_diff[1])
    #   point_y.append(pos_diff[2])
    pos_diff = rays.pos - self.pos
    print(pos_diff)
    point_x.append(pos_diff[1])
    point_y.append(pos_diff[2])
    plt.figure()
    plt.scatter(point_x,point_y)
    plt.show()
    return 1