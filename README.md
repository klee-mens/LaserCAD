# LaserCAD
Procrastination next level



# How to use:
Install FreeCAD
download the repository
Execute the main.py in FreeCAD (like a macro)

examples can be found in basic_optics.moduls and in from basic_optics.tests


# Example main.py


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

from basic_optics.tests import all_moduls_test

peris, teles, amp, stretch, wcell = all_moduls_test()


if freecad_da:
  setview()
