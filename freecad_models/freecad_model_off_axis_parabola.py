#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 17 10:45:09 2025

@author: mens
"""
from .utils import freecad_da, update_geom_info, get_DOC
#import math

DEFALUT_MAX_ANGULAR_OFFSET = 10
DEFAULT_COLOR_LENS = (0/255,170/255,124/255)
LENS_TRANSPARENCY = 50
# LENS_TRANSPARENCY = 0

if freecad_da:
  from FreeCAD import Vector
  import Part
  import Sketcher
  from math import pi
  
  
def model_lens(name="lens", dia=25, Radius1=300, Radius2=0, thickness=3, geom=None, **kwargs):
  return -1