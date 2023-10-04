# -*- coding: utf-8 -*-
"""
Created on Sat Aug 19 13:59:08 2023

@author: mens
"""

from .geom_object import Geom_Object
# from ..non_interactings import 
from .mount import Mount
# from .post import Post_and_holder

from .. freecad_models import freecad_da

class Component(Geom_Object):
  """
  class for shaped components with mounts, posts and bases
  developes into Optical_Element and many non interactings
  """
  def __init__(self, name="Component", **kwargs):
    super().__init__(name, **kwargs)
    self.mount_dict = dict()
    self.mount_dict["pos"] = self.pos
    self.mount_dict["normal"] = self.normal
    self.mount = Mount(name=name+"_mount", elm_type="dont_draw")
    # self.post = Post_and_holder(name=name+"post",elm_type="dont_draw")
    
  # def update_mount(self):
  #   self._update_mount_dict()
  #   self.mount = Mount(**self.mount_dict)

  def _update_mount_dict(self):
    self.mount_dict["pos"] = self.pos
    self.mount_dict["normal"] = self.normal

  def draw_mount(self):
    # self.update_mount()
    return (self.mount.draw())
  
  def _pos_changed(self, old_pos, new_pos):
    self._rearange_subobjects_pos( old_pos, new_pos, [self.mount])
  
  def _axes_changed(self, old_axes, new_axes):
    self._rearange_subobjects_axes( old_axes, new_axes, [self.mount])
  
  #   if freecad_da:
  #     return self.draw_mount_fc()
  #   else:
  #     txt = self.draw_mount_text()
  #     print(txt)
  #     return txt

  # def draw_mount_fc(self):
  #   #ToDo: fürs Debugging hier einfach einen Zylinder mit norm uns k zeichnen
  #   return None

  # def draw_mount_text(self):
  #   txt = "Kein Mount für <" +self.name + "> gefunden."
  #   return txt

  # def __make_unit(self):
  #   """ToDo: one day this will become something like: make a unit consisting of
  #   self, Geom_Obj::mount, Geom_Obj::post
  #   or smt like this...
  #   """
  #   pass