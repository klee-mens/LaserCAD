# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 09:43:43 2023

@author: He
"""

import sys
import os

# pfad = __file__
# pfad = pfad.replace("\\", "/") #just in case
# ind = pfad.rfind("/")
# pfad = pfad[0:ind]
# ind = pfad.rfind("/")
# pfad = pfad[0:ind+1]
# path_added = False
# for path in sys.path:
#   if path ==pfad:
#     path_added = True
# if not path_added:
#   sys.path.append(pfad)
sys.path.append('C:\\Program Files\\Spyder\\pkgs')
from LaserCAD import basic_optics

from LaserCAD.basic_optics import Mirror,Beam,Cylindrical_Mirror,Intersection_plane,Cylindrical_Mirror1,Curved_Mirror,Ray, Composition, Grating
from LaserCAD.non_interactings import Lambda_Plate

from LaserCAD.freecad_models import clear_doc, setview, freecad_da,add_to_composition

# from basic_optics.mirror import curved_mirror_test
import matplotlib.pyplot as plt

import numpy as np
# from copy import deepcopy

if freecad_da:
  clear_doc()

# from basic_optics.tests import Intersection_plane_spot_diagram_test
def cavity_and_stretcher(C_radius = 8000,vertical_mat=True,want_to_draw=True,roundtrip=1,centerlamda=1030e-9*1e3,s_shift=0,ls="CR"):
  Radius = 600 #Radius des großen Konkavspiegels
  Aperture_concav = 6*25.4
  h_StripeM = 10 #Höhe des Streifenspiegels
  # gamma = 33.4906043205826 /180 *np.pi # Seperationswinkel zwischen einfallenden und Mittelpunktsstrahl; Alpha = Gamma + Beta
  gamma = 18.8239722389914963 /180 *np.pi #AOI = 60
  # gamma = 8.3254033412311523321136 /180 *np.pi #AOI = 54
  grat_const = 1/1480 # Gitterkonstante in 1/mm
  seperation = 50 # Differenz zwischen Gratingposition und Radius
  lam_mid = 1030e-9 * 1e3 # Zentralwellenlänge in mm
  delta_lamda = 60e-9*1e3 # Bandbreite in mm
  number_of_rays = 15
  safety_to_StripeM = 5 #Abstand der eingehenden Strahlen zum Concav Spiegel in mm
  periscope_distance = 12
  c0 = 299792458*1000 #mm/s

  # abgeleitete Parameter
  v = lam_mid/grat_const
  s = np.sin(gamma)
  c = np.cos(gamma)
  a = v/2
  b = np.sqrt(a**2 - (v**2 - s**2)/(2*(1+c)))
  sinB = a - b
  # print("angle=",(gamma+np.arcsin(sinB))*180/np.pi)

  Concav = Curved_Mirror(radius=Radius, name="Concav_Mirror")
  Concav.pos = (0,0,0)
  Concav.aperture = Aperture_concav
  Concav.normal = (-1,0,0)

  StripeM = Curved_Mirror(radius= -Radius/2, name="Stripe_Mirror")
  # StripeM.pos = (Radius/2-0.155, 0, 0)
  StripeM.pos = (Radius/2+s_shift, 0, 0)
  StripeM.aperture=75
  StripeM.draw_dict["height"]=h_StripeM
  StripeM.draw_dict["thickness"]=25
  StripeM.draw_dict["model_type"]="Stripe"

  Grat = Grating(grat_const=grat_const, name="Gitter")
  Grat.pos = (Radius-seperation, 0, 0)
  Grat.normal = (np.sqrt(1-sinB**2), -sinB, 0)
  
  ray0 = Ray()
  p_grat = np.array((Radius-seperation, 0, -h_StripeM/2 - safety_to_StripeM - periscope_distance))
  vec = np.array((c, s, 0))
  pos0 = p_grat - 250 * vec
  ray0.normal = vec
  ray0.pos = pos0
  ray0.wavelength = lam_mid
  
  Ring_number = 2
  Beam_radius = 1
  lightsource = Beam(radius=0, angle=0)
  wavels = np.linspace(lam_mid-delta_lamda/2, lam_mid+delta_lamda/2, number_of_rays)
  rays = []
  cmap = plt.cm.gist_rainbow
  for wavel in wavels:
    rn = Ray()
    # rn.normal = vec
    # rn.pos = pos0
    rn.wavelength = wavel
    x = 1-(wavel - lam_mid + delta_lamda/2) / delta_lamda
    rn.draw_dict["color"] = cmap( x )
    rg = Beam(radius=Beam_radius, angle=0,wavelength=wavel)
    rg.make_circular_distribution(ring_number=Ring_number)
    for ray_number in range(0,rg._ray_count):
      rn = rg.get_all_rays()[ray_number]
      rn.draw_dict["color"] = cmap( x )
      rays.append(rn)
  lightsource.override_rays(rays)
  lightsource.draw_dict['model'] = "ray_group"
  
  centerlightsource = Beam(radius=0, angle=0)
  wavels = np.linspace(lam_mid-delta_lamda/2, lam_mid+delta_lamda/2, number_of_rays)
  rays = []
  cmap = plt.cm.gist_rainbow
  for wavel in wavels:
    rn = Ray()
    rn.wavelength = wavel
    x = 1-(wavel - lam_mid + delta_lamda/2) / delta_lamda
    rn.draw_dict["color"] = cmap( x )
    # print(wavel,x,cmap( x ))
    rays.append(rn)
  centerlightsource.override_rays(rays)
  centerlightsource.draw_dict['model'] = "ray_group"
  
  centerray = Beam(radius=0, angle=0)
  ray1 = Ray()
  ray1.wavelength = centerlamda#lam_mid - 15e-9*1e3
  # ray1.wavelength = lam_mid + delta_lamda/2
  ray1.draw_dict["color"] = cmap( 0.5 )
  rays = []
  rays.append(ray1)
  centerray.override_rays(rays)
  centerray.draw_dict['model'] = "ray_group"
  
  nfm1 = - ray0.normal
  pfm1 = Grat.pos + 600 * nfm1 + (0,0,h_StripeM/2 + safety_to_StripeM + periscope_distance)
  flip_mirror1 = Mirror()
  flip_mirror1.pos = pfm1
  flip_mirror1.normal = nfm1 - np.array((0,0,-1))
  def useless():
    return None
  flip_mirror1.draw = useless
  flip_mirror1.draw_dict["mount_type"] = "dont_draw"
  flip_mirror2 = Mirror()
  flip_mirror2.pos = pfm1 - np.array((0,0,periscope_distance))
  flip_mirror2.normal = nfm1 - np.array((0,0,1))
  flip_mirror2.draw = useless
  flip_mirror2.draw_dict["mount_type"] = "dont_draw"
  pure_cosmetic = Mirror(name="RoofTop_Mirror")
  pure_cosmetic.draw_dict["model_type"]="Rooftop"
  pure_cosmetic.draw_dict["mount_type"] = "rooftop_mirror_mount"
  pure_cosmetic.pos = (flip_mirror1.pos + flip_mirror2.pos ) / 2
  pure_cosmetic.normal = (flip_mirror1.normal + flip_mirror2.normal ) / 2
  pure_cosmetic.aperture = periscope_distance
  
  Stretcher_M1 = Mirror(pos = pos0)
  p0 = Stretcher_M1.pos - (500,0,0)
  point0 = p0
  p1 = p_grat
  Stretcher_M1.set_normal_with_2_points(p0, p1)
  Stretcher_M1.aperture = 25.4/2
  Stretcher_M0 = Mirror()
  Stretcher_M0.pos = (-150, Stretcher_M1.pos[1],Stretcher_M1.pos[2])
  p0 = Stretcher_M1.pos
  p1 = Stretcher_M0.pos - (0,200,0)
  Stretcher_M0.set_normal_with_2_points(p0, p1)
  TFP2 = Mirror()
  TFP2.draw_dict["model_type"] = "45_polarizer"
  TFP2.pos = (-150,-300,Stretcher_M1.pos[2])
  p0 = Stretcher_M0.pos
  p1 = TFP2.pos - (100,0,0)
  point1 =p1
  TFP2.set_normal_with_2_points(p0, p1)
  Lam_Plane2=Lambda_Plate(pos=TFP2.pos-(50,0,0))
  Stretcher_M2 = Mirror(pos = p_grat - vec*500 + (0,0,periscope_distance))
  p0 = Stretcher_M2.pos + (250,0,0)
  p1 = p_grat + (0,0,periscope_distance)
  Stretcher_M2.aperture = 25.4/2
  Stretcher_M2.set_normal_with_2_points(p0, p1)
  
  TFP1 = Mirror(pos=p0)
  TFP1.normal = (-1,1,0)
  TFP1.draw_dict["model_type"] = "45_polarizer"
  TFP1.draw_dict["thickness"] = 2
  Lam_Plane1=Lambda_Plate(pos=TFP1.pos+(50,0,0))
  if vertical_mat:
    Matrix_fixing_Mirror1 = Cylindrical_Mirror(radius=Radius*3/2,pos=p0+(600,0,-10))
  else:
    Matrix_fixing_Mirror1 = Cylindrical_Mirror1(radius=Radius*3/2,pos=p0+(600,0,-10))
  # Matrix_fixing_Mirror1 = Mirror(pos=p0+(600,0,0))
  Matrix_fixing_Mirror1.normal=(1,0,0)
  Matrix_fixing_Mirror1.rotate((1,0,0), np.pi/2)
  # Matrix_fixing_Mirror2 = Mirror(pos=Matrix_fixing_Mirror1.pos-(Radius*3/4-0.083,0,11))
  Matrix_fixing_Mirror2 = Mirror(pos=Matrix_fixing_Mirror1.pos-(Radius*3/4,0,9))
  Matrix_fixing_Mirror2.normal=(-1,0,0)
  Matrix_fixing_Mirror2.draw_dict["mount_type"] = "KS1"
  cavity_mirror1 = Mirror()
  cavity_mirror1.pos = TFP1.pos -(0,50,0)
  p0 = TFP1.pos
  p1 = TFP2.pos+(200,0,0)
  cavity_mirror1.set_normal_with_2_points(p0, p1)
  cavity_mirror2 = Mirror(pos=p1)
  cavity_mirror2.aperture = 25.4*2
  p0 = cavity_mirror1.pos
  p1 = TFP2.pos
  cavity_mirror2.set_normal_with_2_points(p0, p1)
  Cavity_mirror = Curved_Mirror(radius=C_radius)
  Cavity_mirror.aperture = 2*25.4
  Cavity_mirror.pos = point1
  Cavity_mirror.normal = (-1,0,0)
  
  ip = Intersection_plane(dia=100)
  # ip.pos = p_grat - vec*1000 + (0,0,periscope_distance)
  ip.pos = Matrix_fixing_Mirror2.pos
  ip.normal = (-1,0,0)
  
  Comp = Composition(name="Strecker", pos=TFP2.pos, normal=(0,1,0))#pos=TFP2.pos - (0,100,0), normal=(0,1,0))
  opt_ax = Ray(pos=TFP2.pos, normal=(0,1,0))
  # Comp = Composition(name="Strecker", pos=TFP2.pos - (0,100,0), normal=(0,1,0))
  # opt_ax = Ray(pos=TFP2.pos - (0,100,0), normal=(0,1,0))
  opt_ax.wavelength = lam_mid
  Comp.redefine_optical_axis(opt_ax)
  if ls == "CB":
    Comp.set_light_source(centerlightsource)
  elif ls == "CR":
    Comp.set_light_source(centerray)
  else:
    Comp.set_light_source(lightsource)
  # Comp.set_light_source(centerray)
  Comp.add_fixed_elm(TFP2)
  Comp.add_fixed_elm(Stretcher_M0)
  Comp.add_fixed_elm(Stretcher_M1)
  Comp.add_fixed_elm(Grat)
  Comp.add_fixed_elm(Concav)
  Comp.add_fixed_elm(StripeM)
  Comp.add_fixed_elm(flip_mirror1)
  Comp.add_fixed_elm(flip_mirror2)
  Comp.add_fixed_elm(Stretcher_M2)
  Comp.add_fixed_elm(Matrix_fixing_Mirror1)
  Comp.add_fixed_elm(Matrix_fixing_Mirror2)
  Comp.add_fixed_elm(TFP1)
  Comp.add_fixed_elm(cavity_mirror1)
  Comp.add_fixed_elm(cavity_mirror2)
  Comp.add_fixed_elm(Cavity_mirror)
  
  Comp.add_fixed_elm(ip)
  
  
  Comp.add_fixed_elm(pure_cosmetic)
  Comp.add_fixed_elm(Lam_Plane1)
  Comp.add_fixed_elm(Lam_Plane2)
  # seq = np.array([1,2,3,4,5,6,3,7,8,3,9,5,10,3,11,12,13,12,13,12,13,12,14,15,16,17])
  # seq1 = np.array([0,1,2,3,4,5,6,3,7,8,3,9,5,10,3,11,12,13,12,13,12,13,12,14,15,16,17])
  seq = np.array([1,2,3,4,5,4,3,6,7,3,4,5,4,3,8,9,10,9,10,9,10,9,11,12,13,14])
  seq1 = np.array([0,1,2,3,4,5,4,3,6,7,3,4,5,4,3,8,9,10,9,10,9,10,9,11,12,13,14])
  
  roundtrip_sequence = list(seq1)
  # if freecad_da:
  #   obj = model_table()
  
  # roundtrip=1
  # seq = np.repeat(roundtrip_sequence, roundtrip)
  for n in range(roundtrip-1):
    # print("step ", n, "of", roundtrip)
    seq = np.append(seq,roundtrip_sequence)
    
  seq=np.append(seq, [18])
  
  Comp.set_sequence(seq)
  Comp.propagate(100)
  Comp.pos = (0,0,100)
  if want_to_draw:
    Comp.draw_mounts()  
    Comp.draw_elements()
  else:
    Comp._beams_part = []
  Comp.compute_beams()
  # ip_test = Intersection_plane(pos=Stretcher_M2.pos,normal=vec)
  # ip_test.spot_diagram(Comp._beams[14])
  # plt.close("all")
  if want_to_draw:
    container = []
    for n in range(-28,1):
      beam = Comp._beams[n]
      beam.draw_dict["model"] = "ray_group"
      obj = beam.draw()
      container.append(obj)
    if freecad_da:
      part = add_to_composition(Comp._beams_part, container)
    else:
      for x in container:
        Comp._beams_part.append(x)
  if Comp._lightsource == centerray:
    diff = []
    roundtrip_group = []
    max_diff = 0
    max_roundtrip = 0
    for n in range(26,27*roundtrip,27):
      beam = Comp._beams[n]
      rayss=beam.get_all_rays()
      for ray in rayss:
        intersection_point =  ray.intersection(ip)
      diff_new = intersection_point - ip.pos
      diff_R = np.sqrt(diff_new[1]**2+diff_new[2]**2)
      diff.append(diff_R)
      roundtrip_group.append(n//27+1)
      if max_diff<diff_R: #and n>roundtrip/2:
        max_diff = diff_R
    print(max_diff)
    plt.figure()
    # plt.plot(roundtrip_group,diff)
    plt.scatter(roundtrip_group,diff,s=10)
    plt.ylabel("diff_radius (mm)")
    plt.xlabel("roundtrip")
    plt.show()
  elif Comp._lightsource == centerlightsource:
    ip.spot_diagram(Comp._beams[-1],aberration_analysis=True)
    pathlength = {}
    for ii in range(Comp._beams[0]._ray_count):
      wavelength = Comp._beams[0].get_all_rays()[ii].wavelength
      pathlength[wavelength] = 0
    for jj in range(len(Comp._beams)-1):
      for ii in Comp._beams[jj].get_all_rays():
        a=pathlength[ii.wavelength]
        pathlength[ii.wavelength] = a +ii.length
    ray_lam = [ray.wavelength for ray in Comp._beams[0].get_all_rays()]
    path = [pathlength[ii] for ii in ray_lam]
    path_diff = [ii-path[int(len(path)/2)] for ii in path]
    fai = [path_diff[ii]/ray_lam[ii]*2*np.pi for ii in range(len(path))]
    omega = [c0/ii*2*np.pi for ii in ray_lam]
    para = np.polyfit(omega, fai, 5)
    fai2 = [20*para[0]*ii**3+12*para[1]*ii**2+6*para[2]*ii+2*para[3] for ii in omega]
    # fai2 = [para[0]*ii**5+para[1]*ii**4+para[2]*ii**3+para[3]*ii**2+para[4]*ii+para[5] for ii in omega]
    delay_mid = path[int(len(path)/2)]/c0
    delay = [(pa/c0-delay_mid)*1E9 for pa in path]
    plt.figure()
    ax1=plt.subplot(1,2,1)
    plt.plot(ray_lam,path)
    plt.ylabel("pathlength (mm)")
    plt.xlabel("wavelength (mm)")
    plt.title("Pathlength at different wavelength")
    plt.axhline(path[int(len(path)/2)], color = 'black', linewidth = 1)
    ax2=plt.subplot(1,2,2)
    plt.plot(ray_lam,delay)
    plt.ylabel("delay (ns)")
    plt.xlabel("wavelength (mm)")
    plt.title("Delay at different wavelength")
    plt.axhline(0, color = 'black', linewidth = 1)
    plt.show()
    # plt.figure()
  else:
    ip.spot_diagram(Comp._beams[-1],aberration_analysis=False)
  if freecad_da:
    setview()
  return Cal_matrix(Comp=Comp)
  # return Comp.matrix()

def Cal_matrix(Comp=Composition()):
  """
  computes the optical matrix of the system
  each iteration consists of a propagation given by the length of the nth
  ray of the optical_axis followed by the matrix multiplication with the
  seq[n] element

  Returns the ABCD-matrix
  """
  Comp._matrix = np.eye(2)
  counter = -1
  for ind in Comp._sequence:
    counter += 1
    B = Comp._beams[counter].get_all_rays()[0].length
    M = Comp._elements[ind]._matrix
    # print(counter)
    # print(B)
    # print(M)
    Comp._matrix = np.matmul(np.array([[1,B], [0,1]]), Comp._matrix )
    Comp._matrix = np.matmul(M, Comp._matrix )
    # print(Comp._matrix)
    # print("--")
  # Comp._matrix = np.matmul(np.array([[1,Comp._last_prop], [0,1]]), Comp._matrix ) #last propagation
  return np.array(Comp._matrix)

roundtrip=1
centerlamda = 1030E-6
C_radius = 8000
StripeM_shift = -0.15
# StripeM_shift =0
# CB=CenterBeam CR=CenterRay 
ls="CB"
mat1 = cavity_and_stretcher(C_radius=C_radius,vertical_mat=True,want_to_draw=True,roundtrip=roundtrip,centerlamda=centerlamda,s_shift=StripeM_shift,ls=ls)
print(mat1)