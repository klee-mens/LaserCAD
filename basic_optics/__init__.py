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
from .beam import Beam,Gaussian_Beam
from .optical_element import Opt_Element
from .lens import Lens
from .mirror import Mirror, Curved_Mirror, Cylindrical_Mirror, Lam_Plane, Cylindrical_Mirror1
from .composition import Composition
from .moduls import Make_Telescope,Make_Periscope, Make_White_Cell,Make_Amplifier_Typ_I_simpler, Make_Amplifier_Typ_I_simple, Make_Amplifier_Typ_II_simple, Make_Stretcher, Make_Amplifier_Typ_II_simpler
from .constants import inch
from .grating import Grating
from .iris import Iris
from .intersection_plane import Intersection_plane
from .resonator import LinearResonator



