# -*- coding: utf-8 -*-
"""
Created on Thu Aug 18 12:29:04 2022

@author: mens
"""


from .utils import freecad_da, update_geom_info, get_DOC, GEOM0, rotate
from .freecad_model_ray import model_ray_1D
import numpy as np
  
ARROW_LENGTH = 12


def model_geom_object(name="GeomObj", geom=GEOM0, **kwargs):
  """
  zeichnet ein Koordinatensystem bestehend aus drei Rays1D in den Farben RGB
  und richtet es entprechend des GEOM0 aus
  """
  DOC = get_DOC()
  mainpart = DOC.addObject('App::Part', name)
  mainpart.Label = name
  pos0 = (0,0,0)
  axes0 = np.eye(3)
  raygeom = (pos0, axes0)
  xray = model_ray_1D(name=name+"_x", length=ARROW_LENGTH, geom=raygeom, color=(1.0,0.0,0.0))
  yray = model_ray_1D(name=name+"_y", length=ARROW_LENGTH, geom=raygeom, color=(0.0,1.0,0.0))
  rotate(yray, vec=(0,0,1), angle=90)
  zray = model_ray_1D(name=name+"_z", length=ARROW_LENGTH, geom=raygeom, color=(0.0,0.0,1.0))
  rotate(zray, vec=(0,1,0), angle=-90)
  
  xray.adjustRelativeLinks(mainpart)
  mainpart.addObject(xray)
  yray.adjustRelativeLinks(mainpart)
  mainpart.addObject(yray)
  zray.adjustRelativeLinks(mainpart)
  mainpart.addObject(zray)
  
  update_geom_info(obj=mainpart, geom_info=geom)
  return mainpart