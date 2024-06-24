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
# import matplotlib.patches as patches
# from .freecad_models import model_intersection_plane,iris_post
from ..freecad_models import model_intersection_plane
from ..freecad_models.freecad_model_ray import RAY_COLOR
from matplotlib.ticker import MultipleLocator

diff_x_cry = [-0.20076010797285335, -0.1752682057638194, -0.14832976837497858, -0.12015735440635117, -0.09099987494151646, -0.06109424159855406, -0.030680196399349085, 0.0, 0.0307019214285767, 0.06117937732711312, 0.09118486873072389, 0.12047010861884357, 0.14879170126868208, 0.17590597398977387, 0.2015544706580202]
diff_y_cry = [-0.10156237363102605, -0.0750474302730737, -0.05241530208066081, -0.03373726562095669, -0.01908489361107968, -0.008529989532291893, -0.0021444304046127627, 0.0, -0.0021681899642942426, -0.008719962919457203, -0.019725470668134903, -0.035253719056612454, -0.05537216198555939, -0.08014624388293612, -0.10963881833544065]
tilt_x_cry = [-2.7526473850164273e-05, -2.414982747700558e-05, -2.0505872992448785e-05, -1.6639956011570334e-05, -1.260514845164071e-05, -8.452289178150265e-06, -4.233069844349944e-06, 0.0, 4.193632299962809e-06, 8.293805118329173e-06, 1.224581310997181e-05, 1.599432491232215e-05, 1.9484451468185168e-05, 2.2660903050038627e-05, 2.5464224627602982e-05]
tilt_y_cry = [-3.608313639199279e-05, -2.6738140103065177e-05, -1.8730088901166558e-05, -1.2093258705964494e-05, -6.8634633913724195e-06, -3.0781793650919874e-06, -7.766486052704896e-07, 0.0, -7.913822926101208e-07, -3.196110027968585e-06, -7.2618241948557955e-06, -1.30386694404533e-05, -2.0579486633780402e-05, -2.994003897978144e-05, -4.117924346314692e-05]

diff_x_sph = [0.16018770658053902, 0.1345679295447665, 0.11010694142276586, 0.08665928248627776, 0.0640767696415976, 0.042208613173014636, 0.020901550553515256, 0.0, -0.020653762970307712, -0.04121940266663089, -0.06185828943071674, -0.08273323005766872, -0.1040081559775854, -0.12584776197683054, -0.14841708666358747]
diff_y_sph = [-0.01527368314286548, -0.011749667338733616, -0.00865827812567943, -0.006008091105513813, -0.0038079376431738865, -0.002066913031569584, -0.0007943846508027264, 0.0, 0.00030630551464128075, 0.00011430112178345553, -0.000586546187932413, -0.001807077799611534, -0.0035584485342923244, -0.005852130287081536, -0.00869991381740931]
tilt_x_sph = [3.2087059435245096e-05, 2.6966832002983275e-05, 2.2076967484525565e-05, 1.738718074860054e-05, 1.2866519239706575e-05, 8.483374320971082e-06, 4.205494381947827e-06, 0.0, -4.166598514272111e-06, -8.328380903245369e-06, -1.2519993596465797e-05, -1.6776622767258376e-05, -2.1133963159938242e-05, -2.562818203004037e-05, -3.029587739915924e-05]
tilt_y_sph = [-2.160214726085714e-06, -1.5991963950451609e-06, -1.1187898907554362e-06, -7.210169624310888e-07, -4.079901005326188e-07, -1.8191844943886155e-07, -4.5114268913630366e-08, 0.0, -4.9116007164417804e-08, -1.9512909938311453e-07, -4.408419102496213e-07, -7.892032693068994e-07, -1.2433196893777006e-06, -1.8064681263263205e-06, -2.4821102102706185e-06]


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
    self.freecad_model = model_intersection_plane
    # self.interacts_with_rays = False
    
  def next_ray(self, ray):
    ray2=deepcopy(ray)
    ray2.pos = ray.intersect_with(self)
    # return ray2
    return ray2
  
  # def draw_fc(self):
    # self.update_draw_dict()
    # return model_intersection_plane(**self.draw_dict)
  
  
  def spot_diagram(self, beam, aberration_analysis=False,default_diagram_size=0):
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
    point_x_red = []
    point_y_red = []
    point_x_blue = []
    point_y_blue = []
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
      if lamuda>=400e-6 and lamuda<=780e-6:
        c = cmap(1-(lamuda-400e-6)/380e-6)
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
      
      # if lamuda<0.001001:
      #   point_x_blue.append(pos_diff1)
      #   point_y_blue.append(pos_diff2)
      # if lamuda>0.001059:
      #   point_x_red.append(pos_diff1)
      #   point_y_red.append(pos_diff2)
      
    ray_middle = rays[int(len(rays)/2)]
    point_x_middle = point_x[int(len(rays)/2)]
    point_y_middle = point_y[int(len(rays)/2)]
    diff_x = [x-point_x_middle for x in point_x]
    diff_y = [y-point_y_middle for y in point_y]
    ray_lam = [ray.wavelength*1E6 for ray in rays]
    for ray in rays:
      if ray.normal[1]>1 or ray_middle.normal[1]>1:
        print(ray.normal,ray_middle.normal)
        print("whyyyyyyyyyyyyyyyyyyy")
    if ray_middle.normal[1]>1:
      ray_middle.normal[1]=1
    # for ray in rays:
    #   ray.normal = np.linalg.norm(ray.normal)
    tilt_x = [np.arcsin(ray.normal[1])-np.arcsin(ray_middle.normal[1]) for ray in rays]
    tilt_y = [np.arcsin(ray.normal[2])-np.arcsin(ray_middle.normal[2]) for ray in rays]
    if aberration_analysis:
      print("diff_x",diff_x)
      print("diff_y",diff_y)
      print("tilt_x",tilt_x)
      print("tilt_y",tilt_y)
      fs = 24
      a=plt.figure()
      # ax1=plt.subplot(5,5,7)
      a.subplots_adjust(wspace=0.5,hspace=0.5)
      ax1=plt.subplot(2,2,1)
      plt.plot(ray_lam, diff_x_sph)
      plt.plot(ray_lam, diff_x)
      plt.legend(['before movement','after movement'], fontsize=fs-6)
      ax1.tick_params(axis='x', labelsize=fs)
      ax1.tick_params(axis='y', labelsize=fs)
      ax1.set_title('(a)',x=-0.1,y=1.05,fontsize=fs)
      # x_loc = MultipleLocator(len(ray_lam)//5)
      # ax1.xaxis.set_major_locator(x_loc)
      plt.ylabel("x-shift (mm)",fontsize=fs)
      plt.xlabel("wavelength (nm)",fontsize=fs)
      # plt.title("The displacement in the x direction at " + self.name,fontsize=15)
      # plt.title("The displacement in the x direction",fontsize=fs)
      plt.axhline(0, color = 'black', linewidth = 1)
      
      # ax2=plt.subplot(5,5,9)
      ax2=plt.subplot(2,2,2)
      ax2.tick_params(axis='x', labelsize=fs)
      ax2.tick_params(axis='y', labelsize=fs)
      ax2.set_title('(b)',x=-0.1,y=1.05,fontsize=fs)
      # ax2.xaxis.set_major_locator(x_loc)
      plt.plot(ray_lam, diff_y_sph)
      plt.plot(ray_lam, diff_y)
      plt.legend(['before movement','after movement'], fontsize=fs-6)
      plt.ylabel("y-shift (mm)",fontsize=fs)
      plt.xlabel("wavelength (nm)",fontsize=fs)
      # plt.title("The displacement in the y direction at " + self.name,fontsize=15)
      # plt.title("The displacement in the y direction",fontsize=fs)
      plt.axhline(0, color = 'black', linewidth = 1)
      # ax3=plt.subplot(5,5,17)
      ax3=plt.subplot(2,2,3)
      ax3.tick_params(axis='x', labelsize=fs)
      ax3.tick_params(axis='y', labelsize=fs)
      ax3.yaxis.get_offset_text().set(size=fs)
      ax3.set_title('(c)',x=-0.1,y=1.05,fontsize=fs)
      plt.plot(ray_lam, tilt_x_sph)
      plt.plot(ray_lam, tilt_x)
      plt.legend(['before movement','after movement'], fontsize=fs-6)
      plt.ylabel("x-tilt (rad)",fontsize=fs)
      plt.xlabel("wavelength (nm)",fontsize=fs)
      # plt.title("The tilt in the x direction at " + self.name,fontsize=15)
      # plt.title("The tilt in the x direction",fontsize=fs)
      plt.axhline(0, color = 'black', linewidth = 1)
      # ax4=plt.subplot(5,5,19)
      ax4=plt.subplot(2,2,4)
      ax4.tick_params(axis='x', labelsize=fs)
      ax4.tick_params(axis='y', labelsize=fs)
      ax4.yaxis.get_offset_text().set(size=fs)
      ax4.set_title('(d)',x=-0.1,y=1.05,fontsize=fs)
      plt.plot(ray_lam, tilt_y_sph)
      plt.plot(ray_lam, tilt_y)
      plt.legend(['before movement','after movement'], fontsize=fs-6)
      plt.ylabel("y-tilt (rad)",fontsize=fs)
      plt.xlabel("wavelength (nm)",fontsize=fs)
      # plt.title("The tilt in the y direction at " + self.name,fontsize=15)
      # plt.title("The tilt in the y direction",fontsize=fs)
      plt.axhline(0, color = 'black', linewidth = 1)
    fig = plt.figure()
    ax_only = fig.add_subplot(1,1,1)
    # area = (20 * np.random.rand(37))**2
    # c = np.sqrt(area)
    fs=24
    a=plt.scatter(point_x,point_y,s=10,c=point_c)
    # xy_red = [[point_x_red[ii],point_y_red[ii]] for ii in range(-12,0,1)]
    # xy_blue = [[point_x_blue[ii],point_y_blue[ii]] for ii in range(-12,0,1)]
    # red_spot = plt.Polygon(xy_red,facecolor="red",alpha=0.5)
    # blue_spot = plt.Polygon(xy_blue,facecolor="blue",alpha=0.5)
    # ax_only.add_patch(red_spot)
    # ax_only.add_patch(blue_spot)
    plt.xticks(fontsize=fs)
    plt.yticks(fontsize=fs)
    if default_diagram_size!=0:
      plt.xlim(-default_diagram_size,default_diagram_size)
      # plt.ylim(-default_diagram_size,default_diagram_size)
      plt.ylim(-5,5)
    # plt.xlim(-0.0015,0.0015)
    # plt.ylim(-0.0015,0.0015)
    plt.xlabel("x-axis (mm)",fontsize=fs)
    plt.ylabel("y-axis (mm)",fontsize=fs)
    # plt.title("The spot diagram at " + self.name,fontsize=fs)
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