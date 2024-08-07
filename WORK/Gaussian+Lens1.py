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


R1 = 2045.3077171808552
# i1 = 2061.844890839514
R2 = 2165.0635094610957
# L = 3485
f =480
phi = 1/f
a = 2500
alpha = 1 - a/f


# Coefficients for the quadratic equation a^2 + b*a + c = 0
a_coef = (phi**2 * alpha**2+phi**4 * R1**2)
b_coef = 2 * phi * alpha
c_coef = 1 - R1/R2
# print(c_coef)

# Calculate the discriminant
discriminant = (b_coef ** 2) - 4 * a_coef * c_coef

# Compute the two roots using the quadratic formula
root1 = (-b_coef + np.sqrt(discriminant)) / (2 * a_coef)
root2 = (-b_coef - np.sqrt(discriminant)) / (2 * a_coef)

delta = max(root1, root2)
C = phi**2 * delta
D = -1 - phi * delta * alpha
dev = D**2 + C**2*R1**2

z2 = 1045
b = (dev*z2+C*R1**2*(1+phi*delta)-D*(2*f-a+delta*alpha)) / ((C*R1**2-D)*(phi*delta)/f - D)
print(delta,b)

Comp = Composition()
B =Gaussian_Beam(radius=1.25,angle=np.arctan(2400E-6/(np.pi*1.25)), wavelength=2400E-6)
Comp.set_light_source(B)
Comp.propagate(a)
L1 = Lens(f=f)
L2 = Lens(f=f)
Comp.add_on_axis(L1)
Comp.propagate(2*f+delta)
Comp.add_on_axis(L2)
Comp.propagate(b)
Comp.compute_beams()
print(Comp._beams[-1])