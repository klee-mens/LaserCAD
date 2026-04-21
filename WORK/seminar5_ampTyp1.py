#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 12 15:22:07 2026

@author: clemens
"""

from LaserCAD.freecad_models import freecad_da, clear_doc, setview
from LaserCAD import inch, Lens, Mirror, Beam, Composition, CircularRayBeam
import numpy as np

if freecad_da:
  clear_doc()

stretching_factor = 0.5

name = "AmpTyp1s"
focal_length1 = 600 * stretching_factor
magnification = 1/3
focal_length2 = magnification * focal_length1

dist1 = 1000 * stretching_factor
dist2 = focal_length1 + focal_length2
dist3 = magnification * (dist2 - magnification*dist1)


roundtrips2 = 3
aperture_mirror = 1*inch
aperture_lens = 2*inch
beam_sep = 10


# theta = np.arctan(beam_sep/dist1) # Seperationswinkel auf Planspiegel
# beam_pos = (dist2+dist3, -dist1 * np.tan(theta* roundtrips2), 0)

plane_mir2 = Mirror()
plane_mir2.pos = (0,0,0) # der Ausgangspunkt
plane_mir2.normal = (-1,0,0) # umgekehrte Ausrichtung des Aufbaus
plane_mir2.aperture = aperture_mirror
# plane_mir2.set_mount_to_default()

lens1 = Lens(f=focal_length2)
lens1.normal = (1,0,0) #eigentlich egal, kann auch +1,0,0 sein
lens1.pos = (dist3,0,0) #d2 = b vom cm2 entfernt
lens1.aperture = aperture_lens
# lens1.set_mount_to_default()

lens2 = Lens(f=focal_length1)
lens2.normal = (1,0,0) #eigentlich egal, kann auch +1,0,0 sein
lens2.pos = (dist3+dist2,0,0) #d2 = b vom cm2 entfernt
lens2.aperture = aperture_lens
# lens2.set_mount_to_default()

plane_mir1 = Mirror()
plane_mir1.pos = (dist1+dist2+dist3, 0, 0)
point1 = lens2.pos
point0 = lens2.pos - (0, beam_sep, 0)
beam_pos = lens2.pos - (0, beam_sep*roundtrips2, 0)
# print("p1:", lens1.pos - (0, beam_sep, 0))
plane_mir1.set_normal_with_2_points(point0, point1)
plane_mir1.aperture = aperture_mirror
# plane_mir1.set_mount_to_default()

# ls = Beam(angle=0, radius=2) # kollimierter Anfangsbeam
ls = CircularRayBeam(angle=0, radius=2) # kollimierter Anfangsbeam
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

AmpTyp1._lightsource.pos += (0,0,-5)
AmpTyp1._lightsource.normal = plane_mir1.pos - AmpTyp1._lightsource.pos


AmpTyp1.pos += (0,0,80)
AmpTyp1.draw()



if freecad_da:
  setview()