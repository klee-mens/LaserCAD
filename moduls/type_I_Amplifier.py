# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 10:56:05 2023

@author: 12816
"""

from basic_optics import Mirror, Lens, Beam, Composition, inch,Curved_Mirror
import numpy as np


def Make_Amplifier_Typ_I_simple(name = "AmpTyp1s", focal_length=600,
                                dist3=600,roundtrips2=2,
                                aperture_small=1*inch, aperture_big=2*inch, beam_sep=15):
  # Radius2 = magnification*focal_length
  dist1 =2*focal_length-dist3
  dist2 = focal_length*2
  theta = np.arctan(beam_sep/dist1) # Seperationswinkel auf Planspiegel
  beam_pos = (dist2+dist1, -dist1 * np.tan(theta* roundtrips2), 0)
  
  plane_mir2 = Mirror()
  plane_mir2.pos = (0,0,0) # der Ausgangspunkt
  plane_mir2.normal = (-1,0,0) # umgekehrte Ausrichtung des Aufbaus
  plane_mir2.aperture = aperture_small
  
  lens1 = Lens(f=focal_length)
  lens1.normal = (1,0,0) #eigentlich egal, kann auch +1,0,0 sein
  lens1.pos = (dist1,0,0) #d2 = b vom cm2 entfernt
  lens1.aperture = aperture_big
  
  lens2 = Lens(f=focal_length)
  lens2.normal = (1,0,0) #eigentlich egal, kann auch +1,0,0 sein
  lens2.pos = (dist1+dist2,0,0) #d2 = b vom cm2 entfernt
  lens2.aperture = aperture_big
  
  plane_mir1 = Mirror()
  plane_mir1.pos = (dist1*2+dist2, 0, 0)
  point1 = lens2.pos
  point0 = lens2.pos - (0, beam_sep, 0)
  # print("p1:", lens1.pos - (0, beam_sep, 0))
  plane_mir1.set_normal_with_2_points(point0, point1)
  plane_mir1.aperture = aperture_small
  
  ls = Beam(angle=0) # kollimierter Anfangsbeam
  # ls.pos = beam_pos
  # ls.normal = plane_mir.pos - beam_pos #soll direkt auch den Planspiegel zeigen

  AmpTyp1 = Composition(name=name)
  # print("geom0:", beam_pos, plane_mir.pos - beam_pos)
  AmpTyp1.pos = beam_pos
  AmpTyp1.normal = plane_mir1.pos - beam_pos
  AmpTyp1.set_light_source(ls)
  AmpTyp1.add_fixed_elm(plane_mir1)
  AmpTyp1.add_fixed_elm(lens2)
  AmpTyp1.add_fixed_elm(lens1)
  AmpTyp1.add_fixed_elm(plane_mir2)

  AmpTyp1.roundtrips = roundtrips2*2 #wird als neue Variable und nur zur Info eingefügt
  seq = [0]
  roundtrip_sequence = [1,2,3,2,1,0]
  seq.extend(roundtrip_sequence)
  for n in range(roundtrips2-1):
    seq.extend(roundtrip_sequence)
  AmpTyp1.set_sequence(seq)
  AmpTyp1.propagate(120)
  return AmpTyp1

def Make_Amplifier_Typ_I_Mirror(name = "AmpTyp1sr", focal_length=600,
                                magnification=1,roundtrips2=2,
                                aperture_small=0.5*inch, aperture_big=2*inch, beam_sep=15):
  # Radius2 = magnification*focal_length
  dist1 = (magnification+1) / (magnification**2+1) * focal_length
  dist2 = magnification * dist1 * 2
  Radius1=focal_length*2
  theta = np.arctan(beam_sep/dist1) # Seperationswinkel auf Planspiegel
  beam_pos = (dist2, -dist1 * np.tan(theta* roundtrips2), 0)
  
  plane_mir2 = Mirror()
  plane_mir2.pos = (dist1*np.cos(theta*2),dist1*np.sin(theta*2),0) # der Ausgangspunkt
  plane_mir2.normal = plane_mir2.pos # umgekehrte Ausrichtung des Aufbaus
  plane_mir2.aperture = aperture_small
  
  cm2 = Curved_Mirror(radius=Radius1)
  cm2.normal = (-np.cos(theta),-np.sin(theta),0) #eigentlich egal, kann auch +1,0,0 sein
  cm2.pos = (0,0,0) #d2 = b vom cm2 entfernt
  cm2.aperture = aperture_big
  
  cm1 = Curved_Mirror(radius=Radius1)
  cm1.normal = (np.cos(theta),np.sin(theta),0) #eigentlich egal, kann auch +1,0,0 sein
  cm1.pos = (dist2,0,0) #d2 = b vom cm2 entfernt
  cm1.aperture = aperture_big
  
  plane_mir1 = Mirror()
  plane_mir1.pos = (dist2-dist1*np.cos(theta*2), -dist1*np.sin(theta*2), 0)
  point1 = cm1.pos
  point0 = cm1.pos - (0, beam_sep, 0)
  # print("p1:", lens1.pos - (0, beam_sep, 0))
  plane_mir1.set_normal_with_2_points(point0, point1)
  plane_mir1.aperture = aperture_small
  
  ls = Beam(angle=0) # kollimierter Anfangsbeam
  # ls.pos = beam_pos
  # ls.normal = plane_mir.pos - beam_pos #soll direkt auch den Planspiegel zeigen

  AmpTyp1 = Composition(name=name)
  # print("geom0:", beam_pos, plane_mir.pos - beam_pos)
  AmpTyp1.pos = beam_pos
  AmpTyp1.normal = plane_mir1.pos - beam_pos
  AmpTyp1.set_light_source(ls)
  AmpTyp1.add_fixed_elm(plane_mir1)
  AmpTyp1.add_fixed_elm(cm1)
  AmpTyp1.add_fixed_elm(cm2)
  AmpTyp1.add_fixed_elm(plane_mir2)

  AmpTyp1.roundtrips = roundtrips2*2 #wird als neue Variable und nur zur Info eingefügt
  seq = [0]
  roundtrip_sequence = [1,2,3,2,1,0]
  seq.extend(roundtrip_sequence)
  for n in range(roundtrips2-1):
    seq.extend(roundtrip_sequence)
  AmpTyp1.set_sequence(seq)
  AmpTyp1.propagate(120)
  return AmpTyp1