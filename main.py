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

# amp = Make_Amplifier_Typ_II_Juergen()
# amp.draw()

from basic_optics.resonator import Resonator

# res = Resonator()

from basic_optics.tests import all_moduls_test
from basic_optics.moduls import Make_Stretcher, Make_Amplifier_Typ_II_with_theta

# amp = Make_Amplifier_Typ_II_with_theta(roundtrips2=2)
# amp.draw_elements()
# amp.draw_mounts()
# amp.draw_rays()
# amp.draw_beams()

# b = Beam()
# b.normal = (1,1,0)
# b.draw()

stretch = Make_Stretcher()
# stretch.draw()
# stretch.draw_rays()
stretch.draw_elements()
stretch.draw_mounts()

# all_moduls_test()

if freecad_da:

  setview()