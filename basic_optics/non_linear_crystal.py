#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 25 11:17:33 2025

@author: clemens
"""

from .optical_element import Opt_Element
from .mount import Unit_Mount, Composed_Mount, Post
from ..freecad_models import model_mirror

DEFAULT_NLO_CRYSTAL_COLOR = (200/255, 200/255, 255/255)


class NLO_Crystal(Opt_Element):
  """
  Class to fake a non linear crystal e.g. for SHG
  Appears as a Lambda Plate
  Multiplies the wavelength of the next beam by <wavelength_multiplier> and 
  sets its color to a fixed, specified value <output_color>
  """
  def __init__(self, name="New_NLO_Crystal", wavelength_multiplier=0.5, 
               output_color=(0.1, 0.7, 0.2), **kwargs):
    super().__init__(name=name, **kwargs)
    self.wavelength_multiplier = wavelength_multiplier
    self.output_color = output_color
    #cosmetics
    self.aperture = 25.4/2
    self.thickness = 2
    self.freecad_model = model_mirror
    self.set_mount_to_default()
    self.draw_dict["Radius"] = 0
    self.draw_dict["color"] = DEFAULT_NLO_CRYSTAL_COLOR    
    
  def set_mount_to_default(self):
    self.Mount = Composed_Mount()
    self.Mount.add(Unit_Mount("lambda_mirror_mount"))
    self.Mount.add(Post())
    self.Mount.set_geom(self.get_geom())
  
  def next_ray(self, ray):
    ray2 = self.just_pass_through(ray)
    ray2.wavelength = ray.wavelength * self.wavelength_multiplier
    return ray2
  
  def next_beam(self, beam):
    beam2 = super().next_beam(beam)
    # beam2.set_wavelength(beam.wavelength() * self.wavelength_multiplier)
    beam2.draw_dict["color"] = self.output_color
    return beam2
  
  