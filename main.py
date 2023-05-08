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
from basic_optics import Beam, Mirror, Opt_Element, Geom_Object, Curved_Mirror
from basic_optics import Lens, Ray, Composition, Grating, Propagation

from basic_optics.tests import all_moduls_test
from basic_optics.moduls import Make_Stretcher


if freecad_da:
  clear_doc()

inch = 25.4




from basic_optics.resonator import Resonator

res = Resonator()
g = 0.2
L = 250
R = L / (1-g)
wavelength = 0.1
res.wavelength = wavelength
cm1 = Curved_Mirror(radius=R)
cm2 = Curved_Mirror(radius=R)
res.add_on_axis(cm1)
res.propagate(L)
res.add_on_axis(cm2)
res.draw()


if freecad_da:
  setview()