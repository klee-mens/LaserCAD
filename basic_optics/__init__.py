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
from .beam import Beam, CircularRayBeam, Gaussian_Beam, RainbowBeam, SquareBeam, Ray_Distribution
from .optical_element import Opt_Element
from .lens import Lens
from .mirror import Mirror, Curved_Mirror, Cylindrical_Mirror,Cylindrical_Mirror1,Stripe_mirror
from .composition import Composition
from .constants import inch
from .grating import Grating
from .intersection_plane import Intersection_plane
from .resonator import LinearResonator
from .component import Component
from .mount import Unit_Mount, Grating_Mount, Composed_Mount, Stripe_Mirror_Mount, Rooftop_Mirror_Mount, Post
from .post import Post_and_holder
from .refractive_plane import Refractive_plane
from .off_axis_parabola import Off_Axis_Parabola
from .beam_splitter import ThinBeamsplitter, ThickBeamsplitter, TFP56
from .non_linear_crystal import NLO_Crystal