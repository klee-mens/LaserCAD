# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 13:57:20 2023
hi
i@author: mens
"""


import numpy as np
import sys
import os
import numpy as np

pfad = __file__
pfad = pfad[0:-7] #nur wenn das Skript auch wirklich main.py heißt
sys.path.append(pfad)
inch = 25.4


from basic_optics.freecad_models import clear_doc, setview, freecad_da, freecad_model_lens
from basic_optics import Beam, Opt_Element, Geom_Object, Curved_Mirror, Mirror
from basic_optics import Lens, Ray, Composition, Grating, Propagation

from basic_optics.tests import all_moduls_test
from basic_optics.moduls import Make_Stretcher


if freecad_da:
  clear_doc()

inch = 25.4




from basic_optics.resonator import Resonator

# res = Resonator(name="2MirrorRes")
# g =1 -0.01
# L = 250
# R = L / (1-g)
# wavelength = 0.1
# res.wavelength = wavelength
# cm1 = Curved_Mirror(radius=R)
# cm2 = Curved_Mirror(radius=R)
# res.add_on_axis(cm1)
# res.propagate(L)
# res.add_on_axis(cm2)
# res.draw()

wavelength = 0.1
beta = -0.1
alpha = -3
focal_length = 250
print("alpha*beta = ", alpha*beta)

mat_fore = np.array([ [beta, focal_length*(1-alpha*beta)], [-1/focal_length, alpha] ])
mat_back = np.array([ [alpha, focal_length*(1-alpha*beta)], [-1/focal_length, beta] ])
mat_all = mat_back @ mat_fore

res2 = Resonator(name="3MirrorRes",pos=(0,0,100))
res2.wavelength = wavelength
dist1 = focal_length*(1-alpha)
dist2 = focal_length*(1-beta)
mir1 = Mirror()
mir2 = Mirror()
le1 = Lens(f=focal_length)

# mir2.pos = (dist1+dist2,0,100)
# mir2.normal = (1,0,0)
# le1.pos = (dist1,0,100)
# mir1.pos = (0,0,100)
# mir1.normal = (-1,0,0)
# res2.add_fixed_elm(mir1)
# res2.add_fixed_elm(le1)
# res2.add_fixed_elm(mir2)

res2.add_on_axis(mir1)
res2.propagate(dist1)
res2.add_on_axis(le1)
res2.propagate(dist2)
res2.add_on_axis(mir2)

res2.pos += (0, 300, 0)

res2.draw()

print()
print(mat_all)
print(res2.matrix())


if freecad_da:
  setview()