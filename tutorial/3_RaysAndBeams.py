# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 10:28:14 2023

@author: 12816
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

from LaserCAD.basic_optics import Mirror, Curved_Mirror, Lens, Beam, Ray, Gaussian_Beam
from LaserCAD.freecad_models import freecad_da, clear_doc, setview

# =============================================================================
# about beams and rays
# =============================================================================

"""

Here you can see the rays and beams setting.
The class 'Ray' is the basic class of light source. Without considering the 
radius of the light ray, the ray only considers the position and direction of 
propagation of the ray. And the class 'Beam' is the most common light source.
Beam has three distrubtion: Cone, square and circular distrubtion. As for the 
cone distrubtion (default setting of beam), it shows some cylinders and cones 
to represent light beams. The square and circular distrubtion is some ray 
groups which has some different shapes.

"""

if freecad_da:
  clear_doc()
  
r1 = Ray()
r1.draw()

print()

b1 = Beam()
b1.pos += (0,100,0)
b1.set_length = 300
b1.draw()

print()
print()

b2 = Beam()
b2.pos += (0,-100,0)
b2.make_square_distribution(10)
b2.draw()

b3 = Beam()
b3.pos += (0,-200,0)
b3.make_circular_distribution(5)
b3.draw()

b4 = Gaussian_Beam()
b4.pos += (0,-300,0)
b4.draw()

print()
print()
