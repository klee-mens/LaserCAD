#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 09:48:44 2023

@author: mens
"""
# =============================================================================
# some usefull imports that should be copied to ANY project
# =============================================================================
import sys
pfad = __file__
pfad = pfad.replace("\\","/") #folder conventions windows linux stuff
pfad = pfad.lower()
ind = pfad.rfind("lasercad")
pfad = pfad[0:ind-1]
if not pfad in sys.path:
  sys.path.append(pfad)

from LaserCAD.basic_optics import Mirror, Curved_Mirror, Lens, Beam, Ray
from LaserCAD.basic_optics import Intersection_plane,Cylindrical_Mirror
from LaserCAD.freecad_models import freecad_da, clear_doc, setview



if freecad_da:
  clear_doc()
  

"""
Here you see some interaction of optical elements with Beams

Standard Beams (=cone distributet bemas with 2 rays, one inner and one outer)
are definded with a radius and an opening angle in radiant, 0 means colimated.

Lenses are defined directly with their focal length. Names are optional, 
they will apear in FreeCAD.

The next_beam function which all Opt_Elements like Lens or Mirror have, 
transformes the incident beam to the outgoing beam. 
"""
le1 = Lens(f=200, name="LensOne")
le1.pos += (0,100,0)
le1.draw()

print()
print()

b1 = Beam(radius=4, angle=0)

le2 = Lens(f=250, name="lens2")
le2.pos += (42, 0, 0)
b2 = le2.next_beam(b1)

le2.draw()
b1.draw()
b2.draw()

print()
print()



"""
Mirrors are defined with two deflection angles: phi gives the angle of 
deflection in the xy Plane, theta the tilt in z-Direction. So a normal Flip-
Mirror would have phi = +- 90, theta=0. Phi=180 is the default and means total
back reflection. You can use the formular phi = 180 - 2*AOI where AOI is the
anlge of incidence. All angles are in degrees. The combinatino phi=0, theta=0 
raises an error (grazing incidence). 
"""
b11 = Beam(radius=4, angle=0)
b11.pos += (0,-100,0)

mir1 = Mirror(phi=120, name="Flipper")
mir1.pos += (42, -100, 0)
b21 = mir1.next_beam(b11)

mir1.draw()
b11.draw()
b21.draw()

print()
print()




"""
The Curved mirror has all values of the mirror and additionally a radius, 
which describes the curvature of the mirror. The outgoing beam will be deflected 
and focused. The usage is again via the next_beam function.
Here are some examples of how curved mirrors can focus beams. 
"""
b12 = Beam(radius=2,angle=0)
b12.pos += (0,200,0)

mir2 = Curved_Mirror(radius=400,phi=90)
mir2.pos += (50,200,0)
b22 = mir2.next_beam(b12)

mir2.draw()
b12.draw()
b22.draw()

print()
print()



"""
The 'Intersection_plane' can set up a plane and is primarily used to show a spot 
diagram of the beam on that plane. 
"""
b13 = Beam(radius=3,angle=0,distribution="square")
b13.pos += (0,300,0)

mir3 = Curved_Mirror(radius=400,phi=90)
mir3.pos += (150,300,0)
b23 = mir3.next_beam(b13)

ip = Intersection_plane()
ip.pos = mir3.pos + (0,200,0)
ip.normal = (0,-1,0)
b33 = ip.next_beam(b23)

mir3.draw()
b13.draw()
b23.draw()
b33.draw()
ip.draw()
ip.spot_diagram(b33)

print()
print()



"""
Besides, an anisotropic mirror named as
'Cylindrical_Mirror' is a special mirror with some certain radius in one 
direction and flat in the other.
"""
b14 = Beam(radius=5,distribution="circular")
b14.pos += (0,500,0)

mir4 = Cylindrical_Mirror(radius=200,phi=90)
mir4.pos += (200,500,0)
b24 = mir4.next_beam(b14)

mir4.draw()
b14.draw()
b24.draw()

if freecad_da:
  setview()
  

