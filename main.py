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


from basic_optics.freecad_models import clear_doc, setview, freecad_da
from basic_optics import Beam, Mirror, Opt_Element, Geom_Object, Curved_Mirror
from basic_optics import Lens, Ray, Composition, Grating, Propagation
from basic_optics.freecad_models import input_output_test
# from basic_optics.tests import all_moduls_test
from basic_optics.moduls import Make_Stretcher, Make_Telescope


from basic_optics.tests import all_moduls_test, three_resonators_test


if freecad_da:
  clear_doc()

a,b,c,d,e = all_moduls_test()

r1,r2,r3 = three_resonators_test()


if freecad_da:
  setview()