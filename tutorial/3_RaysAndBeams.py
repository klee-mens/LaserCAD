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


if freecad_da:
  clear_doc()

"""
Here, you can see a demonstration of the Ray and Beam class.
The class 'Ray' describes the one dimensional ray and only considers the
position and direction.

The draw function will again lead to text output when the script is executed
in a terminal and to new 3D model when executed in FreeCAD
"""

r1 = Ray()
r1.draw()
print()




"""
The class 'Beam' is the most common light source and describes 3D light bundles.
Beam has three distributions: Cone, square, and circular. As for the
cone distribution (default setting of a beam) shows some cylinders and cones
to represent light beams. The square and circular distributions are some ray
groups that have different shapes.
"""
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


"""
Now let's have a look at the inner structure of the beam

"""
print()
print()

b5 = Beam()
rays = b5.get_all_rays()
print("The standard beam has only", len(rays), "rays.")

"""
The standard beam has only 2 rays: One inner Ray for its position and
direction and one outer ray for its divergence and waist.
"""
print()
print(b5.inner_ray())
print(b5.outer_rays())
print()

"""
Inner ray is only one ray (element [0] of get all rays)

The outer rays are a list of rays, containing only one element in this case
"""

b5.pos += (7,-4,20)
b5.normal = (1,1,0)

print()
print(b5)
print(b5.get_all_rays())

"""
As you see, any change in position and axes of the beam will transform its
rays accordingly.
"""




print()
print()
