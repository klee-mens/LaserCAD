# -*- coding: utf-8 -*-
"""
Created on Thu Aug 18 10:42:15 2022

@author: mens

Dieses Paket beinhaltet die Definitionen aller abstrakten Objekte der
Optikworkbench, wie Geom_Object, Ray, Lightsource, Lens, Mirror, Assembly,
Beam etc

im Unterpaket freecad_models befinden sich die entsprechende Anleitungen zum
Erstellen der 3D Obejkte in FreeCAD

"""

from .geom_object import Geom_Object, TOLERANCE
from .ray import Ray
from .beam import Beam
from .optical_element import Opt_Element
from .lens import Lens
from .propagation import Propagation
from .mirror import Mirror, Curved_Mirror
from .composition import Composition
from .moduls import Make_Telescope,Make_Periscope, Make_White_Cell,Make_Amplifier_Typ_I_simpler, Make_Amplifier_Typ_I_simple, Make_Amplifier_Typ_II_simple, Make_Stretcher, Make_Amplifier_Typ_II_simpler
from .constants import inch
from .grating import Grating

pfad = __file__[0:-9]

# print("-----das Paket wird auch importiert-----")

# freecad_da = True
# try:
#   import FreeCAD
#   from basic_optics import start_DOC
# except:
#   freecad_da = False


# if freecad_da:
#   DOC = FreeCAD.activeDocument()
#   DOC_NAME = "labor_116"
#   DOC = start_DOC(DOC)