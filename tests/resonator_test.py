# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 10:53:52 2023

@author: 12816
"""

from basic_optics import LinearResonator,Mirror,Lens,Curved_Mirror,Composition,Beam,Intersection_plane
import numpy as np


def simple_resonator_test():
  res = LinearResonator()
  m0 = Mirror()
  le = Lens(f=250)
  m1 = Mirror()
  res = LinearResonator()
  res.add_on_axis(m0)
  res.propagate(500)
  res.add_on_axis(le)
  res.propagate(270)
  res.add_on_axis(m1)
  res.draw()
  return res

def three_resonators_test():
  from basic_optics.resonator import LinearResonator

  res = LinearResonator(name="SimpleRes")
  g = 0.2
  L = 250
  R = L / (1-g)
  wavelength = 0.1
  res.wavelength = wavelength
  cm1 = Curved_Mirror(radius=R)
  cm2 = Curved_Mirror(radius=R)
  res.add_on_axis(cm1)
  res.propagate(L)
  res.add_on_axis(cm2)
  res.draw()


  alpha = -8
  beta = -0.1
  print("g1*g2 = ", alpha*beta)
  focal = 250
  dist1 = (1-alpha)*focal
  dist2 = (1-beta)*focal
  wavelength = 0.1
  res2 = LinearResonator(name="3ElmRes")
  res2.pos += (0,100, 0)
  mir1 = Mirror()
  mir2 = Mirror()
  le1 = Lens(f=focal)

  res2.add_on_axis(mir1)
  res2.propagate(dist1)
  res2.add_on_axis(le1)
  res2.propagate(dist2)
  res2.add_on_axis(mir2)

  q = res2.compute_eigenmode()

  print()
  print(res2.matrix())
  print()

  redu = (1-alpha*beta)*focal
  mat2 = np.array([[beta*alpha - redu/focal, 2*alpha*redu], [-2*beta/focal, beta*alpha - redu/focal]])
  print()
  print()
  print(mat2)
  print()

  res2.draw()



  res3 = LinearResonator(name="foldedRes")
  res3.pos += (0,-200, 0)

  alpha = -8
  beta = -0.1
  print("g1*g2 = ", alpha*beta)
  focal = 250
  dist1 = (1-alpha)*focal
  dist2 = (1-beta)*focal
  wavelength = 0.1
  frac1 = 0.4
  frac2 = 0.1
  frac3 = 1 - frac1 - frac2

  mir1 = Mirror(phi=180)
  mir2 = Mirror(phi=75)
  mir3 = Mirror(phi=-75)
  mir4 = Mirror(phi=180)
  cm = Curved_Mirror(radius=focal*2, phi = 170)

  res3.add_on_axis(mir1)
  res3.propagate(dist1*frac1)
  res3.add_on_axis(mir2)
  res3.propagate(dist1*frac2)
  res3.add_on_axis(mir3)
  res3.propagate(dist1*frac3)
  res3.add_on_axis(cm)
  res3.propagate(dist2)
  res3.add_on_axis(mir4)

  res3.compute_eigenmode()

  res3.draw()
  return res, res2, res3

def Lab_Resonator_test():
  inch = 25.4

  # from basic_optics.tests import three_resonators_test
  # res1,res2,res3 = three_resonators_test()
  # teles = Make_Telescope()
  # teles.draw()
  # if freecad_da:
  #   input_output_test()
  # stretcher = Make_Stretcher()
  # stretcher.pos=(0,0,100)
  # stretcher.draw_elements()
  # stretcher.draw_rays()
  # stretcher.draw()

  d1 = 317
  d2 = 126
  d3 = 285
  d4 = 384
  angle1 = (np.pi-(np.arctan(7/8)+np.arctan(3/5)))*180/np.pi
  angle_TFP = 56 * 2
  angle2 = 5
  End_Mirror1 = Mirror(phi=180)
  M1 = Mirror(phi = -(180-angle1))
  M_TFP = Mirror(phi = -(180-angle_TFP))
  M_TFP.aperture = inch
  M_TFP.draw_dict["model_type"] = "56_polarizer"
  Curved = Curved_Mirror(phi=-(180-angle2),radius=750)
  Curved.aperture = 2 * inch
  End_Mirror2 = Mirror()
  lightsourse=Beam(distribution="cone")
  lightsourse.normal = (-1,0,0)
  ip = Intersection_plane()
  ip.pos = (317.,  -0., 100.)+(0.30653, -0.95186,  0.)*500

  ip.normal = (0.30653, -0.95186,  0.)
  Comp = Composition(pos=(317,0,100),normal=(-1,0,0))
  # Comp = LinearResonator(pos= (0,0,100),normal=(-1,0,0))
  Comp.set_light_source(lightsourse)
  Comp.propagate(317)
  Comp.add_on_axis(End_Mirror1)
  Comp.propagate(d1)
  Comp.add_on_axis(M1)
  Comp.propagate(d2)
  Comp.add_on_axis(M_TFP)
  Comp.propagate(d3)
  Comp.add_on_axis(Curved)
  Comp.propagate(d4)
  Comp.add_on_axis(End_Mirror2)


  seq = np.array([0,1,2,3,4,3,2,1])
  roundtrip_sequence = list(seq)

  roundtrip=1
  for n in range(roundtrip-1):
    seq = np.append(seq,roundtrip_sequence)
  seq=np.append(seq, [0,1])
  Comp.set_sequence(seq)
  Comp.propagate(500)
  Comp.draw()
  
  return Comp

Lab_Resonator_test()