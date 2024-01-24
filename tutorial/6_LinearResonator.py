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


if freecad_da:
  clear_doc()

# create a resonator, set position and wavelength
reso = LinearResonator()
reso.pos += (0,0,30)
reso.set_wavelength(1e-3)

# add the end mirror with certain aperture, propagate
mir1 = Mirror()
mir1.aperture = 2*inch
mir1.set_mount_to_default()
reso.add_on_axis(mir1)
reso.propagate(100)


# add a Lambda Plate (no influence, polarisation is not included), propagate
reso.add_on_axis(Lambda_Plate())
reso.propagate(100)

# add a flip mirror, propagate
reso.add_on_axis(Mirror(phi=90))
reso.propagate(450)


# add a flip mirror, propagate
reso.add_on_axis(Mirror(phi=90))
reso.propagate(150)

# add a Pockels Cell (no influence, polarisation is not included), propagate
# reso.add_on_axis(Pockels_Cell())
pc = Pockels_Cell()
pc.draw_dict["color"] = (0.3, 0.3, 0.4)
reso.add_on_axis(pc)
reso.propagate(250)

# Add a Curved End Mirror
reso.add_on_axis(Curved_Mirror(radius=2000))

# Draw ALL components and their mounts, compute the eigenmode (TEM00)
# and draws it aus gaussian beam (this may take some seconds)
reso.draw()


from LaserCAD.freecad_models.freecad_model_mirror import model_mirror


if freecad_da:
  model_mirror()
  setview()