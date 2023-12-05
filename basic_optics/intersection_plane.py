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
from ..freecad_models import model_intersection_plane
from ..freecad_models.freecad_model_ray import RAY_COLOR


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
  
  
  def spot_diagram(self, beam, aberration_analysis=False):
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
    ray_lam = []
    # if isinstance(beam, RayGroup) or isinstance(beam, Beam):
    if isinstance(beam, Beam):
      rays = beam.get_all_rays()
    else:
      rays = beam
    cmap = plt.cm.gist_rainbow
    for point_i in rays:
      intersection_point = point_i.intersection(self)
      # print(intersection_point)
      lamuda = point_i.wavelength
      
      ray_lam.append(lamuda)
      if lamuda>=400e-6 and lamuda<=700e-6:
        c = cmap(1-(lamuda-400e-6)/300e-6)
      elif 'color' in point_i.draw_dict:
        c = point_i.draw_dict["color"]
      else:
        c=RAY_COLOR
      point_c.append(c)
      pos_diff = intersection_point - self.pos
      pos_diff1 = np.dot(pos_diff,np.cross((0,0,1),self.normal))
      pos_diff2 = np.dot(pos_diff,(0,0,1))
      # print(pos_diff1,pos_diff2)
      # pos_diff[1] = pow(pos_diff1[0]**2+pos_diff1[1]**2+pos_diff1[2]**2,0.5)
      # pos_diff[2] = pow(pos_diff2[0]**2+pos_diff2[1]**2+pos_diff2[2]**2,0.5)
      if self.draw_dict["dia"]**2<pos_diff1**2+pos_diff2**2:
        self.draw_dict["dia"] = pow(pos_diff1**2+pos_diff2**2,0.5)
        self.aperture=self.draw_dict["dia"]
      point_x.append(pos_diff1)
      point_y.append(pos_diff2)
    ray_middle = rays[int(len(rays)/2)]
    point_x_middle = point_x[int(len(rays)/2)]
    point_y_middle = point_y[int(len(rays)/2)]
    diff_x = [x-point_x_middle for x in point_x]
    diff_y = [y-point_y_middle for y in point_y]
    ray_lam = [ray.wavelength for ray in rays]
    for ray in rays:
      if ray.normal[1]>1 or ray_middle.normal[1]>1:
        print(ray.normal,ray_middle.normal)
        print("whyyyyyyyyyyyyyyyyyyy")
    if ray_middle.normal[1]>1:
      ray_middle.normal[1]=1
    # for ray in rays:
    #   ray.normal = np.linalg.norm(ray.normal)
    tilt_x = [-np.arcsin(ray.normal[1])+np.arcsin(ray_middle.normal[1]) for ray in rays]
    tilt_y = [np.arcsin(ray.normal[2])-np.arcsin(ray_middle.normal[2]) for ray in rays]
    font1 = {'size':24}
    font2 = {'size':11}
    if aberration_analysis:
      plt.figure(figsize=(16,9))
      ax1=plt.subplot(2,2,1)
      plt.plot(ray_lam, diff_x)
      plt.tick_params(labelsize=11)
      plt.ylabel("x-shift (mm)",font2)
      plt.xlabel("wavelength (mm)",font2)
      plt.title("The displacement in the x direction at " + self.name,font2)
      plt.axhline(0, color = 'black', linewidth = 1)
      ax2=plt.subplot(2,2,2)
      plt.plot(ray_lam, diff_y)
      plt.tick_params(labelsize=11)
      plt.ylabel("y-shift (mm)",font2)
      plt.xlabel("wavelength (mm)",font2)
      plt.title("The displacement in the y direction at " + self.name,font2)
      plt.axhline(0, color = 'black', linewidth = 1)
      ax3=plt.subplot(2,2,3)
      plt.plot(ray_lam, tilt_x)
      plt.tick_params(labelsize=11)
      plt.ylabel("x-tilt (rad)",font2)
      plt.xlabel("wavelength (mm)",font2)
      plt.title("The tilt in the x direction at " + self.name,font2)
      plt.axhline(0, color = 'black', linewidth = 1)
      ax4=plt.subplot(2,2,4)
      plt.plot(ray_lam, tilt_y)
      plt.tick_params(labelsize=11)
      plt.ylabel("y-tilt (rad)",font2)
      plt.xlabel("wavelength (mm)",font2)
      plt.title("The tilt in the y direction at " + self.name,font2)
      plt.axhline(0, color = 'black', linewidth = 1)
    plt.figure(figsize=(16,11))
    # area = (20 * np.random.rand(37))**2
    # c = np.sqrt(area)
    plt.scatter(point_x,point_y,s=10,c=point_c)
    plt.tick_params(labelsize=24)
    # plt.xlim(-0.0015,0.0015)
    # plt.ylim(-0.0015,0.0015)
    plt.xlabel("x-axis (mm)",font1,labelpad=20)
    plt.ylabel("y-axis (mm)",font1)
    plt.title("The spot diagram at " + self.name,font1)
    plt.savefig("The spot diagram at " + self.name+'.pdf')
    # plt.axhline(0, color = 'black', linewidth = 1,linestyle = '--')
    # plt.axvline(0, color = 'black', linewidth = 1,linestyle = '--')
    # plt.axis('equal')
    plt.show()
    return point_x,point_y
  
  def __repr__(self):
    n = len(self.class_name())
    txt = 'Intersection_plane(dia=' + repr(self.aperture)
    txt += ', ' + super().__repr__()[n+1::]
    return txt