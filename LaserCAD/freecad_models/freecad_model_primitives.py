# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 20:23:45 2026

@author: mens
"""

from .utils import freecad_da, update_geom_info, get_DOC, rotate, thisfolder#,translate
from .freecad_model_lens import model_lens
from .freecad_model_composition import initialize_composition_old, add_to_composition
import numpy as np
import csv
import math

if freecad_da:
  from FreeCAD import Vector, Placement, Rotation
  import Mesh
  import ImportGui
  import Sketcher
  import Part
  from math import pi


def model_round_mirror(name="mirror", dia=25, thickness=5, Radius=0, geom=None, **kwargs):
  """
    Build a round mirror model with a certain diameter, thickness and radius

    Parameters
    ----------
    name : String, optional
        The name of the mirror. The default is "mirror".
    dia : float/int, optional
        The diameter of the mirror. The default is 25.
    thickness : float/int, optional
        The thickness of the mirror. The default is 5.
    Radius : float/int, optional
        The curvature of the mirror. 0 means plane mirror. The default is 0.
    geom : TYPE, optional
        The geometrical parameter of the mirror. The default is None.
    **kwargs : TYPE
        DESCRIPTION.

    Returns
    -------
    obj : TYPE
    object of mirror.

    Example:
    mirror47 = mirror("mirror_47", dia=25, d=5, R=200)
  """
  DOC = get_DOC()
  obj = model_lens(name, dia, Radius1=-Radius, Radius2=0, thickness=thickness)


  if "color" in kwargs.keys():
    obj.ViewObject.ShapeColor = kwargs["color"]
  else:
    obj.ViewObject.ShapeColor = DEFAULT_COLOR
  if "transparency" in kwargs.keys():
    obj.ViewObject.Transparency = kwargs["transparency"]
  else:
    obj.ViewObject.Transparency = DEFAULT_TRANSPARENCY
  update_geom_info(obj, geom)

  DOC = get_DOC()
  DOC.recompute()
  return obj

def model_cylinder(name="cylinder", dia=25, thickness=5, geom=None, **kwargs):
  return -1