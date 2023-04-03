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

from basic_optics.moduls import Make_Amplifier_Typ_II_simpler, Make_Amplifier_Typ_II_UpDown

# amp2 = Make_Amplifier_Typ_II_simpler()
amp2 = Make_Amplifier_Typ_II_UpDown(roundtrips2=2)
amp2.pos = (0,0,120)
amp2.draw()
# amp2.draw_elements()


# results = all_moduls_test()



if freecad_da:

  setview()