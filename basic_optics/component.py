# -*- coding: utf-8 -*-
"""
Created on Sat Aug 19 13:59:08 2023

@author: mens
"""

from .geom_object import Geom_Object
from .constants import inch
# from ..non_interactings import 
# from .mount import Mount
from .mount2 import Unit_Mount, get_mount_by_aperture_and_element
# from .post import Post_and_holder

from .. freecad_models import freecad_da

class Component(Geom_Object):
  """
  class for shaped components with mounts, posts and bases
  developes into Optical_Element and many non interactings
  """
  def __init__(self, name="Component", **kwargs):
    super().__init__(name, **kwargs)
    # self.mount_dict = dict()
    # self.mount_dict["pos"] = self.pos
    # self.mount_dict["normal"] = self.
    self.aperture = 1*inch # Apertur in mm, wichtig für Klippingabfrage (not yet implemented)
    self.set_mount_to_default()
    
  def set_mount_to_default(self):
    self.Mount = get_mount_by_aperture_and_element(self.aperture, self.class_name())
    self.Mount.set_geom(self.get_geom())
    
    # self.mount = Mount(name=name+"_mount", elm_type="dont_draw")
    # self.mount.pos = self.pos
    # self.mount.normal = self.normal
    # self.post = Post_and_holder(name=name+"post",elm_type="dont_draw")
    
  # def update_mount(self):
  #   self._update_mount_dict()
  #   self.mount = Mount(**self.mount_dict)
  
  
  def _update_mount_dict(self):
    # self.mount_dict["pos"] = self.pos
    # self.mount_dict["normal"] = self.normal
    # self.mount.pos = self.pos
    # self.mount.normal = self.normal
    pass

  def draw_mount(self):
    # self.update_mount()
    return (self.Mount.draw())
  
  def _pos_changed(self, old_pos, new_pos):
    self._rearange_subobjects_pos( old_pos, new_pos, [self.Mount])
  
  def _axes_changed(self, old_axes, new_axes):
    self._rearange_subobjects_axes( old_axes, new_axes, [self.Mount])
  
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