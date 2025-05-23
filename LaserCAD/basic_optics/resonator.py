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

class LinearResonator(Composition):
  """
  class for laser resonators
  inherits from composition
  geometry_type: linear / ring(?)
  this alters the sequence for eigenmode() and compute_beams()
  add_outputcoupler / set_outputcoupler: sets  the OC (type=Mirror)
  """
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self._output_coupler_index = 0
    self._input_coupler_index = 0
    self.wavelength = 1030e-6 #Yb in mm
    self.draw_dict["beam_model"] = "Gaussian"

  def add_output_coupler(self, item):
    if type(item) == type(Mirror()):
      self.add_on_axis(item)
      self._out_putcoupler_index = len(self._elements)-1
    else:
      print("Outputcoupler must be a mirror")
      return -1

  def set_output_coupler_index(self, index):
    if type(self._elements[index]) == type(Mirror()):
      self._output_coupler_index = index
    else:
      print("Outputcoupler must be a mirror")
      return -1

  def set_input_coupler_index(self, index, forward=True):
    """
    sets the index for the input coupler if the resonator is used as an regen-
    erative amplifier. 
    (Should best be used after all elements have been inserted)
    The optical Element[index] becomes the input coupler meaning that the next 
    beams geom will be GEOM0 if forward is true. If not, than the beam before
    will be the input beam with inverted geom.
    All other elements will be turned accordingly and afterwards the geom of 
    the whole resonator is reseted to GEOM0
    

    Parameters
    ----------
    index : integer in the range [0, len(self._elments)-1]
      DESCRIPTION.
    forward : bool, optional
      DESCRIPTION. The default is True.

    Returns
    -------
    None.

    """
    self._input_coupler_index = index
    self.compute_beams()
    if forward:
      direction = self._beams[index].get_axes()
    else:
      helper = Gaussian_Beam()
      helper.normal = - self._beams[index-1].normal
      direction = helper.get_axes()
    rot_mat = np.linalg.inv(direction)
    self.set_axes(rot_mat)
    old_pos = self._elements[index].pos
    self.pos += -old_pos
    # reset to GEOM0
    self._pos = np.zeros(3)
    self._axes = np.eye(3)
      
  def output_beam(self):
    self.compute_beams()
    return self._beams[self._output_coupler_index-1]
        

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
    # gb00 = Beam(wavelength=self.wavelength, distribution="Gaussian") #der -1 strahl
    gb00.q_para = q_para
    gb00.set_geom(self._elements[0].get_geom())
    lsgb = self._elements[0].next_beam(gb00)
    self._lightsource = lsgb
    # set sequence for compute beams
    # self.set_sequence([x for x in range(1, noe)])
    prop = np.linalg.norm(self._elements[-1].pos-self._elements[-2].pos)
    self._last_prop = prop
    return q_para

  def compute_beams(self, external_source=None):
    self.compute_eigenmode()
    self.set_sequence([x for x in range(1, len(self._elements)-1)])
    super().compute_beams(external_source)
    for beam in self._beams:
      # beam.draw_dict["model"] = self.draw_dict["beam_model"]
      beam.draw_dict["model"] = "Gaussian"
        
    
  def transform_gauss_to_cone_beams(self):
    self.compute_beams()
    cones = []
    for gb in self._beams:
      cones.append( gb.transform_to_cone_beam() )
    return cones

    
class CircularResonator(LinearResonator):
  
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    
  def Setting_last_element(self):
    item = self._elements[-1]
    if type(item) == type(Mirror()):
      p0 = self._elements[-2].pos
      p1 = self._elements[0].pos
      item.set_normal_with_2_points(p0, p1)
      # p0 = self._elements[-1].pos
      # p1 = self._elements[1].pos
      # self._elements[0].set_normal_with_2_points(p0, p1)
    else:
      print("The last element must be a mirror")
      return -1
  
  def compute_eigenmode(self, start_index=0):
    noe = len(self._elements)
    seq = [x for x in range(noe)]
    seq.extend([0])
    prop = np.linalg.norm(self._elements[-1].pos-self._elements[0].pos)
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
    gb00.set_geom(self._elements[0].get_geom())
    lsgb = self._elements[0].next_beam(gb00)
    self._lightsource = lsgb
    # set sequence for compute beams
    # self.set_sequence([x for x in range(1, noe)])
    prop = np.linalg.norm(self._elements[-1].pos-self._elements[-2].pos)
    self._last_prop = prop
    return q_para
  # def draw_with_cones(self):
  #   self.draw_elements()
  #   self.draw_mounts()
  #   self.compute_beams()
  #   cones = self.transform_gauss_to_cone_beams()
  #   for cone in cones:
  #     cone.draw()