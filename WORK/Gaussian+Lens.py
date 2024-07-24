# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 12:23:51 2024

@author: 12816
"""
from LaserCAD.basic_optics import Mirror,Beam,Cylindrical_Mirror,Grating,Ray
from LaserCAD.basic_optics import Intersection_plane,Cylindrical_Mirror1
from LaserCAD.basic_optics import Curved_Mirror, Composition,Rainbow,Lens

from LaserCAD.basic_optics import Unit_Mount,Composed_Mount, Crystal,Gaussian_Beam
from LaserCAD.non_interactings import Pockels_Cell
from LaserCAD.non_interactings import Lambda_Plate

from LaserCAD.freecad_models import clear_doc, setview, add_to_composition
from LaserCAD.freecad_models import freecad_da
from LaserCAD.moduls import Make_RoofTop_Mirror, Make_Periscope
from LaserCAD.moduls.periscope import Rooftop_Mirror_Component

import matplotlib.pyplot as plt
import numpy as np

def calculate_a(L, i1, i2):
    # Coefficients for the quadratic equation a^2 + b*a + c = 0
    a_coef = 1
    b_coef = -(-2*i1*L) / (i2 - i1)
    c_coef = -(L**2 * i1 - i1**2 * i2 + i1 * i2**2) / (i2 - i1)
    # print(c_coef)
    
    # Calculate the discriminant
    discriminant = (b_coef ** 2) - 4 * a_coef * c_coef
    
    # Compute the two roots using the quadratic formula
    root1 = (-b_coef + np.sqrt(discriminant)) / (2 * a_coef)
    root2 = (-b_coef - np.sqrt(discriminant)) / (2 * a_coef)
    
    return root1, root2

i1 = 2045.3077171808552

i2 = 2041.1349901770946
L = 3070.68077879392
a=0
# a1 = L-np.sqrt(L*L-i1*i2+(i1*L*L)/(i1-i2))
# a2 = L+np.sqrt(L*L-i1*i2+(i1*L*L)/(i1-i2))

# f1 = a1 + i1*L/(i1-i2)
# f2 = a2 + i1*L/(i1-i2)

a1,a2 = calculate_a(L,i1,i2)
f1 = (a1*(i1+i2)-L*i1)/(i2-i1)
f2 = (a2*(i1+i2)-L*i1)/(i2-i1)
# f1 = a1-a1**2/L
# f2 = a2-a2**2/L
# print(a1,f1)
# print(a2,f2)

if a1>0 and a1<L:
  a=a1;f=f1
else:
  a=a2;f=f2

print(a,f)

if freecad_da:
  clear_doc()

B =Gaussian_Beam(radius=1.25,angle=np.arctan(2400E-6/(np.pi*1.25)), wavelength=2400E-6)
Comp = Composition()
Comp.set_light_source(B)
Comp.propagate(a)
Comp.add_on_axis(Lens(f=f))
Comp.propagate(L-a)
Comp.draw()
print(Comp._beams[1].q_para)

if freecad_da:
  setview()