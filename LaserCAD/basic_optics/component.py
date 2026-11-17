# -*- coding: utf-8 -*-
"""
Created on Sat Aug 19 13:59:08 2023

@author: mens
"""

from .geom_object import Geom_Object
from .constants import inch
from .mount import get_mount_by_aperture_and_element
from ..freecad_models.utils import thisfolder, load_STL

# from .. freecad_models import freecad_da

class Component(Geom_Object):
  """
  class for shaped components with mounts, posts and bases
  developes into Optical_Element and many non interactings
  """
  def __init__(self, name="Component", aperture=1*inch, thickness=5, stl_file=None, **kwargs):
    super().__init__(name, **kwargs)
    if type(aperture) == int:
      aperture = inch*float(aperture) # convert integer values to inch, for easier use
    self._aperture = aperture # Aperture in mm for drawing, Mount and clipping (not yet implemented)
    self.thickness = thickness # Thickness in mm, importent for mount placing and drawing
    self.set_mount_to_default()

    if stl_file is not None:
      self.draw_dict["stl_file"] = rf"{thisfolder}\{stl_file}"
      self.freecad_model = load_STL
   
  @property
  def aperture(self):
    """Diameter of the component in mm. Setting it also resets the mount to the default."""
    return self._aperture
  
  @aperture.setter
  def aperture(self, x):
    self._aperture = x
    self.set_mount_to_default()
    
  def set_mount_to_default(self):
    """Choose a mount that fits aperture, class and thickness and place it at the component."""
    self.Mount = get_mount_by_aperture_and_element(self.aperture, 
                                                   self.class_name(), 
                                                   self.thickness)
    self.Mount.set_geom(self.get_geom())
  
  def set_mount(self, mount):
    """Use <mount> as mount of the component and move it to the geom of the component."""
    mount.set_geom(self.get_geom())
    self.Mount = mount
  
  def set_mount_face_mounted(self):
    """Place the mount so that it holds the component at its front surface."""
    self.Mount.set_geom(self.get_geom())

  def set_mount_back_mounted(self):
    """Place the mount so that it holds the component at its back surface."""
    self.Mount.set_geom(self.get_geom())
    self.Mount.pos += self.normal * (self.thickness - self.Mount.get_depth())
  
  def update_draw_dict(self):
    """Add aperture (as dia) and thickness to <draw_dict>."""
    super().update_draw_dict()
    self.draw_dict["dia"]=self.aperture
    self.draw_dict["thickness"] = self.thickness

  def draw_mount(self):
    # self.update_mount()
    """Draw the mount of the component and return the drawn object."""
    return (self.Mount.draw())
  
  def _pos_changed(self, old_pos, new_pos):
    self._rearange_subobjects_pos( old_pos, new_pos, [self.Mount])
  
  def _axes_changed(self, old_axes, new_axes):
    self._rearange_subobjects_axes( old_axes, new_axes, [self.Mount])