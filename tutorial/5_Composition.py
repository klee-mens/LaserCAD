# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 18:07:15 2023

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

from LaserCAD.basic_optics import Mirror, Lens, Beam, Composition
from LaserCAD.freecad_models import freecad_da, clear_doc, setview

# =============================================================================
# like LensesAndMirrors but with Compositions
# =============================================================================

"""
Quick intro to compositions. Output is similar to the one in LensesAndMirrors 
but the positioning is automatized by the Composition.

You create the composition and add alternating propagations and element. All
elements will be placed on the optical axes in the exact position automatically. 
The draw() command is an abreviation for draw_elements, draw_beams and draw_mounts

The whole output is grouped in an "Part-Feature" in FreeCAD, you can for
example blend mounts in and out.
"""


if freecad_da:
  clear_doc()
  

comp1 = Composition(name="FokusLens")
b1 = Beam(radius=4, angle=0)
comp1.set_light_source(b1)

comp1.propagate(42)

le2 = Lens(f=250, name="lens2")
comp1.add_on_axis(le2)

comp1.propagate(200)

comp1.draw_elements()
comp1.draw_beams()
comp1.draw_mounts()

print()
print()

comp2 = Composition(name="FlipMirror")
b2 = Beam(radius=4, angle=0)
comp2.set_light_source(b2)

comp2.propagate(42)
mir1 = Mirror(phi=120, name="Flipper")
comp2.add_on_axis(mir1)
comp2.propagate(123)

comp2.pos += (0,-100,0)
comp2.draw()



if freecad_da:
  setview()