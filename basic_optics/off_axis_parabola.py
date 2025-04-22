#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 16 11:43:05 2025

@author: mens
"""
from .geom_object import TOLERANCE
from .constants import inch
from .ray import Ray
from .optical_element import Opt_Element
from .mount import Composed_Mount
from ..freecad_models import model_off_axis_parabola
import numpy as np
from copy import deepcopy


class Off_Axis_Parabola_Focus(Opt_Element):
  def __init__(self, name="NewFocusOAP", reflected_focal_length=2*inch, angle=90, **kwargs):
    super().__init__(name=name, **kwargs)
    self.reflected_focal_length = reflected_focal_length
    self.angle = angle #in degrees
    self.aperture = 1*inch # Aperture in mm for drawing, Mount and clipping (not yet implemented)
    self.thickness = 1.25*inch # Thickness in mm, importent for mount placing and drawing
    self.freecad_model = model_off_axis_parabola
    # example referes to https://www.thorlabs.com/thorproduct.cfm?partnumber=MPD129-M01
    self.Mount.pos += (+self._mount_shift() - 5.5, 0, 0) #hacky but works
    # self.Mount.pos += (+self._mount_shift() , 0, 0) #hacky but works
    
  def parent_parabola_apex(self):
    x,y,z = self.get_coordinate_system()
    rfl = self.reflected_focal_length
    c = self.parent_parabola_curvature()
    sa = np.sin(self.angle/180 * np.pi)
    return self.pos + x*c*(sa*rfl)**2 + y*sa*rfl
  
  def parent_parabola_curvature(self):
    ca = np.cos(self.angle/180 * np.pi)
    sa = np.sin(self.angle/180 * np.pi)
    rfl = self.reflected_focal_length
    return np.sqrt( (ca/(2*sa**2*rfl))**2 + 1/(2*sa*rfl)**2 ) - ca/(2*sa**2*rfl) 
  
  def parent_focal_length(self):
    return 1 / (4 * self.parent_parabola_curvature())
  
  def intersection(self, ray):
    # surface: x - ay² - az² = 0
    curv = self.parent_parabola_curvature()
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
    curv = self.parent_parabola_curvature()
    rel = intersec - self.parent_parabola_apex()
    gradient = n0 - 2*curv*np.dot(rel,y0)*y0 - 2*curv*np.dot(rel,z0)*z0
    gradient *= 1/np.linalg.norm(gradient)
    ray2.normal += -2 * np.dot(ray.normal, gradient) * gradient
    return ray2
  
  def update_draw_dict(self):
    super().update_draw_dict()
    parentpos = self.parent_parabola_apex() - self.pos
    self.draw_dict["parent_pos"] = parentpos[0:2]
    self.draw_dict["parent_focal"] = self.parent_focal_length()
    # model_off_axis_parabola(name="off_axis_parab", parent_pos=(25, 50), 
                                # parent_focal=25, dia=25, thickness=30, 
                                # geom=None, **kwargs):
  def set_mount_to_default(self):
    self.Mount = Composed_Mount(unit_model_list=["POLARIS-K1", "0.5inch_post"])
    self.Mount.set_geom(self.get_geom())

  def _mount_shift(self):
    th = self.thickness
    dia = self.aperture
    c = self.parent_parabola_curvature()
    parentpos = self.parent_parabola_apex() - self.pos
    ppy = parentpos[1]
    return th - c*(dia*abs(ppy) + dia**2/4)