#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 21 20:28:02 2022

@author: mens
"""

from ..freecad_models import model_lens, lens_mount
from .optical_element import Opt_Element
from .mount import Unit_Mount
from copy import deepcopy
import numpy as np

class Lens(Opt_Element):
  def __init__(self, f=100, name="NewLens", **kwargs):
    super().__init__(name=name, **kwargs)
    self.focal_length = f
    self.thickness = 4
    self.freecad_model = model_lens

  @property
  def focal_length(self):
    return self.__f
  @focal_length.setter
  def focal_length(self, x):
    self.__f = x
    if x == 0:
      self._matrix[1,0] = 0
    else:
      self._matrix[1,0] = -1/x

  def next_ray(self, ray):
    return self.ABCD_refraction(ray)

  def update_draw_dict(self):
    super().update_draw_dict()
    self.draw_dict["Radius1"] = 400
    self.draw_dict["Radius2"] = 0

  def __repr__(self):
    n = len(self.class_name())
    txt = 'Lens(f=' + repr(self.focal_length)
    txt += ', ' + super().__repr__()[n+1::]
    return txt


class Cylindrical_Lens(Opt_Element):
  """
  The class of Cylindrical mirror.
  Cylindrical mirror have those parameters:
    radius: The curvature of the mirror
    height: The vertical thickness of the mirror
    thickness: The horizontal thickness of the mirror
  The default mirror is placed horizontally, which means the cylinder_center
  points tp the z-axis. Use rotate function if you want to rotate the mirror.
  """
  def __init__(self, f=200,height=10, thickness=25, **kwargs):
    super().__init__(**kwargs)
    self.focal_length = f
    # self.draw_dict["Radius"] = radius
    self.height=height
    self.thickness=thickness
    # self.draw_dict["model_type"]="Stripe"
    # self.freecad_model = model_mirror
    self.Mount = Unit_Mount()

  # @property
  # def radius(self):
  #   return self.__radius
  # @radius.setter
  # def radius(self, x):
  #   """
  #   This part is incorrect. Since I don't know the matrix of Cylindrical_Mirror
  #   Parameters
  #   ----------
  #   x : TYPE
  #     DESCRIPTION.
  #   """
  #   self.__radius = x
  #   if x == 0:
  #     self._matrix[1,0] = 0
  #   else:
  #     self._matrix[1,0] = -2/x


  # def update_draw_dict(self):
  #   super().update_draw_dict()
  #   self.draw_dict["dia"]=self.aperture
  #   self.draw_dict["Radius"] = self.radius
  #   self.draw_dict["height"]=self.height
  #   self.draw_dict["thickness"]=self.thickness

  def next_ray(self, ray):
    """
    erzeugt den nächsten Ray auf Basis der analytischen Berechung von Schnitt-
    punkt von Sphere mit ray und dem vektoriellen Reflexionsgesetz
    siehe S Hb o LaO S 66 f

    Parameters
    ----------
    ray : TYPE Ray
      input ray

    Returns
    -------
    ray2 : TYPE Ray
      output ray

    """
    ray2 = deepcopy(ray)
    ray2.name = "next_" + ray.name
    center = self.pos - self.radius * self.normal
    xx,yy,zz = self.get_coordinate_system()
    ray_origin = ray2.pos
    ray_direction = ray2.normal
    cylinder_center = center
    cylinder_axis = zz

    middle_vec = cylinder_center + cylinder_axis * (np.dot(ray_origin,cylinder_axis) - np.dot(cylinder_center,cylinder_axis))-ray_origin
    middle_vec2 = cylinder_axis*(np.dot(ray_direction,cylinder_axis))-ray_direction
    a = np.dot(middle_vec2 , middle_vec2)
    b = 2 * np.dot(middle_vec2 , middle_vec)
    c = np.dot(middle_vec , middle_vec) - self.radius **2


    # Compute discriminant
    discriminant = b**2 - 4 * a * c

    # If discriminant is negative, no intersection
    if discriminant < 0:
        print("Warning: no interaction of ray with cylindirc lens")
        print(ray2)
        ray2.draw()
        print("ray_origin=",ray_origin)
        print("ray_direction=",ray_direction)
        print("cylinder_center=",cylinder_center)
        print("cylinder_axis=",cylinder_axis)
        return None

    # Compute t parameter (parameter along the ray direction)
    t1 = (-b + np.sqrt(discriminant)) / (2 * a)
    t2 = (-b - np.sqrt(discriminant)) / (2 * a)

    # Check if intersection is within ray segment
    # if t1 < 0 and t2 < 0:
    #     return None

    # Select smallest positive t
    # t = min(t1, t2) if t1 >= 0 and t2 >= 0 else max(t1, t2)
    if self.radius>0:
      t = max(t1, t2)
    else:
      t = min(t1, t2)
    # Compute intersection point

    intersection_point = ray_origin + ray_direction * t
    p0 = intersection_point
    ray.length = np.linalg.norm(p0-ray.pos)
    
    new_center = cylinder_center + cylinder_axis * (np.dot(p0,cylinder_axis)-np.dot(cylinder_center,cylinder_axis))
    surface_norm = p0 - new_center #Normale auf Spiegeloberfläche in p0
    surface_norm *= 1/np.linalg.norm(surface_norm) #normieren
    #Reflektionsgesetz
    # print(cylinder_center,new_center)
    ray2.normal = ray.normal - 2*np.sum(ray.normal*surface_norm)*surface_norm
    ray2.pos = p0
    return ray2


def tests():
  from basic_optics import Ray

  l1 = Lens(name="susanne")
  l2 = eval(repr(l1))
  print(l2)

  print()

  r = Ray(pos = (0,0,90))
  print(r)
  r2 = l1.next_ray(r)
  print(r2)
  s = l1.focal_length / r2.normal[0]
  h = r2.normal[2]*s
  print(h)
  print("sollte bei -10 liegen")


if __name__ == "__main__":
  tests()