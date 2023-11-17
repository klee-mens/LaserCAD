# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 18:06:09 2023

@author: mens
"""


# =============================================================================
# some usefull imports that should be copied to ANY project
# =============================================================================
import sys
pfad = __file__
pfad = pfad.replace("\\","/") #folder conventions windows linux stuff
pfad = pfad.lower()
ind = pfad.rfind("lasercad")
pfad = pfad[0:ind-1]
if not pfad in sys.path:
  sys.path.append(pfad)

from LaserCAD.basic_optics import Mirror, Curved_Mirror, Lens, Composition, Beam, Ray, Grating
from LaserCAD.GUI.tk_GUI import GUI
from LaserCAD.freecad_models import freecad_da, clear_doc, setview

# =============================================================================
# about GUI
# =============================================================================

"""
This is a simple introduction to user interfaces that make modeling easier. 
When running this code you will be able to see several buttons, please press
 'set light source' first to create a light source. After that you can add the
 optics you want. When this code is run in FreeCAD, every time an optic is 
 added it will be automatically modeled in FreeCAD. At the same time, the 
 button 'Generate Code' will generate a code that can be modeled and saved.
"""

if freecad_da:
  clear_doc()

GUI()