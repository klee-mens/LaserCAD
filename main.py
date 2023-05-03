# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 13:57:20 2023
hi
i@author: mens
"""


import numpy as np
import sys
import os

pfad = __file__
pfad = pfad[0:-7] #nur wenn das Skript auch wirklich main.py heißt
sys.path.append(pfad)


from basic_optics.freecad_models import clear_doc, setview, freecad_da, freecad_model_lens

from basic_optics import Beam, Mirror, Opt_Element, Geom_Object, Curved_Mirror
from basic_optics import Lens, Ray, Composition, Grating, Propagation

from basic_optics.tests import all_moduls_test

if freecad_da:
  clear_doc()

inch = 25.4



from basic_optics.moduls import Make_Amplifier_Typ_II_Juergen, Make_White_Cell

wc = Make_White_Cell(roundtrips4=2, mirror_sep=20)
wc.pos = (0,0,80)
wc.draw()

# amp = Make_Amplifier_Typ_II_Juergen()
# amp.draw()

# all_moduls_test()


from basic_optics.resonator import Resonator
# res = Resonator()


# all_moduls_test()

if freecad_da:

  setview()