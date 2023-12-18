# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 09:44:40 2023

@author: 12816
"""


import numpy as np
import sys

pfad = __file__
pfad = pfad.replace("\\","/") #folder conventions windows linux stuff
ind = pfad.rfind("/")
pfad = pfad[0:ind-1]
ind = pfad.rfind("/")
pfad = pfad[0:ind]
if not pfad in sys.path:
  sys.path.append(pfad)
  
  
from LaserCAD.basic_optics import Mirror,Beam
from LaserCAD.basic_optics.mirror import Stripe_mirror
from LaserCAD.basic_optics.mount import Mount

from LaserCAD.basic_optics.mount import MIRROR_LIST

a = Beam(radius=2,angle=0.1)
a.make_cone_distribution(9)
a.draw()
a.draw_dict['model'] = "ray_group"
a.draw()
