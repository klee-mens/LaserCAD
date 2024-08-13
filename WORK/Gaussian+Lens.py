# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 12:23:51 2024

@author: 12816
"""
from LaserCAD.basic_optics import Mirror,Beam,Cylindrical_Mirror,Grating,Ray
from LaserCAD.basic_optics import Intersection_plane,Cylindrical_Mirror1
from LaserCAD.basic_optics import Curved_Mirror, Composition,Rainbow,Lens

from LaserCAD.basic_optics import Unit_Mount,Composed_Mount,Gaussian_Beam
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
# i1 = 2061.844890839514

i2 = 2165.0635094610957
# L = 3485
L = (1965.0131327569663+1.12072420e+03+475)
a_group = []
f_group = []
L_group = []
for i in range(6):
  L = (1965.0131327569663+1.12072420e+03+475)*(i/10+0.5)
  L_group.append(L)
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
  a_group.append(a)
  f_group.append(f)
plt.figure()
plt.plot(L_group,a_group)
plt.xlabel("Length(mm)")
plt.ylabel("a(mm)")
plt.figure()
plt.plot(L_group,f_group)
plt.xlabel("Length(mm)")
plt.ylabel("focal length(mm)")

print(a,f)

if freecad_da:
  clear_doc()

# B =Gaussian_Beam(radius=1.25,angle=np.arctan(2400E-6/(np.pi*1.25)), wavelength=2400E-6)
# Comp = Composition()
# Comp.set_light_source(B)
# Comp.propagate(a)
# Comp.add_on_axis(Lens(f=f))
# Comp.propagate(L-a)
# Comp.draw()
# print(Comp._beams[-1].q_para.imag)
i_test = i1
# f_test = 771.6386056438225
# f_test = 1000
f_test = 480
lenses_d = f_test*2
step = f_test/15.42
first_l = 1600
B =Gaussian_Beam(radius=1.25,angle=np.arctan(2400E-6/(np.pi*1.25)), wavelength=2400E-6)

def Gaussian_Propagation(l=lenses_d):
  # print(B.q_para)
  Comp = Composition()
  # print(l)
  B =Gaussian_Beam(radius=1.25,angle=np.arctan(2400E-6/(np.pi*1.25)), wavelength=2400E-6)
  Comp.set_light_source(B)
  Comp.propagate(first_l)
  L1 = Lens(f=f_test)
  L2 = Lens(f=f_test)
  Comp.add_on_axis(L1)
  Comp.propagate(l)
  Comp.add_on_axis(L2)
  Comp.propagate(L-first_l-l)
  Comp.compute_beams()
  # print(Comp._beams[-1].q_para)
  return Comp._beams[-1].q_para.imag
# print(Gaussian_Propagation(100))
# print(Gaussian_Propagation(100.5))

count = 0
while abs(i_test-i2)>1E-9:
  count=count+1
  lenses_d1 = lenses_d
  lenses_d2 = lenses_d+step
  q1 =Gaussian_Propagation(l=lenses_d1)
  q2 =Gaussian_Propagation(l=lenses_d2)
  q_mid =Gaussian_Propagation(l=(lenses_d2+lenses_d1)/2)
  step = step/2
  if q_mid < i2:
    lenses_d=(lenses_d2+lenses_d1)/2
  i_test=q_mid
  # print(i_test)
  if count>1000:
    break
print((lenses_d2+lenses_d1)/2,i_test,i2)

Comp = Composition()
# print(l)
B =Gaussian_Beam(radius=1.25,angle=np.arctan(2400E-6/(np.pi*1.25)), wavelength=2400E-6)
Comp.set_light_source(B)
Comp.propagate(first_l)
L1 = Lens(f=f_test)
L2 = Lens(f=f_test)
Comp.add_on_axis(L1)
Comp.propagate((lenses_d2+lenses_d1)/2)
Comp.add_on_axis(L2)
Comp.propagate(L-first_l-(lenses_d2+lenses_d1)/2)
Comp.compute_beams()
print(Comp._beams[-1].q_para)

# Comp.draw()
  # print(Comp._beams[-1].q_para)
if freecad_da:
  setview()