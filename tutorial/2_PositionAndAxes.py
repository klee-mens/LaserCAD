# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 17:08:24 2023

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

from LaserCAD.basic_optics import Mirror
from LaserCAD.freecad_models import freecad_da, clear_doc, setview


if freecad_da:
  clear_doc()
  
"""
The following code creates a Mirror and plays around with its geometrical 
properties position <pos> and <normal>. The default values are pos = (0,0,80)
meaning a beam height of 80 mm and a normal = (1,0,0) so that any object points 
in x-Direction.

Btw ALL LENGTHS, EVEN WAVELENGTHS, MUST BE GIVEN IN mm!

"""

# =============================================================================
# Playground
# =============================================================================

mir1 = Mirror()
mir1.draw()

print()
print()
print("Position of mir1:", mir1.pos)
print("Normal of mir1:", mir1.normal)
print("Coordinate system of mir1\nx-Vector, y-Vector, z-Vector:", mir1.get_coordinate_system())


mir1.pos+= (10,50,30)

print()
print()
print("Position of mir1:", mir1.pos)
print("Normal of mir1:", mir1.normal)
print("Coordinate system of mir1\nx-Vector, y-Vector, z-Vector:", mir1.get_coordinate_system())


mir1.normal = (1,1,0)

print()
print()
print("Position of mir1:", mir1.pos)
print("Normal of mir1:", mir1.normal)
print("Coordinate system of mir1\nx-Vector, y-Vector, z-Vector:", mir1.get_coordinate_system())


"""
If executed in FreeCAD, the draw() function will construct and load the 
according 3D files. If executed in a "normal" shell, the draw() function will 
print out some usefull information about the object (which works with nearly any object).
Note that the coordinte system stays always orthonormal and right handed. Also
note, that the normal has always a norm of 1.
The draw_mount function in the end will draw the default mount and post of the
mirror and adjust them to the right position and direction.
"""

print()
print()
mir1.draw()
mir1.draw_mount()

# =============================================================================
# Playground End
# =============================================================================
if freecad_da:
  setview()