# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 16:06:17 2023

@author: HE
"""

from .optical_element import Opt_Element
import numpy as np
from copy import deepcopy
from .ray import Ray
from .beam import Beam #,RayGroup
import matplotlib.pyplot as plt
# from .freecad_models import model_intersection_plane,iris_post
from .freecad_models import model_intersection_plane
from .freecad_models.freecad_model_ray import RAY_COLOR


class Intersection_plane(Opt_Element):
  """
  The class of the intersection plane.
  special functions: spot_diagram. Draw the Spot diagram at the intersection 
  plane
  """
  def __init__(self, dia=100, name="NewPlane", **kwargs):
    super().__init__(name=name, **kwargs)
    self.draw_dict["Radius"] = dia/2
    self.draw_dict["dia"]=dia
    self.aperture=dia
    # self.interacts_with_rays = False
    
  def next_ray(self, ray):
    ray2=deepcopy(ray)
    ray2.pos = ray.intersect_with(self)
    # return ray2
    return ray2
  
  def draw_fc(self):
    self.update_draw_dict()
    return model_intersection_plane(**self.draw_dict)
  
  
  def spot_diagram(self, beam):
    """
      Draw the Spot diagram at the intersection plane

      Parameters
      ----------
      beam : Beam
          Input beam.

      Returns
      -------
      None.

      """
    point_x = []
    point_y = []
    point_c = []
    # if isinstance(beam, RayGroup) or isinstance(beam, Beam):
    if isinstance(beam, Beam):
      rays = beam.get_all_rays()
    else:
      rays = beam
    cmap = plt.cm.gist_rainbow
    for point_i in rays:
      intersection_point = point_i.intersection(self)
      lamuda = point_i.wavelength
      if lamuda>=400e-6 and lamuda<=780e-6:
        c = cmap((lamuda-400e-6)/380e-6)
      elif 'color' in point_i.draw_dict:
        c = point_i.draw_dict["color"]
      else:
        c=RAY_COLOR
      point_c.append(c)
      pos_diff = intersection_point - self.pos
      pos_diff1 = np.dot(pos_diff,np.cross((0,0,1),self.normal))
      pos_diff2 = np.dot(pos_diff,(0,0,-1))
      # print(pos_diff1,pos_diff2)
      # pos_diff[1] = pow(pos_diff1[0]**2+pos_diff1[1]**2+pos_diff1[2]**2,0.5)
      # pos_diff[2] = pow(pos_diff2[0]**2+pos_diff2[1]**2+pos_diff2[2]**2,0.5)
      if self.draw_dict["dia"]**2<pos_diff1**2+pos_diff2**2:
        self.draw_dict["dia"] = pow(pos_diff1**2+pos_diff2**2,0.5)
        self.aperture=self.draw_dict["dia"]
      point_x.append(pos_diff1)
      point_y.append(pos_diff2)
    plt.figure()
    # area = (20 * np.random.rand(37))**2
    # c = np.sqrt(area)
    plt.scatter(point_x,point_y,c=point_c)
    plt.xlabel("x-axis, or y-axis if you follow the 3D coordinate (mm)")
    plt.ylabel("y-axis, or z-axis if you follow the 3D coordinate (mm)")
    plt.title("The spot diagram at " + self.name)
    plt.axis('equal')
    plt.show()
  
  def __repr__(self):
    n = len(self.class_name())
    txt = 'Intersection_plane(dia=' + repr(self.aperture)
    txt += ', ' + super().__repr__()[n+1::]
    return txt