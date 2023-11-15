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
from LaserCAD.freecad_models import freecad_da, clear_doc, setview

# =============================================================================
# about lenses, curved mirrors and spot diagrams
# =============================================================================

"""
Here you see some interaction of optical elements with Beams

Standard Beams (=cone distributet bemas with 2 rays, one inner and one outer)
are definded with a radius and an opening angle in radiant, 0 means colimated.

Lenses are defined directly with their focal length. Names are optional, 
they will apear in FreeCAD. 

Mirrors are defined with two deflection angles: phi gives the angle of 
deflection in the xy Plane, theta the tilt in z-Direction. So a normal Flip-
Mirror would have phi = +- 90, theta=0. Phi=180 is the default and means total
back reflection. You can use the formular phi = 180 - 2*AOI where AOI is the
anlge of incidence. All angles are in degrees. The combinatino phi=0, theta=0 
raises an error (grazing incidence).


"""


if freecad_da:
  clear_doc()
  

le1 = Lens(f=200, name="Lens1")
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


# =============================================================================
# ToDo: Curved Mirror -> He
# =============================================================================

if freecad_da:
  setview()
  

