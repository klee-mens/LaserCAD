# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 16:55:29 2023

@author: mens
"""

# =============================================================================
# some usefull imports that should be copied to ANY project
# =============================================================================

"""
The following code does nothing than importing some usefull LaserCAD functions
The first block assures, that the LaserCAD package location is added to the 
sys.path list so that in can be importet AS LONG AS THE EXECUTED SCRIPT IS IN
THE SMAE FOLDER AS LaserCAD OR ABOVE!

Unfortunatey most python environments doesn't have the same default package 
location as FreeCAD so line 22-29 is more or less mandatory in every project

The clear_doc function creates a new document in FreeCAD and or delete all 
objects in it, that you can start from blank any time, the setview function 
sets the view after drawing the elements
"""

import sys
pfad = __file__
pfad = pfad.replace("\\","/") #folder conventions windows linux stuff
pfad = pfad.lower()
ind = pfad.rfind("lasercad")
pfad = pfad[0:ind-1]
if not pfad in sys.path:
  sys.path.append(pfad)


from LaserCAD.basic_optics import Mirror
from LaserCAD.freecad_models import freecad_da, clear_doc, setview


if freecad_da:
  clear_doc()
  



if freecad_da:
  setview()