#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 00:51:06 2023

@author: mens
"""

from .composition import Composition
from .mirror import Mirror
from .beam import Gaussian_Beam
import numpy as np

class Resonator(Composition):
  """
  class for laser resonators
  inherits from composition
  geometry_type: linear / ring(?)
  this alters the sequence for eigenmode() and compute_beams()
  add_outputcoupler / set_outputcoupler: sets  the OC (type=Mirror)
  """
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self._outputcoupler_index = 0
    self.wavelength = 1030e-6 #Yb in mm
    
  def add_outputcoupler(self, item):
    if type(item) == type(Mirror()):
      self.add_on_axis(item)
      self._outputcoupler_index = len(self._elements)-1
    else:
      print("Outputcoupler must be a mirror")
      return -1
    
  def set_outputcoupler_index(self, index):
    if type(self._elements[index]) == type(Mirror()):
      self._outputcoupler_index = index
    else:
      print("Outputcoupler must be a mirror")
      return -1
  
    def set_wavelength(self, wavelength):
      """
      sets the own wavelength and thus the one of the lightsource and eigenmode
      PARAMETER: wavelength in mm
      """
      self.wavelength = wavelength
      self._lightsource.wavelength = wavelength
  
  def compute_eigenmode(self, start_index=0):
    """
    computes the gaussian TEM00 eigenmode from the matrix law

    Returns
    -------
    q : TYPE complex number
      the q parameter

    """
    #claculate the matrix with the correct sequence
    noe = len(self._elements)
    seq = [x for x in range(noe)]
    seq.extend([x for x in range(noe-2, 0, -1)])
    prop = np.linalg.norm(self._elements[0].pos-self._elements[1].pos)
    self._last_prop = prop
    self.set_sequence(seq)
    matrix = self.matrix()
    A = matrix[0,0]
    B = matrix[0,1]
    C = matrix[1,0]
    D = matrix[1,1]
    z = (A-D)/(2*C)
    E = -B/C - z**2
    if E < 0:
      print("Resonator is unstable")
      return -1
    ### set Lightsource accordingly 
    z0 = np.sqrt(E)
    q_para = (z +1j*z0)
    gb00 = Gaussian_Beam(wavelength=self.wavelength) #der -1 strahl
    gb00.q_para = q_para
    gb00.set_geom(self.get_geom())
    lsgb = self._elements[0].next_beam(gb00)
    self._lightsource = lsgb
    # set sequence for compute beams
    self.set_sequence([x for x in range(1, noe)])
    return q_para
  
  def compute_beams(self, external_source=None):
    self.compute_eigenmode()
    super().compute_beams(external_source)