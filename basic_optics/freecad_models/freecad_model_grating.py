# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 12:14:01 2023

@author: mens
"""


from .utils import freecad_da, update_geom_info, get_DOC, GEOM0
if freecad_da:
  from FreeCAD import Vector, Placement, Rotation
  import Part
  
DEFUALT_DIM = (50, 50, 8)
DEFUALT_COLOR = (170/255, 170/255, 1.0)  

def model_grating(name="grating", dimensions=DEFUALT_DIM, geom=GEOM0, 
                  color=DEFUALT_COLOR):
  """
  kreiert das Model eines Gitters durch simples Erzeugen eines Quaders

  Parameters
  ----------
  name : TYPE, optional
    DESCRIPTION. The default is "grating".
  dimensions : TYPE, optional
    DESCRIPTION. The default is DEFUALT_DIM.
  geom : TYPE, optional
    DESCRIPTION. The default is GEOM0.
  color : TYPE, optional
    DESCRIPTION. The default is DEFUALT_COLOR.

  Returns
  -------
  obj

  """
  DOC = get_DOC()
  obj = DOC.addObject("Part::Box",name)
  obj.Label = name
  obj.Height = dimensions[0]
  obj.Width = dimensions[1]
  obj.Length = dimensions[2]
  obj.ViewObject.ShapeColor = color
  offset = Vector(0, -obj.Width/2,-obj.Height/2)
  obj.Placement = Placement(offset, Rotation(0,0,0), Vector(0,0,0))

  update_geom_info(obj, geom, off0=offset)
  DOC.recompute()
  return obj