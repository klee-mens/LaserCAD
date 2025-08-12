#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 28 17:24:22 2025

@author: mens
"""
from .geom_object import Geom_Object
from .composition import Composition


class Multi_Beamline_Composition(Geom_Object):
  def __init__(self, name="New_Multi_Line", **kwargs):
    super().__init__(name=name, **kwargs)
    self._max_index = 0
    self._active_index = 0
    self._subcomps = [Composition(name=self.name + "Line1")]

  def set_light_source(self, beam):
    """
    only works correctly if set directly after initialization
    """
    self._subcomps[0].set_light_source(beam)

  def add_on_axis(self, item):
    self._subcomps[self._active_index].add_on_axis(item)

  def add_fixed_elm(self, item):
    self._subcomps[self._active_index].add_fixed_elm(item)

  def add_supcomposition_on_axis(self, scomp):
    self._subcomps[self._active_index].add_supcomposition_on_axis(scomp)

  def add_supcomposition_fixed(self, scomb):
    self._subcomps[self._active_index].add_supcomposition_fixed(scomb)

  def propagate(self, x):
    self._subcomps[self._active_index].propagate(x)

  def get_acitve_index(self):
    return self._active_index

  def change_acitve_index(self, index):
    self._active_index = index

  def add_new_line(self, beam):
    newcomp = Composition(name="asdf")
    newcomp.set_geom(beam.get_geom())
    newcomp.set_light_source(beam)
    self._subcomps.append(newcomp)
    self._active_index += 1


  def draw(self):
    for comp in self._subcomps:
      comp.draw()

  def compute_beams(self):
    for comp in self._subcomps:
      comp.compute_beams()

  def recompute_optical_axis(self):
    for comp in self._subcomps:
      comp.recompute_optical_axis()

  def _pos_changed(self, old_pos, new_pos):
    """
    wird aufgerufen, wen die Position von <self> verändert wird
    ändert die Position aller __rays mit
    """
    super()._pos_changed(old_pos, new_pos)
    self._rearange_subobjects_pos(old_pos, new_pos, self._subcomps)

  def _axes_changed(self, old_axes, new_axes):
    """
    wird aufgerufen, wen die axese von <self> verändert wird
    dreht die axese aller __rays mit

    dreht außerdem das eigene Koordiantensystem
    """
    super()._axes_changed(old_axes, new_axes)
    self._rearange_subobjects_axes(old_axes, new_axes, [self._subcomps]) #sonst wird ls doppelt geshifted
