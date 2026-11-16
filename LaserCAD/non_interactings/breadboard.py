# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 13:52:28 2023

@author: mens
"""


from ..basic_optics import Geom_Object
from ..freecad_models.utils import thisfolder, load_STL

class Breadboard(Geom_Object):
  """Optical breadboard (STL model) as a base for the setup.

  Parameters
  ----------
  pos : array-like
    Position of the breadboard (note: unlike other objects this class takes
    the position as a constructor argument).
  Xdimension, Ydimension are attributes with the size in mm.
  """
  def __init__(self, name="BreadBoard", pos=(0,0,0), **kwargs):
    super().__init__(name, **kwargs)
    self.pos = pos
    stl_file=thisfolder+"/post/optical_breadboard.stl"
    self.draw_dict["stl_file"]=stl_file
    self.freecad_model = load_STL
    self.Xdimension = 1500
    self.Ydimension = 800
    