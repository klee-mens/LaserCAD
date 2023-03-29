# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 13:57:20 2023

i@author: mens
"""


import sys
import os

pfad = __file__
pfad = pfad[0:-7] #nur wenn das Skript auch wirklich main.py heißt
sys.path.append(pfad)

# import basic_optics.freecad_models as fcm
# from importlib import reload
# reload(fcm)

from basic_optics.freecad_models import clear_doc, setview, freecad_da, freecad_model_lens
from basic_optics import Beam, Mirror, Opt_Element, Geom_Object, Curved_Mirror, Lens,Iris,Diaphragms, Ray, Composition, inch, Grating, Propagation
from basic_optics.mirror import curved_mirror_test
from basic_optics.tests import all_moduls_test

if freecad_da:
  clear_doc()
  
peris, teles, amp, stretch, wcell = all_moduls_test()

from basic_optics.moduls import Make_Amplifier_Typ_I_simpler,Make_Stretcher,Make_Amplifier_Typ_II_simpler,Make_Amplifier_Typ_II_simple,Make_Amplifier_Typ_I_simple
from basic_optics.moduls import diaphragms_test




# b = Beam(angle=0, radius=2)
# m = Mirror(phi=90)

# c = Composition(name="alfred")
# c.set_light_source(b)
# c.propagate(150)
# c.add_on_axis(m)
# c.propagate(150)

# c.draw()

# stretch = Make_Stretcher()
# stretch.pos += (0,0,100)
# stretch.draw_elements()
# stretch.draw_rays()
# stretch.draw_mounts()

# amp = Make_Amplifier_Typ_II_simpler()
# amp.pos = (0,0,200)
# amp.draw()





if freecad_da:

  setview()

