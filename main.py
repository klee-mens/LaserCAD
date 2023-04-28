# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 13:57:20 2023
hi
i@author: mens
"""


import sys
import os

pfad = __file__
pfad = pfad[0:-7] #nur wenn das Skript auch wirklich main.py heißt
sys.path.append(pfad)


from basic_optics.freecad_models import clear_doc, setview, freecad_da, freecad_model_lens

from basic_optics import Beam, Mirror, Opt_Element, Geom_Object, Curved_Mirror
from basic_optics import Lens, Ray, Composition, Grating, Propagation

# from basic_optics.mirror import curved_mirror_test
from basic_optics.tests import all_moduls_test

if freecad_da:
  clear_doc()

inch = 25.4
import numpy as np



from basic_optics.moduls import Make_Amplifier_Typ_II_Juergen
from basic_optics.tests import all_moduls_test

# all_moduls_test()

# amp = Make_Amplifier_Typ_II_Juergen()
# amp.draw()

from basic_optics.resonator import Resonator

res = Resonator()
m0 = Mirror()
le = Lens(f=250)
m1 = Mirror()
res = Resonator()
res.add_on_axis(m0)
res.propagate(500)
res.add_on_axis(le)
res.propagate(270)
res.add_on_axis(m1)


if freecad_da:

  setview()