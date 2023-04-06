# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 11:11:57 2023

@author: mens
"""

import sys

pfad = __file__
pfad = pfad.replace("\\", "/") #just in case
ind = pfad.rfind("/")
pfad = pfad[0:ind+1]
sys.path.append(pfad)

from basic_optics import Mirror,Lens,Gaussian_Beam
from basic_optics.freecad_models import clear_doc, setview, freecad_da
from basic_optics.freecad_models.freecad_model_mirror import mirror_mount
from basic_optics.freecad_models.freecad_model_beam import model_Gaussian_beam

if freecad_da:
  clear_doc()


# m = Mirror(name="Standard_Mirror", pos=(0,0,60))
# m.normal = (1,1,0)
# m.draw_dict["mount_type"] = "POLARIS-K1"
# m.aperture = 25.4
# m.draw()
# m.draw_mount()

# b=model_Gaussian_beam("laser1", -100+100j, 200, 1030E-3)
# m=Mirror(pos=(0,0,100))
# m.draw()
# m.draw_mount()
gb1 = Gaussian_Beam(wavelength=1030E-6,pos=(0,0,100))
# gb1.q_para = 10E5j
le = Lens(f=100,pos = (100,0,100))
mr = Mirror(phi=90, pos = (295,0,100))
mr.aperture = 100
gb2 = le.next_gauss(gb1)
gb3 = mr.next_gauss(gb2)
gb1.draw()
le.draw()
mr.draw()
gb2.draw()
gb3.draw()

if freecad_da:
  setview()
