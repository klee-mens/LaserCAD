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
    if abs(sinB)>1:
      ray2 = self.reflection(ray)
      print("Warning, there is no diffraction of this order, retun next ray as a reflection")
      return ray2
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

  def angle_of_incidence(self, ray=Ray()):
    """
    calulates the AOI of an incident or outgoing ray
    The angle is defined as the angle to the normal of the grating, the ray
    is projected in a plane of the grating normal and the grating vector
    (which is perpendicular to its lines/grooves)

    Parameters
    ----------
    ray : Ray
      incident or outgoing ray

    Returns
    -------
    anlge in radiants, can be between -pi/2 to plus pi/2
    """
    xvec, yvec, zvec = self.get_coordinate_system()
    rx = np.sum( ray.normal * xvec )
    ry = np.sum( ray.normal * yvec )
    # rz = np.sum( ray.normal * zvec )
    return np.arctan(ry / rx) # only in plane with normal and grat vector (perp to lines)
    # return np.arctan(np.abs(rx / ry)) # only in plane with normal and grat vector (perp to lines)

  def matrix(self, inray=Ray()):
    # optical matrix, see https://www.brown.edu/research/labs/mittleman/sites/brown.edu.research.labs.mittleman/files/uploads/lecture11.pdf
    omatrix = np.eye(2)
    angleIN = self.angle_of_incidence(inray)
    try:
      outray = self.next_ray(inray)
    except:
      outray = Ray()
      print("Irgendwas bei Matrix Gitter Berechnung falsch gelaufen")
    angleOUT = self.angle_of_incidence(outray)
    A = np.cos(angleOUT) / np.cos(angleIN)
    # A = np.sin(angleOUT) / np.sin(angleIN)
    A *= 1 #??? Steht so in den Folien
    omatrix[0,0] = A
    omatrix[1,1] = 1/A
    return omatrix



  def kostenbauder(self, inray=Ray()):
    # kostenbauder matrix, see https://www.brown.edu/research/labs/mittleman/sites/brown.edu.research.labs.mittleman/files/uploads/lecture11.pdf
    kmatrix = np.eye(4)
    aoi = self.angle_of_incidence(inray)
    # angleIN = aoi + np.pi/2 if aoi < 0 else aoi
    # angleIN = aoi + np.pi if aoi < 0 else aoi
    angleIN = aoi

    # aoi = self.angle_to(inray)
    # angleIN = np.pi/2 - aoi if aoi > 0 else aoi
    # angleIN = np.pi/2 - aoi
    # angleIN = np.abs(angleIN)
    try:
      outray = self.next_ray(inray)
    except:
      outray = Ray()
      print("Irgendwas bei Matrix Gitter Berechnung falsch gelaufen")
    # aoo = outray.angle_to(self)
    # angleOUT = np.pi/2 + aoo if aoo > 0 else aoo #?1
    # angleOUT = 90 + aoo
    # angleOUT = np.abs(angleOUT)
    # angleOUT = np.pi - angleOUT
    theta = inray.wavelength/self.grating_constant
    # angleOUT = np.arccos(np.cos(angleIN) + theta)
    angleOUT = np.arcsin(theta*self.diffraction_order - np.sin(angleIN))

    # angleOUT = self.angle_of_incidence(outray)
    A = np.cos(angleOUT) / np.cos(angleIN)
    # A = np.sin(angleOUT) / np.sin(angleIN)
    A *= -1 #??? Steht so in den Folien
    c = 299792458 * 1e3 # speed of light in mm / s
    # c = 299792458 # speed of light in m / s
    # c = 299792458 * 1e-12 # speed of light in mm / fs

    kmatrix[0,0] = A
    kmatrix[1,1] = 1/A
    
    # wl = inray.wavelength * 1e-3 # wavelength in m
    # sign_factor = np.sign( np.sum(self.get_coordinate_system()[2] * inray.get_coordinate_system()[2] ) * np.sum(self.get_coordinate_system()[1] * inray.get_coordinate_system()[1] ))
    # sign_factor = np.sign( np.sum(self.get_coordinate_system()[2] * inray.get_coordinate_system()[2] ) * np.sum(self.get_coordinate_system()[1] * inray.get_coordinate_system()[1] ))
    sign_factor_y = np.sign( np.sum(self.get_coordinate_system()[1] * inray.get_coordinate_system()[1] ))
    sign_factor_z = np.sign( np.sum(self.get_coordinate_system()[2] * inray.get_coordinate_system()[2] ))
    wl = inray.wavelength * 1 # wavelength in mm
    D = inray.wavelength**2 / (c * self.grating_constant * np.cos(angleOUT)) * -1 * self.diffraction_order
    # D = inray.wavelength * (np.sin(angleOUT) - np.sin(angleIN)) / (c * np.cos(angleOUT))
    # D = - wl * (np.sin(angleOUT) + np.sin(angleIN)) / (c * np.cos(angleOUT))
    # kmatrix[1,3] = inray.wavelength * (np.cos(angleOUT) - np.cos(angleIN)) / (c * np.sin(angleOUT))
    # kmatrix[2,0] = (np.cos(angleIN) - np.cos(angleOUT)) / (c * np.sin(angleIN))

    kmatrix[1,3] = D 
    kmatrix[2,0] = A*D / wl

    print()
    print("AlphaIN =", angleIN*180/np.pi)
    print("AlphaOUT =", angleOUT*180/np.pi)
    print("A, 1/A", A, 1/A)
    print("D, D*A", D, A*D)
    print("SignFactorY", sign_factor_y)
    print("SignFactorZ", sign_factor_z)
    # print("sinIN =", np.sin(angleIN),"AlphaIN =", angleIN*180/np.pi)
    # print("sinOUT =", np.sin(angleOUT), "AlphaOUT =", angleOUT*180/np.pi)
    # print("cosIN =", np.cos(angleIN))
    # print("cosOUT =", np.cos(angleOUT))
    print()

    self._kostenbauder = kmatrix
    return kmatrix

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
