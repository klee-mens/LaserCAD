#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 00:52:09 2023

@author: mens
"""

import numpy as np
from copy import deepcopy
from .optical_element import Opt_Element
from .ray import Ray
from .freecad_models import model_grating
from .freecad_models import grating_mount

class Grating(Opt_Element):
  """
  Klasse für Gitter
  """
  def __init__(self, grat_const=0.005, **kwargs):
    super().__init__(**kwargs)
    self.grating_constant = grat_const
    #Konstanten zum zeichnen, für die sonstige Berechnung unwichtig
    self.width = 50
    self.height = 60
    self.thickness = 8
    self.blazeangel = 32
    # self.draw_dict['width'] = self.width
    # self.draw_dict['thickness'] = self.thickness
    # self.draw_dict['height'] = self.height
    # dims = (self.thickness, self.width, self.height)
    # print("dims:", dims)
    
  def next_ray(self, ray, order=1):
    """
    Beugung entsprechend des Gittergesetzes g(sinA + sinB) = m*lam 
    m = order
    """
    
    norm, gratAx, sagit = self.get_coordinate_system() # Normale, Gitterachse, Sagitalvector
    norm *= -1 #selbe Konvention wie beim Spiegel, 1,0,0 heißt Reflektion von 1,0,0
    gratAx *= -1 #selbe Konvention wie beim Spiegel, 1,0,0 heißt Reflektion von 1,0,0
    r1 = ray.normal #einfallender Strahl
    pos = ray.intersect_with(self)
    # print("Gitternorm, Raynorm", norm, r1)
    
    sinA = np.sum( sagit * np.cross(r1, norm) )
    # print("sinA:", sinA)
    sinB = order * ray.wavelength/ self.grating_constant - sinA
    ray2 = deepcopy(ray)
    ray2.name = "next_" + ray.name
    ray2.pos = pos
    ray2.normal = np.sqrt(1-sinB**2) * norm + sinB * gratAx
    return ray2
  
  def draw_fc(self):
    dims = (self.width, self.height, self.thickness)
    return model_grating(name=self.name, dimensions=dims, geom=self.get_geom())
  
  def draw_mount_fc(self):
    # helper_dict = dict(self.draw_dict)
    # obj = grating_mount(**helper_dict)
    obj = grating_mount(name=self.name,height=self.height,
                        thickness=self.thickness,#base_exists=self.draw_dict['base_exists'], 
                        geom=self.get_geom())
    return obj
  
  def draw_mount_text(self):
    # if self.mount_type == "dont_draw":
    #   txt = self.name + "'s mount will not be drawn."
    # elif self.mount_type == "default":
      txt = "<" + self.name + ">'s mount is the default mount."
    # else:
    #   txt = self.name + "'s mount is " + self.mount_type + "."
      return txt
  
  
def grating_test1():
  grat = Grating()
  grat.pos += (10, 0, 0)
  r1 = Ray()
  r1.normal = (1,1,0)
  r2 = grat.next_ray(r1, order=0)
  return grat, r1, r2


def grating_test2():
  grat = Grating()
  grat.pos += (10, 0, 0)
  r1 = Ray()
  r2 = grat.next_ray(r1, order=1)
  
  print()
  print("Theorie: beta=", np.arcsin(r1.wavelength/grat.grating_constant)*180/np.pi)
  print("Winkel von r2 zu Grat:", np.arccos(np.sum(r2.normal * -grat.normal))*180/np.pi)
  print()
  return grat, r1, r2

def grating_test3():
  #der Fall Litrow, sollte eine umgedrehte normale erzeuge r1.normal = -r2.normal
  lam = 1e-3 #1um
  g = lam*1.5
  grat = Grating(grat_const=g)
  grat.pos += (10, 0, 0)
  sinA = lam / (2*g)
  r1 = Ray()
  r1.wavelength = lam
  r1.normal = (np.sqrt(1-sinA**2), sinA, 0)
  
  r2 = grat.next_ray(r1)
  
  return grat, r1, r2
  