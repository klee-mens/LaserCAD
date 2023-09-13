# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 10:56:05 2023

@author: 12816
"""

from .. basic_optics import Mirror, Lens, Beam, Composition, inch,Curved_Mirror
import numpy as np


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

  whitecell = Composition(name=name, pos=pos0,normal = pos_cm1 - pos0)

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