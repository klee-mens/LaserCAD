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
from ..freecad_models import model_grating
from .mount import Grating_Mount


class Grating(Opt_Element):
  """
  Klasse für Gitter
  """
  def __init__(self, grat_const=0.005, order=1, **kwargs):
    self.height = 60
    self.thickness = 8
    super().__init__(**kwargs)
    self.grating_constant = grat_const
    self.width = 50
    self.diffraction_order = order
    self.update_draw_dict()
    self.freecad_model = model_grating
    self.set_mount_to_default()

  def next_ray(self, ray, order=None):
    """
    Beugung entsprechend des Gittergesetzes g(sinA + sinB) = m*lam
    m = order
    """
    if order == None:
      order = self.diffraction_order
    norm, gratAx, sagit = self.get_coordinate_system() # Normale, Gitterachse, Sagitalvector
    norm *= -1 #selbe Konvention wie beim Spiegel, 1,0,0 heißt Reflektion von 1,0,0
    gratAx *= -1 #selbe Konvention wie beim Spiegel, 1,0,0 heißt Reflektion von 1,0,0
    r1 = ray.normal #einfallender Strahl
    pos = ray.intersect_with(self)
    sagital_component = np.sum(r1 * sagit)
    sinA = np.sum( sagit * np.cross(r1, norm) )
    sinB = order * ray.wavelength/ self.grating_constant - sinA
    ray2 = deepcopy(ray)
    ray2.name = "next_" + ray.name
    ray2.pos = pos
    ray2.normal = (np.sqrt(1-sinB**2) * norm + sinB * gratAx) * np.sqrt(1-sagital_component**2) + sagital_component * sagit
    k_prop = np.cross(norm,np.cross(ray.normal*2*np.pi/ray.wavelength,norm))
    k_p_out = k_prop+order*2*np.pi/self.grating_constant*gratAx
    k_r = k_p_out + abs(np.sqrt((2*np.pi/ray.wavelength)**2-np.linalg.norm(k_p_out)**2))*norm
    n_r = k_r/np.linalg.norm(k_r)
    ray2.normal = n_r
    return ray2

  def update_draw_dict(self):
    super().update_draw_dict()
    self.draw_dict["dimensions"] = (self.width, self.height, self.thickness)
  
  def set_mount_to_default(self):
    smm = Grating_Mount(height=self.height,thickness=self.thickness)
    smm.set_geom(self.get_geom())
    self.Mount = smm

  def matrix(self, inray=Ray()):
    omatrix = np.eye(2)
    try:
      outray = self.next_ray(inray)
    except:
      outray = Ray()
      print("Irgendwas bei Matrix Gitter Berechnung falsch gelaufen")
    A = np.sum(self.normal * inray.normal) / np.sum(self.normal * outray.normal)
    A *= -1 #??? Steht so in den Folien    
    omatrix[0,0] = A
    omatrix[1,1] = 1/A
    return omatrix
  
  def kostenbauder(self, inray=Ray()):
    kmatrix = np.eye(4)
    kmatrix[0:2, 0:2] = self.matrix(inray=inray)
    #heute keinen Bock mehr
    return kmatrix * 999

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
