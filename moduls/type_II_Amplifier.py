# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 10:56:05 2023

@author: 12816
"""

from .. basic_optics import Mirror, Lens, Beam, Composition, inch
from .. basic_optics import Curved_Mirror, Unit_Mount
import numpy as np


def Make_Amplifier_Typ_II_simple(name="AmpTyp2s", focal_length=600, magnification=1,
                              roundtrips2=2,
                              aperture_small=1*inch, aperture_big=2*inch, beam_sep=15):
    """
    generiert die Strahlführung eines einfachen Typ II Verstärkers mit einer Linse
    und einem gekrümmten Spiegel

    V = magnification
    f = focal_length
    a = (V+1)/V * f
    b = a*V
    f2 = V/2 * f

    Returns
    -------
    composition: Amplifier_TypII_simple


    """
    Radius2 = magnification*focal_length
    dist1 = (magnification+1) / magnification * focal_length
    dist2 = magnification * dist1
    theta = np.arctan(beam_sep/dist1) # Seperationswinkel auf Planspiegel
    beam_pos = (dist2, -dist1 * np.tan(theta* roundtrips2), 0)
    # print("Bemapos,", beam_pos)
    # Position der Lichtquelle = n*Ablenkwinkel unter dem waagerechtem Strahl

    cm2 = Curved_Mirror(radius= Radius2)
    cm2.pos = (0,0,0) # der Ausgangspunkt
    cm2.normal = (-1,0,0) # umgekehrte Ausrichtung des Aufbaus
    cm2.aperture = aperture_small
    cm2.set_mount_to_default()

    lens1 = Lens(f=focal_length)
    lens1.normal = (1,0,0) #eigentlich egal, kann auch +1,0,0 sein
    lens1.pos = (dist2,0,0) #d2 = b vom cm2 entfernt
    lens1.aperture = aperture_big
    lens1.set_mount_to_default()

    plane_mir = Mirror()
    plane_mir.pos = (dist1+dist2, 0, 0)
    point1 = lens1.pos
    point0 = lens1.pos - (0, beam_sep, 0)
    # print("p1:", lens1.pos - (0, beam_sep, 0))
    plane_mir.set_normal_with_2_points(point0, point1)
    plane_mir.aperture = aperture_small
    plane_mir.set_mount_to_default()

    ls = Beam(angle=0) # kollimierter Anfangsbeam
    # ls.pos = beam_pos
    # ls.normal = plane_mir.pos - beam_pos #soll direkt auch den Planspiegel zeigen

    AmpTyp2 = Composition(name=name)
    # print("geom0:", beam_pos, plane_mir.pos - beam_pos)
    AmpTyp2.pos = beam_pos
    AmpTyp2.normal = plane_mir.pos - beam_pos
    AmpTyp2.set_light_source(ls)
    AmpTyp2.add_fixed_elm(plane_mir)
    AmpTyp2.add_fixed_elm(lens1)
    AmpTyp2.add_fixed_elm(cm2)

    AmpTyp2.roundtrips = roundtrips2*2 #wird als neue Variable und nur zur Info eingefügt
    seq = [0]
    roundtrip_sequence = [1,2,1,0]
    seq.extend(roundtrip_sequence)
    for n in range(roundtrips2-1):
      seq.extend(roundtrip_sequence)
    AmpTyp2.set_sequence(seq)
    AmpTyp2.propagate(120)
    return AmpTyp2

def Make_Amplifier_Typ_II_Mirror(name="AmpTyp2sr", focal_length=600, magnification=1,
                              roundtrips2=2,
                              aperture_small=0.5*inch, aperture_big=2*inch, beam_sep=15):

  Radius2 = magnification*focal_length
  dist1 = (magnification+1) / magnification * focal_length
  dist2 = magnification * dist1
  Radius1 = focal_length*2
  theta = np.arctan(beam_sep/dist1) # Seperationswinkel auf Planspiegel
  beam_pos = (dist2, -dist1 * np.tan(theta* roundtrips2), 0)
  # print("Bemapos,", beam_pos)
  # Position der Lichtquelle = n*Ablenkwinkel unter dem waagerechtem Strahl

  cm2 = Curved_Mirror(radius= Radius2)
  cm2.pos = (0,0,0) # der Ausgangspunkt
  cm2.normal = (-1,0,0) # umgekehrte Ausrichtung des Aufbaus
  cm2.aperture = aperture_small
  cm2.set_mount_to_default()

  cm1 = Curved_Mirror(radius= Radius1)
  cm1.pos = (dist2,0,0)
  cm1.normal = (np.cos(theta),np.sin(theta),0)
  cm1.aperture = aperture_big
  cm1.set_mount_to_default()

  plane_mir = Mirror()
  plane_mir.pos = (dist2-dist1*np.cos(theta*2), -dist1*np.sin(theta*2), 0)
  point1 = cm1.pos
  point0 = cm1.pos - (0, beam_sep, 0)
  # print("p1:", lens1.pos - (0, beam_sep, 0))
  plane_mir.set_normal_with_2_points(point0, point1)
  plane_mir.aperture = aperture_small
  plane_mir.set_mount_to_default()

  ls = Beam(angle=0) # kollimierter Anfangsbeam
  # ls.pos = beam_pos
  # ls.normal = plane_mir.pos - beam_pos #soll direkt auch den Planspiegel zeigen

  AmpTyp2 = Composition(name=name)
  # print("geom0:", beam_pos, plane_mir.pos - beam_pos)
  AmpTyp2.pos = beam_pos
  AmpTyp2.normal = plane_mir.pos - beam_pos

  # AmpTyp2.normal=np.array((AmpTyp2.normal[0],-AmpTyp2.normal[1],AmpTyp2.normal[2]))
  AmpTyp2.set_light_source(ls)
  AmpTyp2.add_fixed_elm(plane_mir)
  AmpTyp2.add_fixed_elm(cm1)
  AmpTyp2.add_fixed_elm(cm2)

  AmpTyp2.roundtrips = roundtrips2*2 #wird als neue Variable und nur zur Info eingefügt
  seq = [0]
  roundtrip_sequence = [1,2,1,0]
  seq.extend(roundtrip_sequence)
  for n in range(roundtrips2-1):
    seq.extend(roundtrip_sequence)
  AmpTyp2.set_sequence(seq)
  AmpTyp2.propagate(120)
  return AmpTyp2

def Make_Amplifier_Typ_II_UpDown(name="AmpTyp2sr", focal_length=600, magnification=1,
                              roundtrips2=2,
                              aperture_small=0.5*inch, aperture_big=2*inch, beam_sep=15):

  Radius2 = magnification*focal_length
  dist1 = (magnification+1) / magnification * focal_length
  dist2 = magnification * dist1
  Radius1 = focal_length*2
  theta = np.arctan(beam_sep/dist1) # Seperationswinkel auf Planspiegel
  beam_z = 8
  beam_pos = (dist2, -dist1 * np.tan(theta* roundtrips2), -beam_z)
  # print("Bemapos,", beam_pos)
  # Position der Lichtquelle = n*Ablenkwinkel unter dem waagerechtem Strahl

  cm2 = Curved_Mirror(radius= Radius2)
  cm2.pos = (0,0,0) # der Ausgangspunkt
  cm2.normal = (-1,0,0) # umgekehrte Ausrichtung des Aufbaus
  cm2.aperture = aperture_small
  cm2.set_mount_to_default()

  cm1 = Curved_Mirror(radius= Radius1)
  cm1.pos = (dist2,0,0)
  cm1.normal = (np.cos(theta),np.sin(theta),0)
  cm1.aperture = aperture_big
  cm1.set_mount_to_default()

  PHI = 180*theta/np.pi*(roundtrips2+1) - 180 #?
  plane_mir = Mirror(phi=PHI)
  plane_mir.pos = (dist2-dist1*np.cos(theta*2), -dist1*np.sin(theta*2), 0)
  point1 = cm1.pos
  point0 = cm1.pos - (0, beam_sep, 0)
  # print("p1:", lens1.pos - (0, beam_sep, 0))
  # plane_mir.set_normal_with_2_points(point0, point1)
  plane_mir.aperture = aperture_small
  plane_mir.set_mount_to_default()

  ls = Beam(angle=0) # kollimierter Anfangsbeam
  # ls.pos = beam_pos
  # ls.normal = plane_mir.pos - beam_pos #soll direkt auch den Planspiegel zeigen

  AmpTyp2 = Composition(name=name)
  # print("geom0:", beam_pos, plane_mir.pos - beam_pos)
  AmpTyp2.pos = beam_pos
  AmpTyp2.normal = plane_mir.pos - beam_pos

  # AmpTyp2.normal=np.array((AmpTyp2.normal[0],-AmpTyp2.normal[1],AmpTyp2.normal[2]))
  AmpTyp2.set_light_source(ls)
  AmpTyp2.propagate(np.linalg.norm(plane_mir.pos - beam_pos))
  # AmpTyp2.add_fixed_elm(plane_mir)
  AmpTyp2.add_on_axis(plane_mir)
  AmpTyp2.add_fixed_elm(cm1)
  AmpTyp2.add_fixed_elm(cm2)

  AmpTyp2.roundtrips = roundtrips2*2 #wird als neue Variable und nur zur Info eingefügt
  seq = [0]
  roundtrip_sequence = [1,2,1,0]
  seq.extend(roundtrip_sequence)
  for n in range(roundtrips2-1):
    seq.extend(roundtrip_sequence)
  AmpTyp2.set_sequence(seq)
  AmpTyp2.propagate(Radius1+30)

  # # colorshift for better understanding of the beam order
  # draw_beam_color_shift = True
  # if draw_beam_color_shift:
  #   beams = AmpTyp2.compute_beams()
  #   count = len(beams)
  #   for n in range(count):
  #     color = np.array( [ 1- n/(count-1) , 0 , n/(count-1) ] ) #rgb
  #     beam = beams[n]
  #     beam.draw_dict["color"] = color
  #     beam.draw()

  return AmpTyp2


def Make_Amplifier_Typ_II_plane(name="AmpTyp2s" ,focal_length=600 ,magnification=1,roundtrips2=2,aperture_small=1*inch ,beam_sep=15):
  # aperture_big = beam_sep * (roundtrips2+1)
  aperture_big = 12 + (roundtrips2-1)*2*beam_sep

  Radius2 = magnification*focal_length
  dist1 = (magnification+1) / magnification * focal_length
  dist2 = magnification * dist1
  PHI0 = 180 - 180/np.pi*beam_sep/dist1

  end_sphere = Curved_Mirror(radius= Radius2)
  end_sphere.aperture = aperture_small

  big_sphere = Curved_Mirror(radius=focal_length*2, phi=180-3)
  big_sphere.aperture = aperture_big
  big_sphere.set_mount_to_default()
  # big_sphere.set_mount(Unit_Mount()) # set the invisible mount for the first try

  plane_mir = Mirror(phi=PHI0)
  plane_mir.aperture = aperture_small

  ls = Beam(angle=0) # kollimierter Anfangsbeam

  #bauen wir den Amp von hinten auf
  helper = Composition()
  helper.add_on_axis(end_sphere)
  helper.propagate(dist2)
  helper.add_on_axis(big_sphere)
  helper.propagate(dist1)
  helper.add_on_axis(plane_mir)

  helper_seq = [0,1,2]
  helper_roundtrip_sequence = [1,0,1,2]
  for n in range(roundtrips2-1):
    helper_seq.extend(helper_roundtrip_sequence)
  helper.set_sequence(helper_seq)

  helper.propagate(2.2*focal_length)
  ls = Beam(radius=1.5, angle=0)
  helper.set_light_source(ls)
  bs = helper.compute_beams()
  lastbeam = bs[-1]
  lastray = lastbeam.inner_ray()
  start_pos = lastray.endpoint()
  start_pos += (0,0,-5) # height seperation between in and outgoing beam = 10 mm
  start_normal = plane_mir.pos - start_pos


  AmpTyp2 = Composition(name=name)
  AmpTyp2.pos = start_pos
  AmpTyp2.normal = start_normal
  AmpTyp2.set_light_source(ls)
  AmpTyp2.add_fixed_elm(plane_mir)
  AmpTyp2.add_fixed_elm(big_sphere)
  AmpTyp2.add_fixed_elm(end_sphere)

  AmpTyp2.roundtrips = roundtrips2*2 #wird als neue Variable und nur zur Info eingefügt
  seq = [0]
  roundtrip_sequence = [1,2,1,0]
  seq.extend(roundtrip_sequence)
  for n in range(roundtrips2-1):
    seq.extend(roundtrip_sequence)
    seq.extend(roundtrip_sequence)
  AmpTyp2.set_sequence(seq)
  AmpTyp2.propagate(3*focal_length)

  AmpTyp2.pos = (0,0,120)
  return AmpTyp2



# def Make_Amplifier_Typ_II_Juergen(name="AmpTyp2s", focal_length=600 ,
#                                   magnification=1, roundtrips2=4,
#                                   aperture_small=1*inch, beam_sep=10):
#   # name="AmpTyp2s"
#   # focal_length=600
#   # magnification=1
#   # roundtrips2=4
#   # aperture_small=1*inch
#   # beam_sep=10
#   aperture_big = beam_sep * (roundtrips2*2-1)

#   Radius2 = magnification*focal_length
#   dist1 = (magnification+1) / magnification * focal_length
#   dist2 = magnification * dist1
#   theta = np.arctan(beam_sep/dist1) # Seperationswinkel auf Planspiegel
#   PHI0 = 180 - 180/np.pi*theta
#   THETA0 = 5
#   normal_helper = np.array((np.cos(THETA0/180*np.pi), 0, np.sin(THETA0/180*np.pi)))
#   a = dist1 * 0.65
#   b = 85
#   c = dist1 - a - b
#   # beam_pos = (dist2, -dist1 * np.tan(theta* roundtrips2), 0)

#   # curved = Curved_Mirror(radius= Radius2)
#   curved = Curved_Mirror(radius= Radius2, phi=0, theta=180)
#   curved.aperture = aperture_small
#   curved.set_mount_to_default()

#   # lens1 = Curved_Mirror(radius=focal_length*2, theta=-THETA0)
#   lens1 = Curved_Mirror(radius=focal_length*2, phi=0, theta=THETA0-180)
#   lens1.aperture = aperture_big
#   lens1.set_mount_to_default()

#   flip1 = Mirror(phi=90)
#   flip1.aperture=2*inch
#   flip1.set_mount_to_default()
#   flip2 = Mirror(phi=90)
#   flip2.aperture=2*inch
#   flip2.set_mount_to_default()

#   # plane_mir = Mirror(phi=PHI0, theta=2*THETA0)
#   plane_mir = Mirror(phi=-PHI0)
#   plane_mir.aperture = aperture_small
#   plane_mir.set_mount_to_default()

#   ls = Beam(angle=0, radius=1.5) # kollimierter Anfangsbeam

#   #bauen wir den Amp von hinten auf
#   helper = Composition(normal=normal_helper)
#   helper.add_on_axis(curved)
#   helper.propagate(dist2)
#   helper.add_on_axis(lens1)
#   helper.propagate(a)
#   helper.add_on_axis(flip1)
#   helper.propagate(b)
#   helper.add_on_axis(flip2)
#   helper.propagate(c)

#   helper.add_on_axis(plane_mir)

#   helper_seq = [0,1,2,3,4]
#   helper_roundtrip_sequence = [3,2,1,0,1,2,3,4]
#   for n in range(roundtrips2-1):
#     helper_seq.extend(helper_roundtrip_sequence)
#   last_seq = [3,2]
#   helper_seq.extend(last_seq)
#   helper.set_sequence(helper_seq)


#   helper.propagate(2.2*focal_length)
#   ls = Beam(radius=1.5, angle=0)
#   helper.set_geom(ls.get_geom())
#   helper.set_light_source(ls)
#   bs = helper.compute_beams()
#   last = bs[-1]
#   lastray = last.inner_ray()
#   ps = lastray.endpoint()
#   ps += (0,0,-5)
#   # ns = lastray.normal
#   ns = lastray.pos - ps

#   helper.draw_elements()
#   helper.draw_beams()

#   AmpTyp2 = Composition(name=name, pos=ps, normal=ns)
#   ls = Beam(angle=0) # kollimierter Anfangsbeam
#   AmpTyp2.set_geom(ls.get_geom())
#   AmpTyp2.set_light_source(ls)
#   AmpTyp2.add_fixed_elm(flip1)
#   AmpTyp2.add_fixed_elm(flip2)
#   AmpTyp2.add_fixed_elm(plane_mir)
#   AmpTyp2.add_fixed_elm(lens1)
#   AmpTyp2.add_fixed_elm(curved)

#   #jetzt kommt eine weirde sequenZ...
#   seq = [0,1,2]
#   roundtrip_sequence = [1,0,3,4,3,0,1,2]
#   seq.extend(roundtrip_sequence)
#   for n in range(roundtrips2-1):
#     seq.extend(roundtrip_sequence)
#     seq.extend(roundtrip_sequence)
#   last_seq = [1,0]
#   seq.extend(last_seq)
#   AmpTyp2.set_sequence(seq)
#   AmpTyp2.propagate(3*focal_length)

#   AmpTyp2.pos = (0,0,120)
#   AmpTyp2.normal = (1,0,0)
#   return AmpTyp2