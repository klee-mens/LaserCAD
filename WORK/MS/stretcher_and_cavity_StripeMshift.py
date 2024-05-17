# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 15:21:13 2024

@author: 12816
"""

import sys
# import os

pfad = __file__
pfad = pfad.replace("\\","/") #folder conventions windows linux stuff
pfad = pfad.lower()
ind = pfad.rfind("lasercad")
pfad = pfad[0:ind-1]
if not pfad in sys.path:
  sys.path.append(pfad)
from copy import deepcopy

from LaserCAD.basic_optics import Mirror,Beam,Cylindrical_Mirror,Grating,Ray
from LaserCAD.basic_optics import Intersection_plane,Cylindrical_Mirror1
from LaserCAD.basic_optics import Curved_Mirror, Composition

from LaserCAD.basic_optics import Unit_Mount,Composed_Mount, Crystal
from LaserCAD.non_interactings import Pockels_Cell
from LaserCAD.non_interactings import Lambda_Plate

from LaserCAD.freecad_models import clear_doc, setview, add_to_composition
from LaserCAD.freecad_models import freecad_da
from LaserCAD.moduls import Make_RoofTop_Mirror, Make_Periscope
from LaserCAD.moduls.periscope import Rooftop_Mirror_Component

import matplotlib.pyplot as plt
import numpy as np

if freecad_da:
  clear_doc()

# centerlamda =1030e-9*1e3
# vertical_mat = True
# s_shift = 0
# ls="CB"
Plane_height = 150 # The height of the second floor.
# focal_length = 428.0733746200338 # The focal length of the telescope
angle =1
para_d = 10

def cavity_and_stretcher(C_radius = 7000,vertical_mat=True,want_to_draw=True,
                         roundtrip=20,centerlamda=1030e-9*1e3,s_shift=0,
                         ls="CR",seperation=150,Tele_added = True,
                         Concav_shift= [0,0,0,0],tele_shift=0):
  """
  build the stretcher and cavity.
  Parameters
  ----------
  C_radius : float
    The radius of the curvature of the Curved mirror in the resonator. 
    The default is 7000.
  vertical_mat : bool, optional
    Decide whether to calculate a horizontal or vertical matrix. 
    The default is True.
  want_to_draw : bool, optional
    Decide whether to draw the 3D model. The default is True.
  roundtrip : int, optional
    The round trips. The default is 20.
  centerlamda : float, optional
    The center wavelength. The default is 1030e-9*1e3.
  s_shift : float, optional
    The small shift of the stripe mirror at the middle of the Stretcher. 
    The default is 0.
  ls : string, optional
    The light sourse. CR is the center ray in single wavelength. CB is the 
    center beam in different wavelength. The default is "CR".
  seperation : float, optional
    The seperation length of the Stretcher. The default is 150.

  Returns
  -------
  float or matrix
    The maxium radius of the beam in vertical/horizontal direction.
    Or the ABCD matrix of the system.

  """
  Radius = 600 #Radius des großen Konkavspiegels
  Aperture_concav = 100
  h_StripeM = 10 #Höhe des Streifenspiegels
  # gamma = 33.4906043205826 /180 *np.pi
  # gamma = 18.8239722389914963 /180 *np.pi #AOI = 60
  gamma = 8.3254033412311523321136 /180 *np.pi #AOI = 54
  grat_const = 1/1480 # Gitterkonstante in 1/mm
  # seperation = 203 # Differenz zwischen Gratingposition und Radius
  focal_length = (12*300-4*seperation*(1-np.cos(54/180*np.pi)**2/np.cos(54/180*np.pi-gamma)**2))/8
  lam_mid = centerlamda # Zentralwellenlänge in mm
  lam_mid_grating = 1030E-6 # Zentralwellenlänge in mm
  delta_lamda = 60e-9*1e3 # Bandbreite in mm
  number_of_rays = 15
  safety_to_StripeM = 5 
  periscope_distance = 12
  c0 = 299792458*1000 #mm/s
  v = lam_mid_grating/grat_const
  s = np.sin(gamma)
  c = np.cos(gamma)
  a = v/2
  b = np.sqrt(a**2 - (v**2 - s**2)/(2*(1+c)))
  sinB = a - b
  # print("angle=",(gamma+np.arcsin(sinB))*180/np.pi)
  
  Ring_number = 2
  Beam_radius = 1
  lightsource = Beam(radius=0, angle=0)
  wavels = np.linspace(lam_mid-delta_lamda/2, lam_mid+delta_lamda/2, 
                       number_of_rays)
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
  wavels = np.linspace(lam_mid-delta_lamda/2, lam_mid+delta_lamda/2, 
                       number_of_rays)
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
  
  centerray = Beam(radius=0.5, angle=0,wavelength=centerlamda)
  centerray.make_cone_distribution(ray_count=13)
  for ray1 in centerray.get_all_rays():
    ray1.wavelength = centerlamda
  ray1 = Ray()
  ray1.wavelength = centerlamda#lam_mid - 15e-9*1e3
  ray1.draw_dict["color"] = cmap( 0.5 )
  rays = []
  rays.append(ray1)
  
  if vertical_mat:
    Concav1 = Cylindrical_Mirror1(radius=Radius,name="Concav_Mirror")
    Concav2 = Cylindrical_Mirror1(radius=Radius,name="Concav_Mirror")
    Concav3 = Cylindrical_Mirror1(radius=Radius,name="Concav_Mirror")
    Concav4 = Cylindrical_Mirror1(radius=Radius,name="Concav_Mirror")
    StripeM = Cylindrical_Mirror1(radius= -Radius/2, name="Stripe_Mirror")
  else:
    Concav1 = Cylindrical_Mirror(radius=Radius,name="Concav_Mirror")
    Concav2 = Cylindrical_Mirror(radius=Radius,name="Concav_Mirror")
    Concav3 = Cylindrical_Mirror(radius=Radius,name="Concav_Mirror")
    Concav4 = Cylindrical_Mirror(radius=Radius,name="Concav_Mirror")
    StripeM = Cylindrical_Mirror(radius= -Radius/2, name="Stripe_Mirror")
  Concav1.pos = (Radius/2-np.sqrt(((Radius/2+Concav_shift[0])**2)-(h_StripeM/2 + safety_to_StripeM)**2),
                 0,-h_StripeM/2 - safety_to_StripeM)
  # Concav1.pos = (0,0,-h_StripeM/2 - safety_to_StripeM)
  Concav1.aperture = Aperture_concav
  Concav1.normal = (-1,0,0)
  Concav1.draw_dict["height"]=10
  Concav1.draw_dict["thickness"]=25
  point0 = (Radius-seperation, 0, -h_StripeM/2 - safety_to_StripeM)
  point1 = (Radius/2, 0, 0)
  Concav1.set_normal_with_2_points(point0, point1)
  Concav1.draw_dict["mount_type"] = "dont_draw"
  
  StripeM.pos = (Radius/2+s_shift, 0, 0)
  StripeM.aperture=50
  StripeM.draw_dict["height"]=9
  StripeM.draw_dict["thickness"]=25
  StripeM.Mount = Composed_Mount(unit_model_list=["Stripe_mirror_mount",
                                                  "POLARIS-K2","1inch_post"])
  StripeM.Mount.set_geom(StripeM.get_geom())
  StripeM.Mount.pos += StripeM.normal*25
  
  Grat = Grating(grat_const=grat_const, name="Gitter")
  Grat.pos = (Radius-seperation, 0, 0)
  Grat.normal = (np.sqrt(1-sinB**2), -sinB, 0)
  
  Concav2.pos = (Radius/2-np.sqrt(((Radius/2+Concav_shift[1])**2)-(h_StripeM/2 + safety_to_StripeM)**2), 
                 0, h_StripeM/2 + safety_to_StripeM)
  Concav2.aperture = Aperture_concav
  Concav2.normal = (-1,0,0)
  Concav2.draw_dict["height"]=10
  Concav2.draw_dict["thickness"]=25
  point0 = (Radius-seperation, 0, h_StripeM/2 + safety_to_StripeM)
  point1 = (Radius/2, 0, 0)
  Concav2.set_normal_with_2_points(point0, point1)
  Concav2.draw_dict["mount_type"] = "dont_draw"
  Concav3.pos = (Radius/2-np.sqrt(((Radius/2+Concav_shift[2])**2)-(h_StripeM/2 + safety_to_StripeM+periscope_distance)**2), 
                 0, h_StripeM/2 + safety_to_StripeM + periscope_distance)
  Concav3.aperture = Aperture_concav
  Concav3.normal = (-1,0,0)
  Concav3.draw_dict["height"]=10
  Concav3.draw_dict["thickness"]=25
  point0 = (Radius-seperation, 0, h_StripeM/2 + safety_to_StripeM + periscope_distance)
  point1 = (Radius/2, 0, 0)
  Concav3.set_normal_with_2_points(point0, point1)
  Concav3.draw_dict["mount_type"] = "dont_draw"
  Concav4.pos = (Radius/2-np.sqrt(((Radius/2+Concav_shift[3])**2)-(h_StripeM/2 + safety_to_StripeM+periscope_distance)**2), 
                 0, -h_StripeM/2 - safety_to_StripeM - periscope_distance)
  Concav4.aperture = Aperture_concav
  Concav4.normal = (-1,0,0)
  Concav4.draw_dict["height"]=10
  Concav4.draw_dict["thickness"]=25
  point0 = (Radius-seperation, 0, -h_StripeM/2 - safety_to_StripeM - periscope_distance)
  point1 = (Radius/2, 0, 0)
  Concav4.set_normal_with_2_points(point0, point1)
  Concav4.draw_dict["mount_type"] = "dont_draw"
  ray0 = Ray()
  p_grat = np.array((Radius-seperation, 0, -h_StripeM/2 - safety_to_StripeM - periscope_distance))
  vec = np.array((c, s, 0))
  pos0 = p_grat - 250 * vec
  ray0.normal = vec
  ray0.pos = pos0
  ray0.wavelength = lam_mid
  
  nfm1 = - ray0.normal
  pfm1 = Grat.pos + 300 * nfm1 + (0,0,h_StripeM/2 + safety_to_StripeM + periscope_distance)
  
  # roof = Make_RoofTop_Mirror(height=periscope_distance,up=False)
  roof = Make_Periscope(height=periscope_distance, up=False, backwards=True)
  roof.height = periscope_distance # just for the records
  m1, m2 = roof._elements
  m1.invisible = True
  m2.invisible = True
  roof.pos = pfm1
  roof.normal = nfm1
  pure_cosmetic = Rooftop_Mirror_Component(name="RoofTop_Mirror",aperture=periscope_distance)
  pure_cosmetic.pos = (m1.pos+m2.pos)/2
  pure_cosmetic.normal = (m1.normal+m2.normal)/2
  pure_cosmetic.draw_dict["model_type"] = "Rooftop"
  pure_cosmetic.Mount= Unit_Mount("dont_draw")
  pure_cosmetic.draw_dict["length"] = 28
  pure_cosmetic.draw_dict["l_height"] = 15
  
  
  Stretcher = Composition()
  Stretcher.pos = pos0
  Stretcher.normal = -nfm1
  if ls == "CB":
    Stretcher.set_light_source(centerlightsource)
  elif ls == "CR":
    Stretcher.set_light_source(centerray)
  else:
    Stretcher.set_light_source(lightsource)
  
  Stretcher.add_fixed_elm(Grat)#0
  Stretcher.add_fixed_elm(Concav4)#1
  Stretcher.add_fixed_elm(StripeM)#2
  Stretcher.add_fixed_elm(Concav3)#3
  Stretcher.add_supcomposition_fixed(roof) #4,5
  Stretcher.add_fixed_elm(Concav2)#6
  Stretcher.add_fixed_elm(Concav1)#7
  # Stretcher.add_fixed_elm(pure_cosmetic)#8
  seq = [0,1,2,3,0,4,5,0,6,2,7,0]
  Stretcher.set_sequence(seq)
  Stretcher.recompute_optical_axis()
  Stretcher.propagate(250+44)
  
  Stretcher.pos += (0,0,Plane_height+100)
  for ii in Stretcher._elements:
    if type(ii.Mount) != Unit_Mount:
      ii.Mount.mount_list[-1]._lower_limit = Plane_height
  
# =============================================================================
#   telescope
# =============================================================================
  
  Tele = Composition()
  Tele.set_light_source(Beam())
  Tele_M1 = Mirror()
  Tele_M1.pos = (120,0,80)
  Tele_M1.normal = (1,-1,0)
  Tele_M1.aperture = 25.4/2
  Tele_M1.set_mount_to_default()
  if Tele_added:
    if vertical_mat:  
      Tele_CM1 = Cylindrical_Mirror(radius=focal_length*2,height=20,thickness=10)
      Tele_CM2 = Cylindrical_Mirror(radius=focal_length*2,height=20,thickness=10)
    else:
      Tele_CM1 = Cylindrical_Mirror1(radius=focal_length*2,height=20,thickness=10)
      Tele_CM2 = Cylindrical_Mirror1(radius=focal_length*2,height=20,thickness=10)    
  else:
    Tele_CM1 = Mirror()
    Tele_CM2 = Mirror()
  Tele_CM1.pos = (120+para_d/2,focal_length/2,80)
  Tele_CM1.normal = (0,1,0)
  Tele_CM1.rotate((1,0,0), -angle/180*np.pi)
  Tele_CM2.pos = (120+para_d/2,(focal_length*2+tele_shift)*(1-np.cos(angle*2/180*np.pi))-3/2*focal_length,
                  np.sin(angle*2/180*np.pi)*(focal_length*2+tele_shift)+80)
  Tele_CM2.normal = (0,-1,0)
  Tele_CM2.rotate((1,0,0), -angle/180*np.pi)
  Tele_CM1.rotate(Tele_CM1.normal, np.pi/2)
  Tele_CM2.rotate(Tele_CM2.normal, np.pi/2)
  Tele_CM1.aperture = Tele_CM2.aperture = 30

  Tele_pm1 = Mirror()
  Tele_pm2 = Mirror()
  Tele_pm1.pos = Tele_CM2.pos + (-para_d/2,focal_length/2-para_d/2,0)
  Tele_pm1.normal = (-1,1,0)
  Tele_pm2.pos = Tele_pm1.pos + (para_d,0,0)
  Tele_pm2.normal = (1,1,0)
  Tele_pm2.invisible = True
  Tele_pm1.invisible = True

  Tele_M2 = Mirror()
  Tele_M2.pos = (120+para_d,0,80)
  Tele_M2.normal = (-1,-1,0)
  Tele_M2.aperture = 25.4/2
  
  Tele_M1.invisible = Tele_M2.invisible = True
  Tele_pm2.Mount = Tele_pm1.Mount = Tele_M1.Mount = Tele_M2.Mount = Unit_Mount("dont_draw")
  Tele.add_fixed_elm(Tele_M1)
  Tele.add_fixed_elm(Tele_CM1)
  Tele.add_fixed_elm(Tele_CM2)
  Tele.add_fixed_elm(Tele_pm1)
  Tele.add_fixed_elm(Tele_pm2)
  Tele.add_fixed_elm(Tele_M2)
  # Tele.add_fixed_elm(pure_cosmetic2)
  # Tele.add_fixed_elm(pure_cosmetic1)
  Tele.set_sequence([0,1,2,3,4,2,1,5])
  Tele.recompute_optical_axis()
  Tele.propagate(10)
  
  
# =============================================================================
# Amplifler
# =============================================================================
  d_TFP1_Lam1 = 200
  d_lam1_PC =50
  d_PC_TFP2 = 150
  a_TFP = 50
  d_TFP2_M1 = 150
  d_M1_CM = 620
  R_CM = C_radius
  d_CM_M2 = 300
  d_M2_M3 = 515
  d_M2_p = 200
  d_p = d_M2_M3-d_M2_p*2
  d_M3_Crys = 300
  
  Amp = Composition()
  Amp.set_light_source(Beam())
  Amp.propagate(100)
  TFP1= Mirror(phi=a_TFP)
  TFP1.pos = (50,0,80)
  TFP1.normal = -TFP1.normal
  # TFP1.Mount = Composed_Mount(["65_degree_mounts","POLARIS-K1","1inch_post"])
  # TFP1.Mount.set_geom(TFP1.get_geom())
  Amp.propagate(d_TFP1_Lam1)
  Lam1 = Lambda_Plate()
  Amp.add_on_axis(Lam1)
  Amp.propagate(d_lam1_PC)
  PC = Pockels_Cell()
  Amp.add_on_axis(PC)
  PC.rotate(vec=PC.normal, phi=np.pi)
  Amp.propagate(d_PC_TFP2)
  TFP2 = Mirror(phi=-a_TFP)
  TFP2.Mount = Composed_Mount(["56_degree_mounts","POLARIS-K1","1inch_post"])
  TFP2.Mount.set_geom(TFP2.get_geom())
  Amp.add_on_axis(TFP2) #0
  Amp.propagate(d_TFP2_M1)
  M1 = Mirror(phi=-(180-2*a_TFP))
  Amp.add_on_axis(M1) #1
  Amp.propagate(d_M1_CM)
  CM = Curved_Mirror(phi=178,radius=R_CM)
  Amp.add_on_axis(CM) #2
  Amp.propagate(d_CM_M2)
  M2 = Mirror(phi = 92)
  M2.Mount = Composed_Mount(unit_model_list=["MH25_KMSS","1inch_post"])
  M2.Mount.set_geom(M2.get_geom())
  Amp.add_on_axis(M2) #3
  Amp.propagate(d_M2_p)
  Amp.recompute_optical_axis()
  peri_geom = Amp.last_geom()
  peri1 = Mirror()
  peri1.set_geom(peri_geom)
  Amp.propagate(d_p)
  peri4 = Mirror()
  peri4.set_geom(Amp.last_geom())
  Amp.propagate(d_M2_p)
  M3 = Mirror(phi = 92)
  Amp.add_on_axis(M3) #8
  M3.Mount = Composed_Mount(unit_model_list=["MH25_KMSS","1inch_post"])
  M3.Mount.set_geom(M3.get_geom())
  Crys = Crystal(width=7.5,model="round",thickness=12.5,n=1.5)
  Amp.propagate(d_M3_Crys)
  Amp.add_on_axis(Crys) #9
  Amp.propagate(15)
  Amp.recompute_optical_axis()
  M4 = Mirror()
  M4.pos = Amp.last_geom()[0]
  p0 = M3.pos
  p1 = TFP1.pos 
  M4.set_normal_with_2_points(p0, p1)
  p0 = TFP2.pos
  p1 = M4.pos 
  TFP1.set_normal_with_2_points(p0, p1)
  Amp.add_fixed_elm(M4) #10
  Amp.add_fixed_elm(TFP1) #11
  seq = np.array([0,1,2,3])
  # seq = np.append(seq,list(np.array([4,5,6,7,8,10,11])))
  seq = np.append(seq,list(np.array([4,6,7])))
  Amp.set_sequence(seq)
  Amp.propagate(500)
  Stretcher.set_geom(peri_geom)
  Stretcher.pos += (0,0,Plane_height)
  Stretcher.normal = -Stretcher.normal
  
  peri2 = Mirror()
  peri2.aperture = 25.4/2
  peri2.set_geom(Stretcher.get_geom())
  peri3 = Mirror()
  peri3.pos = peri4.pos +(0,0,Plane_height+12)
  # peri3.pos = Stretcher.last_geom()[0]
  
  Tele.set_geom(Stretcher.get_geom())
  Tele.normal = -Tele.normal
  Tele.pos += (0,0,12)
  Tele.pos -=  100 * Tele.normal
  
  pure_cosmetic2 = Rooftop_Mirror_Component(name="RoofTop_Mirror",aperture=5)
  pure_cosmetic2.pos = (Tele_pm1.pos+Tele_pm2.pos)/2
  pure_cosmetic2.normal = (Tele_pm1.normal+Tele_pm2.normal)/2
  pure_cosmetic2.draw_dict["model_type"] = "Rooftop"
  pure_cosmetic2.Mount= Unit_Mount("dont_draw")
  pure_cosmetic2.draw_dict["length"] = 15
  pure_cosmetic2.draw_dict["l_height"] = 15
  pure_cosmetic2.draw_dict["rotate90"] =True
  
  pure_cosmetic1 = Rooftop_Mirror_Component(name="RoofTop_Mirror",aperture=5)
  pure_cosmetic1.pos = (Tele_M1.pos+Tele_M2.pos)/2
  pure_cosmetic1.normal = -(Tele_M1.normal+Tele_M2.normal)/2
  pure_cosmetic1.draw_dict["model_type"] = "Rooftop"
  pure_cosmetic1.Mount= Unit_Mount("dont_draw")
  pure_cosmetic1.draw_dict["length"] = 15
  pure_cosmetic1.draw_dict["l_height"] = 15
  pure_cosmetic1.draw_dict["rotate90"] =True
  
  # pure_cosmetic2.draw()
  # pure_cosmetic1.draw()
  
  p0=M2.pos
  p1=peri2.pos
  peri1.set_normal_with_2_points(p0, p1)
  p0=peri1.pos 
  p1=Grat.pos +(0, 0, -h_StripeM/2 - safety_to_StripeM - periscope_distance)
  peri2.set_normal_with_2_points(p0, p1)
  p0 = Grat.pos + (0, 0, -h_StripeM/2 - safety_to_StripeM)
  p1 = peri4.pos
  peri3.set_normal_with_2_points(p0, p1)
  p0 = peri3.pos
  p1 = M3.pos
  peri4.set_normal_with_2_points(p0, p1)
  peri1.Mount = peri2.Mount = peri3.Mount = peri4.Mount = Unit_Mount("dont_draw")
  # Amp.draw()
  # Stretcher.draw()
  # peri1.draw()
  # peri2.draw()
  # peri3.draw()
  # peri4.draw()
  
  Comp= Composition()
  if ls == "CB":
    Comp.set_light_source(centerlightsource)
  elif ls == "CR":
    Comp.set_light_source(centerray)
  else:
    Comp.set_light_source(lightsource)
  Comp.add_fixed_elm(Lam1)
  Comp.add_fixed_elm(PC)
  Comp.add_fixed_elm(TFP2) #0
  Comp.add_fixed_elm(M1) #1
  Comp.add_fixed_elm(CM) #2
  Comp.add_fixed_elm(M2) #3
  Comp.add_fixed_elm(peri1) #4
  Comp.add_fixed_elm(peri2) #5
  for element in Stretcher._elements:
    Comp.add_fixed_elm(element) #6-13
  for element in Tele._elements:
    Comp.add_fixed_elm(element) #14-19
  Comp.add_fixed_elm(peri3) #20
  Comp.add_fixed_elm(peri4) #21
  Comp.add_fixed_elm(M3) #22
  Comp.add_fixed_elm(Crys) #23
  Comp.add_fixed_elm(M4) #24
  Comp.add_fixed_elm(TFP1) #25
  pure_cosmetic.pos = (m1.pos+m2.pos)/2
  pure_cosmetic.normal = (m1.normal+m2.normal)/2
  ip = Intersection_plane()
  ip.pos = Comp.pos + (600,0,0)
  Comp.add_fixed_elm(ip) #26
  Comp.add_fixed_elm(pure_cosmetic) #27
  Comp.add_fixed_elm(pure_cosmetic1) #28
  Comp.add_fixed_elm(pure_cosmetic2) #29
  seq = [0,1,2,3,4,5, 6,7,8,9,6,10,11,6,12,8,13,6,14,15,16,17,18,16,15,19, 
         20,21,22,24,25,26]
  seq1 = deepcopy(seq)
  roundtrip_sequence = (list(seq1))
  for n in range(roundtrip-1):
    seq = np.append(seq,roundtrip_sequence)
  
  Comp.set_sequence(seq)
  # Comp.recompute_optical_axis()
  Comp.propagate(0.1)
  if want_to_draw:
    Comp.draw_mounts()  
    Comp.draw_elements()
  else:
    Comp._beams_part = []
  Comp.compute_beams()
  if want_to_draw:
    container = []
    for n in range(-33,1):
    # for n in range(-19,1):
      beam = Comp._beams[n]
      beam.draw_dict["model"] = "ray_group"
      obj = beam.draw()
      container.append(obj)
    if freecad_da:
      part = add_to_composition(Comp._beams_part, container)
    else:
      for x in container:
        Comp._beams_part.append(x)
  # print(Comp._beams[-5].normal)
  if Comp._lightsource == centerray:
    ip_stripe = Intersection_plane()
    ip_stripe.set_geom(StripeM.get_geom())
    rays_0 = Comp._beams[-25].get_all_rays()
    for ray in Comp._beams[-24].get_all_rays():
      rays_0.append(ray)
    for ray in Comp._beams[-18].get_all_rays():
      rays_0.append(ray)
    for ray in Comp._beams[-17].get_all_rays():
      rays_0.append(ray)
    B0 = Beam()
    B0.override_rays(rays_0)
    ip_stripe.spot_diagram(B0,aberration_analysis=False)
    # ip_stripe.spot_diagram(Comp._beams[-25],aberration_analysis=False)
    # ip_stripe.spot_diagram(Comp._beams[-24],aberration_analysis=False)
    # ip_stripe.spot_diagram(Comp._beams[-18],aberration_analysis=False)
    # ip_stripe.spot_diagram(Comp._beams[-17],aberration_analysis=False)
    ip_stripe.draw()
    diff = []
    diff_out = []
    diff_hor = []
    roundtrip_group = []
    max_diff = 0
    for n in range(0,32*roundtrip+1,32):
      beam = Comp._beams[n]
      rayss=beam.get_all_rays()
      intersection_point_ver = beam.get_all_rays()[1].intersection(ip)
      intersection_point_inner = beam.get_all_rays()[0].intersection(ip)
      intersection_point_hor = beam.get_all_rays()[4].intersection(ip)
      diff_new = intersection_point_ver - ip.pos
      diff_R_ver = np.sqrt(diff_new[1]**2+diff_new[2]**2)
      diff_out.append(diff_R_ver)
      diff_new = intersection_point_inner - ip.pos
      diff_R = np.sqrt(diff_new[1]**2+diff_new[2]**2)
      diff.append(diff_R)
      diff_new = intersection_point_hor - ip.pos
      diff_R_hor = np.sqrt(diff_new[1]**2+diff_new[2]**2)
      diff_hor.append(diff_R_hor)
      roundtrip_group.append(n//32+1)
      if max_diff<diff_R_ver: #and n>roundtrip/2:
        max_diff = diff_R_ver
        max_roundtrip = n//32+1
    
    return max_diff
  elif Comp._lightsource == centerlightsource:
    # ip.spot_diagram(Comp._beams[-1],aberration_analysis=False)
    rays_end = Comp._beams[-1].get_all_rays()
    max_pos_diff = 0
    pos_diff = []
    for point_i in rays_end:
      intersection_point = point_i.intersection(ip)
      # print(intersection_point)
      # pos_diff = intersection_point - ip.pos
      pos_diff.append(intersection_point)
    # print(pos_diff)
    pos_center = pos_diff[int(len(pos_diff)/2)]
    # for ii in pos_diff:
    #   for jj in pos_diff:
    #     if max_pos_diff < np.linalg.norm(ii-jj):
    #       max_pos_diff = np.linalg.norm(ii-jj)
    leftii = rightii = pos_center[1]
    for ii in pos_diff:
      if leftii > ii[1]:
        leftii = ii[1]
      if rightii < ii[1]:
        rightii = ii[1]
    #     a = ii-pos_center
    # print(a)
    max_pos_diff=abs(leftii-rightii)
    return (max_pos_diff)

  else:
    ip.spot_diagram(Comp._beams[-1],aberration_analysis=False)
    ip_stripe = Intersection_plane()
    ip_stripe.set_geom(StripeM.get_geom())
    rays_0 = Comp._beams[-25].get_all_rays()
    for ray in Comp._beams[-24].get_all_rays():
      rays_0.append(ray)
    for ray in Comp._beams[-18].get_all_rays():
      rays_0.append(ray)
    for ray in Comp._beams[-17].get_all_rays():
      rays_0.append(ray)
    B0 = Beam()
    B0.override_rays(rays_0)
    ip_stripe.spot_diagram(B0,aberration_analysis=False,default_diagram_size=22)
    ip_stripe.draw()
    # print(ip_stripe.get_geom())
  if freecad_da:
    setview()
  return Cal_matrix(Comp=Comp,vertical_mat=vertical_mat)

def Cal_matrix(Comp=Composition(),vertical_mat = True):
  """
  computes the optical matrix of the system
  each iteration consists of a propagation given by the length of the nth
  ray of the optical_axis followed by the matrix multiplication with the
  seq[n] element

  Returns the ABCD-matrix
  """
  Comp._matrix = np.eye(2)
  counter = -1
  a=0
  for ind in Comp._sequence:
    counter += 1
    B = Comp._beams[counter].get_all_rays()[0].length
    a+=B
    M = Comp._elements[ind]._matrix
    # print(counter)
    # print(B)
    if type(Comp._elements[ind]) == Grating:
      if not vertical_mat:
        M = Comp._elements[ind].matrix(inray=Comp._beams[counter].get_all_rays()[0])
      else:
        M = np.eye(2)
      # print(M)
    Comp._matrix = np.matmul(np.array([[1,B], [0,1]]), Comp._matrix )
    Comp._matrix = np.matmul(M, Comp._matrix )
    # print(Comp._matrix)
    # print("--")
  # Comp._matrix = np.matmul(np.array([[1,Comp._last_prop], [0,1]]), Comp._matrix ) #last propagation
  return np.array(Comp._matrix)

roundtrip = 1
centerlamda = 1030E-6
C_radius = 7000
# StripeM_shift = 0.07
# StripeM_shift = 0.13
StripeM_shift = 0
# StripeM_shift = 0.115
# CB=CenterBeam CR=CenterRay B=Beamwithradius
ls = "CB"
min_Concav_shift = []
min_spot = 10
# ii_test = [-0.4,-0.35,-0.3]
# jj_test = [-0.2,-0.15,-0.1]
# kk_test = [-0.1,-0.05, 0  ]
# ll_test = [-0.4,-0.35,-0.3]
loop = [-0.1,-0.05,0,0.05,0.1]
# for ii in range(-10,10,1):
#   for jj in range(-10,10,1):
#     for kk in range(-10,10,1):
#       for ll in range(-10,10,1):
for ii in loop:
  for jj in loop:
    for kk in loop:
      for ll in loop:
        Concav_shift = [ii,jj,kk,ll]
        mat1 = cavity_and_stretcher(C_radius=C_radius,vertical_mat=True,want_to_draw=False,
                                    roundtrip=roundtrip,centerlamda=centerlamda,
                                    s_shift=StripeM_shift,ls=ls,seperation=71.381485,
                                    Tele_added = True,Concav_shift=Concav_shift)
        if min_spot>mat1:
          min_spot = mat1
          min_Concav_shift=Concav_shift
print(min_spot,min_Concav_shift)
# [-0.3, -0.1, 0, -0.3]
# [-0.35, -0.2, 0, -0.4]
min_tele_shift = 0
# min_spot = 10
# for ii in range(-500,-490,1):
#   mat1 = cavity_and_stretcher(C_radius=C_radius,vertical_mat=True,want_to_draw=False,
#                               roundtrip=roundtrip,centerlamda=centerlamda,
#                               s_shift=StripeM_shift,ls=ls,seperation=71.38147,
#                               Tele_added = True,Concav_shift=[-0.1, -0.05, 0.05, -0.1],tele_shift=ii/10)
#   if min_spot>mat1:
#     min_spot = mat1
#     min_tele_shift = ii/10
# print(min_spot,min_tele_shift)

# mat1 = cavity_and_stretcher(C_radius=C_radius,vertical_mat=True,want_to_draw=False,
#                             roundtrip=roundtrip,centerlamda=centerlamda,
#                             s_shift=StripeM_shift,ls=ls,seperation=71.381485,
#                             Tele_added = True,
#                             Concav_shift=[-0.1, -0.05, 0.05, -0.1],tele_shift=-0)
# print(mat1)
# [-0.1, -0.05, 0.05, -0.1]