# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 13:00:00 2023

@author: mens
"""

import numpy as np
import sys

pfad = __file__
pfad = pfad.replace("\\","/") #folder conventions windows linux stuff
pfad = pfad.lower()
ind = pfad.rfind("lasercad")
pfad = pfad[0:ind-1]
if not pfad in sys.path:
  sys.path.append(pfad)
  
  
from LaserCAD.freecad_models import clear_doc, setview, freecad_da
from LaserCAD.basic_optics import Mirror, Beam, Composition, inch
from LaserCAD.basic_optics import Curved_Mirror, Ray, Component
from LaserCAD.basic_optics import LinearResonator, Lens
from LaserCAD.basic_optics import Crystal
from LaserCAD.non_interactings import Faraday_Isolator, Pockels_Cell, Lambda_Plate

from LaserCAD.freecad_models.utils import load_STL

if freecad_da:
  clear_doc()

# c1 = Component()
# c1.freecad_model = load_STL
# c1.draw_dict["stl_file"] = "C:\\Users\\mens\\AppData\\Local\\Programs\\Spyder\\pkgs\\LaserCAD\\freecad_models\\/mount_meshes/adjusted mirror mount/POLARIS-K1.stl"
# c1.draw()




reso = LinearResonator()
reso.pos += (0,0,30)
reso.set_wavelength(1e-3)

mir1 = Mirror()
mir1.aperture = 2*inch
# mir1.draw()
# mir1.draw_mount()

reso.add_on_axis(mir1)

reso.propagate(100)

reso.add_on_axis(Lambda_Plate())

reso.propagate(100)

reso.add_on_axis(Mirror(phi=90))



reso.propagate(450)

reso.add_on_axis(Mirror(phi=90))

reso.propagate(150)

reso.add_on_axis(Pockels_Cell())

reso.propagate(250)


reso.add_on_axis(Curved_Mirror(radius=2000))

reso.draw()



if freecad_da:
  setview()