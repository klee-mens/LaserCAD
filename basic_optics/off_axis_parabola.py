#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 16 11:43:05 2025

@author: mens
"""
from .geom_object import TOLERANCE, NORM0
from .ray import Ray
from .optical_element import Opt_Element
from .mount import Stripe_Mirror_Mount, Rooftop_Mirror_Mount, Unit_Mount
from ..freecad_models import model_mirror, model_stripe_mirror, model_rooftop_mirror
import numpy as np
from copy import deepcopy


class Off_Axis_Parabola_Focus(Opt_Element):
  def __init__(self, name="NewFocusOAP", reflected_focal_length=100, 
               parent_focal_length=50, **kwargs):
    super().__init__(name=name, **kwargs)
    self.reflected_focal_length = reflected_focal_length
    self.parent_focal_length = parent_focal_length
    
  def parent_parabola_apex(self):
    x,y,z = self.get_coordinate_system()
    rfl = self.reflected_focal_length
    pfl = self.parent_focal_length
    # return self.pos - y*rfl - x*pfl
    return self.pos + y*rfl + x*pfl
  
  def _curv(self):
    return 1 / (4 * self.parent_focal_length)
  
  def intersection(self, ray):
    # surface: x - ay² - az² = 0
    curv = self._curv()
    n0, y0, z0 = self.get_coordinate_system()
    n0 *= -1
    ppa = self.parent_parabola_apex()
    rel = ray.pos - ppa
    ns = ray.normal
    # a1*s² + b1*s + c1 = 0
    a1 = np.dot(ns, y0)**2 + np.dot(ns, z0)**2
    b1 = np.dot(n0,ns)/curv - 2*np.dot(ns, y0)*np.dot(rel,y0) - 2*np.dot(ns,z0)*np.dot(rel,z0)
    c1 = np.dot(rel,n0)/curv - np.dot(rel,y0)**2 - np.dot(rel,z0)**2
    
    if abs(a1) < TOLERANCE:
      s = -c1/b1
    else:
      s1 = -b1/2/a1 + np.sqrt( (b1/2/a1)**2 - c1/a1)
      s2 = -b1/2/a1 - np.sqrt( (b1/2/a1)**2 - c1/a1)
      abs1 = np.linalg.norm(ray.pos + s1*ns - self.pos)
      abs2 = np.linalg.norm(ray.pos + s2*ns - self.pos)
      s = s1 if abs1 < abs2 else s2
    
    ray.length = s
    return ray.endpoint()

  def next_ray(self, ray):
    ray2 = deepcopy(ray)
    intersec = self.intersection(ray)
    ray2.pos = intersec
    n0, y0, z0 = self.get_coordinate_system()
    n0 *= -1
    curv = self._curv()
    rel = intersec - self.parent_parabola_apex()
    gradient = n0 - 2*curv*np.dot(rel,y0)*y0 - 2*curv*np.dot(rel,z0)*z0
    gradient *= 1/np.linalg.norm(gradient)
    ray2.normal += -2 * np.dot(ray.normal, gradient) * gradient
    return ray2
