#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 21 19:50:31 2022

@author: mens
"""

from basic_optics import Opt_Element


class Propagation(Opt_Element):
  def __init__(self, d=100, **kwargs):
    super().__init__(**kwargs)
    self.distance = d
    self.length = d

  @property
  def distance(self):
    return self.__d
  @distance.setter
  def distance(self, x):
    self.__d = x
    self._matrix[0,1] = x
    self.length = x

  def __repr__(self):
    n = len(self.Klassenname())
    txt = 'Propagation(d=' + repr(self.distance)
    txt += ', ' + super().__repr__()[n+1::]
    return txt
  
  def next_ray(self, ray):
    pass # neue Rays sollen nur von opt. Elem. wie Lens, etc erzeugt werden
    
#   def next_beam(self, beam):
#     pass # neue Beams sollen nur von opt. Elem. wie Lens, etc erzeugt werden
  
  def next_geom(self, geom):
    pos, normal = geom[0], geom[1]
    pos += normal*self.distance
    return (pos, normal)
  
  def draw_ray(self, ray):
    pass
  
  def draw(self):
    return None
  
def tests():
  p = Propagation(100)
  print(p.matrix())
  p.distance = 150
  print(p.matrix())
  
  print()
  
  oe = Opt_Element()
  print(oe)
  oe.set_geom(p.next_geom(oe.get_geom()))
  print(oe)
  
  print()
  
  p.name = "erwin"
  p2 = eval(repr(p))
  print(p2)
  
  
if __name__ == "__main__":
  tests()