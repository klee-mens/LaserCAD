#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 11:46:23 2023

@author: mens
"""

from ..basic_optics import Component, Composition, Composed_Mount, Unit_Mount, Post

from ..freecad_models import (model_crystal, model_mirror,
                              model_crystal_mounts)
from ..freecad_models.utils import load_STL, thisfolder
import numpy as np

class Cylindric_Crystal(Component):
  def __init__(self, name="LaserCrystal", aperture=6, thickness=3, **kwargs):
    super().__init__(name=name, **kwargs)
    self.aperture = aperture
    self.thickness = thickness
    self.draw_dict["color"] = (0.8, 0.3, 0.1)
    self.freecad_model = model_mirror


class Crystal(Component):
  shapes = ["cylindrical", "rectangular"]

  def __init__(self, width=10, height=10, thickness=10, aperture=6,
               n=1.5, shape="rectangular", name="NewCrystal", **kwargs):
    super().__init__(name=name, **kwargs)
    if shape not in self.shapes:
      raise ValueError(
        f"Invalid shape {shape!r}. Choose one of: {', '.join(self.shapes)}."
      )

    self.shape = shape
    self.thickness = thickness
    self.aperture = aperture
    self.width = width
    self.height = height
    self.relative_refractive_index = n
    self.freecad_model = (
      model_mirror if shape == "cylindrical" else model_crystal
    )
    self.draw_dict["color"] = (131/255,27/255,44/255)
    self.set_mount(Crystal_Mount(
      shape=shape,
      thickness=thickness,
      inner_aperture=aperture,
      inner_width=width,
      inner_height=height,
    ))

  def update_draw_dict(self):
    super().update_draw_dict()
    if self.shape == "rectangular":
      self.draw_dict["height"] = self.height
      self.draw_dict["width"] = self.width
    self.draw_dict["thickness"] = self.thickness


class Crystal_Unit_Mount(Unit_Mount):
  shapes = ["cylindrical", "rectangular"]

  def __init__(self, shape="rectangular", width=30, height=30, thickness=10,
               inner_aperture=10, inner_width=10, inner_height=10,
               name="Crystal Unit Mount", **kwargs):
    if shape not in self.shapes:
      raise ValueError(
        f"Invalid shape {shape!r}. Choose one of: {', '.join(self.shapes)}."
      )
    super().__init__(model="dont_draw", name=name, **kwargs)
    self.shape = shape
    self.width = width
    self.height = height
    self.thickness = thickness
    self.inner_aperture = inner_aperture
    self.inner_width = inner_width
    self.inner_height = inner_height
    self.freecad_model = model_crystal_mounts
    self._update_docking_obj()

  def _update_docking_obj(self):
    self.docking_obj.pos = (
      self.pos + self.normal * (self.thickness / 2)
      + self.get_coordinate_system()[2] * (-self.height / 2)
    )
    self.docking_obj.normal = self.normal

  def _pos_changed(self, old_pos, new_pos):
    super()._pos_changed(old_pos, new_pos)
    self._update_docking_obj()

  def _axes_changed(self, old_axes, new_axes):
    super()._axes_changed(old_axes, new_axes)
    self._update_docking_obj()

  def draw_freecad(self, **kwargs):
    self.update_draw_dict()
    self.draw_dict.update({
      "shape": self.shape,
      "width": self.width,
      "height": self.height,
      "thickness": self.thickness,
      "inner_aperture": self.inner_aperture,
      "inner_width": self.inner_width,
      "inner_height": self.inner_height,
    })
    return self.freecad_model(**self.draw_dict)


class Crystal_Mount(Composed_Mount):
  def __init__(self, shape="rectangular", width=30, height=30, thickness=10,
               inner_aperture=10.0, inner_width=10., inner_height=10.0,
               name="Crystal Mount", **kwargs):
    super().__init__(name=name, **kwargs)
    self.add(Crystal_Unit_Mount(
      shape=shape,
      width=width,
      height=height,
      thickness=thickness,
      inner_aperture=inner_aperture,
      inner_width=inner_width,
      inner_height=inner_height,
    ))
    self.add(Post(model="0.5inch_post"))
