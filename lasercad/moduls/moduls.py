# -*- coding: utf-8 -*-
"""
Created on Tue Aug 30 17:03:16 2022

@author: mens
"""
from .lens import Lens
from .mirror import Mirror, Curved_Mirror, mirror_mount,Cylindrical_Mirror
# from .propagation import Propagation
# from .composition import Composition_old
from .composition import Composition
from .beam import Beam
from .constants import inch
from .grating import Grating
from .ray import Ray
from .optical_element import Opt_Element
import numpy as np
import matplotlib.pyplot as plt



def Make_Telescope(name="Teleskop", f1=100.0, f2=100.0, d0=100.0, lens1_aperture=25,
             lens2_aperture=inch):
  """
  erstellt ein Teleskop mit dem Kram da oben

  Bsp:
  teles = Teleskop()
  teles.draw_elements()
  teles.draw_beams()
  teles.draw_mounts()
  teles.draw_rays()

  Parameters
  ----------
  name : TYPE, optional
    DESCRIPTION. The default is "Teleskop".
  f1 : TYPE, optional
    Brennweite der ersten Linse. The default is 100.
  f2 : TYPE, optional
    Brennweite der zweiten Linse, Das Verhältnis f2/f1 gitb die Vergrößerung
    <amplification> des Teleskops an. The default is 100. -> amp=1.0
  d0 : TYPE, optional
    gibt den Abstand pos0 von Teleskop und erster Linse an. The default is 100.

  Returns
  -------focal_length = 200
  teles : Composition


  """
  ls = Beam(radius=1.5, angle=0)
  l1 = Lens(f=f1)
  l1.aperture = lens1_aperture
  # p2 = Propagation(f1+f2)
  l2 = Lens(f=f2)
  l2.aperture = lens2_aperture
  amp = f2/f1
  d3 = f1*(1+amp)*amp - d0*amp*amp
  # p3 = Propagation(d3)

  teles = Composition(name=name)
  teles.set_light_source(ls)
  teles.propagate(d0)
  teles.add_on_axis(l1)
  teles.propagate(f1+f2)
  teles.add_on_axis(l2)
  teles.propagate(d3)
  teles.amplification = amp


  return teles


def Make_Periscope(name="Periskop", length=150, theta = 90, dist1=75, dist2=75):

  m1 = Mirror(theta=theta)
  # p = Propagation(d=length)
  m2 = Mirror(theta=-theta)
  peris = Composition(name=name)
  peris.propagate(dist1)
  peris.add_on_axis(m1)
  peris.propagate(length)
  peris.add_on_axis(m2)
  peris.propagate(dist2)

  return peris



def Periscope2(name="Periskop", length=160,theta = 90, phi = 0, dist1=75, dist2=75):
# def Periscope(name="Periskop", length=120, theta=0, dist1=75, dist2=75):
  """
  constructs a Periscope with <name> and Distance <dist1> to the first mirror,
  <length> between the two mirrors and <dist2> after the last mirror
  
  irgendwann einmal:
  the vector between the two mirrors has an angle of <theta> to the z-Axis  

  Parameters
  ----------
  name : TYPE, optional
    DESCRIPTION. The default is "Periskop".
  length : TYPE, optional
    DESCRIPTION. The default is 120.
  theta : TYPE, optional
    Angle to the z-Axis in Degress (0->360°). The default is 0.
  dist1 : TYPE, optional
    DESCRIPTION. The default is 75.
  dist2 : TYPE, optional
    DESCRIPTION. The default is 75.

  Returns
  -------
  the Compostion

  """
  lightsource = Beam(radius=1, angle=0)
  peris = Composition(name=name)
  peris.set_light_source(lightsource)
  peris.propagate(dist1)
  m1 = Mirror()
  peris.add_on_axis(m1)
  m1.normal = (1,0,1)
  peris.recompute_optical_axis()
  
  # theta *= 180/np.pi
  # m1.normal = (1, -np.sin(theta), -np.cos(theta)) #siehe Skizze irgendwo...
  peris.propagate(length)
  m2 = Mirror()
  peris.add_on_axis(m2)
  m2.normal= (1,0,-1)
  peris.recompute_optical_axis()
  # m2.normal = -m1.normal
  peris.propagate(dist2)
  
  return peris

def Make_White_Cell(name="White Cell", Radius=300, roundtrips4=1, aperture_small=1*inch,
               aperture_big=2*inch, mirror_sep=10):
  """
  Versuch...
  generiert eine Whitcelle mit Doppelpass (=4*2 round trips)
  legt Anfangsstrahlposition in x,y Ebene bei (0,0,0)
  Spiegel stehen alle senkrecht, d.h. Normale entweder x oder -x


  """
  pos0 = np.array((0,0,0))
  cm2_hits = roundtrips4*2 - 1
  seperation = aperture_big / cm2_hits
  pos_cm2 = pos0 + (0, seperation * roundtrips4, 0)
  h = (mirror_sep + aperture_small) / 2
  pos_cm1 = pos_cm2 + (np.sqrt(Radius**2 - h**2), -h, 0)
  pos_cm3 = pos_cm2 + (np.sqrt(Radius**2 - h**2), +h, 0)
  cm1_regarding_point = pos_cm2 - (0, seperation/2, 0)
  cm3_regarding_point = pos_cm2 + (0, seperation/2, 0)

  whitecell = Composition(name=name, pos=pos0,base_exists=False, normal = pos_cm1 - pos0)

  ls = Beam(angle=0, pos=pos0)
  # ls.normal = pos_cm1 - pos0
  whitecell.set_light_source(ls)

  cm1 = Curved_Mirror(radius=Radius)
  cm1.pos = pos_cm1
  cm1.aperture = aperture_small
  whitecell.add_fixed_elm(cm1)
  cm1.normal = pos_cm1 - cm1_regarding_point

  cm2 = Curved_Mirror(radius=Radius)
  cm2.aperture = aperture_big
  cm2.pos = pos_cm2
  whitecell.add_fixed_elm(cm2)
  cm2.normal = (-1,0,0)

  cm3 = Curved_Mirror(radius=Radius)
  cm3.pos = pos_cm3
  cm3.aperture = aperture_small
  whitecell.add_fixed_elm(cm3)
  cm3.normal = pos_cm3 - cm3_regarding_point

  whitecell.roundtrips = roundtrips4*4
  seq = [0, 1, 2]
  roundtrip_sequence = [1, 0, 1, 2]
  for n in range(roundtrips4-1):
    seq.extend(roundtrip_sequence)
  # seq.append(6)
  whitecell.set_sequence(seq)
  # whitecell.recompute_optical_axis()
  whitecell.propagate(120)

  return whitecell



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

def Make_Amplifier_Typ_I_simpler(name = "AmpTyp1sr", focal_length=600,
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

    lens1 = Lens(f=focal_length)
    lens1.normal = (1,0,0) #eigentlich egal, kann auch +1,0,0 sein
    lens1.pos = (dist2,0,0) #d2 = b vom cm2 entfernt
    lens1.aperture = aperture_big

    plane_mir = Mirror()
    plane_mir.pos = (dist1+dist2, 0, 0)
    point1 = lens1.pos
    point0 = lens1.pos - (0, beam_sep, 0)
    # print("p1:", lens1.pos - (0, beam_sep, 0))
    plane_mir.set_normal_with_2_points(point0, point1)
    plane_mir.aperture = aperture_small

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

def Make_Amplifier_Typ_II_simpler(name="AmpTyp2sr", focal_length=600, magnification=1,
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

  cm1 = Curved_Mirror(radius= Radius1)
  cm1.pos = (dist2,0,0)
  cm1.normal = (np.cos(theta),np.sin(theta),0)
  cm1.aperture = aperture_big

  plane_mir = Mirror()
  plane_mir.pos = (dist2-dist1*np.cos(theta*2), -dist1*np.sin(theta*2), 0)
  point1 = cm1.pos
  point0 = cm1.pos - (0, beam_sep, 0)
  # print("p1:", lens1.pos - (0, beam_sep, 0))
  plane_mir.set_normal_with_2_points(point0, point1)
  plane_mir.aperture = aperture_small

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

  cm1 = Curved_Mirror(radius= Radius1)
  cm1.pos = (dist2,0,0)
  cm1.normal = (np.cos(theta),np.sin(theta),0)
  cm1.aperture = aperture_big

  PHI = 180*theta/np.pi*(roundtrips2+1) - 180 #?
  plane_mir = Mirror(phi=PHI)
  plane_mir.pos = (dist2-dist1*np.cos(theta*2), -dist1*np.sin(theta*2), 0)
  point1 = cm1.pos
  point0 = cm1.pos - (0, beam_sep, 0)
  # print("p1:", lens1.pos - (0, beam_sep, 0))
  # plane_mir.set_normal_with_2_points(point0, point1)
  plane_mir.aperture = aperture_small

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

# def Make_Stretcher_older():
#   """
#   tja, versuchen wir mal einen Offner Strecker...

#   Returns
#   -------
#   TYPE Composition
#     den gesamten, geraytracten Strecker...

#   """
#   # definierende Parameter
#   Radius = 1000 #Radius des großen Konkavspiegels
#   Aperture_concav = 6 * inch
#   h_StripeM = 10 #Höhe des Streifenspiegels
#   gamma = 21 /180 *np.pi # Seperationswinkel zwischen einfallenden und Mittelpunktsstrahl; Alpha = Gamma + Beta
#   grat_const = 1/450 # Gitterkonstante in 1/mm
#   seperation = 100 # Differenz zwischen Gratingposition und Radius
#   lam_mid = 2400e-9 * 1e3 # Zentralwellenlänge in mm
#   delta_lamda = 250e-9*1e3 # Bandbreite in mm
#   number_of_rays = 20
#   safety_to_StripeM = 5 #Abstand der eingehenden Strahlen zum Concav Spiegel in mm
#   periscope_distance = 8
  
#   # abgeleitete Parameter
#   v = lam_mid/grat_const
#   s = np.sin(gamma)
#   c = np.cos(gamma)
#   a = v/2
#   b = np.sqrt(a**2 - (v**2 - s**2)/(2*(1+c)))
#   sinB = a - b
  
#   Concav = Curved_Mirror(radius=Radius, name="Concav_Mirror")
#   Concav.pos = (0,0,0)
#   Concav.aperture = Aperture_concav
#   Concav.normal = (-1,0,0)
  
#   StripeM = Curved_Mirror(radius= -Radius/2, name="Stripe_Mirror")
#   StripeM.pos = (Radius/2, 0, 0)
#   #Cosmetics
#   StripeM.aperture=75
#   StripeM.draw_dict["height"]=10
#   StripeM.draw_dict["thickness"]=25
#   StripeM.draw_dict["model_type"]="Stripe"
  
#   Grat = Grating(grat_const=grat_const, name="Gitter")
#   Grat.pos = (Radius-seperation, 0, 0)
#   Grat.normal = (np.sqrt(1-sinB**2), -sinB, 0)
  
#   ray0 = Ray()
#   p_grat = np.array((Radius-seperation, 0, h_StripeM/2 + safety_to_StripeM))
#   vec = np.array((c, s, 0))
#   pos0 = p_grat - 250 * vec
#   ray0.normal = vec
#   ray0.pos = pos0
#   ray0.wavelength = lam_mid
  
#   lightsource = Beam(radius=0, angle=0)
#   wavels = np.linspace(lam_mid-delta_lamda/2, lam_mid+delta_lamda/2, number_of_rays)
#   rays = []
#   cmap = plt.cm.gist_rainbow
#   for wavel in wavels:
#     rn = Ray()
#     # rn.normal = vec
#     # rn.pos = pos0
#     rn.wavelength = wavel
#     x = (wavel - lam_mid + delta_lamda/2) / delta_lamda
#     rn.draw_dict["color"] = cmap( x )
#     rays.append(rn)
#   lightsource.override_rays(rays)
  
#   nfm1 = - ray0.normal
#   pfm1 = Grat.pos + 200 * nfm1 + (0,0,-h_StripeM/2 - safety_to_StripeM)
#   # subperis = Periscope(length=8, theta=-90, dist1=0, dist2=0)
#   # subperis.pos = pfm1
#   # subperis.normal = nfm1
#   flip_mirror1 = Mirror()
#   flip_mirror1.pos = pfm1
#   flip_mirror1.normal = nfm1 - np.array((0,0,-1))
  
  
#   flip_mirror2 = Mirror()
#   flip_mirror2.pos = pfm1 - np.array((0,0,periscope_distance))
#   flip_mirror2.normal = nfm1 - np.array((0,0,1))

  
#   Stretcher = Composition(name="Strecker", pos=pos0, normal=vec)
  
#   Stretcher.set_light_source(lightsource)
#   Stretcher.add_fixed_elm(Grat)
#   Stretcher.add_fixed_elm(Concav)
#   Stretcher.add_fixed_elm(StripeM)
#   Stretcher.add_fixed_elm(flip_mirror1)
#   Stretcher.add_fixed_elm(flip_mirror2)
  
#   # for item in subperis._elements:
#   #   Stretcher.add_fixed_elm(item)
  
  
#   # seq = [0,1,2,1,0]
#   # seq = [0,1,2,1,0, 3]
#   # seq = [0,1,2,1,0, 3,4]
#   seq = [0,1,2,1,0, 3,4, 0, 1, 2, 1, 0]
#   Stretcher.set_sequence(seq)
#   Stretcher.propagate(300)
#   return Stretcher


def Make_Stretcher_old():
  """
  tja, versuchen wir mal einen Offner Strecker...
  Note: When drawing a rooftop mirror, we will draw apure_cosmetic mirror to 
  confirm the position of the mount. The mirror's geom is the average of two 
  flip mirror. And its aperture is the periscope_distance.
  Returns
  -------
  TYPE Composition
    den gesamten, geraytracten Strecker...
  """
  # definierende Parameter
  Radius = 1000 #Radius des großen Konkavspiegels
  Aperture_concav = 6 * inch
  h_StripeM = 10 #Höhe des Streifenspiegels
  gamma = 21 /180 *np.pi # Seperationswinkel zwischen einfallenden und Mittelpunktsstrahl; Alpha = Gamma + Beta
  grat_const = 1/450 # Gitterkonstante in 1/mm
  seperation = 100 # Differenz zwischen Gratingposition und Radius
  lam_mid = 2400e-9 * 1e3 # Zentralwellenlänge in mm
  delta_lamda = 250e-9*1e3 # Bandbreite in mm
  number_of_rays = 20
  safety_to_StripeM = 5 #Abstand der eingehenden Strahlen zum Concav Spiegel in mm
  periscope_distance = 16
  
  # abgeleitete Parameter
  v = lam_mid/grat_const
  s = np.sin(gamma)
  c = np.cos(gamma)
  a = v/2
  b = np.sqrt(a**2 - (v**2 - s**2)/(2*(1+c)))
  sinB = a - b
  
  Concav = Curved_Mirror(radius=Radius, name="Concav_Mirror")
  Concav.pos = (0,0,0)
  Concav.aperture = Aperture_concav
  Concav.normal = (-1,0,0)
  # Concav._axes = np.array([[-1,0,0],[0,0,1],[0,1,0]])
  # Concav.draw_dict["height"]=40
  # Concav.draw_dict["thickness"]=25
  # Concav.draw_dict["model_type"]="Stripe"
  
  StripeM = Cylindrical_Mirror(radius= -Radius/2, name="Stripe_Mirror")
  StripeM.pos = (Radius/2, 0, 0)
  #Cosmetics
  StripeM.aperture=75
  StripeM.draw_dict["height"]=10
  StripeM.draw_dict["thickness"]=25
  StripeM.draw_dict["model_type"]="Stripe"
  
  Grat = Grating(grat_const=grat_const, name="Gitter")
  Grat.pos = (Radius-seperation, 0, 0)
  Grat.normal = (np.sqrt(1-sinB**2), -sinB, 0)
  
  ray0 = Ray()
  p_grat = np.array((Radius-seperation, 0, -h_StripeM/2 - safety_to_StripeM))
  vec = np.array((c, s, 0))
  pos0 = p_grat - 250 * vec
  ray0.normal = vec
  ray0.pos = pos0
  ray0.wavelength = lam_mid
  
  lightsource = Beam(radius=0, angle=0)
  wavels = np.linspace(lam_mid-delta_lamda/2, lam_mid+delta_lamda/2, number_of_rays)
  rays = []
  cmap = plt.cm.gist_rainbow
  for wavel in wavels:
    rn = Ray()
    # rn.normal = vec
    # rn.pos = pos0
    rn.wavelength = wavel
    x = (wavel - lam_mid + delta_lamda/2) / delta_lamda
    rn.draw_dict["color"] = cmap( x )
    rays.append(rn)
  lightsource.override_rays(rays)
  
  nfm1 = - ray0.normal
  pfm1 = Grat.pos + 400 * nfm1 + (0,0,h_StripeM/2 + safety_to_StripeM + periscope_distance)
  # subperis = Periscope(length=8, theta=-90, dist1=0, dist2=0)
  # subperis.pos = pfm1
  # subperis.normal = nfm1
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
  pure_cosmetic.draw_dict["mount_type"] = "rooftop_mirror"
  pure_cosmetic.pos = (flip_mirror1.pos + flip_mirror2.pos ) / 2
  pure_cosmetic.normal = (flip_mirror1.normal + flip_mirror2.normal ) / 2
  pure_cosmetic.aperture = periscope_distance

  # pure_cosmetic.draw = useless
  
  Stretcher = Composition(name="Strecker", pos=pos0, normal=vec)
  
  Stretcher.set_light_source(lightsource)
  Stretcher.add_fixed_elm(Grat)
  Stretcher.add_fixed_elm(Concav)
  Stretcher.add_fixed_elm(StripeM)
  Stretcher.add_fixed_elm(flip_mirror2)
  Stretcher.add_fixed_elm(flip_mirror1)
  Stretcher.add_fixed_elm(pure_cosmetic)
  
  # for item in subperis._elements:
  #   Stretcher.add_fixed_elm(item)
  
  
  # seq = [0,1,2,1,0]
  # seq = [0,1,2,1,0, 3]
  # seq = [0,1,2,1,0, 3,4]
  seq = [0,1,2,1,0, 3,4, 0, 1, 2, 1, 0]
  Stretcher.set_sequence(seq)
  Stretcher.propagate(300)
  return Stretcher

def Make_Stretcher():
  """
  tja, versuchen wir mal einen Offner Strecker...
  Note: When drawing a rooftop mirror, we will draw apure_cosmetic mirror to 
  confirm the position of the mount. The mirror's geom is the average of two 
  flip mirror. And its aperture is the periscope_distance.

  Returns
  -------
  TYPE Composition
    den gesamten, geraytracten Strecker...

  """
  # definierende Parameter
  Radius = 1000 #Radius des großen Konkavspiegels
  Aperture_concav = 6 * inch
  h_StripeM = 10 #Höhe des Streifenspiegels
  gamma = 5 /180 *np.pi # Seperationswinkel zwischen einfallenden und Mittelpunktsstrahl; Alpha = Gamma + Beta
  grat_const = 1/450 # Gitterkonstante in 1/mm
  seperation = 100 # Differenz zwischen Gratingposition und Radius
  lam_mid = 2400e-9 * 1e3 # Zentralwellenlänge in mm
  delta_lamda = 250e-9*1e3 # Bandbreite in mm
  number_of_rays = 20
  safety_to_StripeM = 5 #Abstand der eingehenden Strahlen zum Concav Spiegel in mm
  periscope_distance = 8
  
  # abgeleitete Parameter
  v = lam_mid/grat_const
  s = np.sin(gamma)
  c = np.cos(gamma)
  a = v/2
  b = np.sqrt(a**2 - (v**2 - s**2)/(2*(1+c)))
  sinB = a - b
  
  Concav = Curved_Mirror(radius=Radius, name="Concav_Mirror")
  Concav.pos = (0,0,0)
  Concav.aperture = Aperture_concav
  Concav.normal = (-1,0,0)
  
  StripeM = Curved_Mirror(radius= -Radius/2, name="Stripe_Mirror")
  StripeM.pos = (Radius/2, 0, 0)
  #Cosmetics
  StripeM.aperture=75
  StripeM.draw_dict["height"]=10
  StripeM.draw_dict["thickness"]=25
  StripeM.draw_dict["model_type"]="Stripe"
  
  Grat = Grating(grat_const=grat_const, name="Gitter")
  Grat.pos = (Radius-seperation, 0, 0)
  Grat.normal = (np.sqrt(1-sinB**2), -sinB, 0)
  
  ray0 = Ray()
  p_grat = np.array((Radius-seperation, 0, h_StripeM/2 + safety_to_StripeM))
  vec = np.array((c, s, 0))
  pos0 = p_grat - 250 * vec
  ray0.normal = vec
  ray0.pos = pos0
  ray0.wavelength = lam_mid
  
  lightsource = Beam(radius=0, angle=0)
  wavels = np.linspace(lam_mid-delta_lamda/2, lam_mid+delta_lamda/2, number_of_rays)
  rays = []
  cmap = plt.cm.gist_rainbow
  for wavel in wavels:
    rn = Ray()
    # rn.normal = vec
    # rn.pos = pos0
    rn.wavelength = wavel
    x = (wavel - lam_mid + delta_lamda/2) / delta_lamda
    rn.draw_dict["color"] = cmap( x )
    rays.append(rn)
  lightsource.override_rays(rays)
  lightsource.draw_dict['model'] = "ray_group"
  
  nfm1 = - ray0.normal
  pfm1 = Grat.pos + 200 * nfm1 + (0,0,-h_StripeM/2 - safety_to_StripeM)
  # subperis = Periscope(length=8, theta=-90, dist1=0, dist2=0)
  # subperis.pos = pfm1
  # subperis.normal = nfm1
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
  pure_cosmetic.draw_dict["mount_type"] = "rooftop_mirror_mount"
  pure_cosmetic.pos = (flip_mirror1.pos + flip_mirror2.pos ) / 2
  pure_cosmetic.normal = (flip_mirror1.normal + flip_mirror2.normal ) / 2
  pure_cosmetic.aperture = periscope_distance

  pure_cosmetic.draw = useless
  
  Stretcher = Composition(name="Strecker", pos=pos0, normal=vec)
  
  Stretcher.set_light_source(lightsource)
  Stretcher.add_fixed_elm(Grat)
  Stretcher.add_fixed_elm(Concav)
  Stretcher.add_fixed_elm(StripeM)
  Stretcher.add_fixed_elm(flip_mirror1)
  Stretcher.add_fixed_elm(flip_mirror2)
  Stretcher.add_fixed_elm(pure_cosmetic)
  
  # for item in subperis._elements:
  #   Stretcher.add_fixed_elm(item)
  
  
  # seq = [0,1,2,1,0]
  # seq = [0,1,2,1,0, 3]
  # seq = [0,1,2,1,0, 3,4]
  seq = [0,1,2,1,0, 3,4, 0, 1, 2, 1, 0]
  Stretcher.set_sequence(seq)
  Stretcher.propagate(300)
  return Stretcher

def Make_Amplifier_Typ_II_plane():
  name="AmpTyp2s" 
  focal_length=600 
  magnification=1
  roundtrips2=2
  aperture_small=1*inch 
  beam_sep=15
  aperture_big = beam_sep * (roundtrips2+1)
  
  Radius2 = magnification*focal_length
  dist1 = (magnification+1) / magnification * focal_length
  dist2 = magnification * dist1
  theta = np.arctan(beam_sep/dist1) # Seperationswinkel auf Planspiegel
  PHI0 = 180 - 180/np.pi*theta
  # beam_pos = (dist2, -dist1 * np.tan(theta* roundtrips2), 0)
  
  curved = Curved_Mirror(radius= Radius2)
  curved.aperture = aperture_small
  
  lens1 = Curved_Mirror(radius=focal_length*2, phi=180-3)
  lens1.aperture = aperture_big
  
  plane_mir = Mirror(phi=PHI0)
  plane_mir.aperture = aperture_small
  
  ls = Beam(angle=0) # kollimierter Anfangsbeam
  
  #bauen wir den Amp von hinten auf
  helper = Composition()
  helper.add_on_axis(curved)
  helper.propagate(dist2)
  helper.add_on_axis(lens1)
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
  last = bs[-1]
  lastray = last.inner_ray()
  ps = lastray.endpoint()
  ps += (0,0,-5)
  # ns = lastray.normal
  ns = plane_mir.pos - ps
  
  # helper.draw_elements()
  
  AmpTyp2 = Composition(name=name, pos=ps, normal=ns)
  ls = Beam(angle=0) # kollimierter Anfangsbeam
  AmpTyp2.set_light_source(ls)
  AmpTyp2.add_fixed_elm(plane_mir)
  AmpTyp2.add_fixed_elm(lens1)
  AmpTyp2.add_fixed_elm(curved)
  
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



def Make_Amplifier_Typ_II_with_theta():
  name="AmpTyp2s" 
  focal_length=600 
  magnification=1
  roundtrips2=3
  aperture_small=1*inch 
  beam_sep=15
  aperture_big = beam_sep * (roundtrips2*2-1)
  
  Radius2 = magnification*focal_length
  dist1 = (magnification+1) / magnification * focal_length
  dist2 = magnification * dist1
  theta = np.arctan(beam_sep/dist1) # Seperationswinkel auf Planspiegel
  PHI0 = 180 - 180/np.pi*theta
  THETA0 = 5
  normal_helper = np.array((np.cos(THETA0/180*np.pi), 0, np.sin(THETA0/180*np.pi)))
  # beam_pos = (dist2, -dist1 * np.tan(theta* roundtrips2), 0)
  
  # curved = Curved_Mirror(radius= Radius2)
  curved = Curved_Mirror(radius= Radius2, phi=0, theta=180)
  curved.aperture = aperture_small
  
  # lens1 = Curved_Mirror(radius=focal_length*2, theta=-THETA0)
  lens1 = Curved_Mirror(radius=focal_length*2, phi=0, theta=THETA0-180)
  lens1.aperture = aperture_big
  
  # plane_mir = Mirror(phi=PHI0, theta=2*THETA0)
  plane_mir = Mirror(phi=PHI0)
  plane_mir.aperture = aperture_small
  
  ls = Beam(angle=0) # kollimierter Anfangsbeam
  
  #bauen wir den Amp von hinten auf
  helper = Composition(normal=normal_helper)
  helper.add_on_axis(curved)
  helper.propagate(dist2)
  helper.add_on_axis(lens1)
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
  last = bs[-1]
  lastray = last.inner_ray()
  ps = lastray.endpoint()
  ps += (0,0,-5)
  # ns = lastray.normal
  ns = plane_mir.pos - ps
  
  # helper.draw_elements()
  # helper.draw_beams()
  
  AmpTyp2 = Composition(name=name, pos=ps, normal=ns)
  ls = Beam(angle=0) # kollimierter Anfangsbeam
  AmpTyp2.set_light_source(ls)
  AmpTyp2.add_fixed_elm(plane_mir)
  AmpTyp2.add_fixed_elm(lens1)
  AmpTyp2.add_fixed_elm(curved)
  
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
  AmpTyp2.normal = (1,0,0)
  return AmpTyp2


def Make_Amplifier_Typ_II_Juergen():
  name="AmpTyp2s" 
  focal_length=600 
  magnification=1
  roundtrips2=4
  aperture_small=1*inch 
  beam_sep=10
  aperture_big = beam_sep * (roundtrips2*2-1)
  
  Radius2 = magnification*focal_length
  dist1 = (magnification+1) / magnification * focal_length
  dist2 = magnification * dist1
  theta = np.arctan(beam_sep/dist1) # Seperationswinkel auf Planspiegel
  PHI0 = 180 - 180/np.pi*theta
  THETA0 = 5
  normal_helper = np.array((np.cos(THETA0/180*np.pi), 0, np.sin(THETA0/180*np.pi)))
  a = dist1 * 0.65
  b = 85
  c = dist1 - a - b
  # beam_pos = (dist2, -dist1 * np.tan(theta* roundtrips2), 0)
  
  # curved = Curved_Mirror(radius= Radius2)
  curved = Curved_Mirror(radius= Radius2, phi=0, theta=180)
  curved.aperture = aperture_small
  
  # lens1 = Curved_Mirror(radius=focal_length*2, theta=-THETA0)
  lens1 = Curved_Mirror(radius=focal_length*2, phi=0, theta=THETA0-180)
  lens1.aperture = aperture_big
  
  flip1 = Mirror(phi=90)
  flip1.aperture=2*inch
  flip2 = Mirror(phi=90)
  flip2.aperture=2*inch

  # plane_mir = Mirror(phi=PHI0, theta=2*THETA0)
  plane_mir = Mirror(phi=-PHI0)
  plane_mir.aperture = aperture_small
  
  ls = Beam(angle=0, radius=1.5) # kollimierter Anfangsbeam
  
  
  
    
  
  #bauen wir den Amp von hinten auf
  helper = Composition(normal=normal_helper)
  helper.add_on_axis(curved)
  helper.propagate(dist2)
  helper.add_on_axis(lens1)
  helper.propagate(a)
  helper.add_on_axis(flip1)
  helper.propagate(b)
  helper.add_on_axis(flip2)
  helper.propagate(c)

  helper.add_on_axis(plane_mir)
  
  helper_seq = [0,1,2,3,4]
  helper_roundtrip_sequence = [3,2,1,0,1,2,3,4]
  for n in range(roundtrips2-1):
    helper_seq.extend(helper_roundtrip_sequence)
  last_seq = [3,2]
  helper_seq.extend(last_seq)
  helper.set_sequence(helper_seq)  
  

  helper.propagate(2.2*focal_length)
  ls = Beam(radius=1.5, angle=0)
  helper.set_light_source(ls)
  bs = helper.compute_beams()
  last = bs[-1]
  lastray = last.inner_ray()
  ps = lastray.endpoint()
  ps += (0,0,-5)
  # ns = lastray.normal
  ns = lastray.pos - ps
  
  # helper.draw_elements()
  # helper.draw_beams()
  
  AmpTyp2 = Composition(name=name, pos=ps, normal=ns)
  ls = Beam(angle=0) # kollimierter Anfangsbeam
  AmpTyp2.set_light_source(ls)
  AmpTyp2.add_fixed_elm(flip1)
  AmpTyp2.add_fixed_elm(flip2)
  AmpTyp2.add_fixed_elm(plane_mir)
  AmpTyp2.add_fixed_elm(lens1)
  AmpTyp2.add_fixed_elm(curved)

  #jetzt kommt eine weirde sequenZ...  
  seq = [0,1,2]
  roundtrip_sequence = [1,0,3,4,3,0,1,2]
  seq.extend(roundtrip_sequence)
  for n in range(roundtrips2-1):
    seq.extend(roundtrip_sequence)
    seq.extend(roundtrip_sequence)
  last_seq = [1,0]
  seq.extend(last_seq)
  AmpTyp2.set_sequence(seq)
  AmpTyp2.propagate(3*focal_length)

  AmpTyp2.pos = (0,0,120)
  AmpTyp2.normal = (1,0,0)
  return AmpTyp2


# =============================================================================
# Regen Amp1 Section
# =============================================================================
from .. basic_optics import LinearResonator
from .. non_interactings import Pockels_Cell, Lambda_Plate


def Make_Amplifier_I():

  tfp_angle = 65
  tfp_aperture = 2*inch
  angle_on_sphere = 10
  alpha = -0.8
  beta = -0.8
  print("g1*g2 = ", alpha*beta)
  focal = 500
  dist1 = (1-alpha)*focal
  dist2 = (1-beta)*focal
  wavelength = 2400*1e-6

  # geometric restrictions
  dist_tfp1_2 = 230
  dist_tfp1_pockels = 50
  dist_pockels_lambda = 115
  dist_tfp2_sphere = 400
  dist_m1_tfp1 = dist1 - dist_tfp1_2 - dist_tfp2_sphere
  dist_crystal_end = 15

  mir1 = Mirror(phi=180)
  TFP1 = Mirror(phi= 180 - 2*tfp_angle, name="TFP1")
  TFP1.draw_dict["color"] = (1.0, 0.0, 2.0)
  TFP1.aperture = tfp_aperture
  TFP2 = Mirror(phi= - 180 + 2*tfp_angle, name="TFP2")
  TFP2.draw_dict["color"] = (1.0, 0.0, 2.0)
  TFP2.aperture = tfp_aperture
  mir4 = Mirror(phi=180)
  cm = Curved_Mirror(radius=focal*2, phi = 180 - angle_on_sphere)
  PockelsCell = Pockels_Cell()
  Lambda2 = Lambda_Plate()

  amp1 = LinearResonator(name="foldedRes")
  amp1.set_wavelength(wavelength)
  amp1.add_on_axis(mir1)
  amp1.propagate(dist_m1_tfp1)
  amp1.add_on_axis(TFP1)
  amp1.propagate(dist_tfp1_pockels)
  amp1.add_on_axis(PockelsCell)
  amp1.propagate(dist_pockels_lambda)
  amp1.add_on_axis(Lambda2)
  amp1.propagate(dist_tfp1_2-dist_tfp1_pockels-dist_pockels_lambda)
  amp1.add_on_axis(TFP2)
  amp1.propagate(dist_tfp2_sphere)
  amp1.add_on_axis(cm)
  amp1.propagate(dist2 - dist_crystal_end)


  crystal = Beam(radius=3, angle=0)
  crystal.draw_dict['color'] = (182/255, 109/255, 46/255)
  crystal.set_length(10)

  amp1.add_on_axis(crystal)
  amp1.propagate(dist_crystal_end)
  amp1.add_on_axis(mir4)

  amp1.compute_eigenmode()
  return amp1


from .. non_interactings import Crystal
def Make_Butterfly_Amplifier():
  # =============================================================================
  # Amplifier2 Butterfly
  # =============================================================================
  bigcrys = Crystal(width=18,height=18,thickness=15,n=2.45)

  source = Beam(radius=5, angle=0)

  Butterfly = Composition(name="Butterlfy")
  Butterfly.set_light_source(source)
  Butterfly.propagate(300)
  Butterfly.add_on_axis(bigcrys)
  bigcrys.rotate((0,0,1), 6*np.pi/180)

  Butterfly.propagate(200)
  flip1 = Mirror(phi=90)
  Butterfly.add_on_axis(flip1)
  Butterfly.propagate(70)
  backmirror1 = Mirror()
  Butterfly.add_on_axis(backmirror1)
  backmirror1.set_normal_with_2_points(flip1.pos, bigcrys.pos)
  Butterfly.propagate(500)
  return Butterfly


# def Teleskop_old(name="Teleskop", f1=100.0, f2=100.0, d0=100.0, lens1_aperture=25,
#              lens2_aperture=inch):
#   """
#   erstellt ein Teleskop mit dem Kram da oben

#   Parameters
#   ----------
#   name : TYPE, optional
#     DESCRIPTION. The default is "Teleskop".
#   f1 : TYPE, optional
#     Brennweite der ersten Linse. The default is 100.
#   f2 : TYPE, optional
#     Brennweite der zweiten Linse, Das Verhältnis f2/f1 gitb die Vergrößerung
#     <amplification> des Teleskops an. The default is 100. -> amp=1.0
#   d0 : TYPE, optional
#     gibt den Abstand pos0 von Teleskop und erster Linse an. The default is 100.

#   Returns
#   -------focal_length = 200
#   teles : Composition_old
#   """
#   p1 = Propagation(d=d0)
#   l1 = Lens(f=f1)
#   l1.aperture = lens1_aperture
#   p2 = Propagation(f1+f2)
#   l2 = Lens(f=f2)
#   l2.aperture = lens2_aperture
#   amp = f2/f1
#   d3 = f1*(1+amp)*amp - d0*amp*amp
#   p3 = Propagation(d3)

#   teles = Composition_old(name=name)
#   teles.add(p1)
#   teles.add(l1)
#   teles.add(p2)
#   teles.add(l2)
#   teles.add(p3)
#   teles.amplification = amp
#   return teles


# def Amplifier_Typ_II_simple_old(name="AmpTyp2s", focal_length=600, magnification=1,
#                             roundtrips2=1,
#                             aperture_small=1*inch, aperture_big=2*inch, beam_sep=15):
#   """
#   generiert die Strahlführung eines einfachen Typ II Verstärkers mit einer Linse
#   und einem gekrümmten Spiegel

#   V = magnification
#   f = focal_length
#   a = (V+1)/V * f
#   b = a*V
#   f2 = V/2 * f

#   Returns
#   -------
#   Composition_old: Amplifier_TypII_simple


#   """
#   Radius2 = magnification*focal_length
#   dist1 = (magnification+1) / magnification * focal_length
#   dist2 = magnification * dist1
#   theta = np.arctan(beam_sep/dist1) # Seperationswinkel auf Planspiegel
#   beam_pos = (dist2, -dist1 * np.tan(theta* roundtrips2), 0)
#   # Position der Lichtquelle = n*Ablenkwinkel unter dem waagerechtem Strahl

#   cm2 = Curved_Mirror(radius= Radius2)
#   cm2.pos = (0,0,0) # der Ausgangspunkt
#   cm2.normal = (-1,0,0) # umgekehrte Ausrichtung des Aufbaus
#   cm2.aperture = aperture_small

#   lens1 = Lens(f=focal_length)
#   lens1.normal = (1,0,0) #eigentlich egal, kann auch +1,0,0 sein
#   lens1.pos = (dist2,0,0) #d2 = b vom cm2 entfernt
#   lens1.aperture = aperture_big

#   plane_mir = Mirror()
#   plane_mir.pos = (dist1+dist2, 0, 0)
#   point1 = lens1.pos
#   point0 = lens1.pos - (0, beam_sep, 0)
#   plane_mir.set_normal_with_2_points(point0, point1)
#   plane_mir.aperture = aperture_small

#   ls = Beam(angle=0) # kollimierter Anfangsbeam
#   ls.pos = beam_pos
#   ls.normal = plane_mir.pos - beam_pos #soll direkt auch den Planspiegel zeigen


#   AmpTyp2 = Composition_old(name=name)
#   AmpTyp2.set_light_source(ls)
#   AmpTyp2.add_only_elm(plane_mir)
#   AmpTyp2.add_only_elm(lens1)
#   AmpTyp2.add_only_elm(cm2)

#   # lastprop
#   # lastprop = Propagation(d = 300)
#   # lastprop.pos = plane_mir.pos
#   # lastprop.normal = ls.pos - plane_mir.pos
#   # AmpTyp2.add_only_elm(lastprop)

#   AmpTyp2.roundtrips = roundtrips2*2 #wird als neue Variable und nur zur Info eingefügt
#   seq = [0, 1]
#   roundtrip_sequence = [2,3,4,5,4,3,2,1]
#   seq.extend(roundtrip_sequence)
#   for n in range(roundtrips2-1):
#     seq.extend(roundtrip_sequence)
#   # seq.append(6)
#   AmpTyp2.sequence = seq
#   return AmpTyp2


# def White_Cell_old(name="White Cell", Radius=300, roundtrips4=1, aperture_small=1*inch,
#                aperture_big=2*inch, mirror_sep=10):
#   """
#   Versuch...
#   generiert eine Whitcelle mit Doppelpass (=4*2 round trips)
#   legt Anfangsstrahlposition in x,y Ebene bei (0,0,0)
#   Spiegel stehen alle senkrecht, d.h. Normale entweder x oder -x


#   """
#   pos0 = np.array((0,0,0))
#   cm2_hits = roundtrips4*2 - 1
#   seperation = aperture_big / cm2_hits
#   pos_cm2 = pos0 + (0, seperation * roundtrips4, 0)
#   h = (mirror_sep + aperture_small) / 2
#   pos_cm1 = pos_cm2 + (np.sqrt(Radius**2 - h**2), -h, 0)
#   pos_cm3 = pos_cm2 + (np.sqrt(Radius**2 - h**2), +h, 0)
#   cm1_regarding_point = pos_cm2 - (0, seperation/2, 0)
#   cm3_regarding_point = pos_cm2 + (0, seperation/2, 0)

#   whitecell = Composition_old(name=name)

#   ls = Beam(angle=0, pos=pos0)
#   ls.normal = pos_cm1 - pos0
#   whitecell.set_light_source(ls)

#   cm1 = Curved_Mirror(radius=Radius)
#   cm1.pos = pos_cm1
#   cm1.aperture = aperture_small
#   whitecell.add_only_elm(cm1)
#   cm1.normal = pos_cm1 - cm1_regarding_point

#   cm2 = Curved_Mirror(radius=Radius)
#   cm2.aperture = aperture_big
#   cm2.pos = pos_cm2
#   whitecell.add_only_elm(cm2)
#   cm2.normal = (-1,0,0)

#   cm3 = Curved_Mirror(radius=Radius)
#   cm3.pos = pos_cm3
#   cm3.aperture = aperture_small
#   whitecell.add_only_elm(cm3)
#   cm3.normal = pos_cm3 - cm3_regarding_point


#   prop4 = Propagation(d=Radius) #müsste auch mit beamberechnung gehen...
#   prop4.pos = cm3.pos
#   prop4.normal = pos0 + (0, roundtrips4*2*seperation, 0) - cm3.pos
#   whitecell.add(prop4)

#   whitecell.roundtrips = roundtrips4*4
#   seq = [0, 1, 2, 3, 4, 5]
#   roundtrip_sequence = [4, 3 ,2, 1, 2, 3, 4, 5]
#   for n in range(roundtrips4-1):
#     seq.extend(roundtrip_sequence)
#   seq.append(6)
#   whitecell.sequence = seq

#   return whitecell


# def Periskop_old(name="Periskop", length=150, theta = 90, phi = 0):
#   # if direction == "x":
#   #   vec = np.array((1,0,0))
#   # elif direction == "y":
#   #   vec = np.array((0,1,0))
#   # elif direction == "z":
#   #   vec = np.array((0,0,1))
#   # else:
#   #   vec = direction
#   m1 = Mirror(phi = phi, theta=theta)
#   p = Propagation(d=length)
#   m2 = Mirror(phi = -phi, theta = -theta)
#   peris = Composition_old(name=name)
#   peris.add(m1)
#   peris.add(p)
#   peris.add(m2)

#   return peris