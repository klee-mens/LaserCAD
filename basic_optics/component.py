# -*- coding: utf-8 -*-
"""
Created on Sat Aug 19 13:59:08 2023

@author: mens
"""

from .geom_object import Geom_Object
from .. freecad_models import freecad_da

class Component(Geom_Object):
  """
  class for shaped components with mounts, posts and bases
  developes into Optical_Element and many non interactings
  """


  def draw_mount(self):
    if freecad_da:
      return self.draw_mount_fc()
    else:
      txt = self.draw_mount_text()
      print(txt)
      return txt

  def draw_mount_fc(self):
    #ToDo: fürs Debugging hier einfach einen Zylinder mit norm uns k zeichnen
    return None

  def draw_mount_text(self):
    txt = "Kein Mount für <" +self.name + "> gefunden."
    return txt

  def __make_unit(self):
    """ToDo: one day this will become something like: make a unit consisting of
    self, Geom_Obj::mount, Geom_Obj::post
    or smt like this...
    """
    pass