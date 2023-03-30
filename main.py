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

# import basic_optics.freecad_models as fcm
# from importlib import reload
# reload(fcm)

from basic_optics.freecad_models import clear_doc, setview, freecad_da, freecad_model_lens

from basic_optics import Beam, Mirror,RayGroup, Opt_Element, Geom_Object, Curved_Mirror
from basic_optics import Lens,Iris,Barriers,Intersection_plane, Ray, Composition, inch, Grating, Propagation
#from basic_optics.composition import Teleskop_test, Composition_mirror_test, Mirror_Teleskop_test, add_only_elem_test

# from basic_optics.mirror import curved_mirror_test
# from basic_optics.tests import all_moduls_test

if freecad_da:
  clear_doc()

# peris, teles, amp, stretch, wcell = all_moduls_test()

from basic_optics.moduls import Make_Telescope,Make_Amplifier_Typ_I_simpler,Make_Stretcher,Make_Amplifier_Typ_II_simpler,Make_Amplifier_Typ_II_simple,Make_Amplifier_Typ_I_simple
from basic_optics.moduls import diaphragms_test





rg=RayGroup(waist=2.5,pos=(0,0,100))
rg.make_square_distribution(10)
dia1 = Composition(name="RayGroup test")
dia1.set_light_source(rg)
dia1.normal=(-1,0,0)
dia1.propagate(100)
m1=Mirror(phi=-90)
dia1.add_on_axis(m1)
dia1.propagate(150)
m2=Mirror(phi=-90)
dia1.add_on_axis(m2)
dia1.propagate(150)
l1=Lens(f=150)
dia1.add_on_axis(l1)
dia1.propagate(150)
ip1=Intersection_plane()
dia1.add_on_axis(ip1)
ip1.spot_diagram(dia1.compute_beams().pop())
dia1.propagate(150)
l2=Lens(f=150)
dia1.add_on_axis(l2)
dia1.propagate(300)
l3=Lens(f=150)
dia1.add_on_axis(l3)
dia1.propagate(150)
ip2=Intersection_plane()
dia1.add_on_axis(ip2)
dia1.propagate(150)
ip2.spot_diagram(dia1.compute_beams().pop())
# teles = Make_Telescope()
# teles.draw()




if freecad_da:

  setview()