# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 14:01:12 2024

@author: 12816
"""
from LaserCAD.basic_optics import Beam, Refractive_plane, Composition, inch
from LaserCAD.basic_optics import Curved_Mirror, Mirror, Unit_Mount
from LaserCAD.freecad_models import freecad_da, clear_doc, setview
import numpy as np
from LaserCAD.non_interactings import Faraday_Isolator, Crystal, Cylindric_Crystal

if freecad_da:
  clear_doc()

# def Make_Amplifier_Typ_II_Juergen(name="AmpTyp2s", focal_length=600 ,
#                                   magnification=1, roundtrips2=4,
#                                   aperture_small=1*inch, beam_sep=10):
name="AmpTyp2s"
# focal_length=600
focal_length=400
magnification=1
roundtrips2=3
aperture_small=1*inch
beam_sep=12 #mm
THETA0 = 3 #deg
beam_diameter = 5
 
# name="AmpTyp2s"
# focal_length=600
# magnification=1
# roundtrips2=4
# aperture_small=1*inch
# beam_sep=10
aperture_big = beam_sep * (roundtrips2*2-1)
Radius2 = magnification*focal_length
dist1 = (magnification+1) / magnification * focal_length
dist2 = magnification * dist1
theta = np.arctan(beam_sep/dist1) # Seperationswinkel auf Planspiegel
# PHI0 = 180 - 180/np.pi*theta
PHI0 = 180 + 180/np.pi*theta
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
lens1.Mount.invisible = True

flip1 = Mirror(phi=90)
flip1.aperture=1.5*inch
flip1.set_mount_to_default()
flip2 = Mirror(phi=90)
flip2.aperture=1.5*inch
flip2.set_mount_to_default()

# plane_mir = Mirror(phi=PHI0, theta=2*THETA0)
plane_mir = Mirror(phi=-PHI0)
plane_mir.aperture = aperture_small
plane_mir.set_mount_to_default()

crys = Cylindric_Crystal(name="Tm:YAG", aperture=20, thickness=10)

ls = Beam(angle=0, radius=1.5) # kollimierter Anfangsbeam

#bauen wir den Amp von hinten auf
helper = Composition()
helper.normal = normal_helper
helper.add_on_axis(curved)
helper.propagate(dist2)
helper.add_on_axis(lens1)
helper.propagate(a)
helper.add_on_axis(flip1)
helper.propagate(b)
helper.add_on_axis(flip2)
helper.propagate(c-15)
helper.add_on_axis(crys)
helper.propagate(15)
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
helper.set_geom(ls.get_geom())
helper.set_light_source(ls)
bs = helper.compute_beams()
last = bs[-1]
lastray = last.inner_ray()
ps = lastray.endpoint()
ps += (0,0,-5)
# ns = lastray.normal
ns = lastray.pos - ps


# AmpTyp2 = Composition(name=name, pos=ps, normal=ns)
AmpTyp2 = Composition(name=name)
AmpTyp2.pos = ps
AmpTyp2.normal=ns
ls = Beam(angle=0, radius=beam_diameter/2) # kollimierter Anfangsbeam
# AmpTyp2.set_geom(ls.get_geom())
AmpTyp2.set_light_source(ls)
AmpTyp2.add_fixed_elm(flip1)
AmpTyp2.add_fixed_elm(flip2)
AmpTyp2.add_fixed_elm(plane_mir)
AmpTyp2.add_fixed_elm(lens1)
AmpTyp2.add_fixed_elm(curved)
AmpTyp2.add_fixed_elm(crys)

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

AmpTyp2.pos = (0,0,50)
AmpTyp2.normal = (1,0,0)


# from LaserCAD.non_interactings import LaserPointer

# las = LaserPointer()
# las.draw()
# las.draw_mount()
# b = Beam()
# b.draw()


# =============================================================================
# Draw section
# =============================================================================
AmpTyp2.draw()
# helper.draw_elements()
# helper.draw_mounts()
# helper.draw_beams()



if freecad_da:
  setview()