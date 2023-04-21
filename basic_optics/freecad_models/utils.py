# -*- coding: utf-8 -*-
"""
Created on Thu Aug 18 12:31:27 2022

@author: mens
"""

thisfolder = __file__[0:-8]

freecad_da = True
DOC_NAME = "labor_116"
inch = 25.4

import numpy as np
POS0 = np.array((0.0, 0.0, 80.0))
NORMAL0 = np.array((1.0, 0.0, 0.0))
GEOM0 = (POS0, NORMAL0)


try:
  import FreeCAD
  DOC = FreeCAD.activeDocument()
  print(DOC)
  from FreeCAD import Vector, Placement, Rotation
except:
  freecad_da = False
  DOC = None

# some basic functions, to open, clear, name and show the Document
# DOC = FreeCAD.activeDocument()
def clear_doc():
  """
  Clear the active document deleting all the objects
  """
  DOC = get_DOC()
  for obj in DOC.Objects:
    try:
      DOC.removeObject(obj.Name)
    except:
      continue

def setview():
  """Rearrange View"""
  FreeCAD.Gui.SendMsgToActiveView("ViewFit")
  FreeCAD.Gui.activeDocument().activeView().viewAxometric()

def start_DOC(DOC):
  """Has to called to open the Document for the FreeCAD objects to show
  
  """
  if DOC is None:
    FreeCAD.newDocument(DOC_NAME)
    FreeCAD.setActiveDocument(DOC_NAME)
    DOC = FreeCAD.activeDocument()
  else:
    clear_doc()
  return DOC

def warning(string):
  print(string)

def get_DOC():
  try:
    doc = FreeCAD.getDocument(DOC_NAME)
  except:
    FreeCAD.newDocument(DOC_NAME)
    FreeCAD.setActiveDocument(DOC_NAME)
    doc = FreeCAD.activeDocument()
  return doc





def translate(obj, vec):
  """Example:
  obj47 =  model_lens("lens01", 25, 50, 0, 10)
  obj42  = model_beam("laser1", 10, 200, 100)
  translate(obj47, Vector(1, 1, 0))
  """
  vec = Vector(vec)
  #obj.Placement.translate(vec)
  p0 = obj.Placement
  obj.Placement = Placement(vec, Rotation(Vector(0,0,1),0), Vector(0,0,0)).multiply(p0)
  return obj.Placement


def rotate(obj, vec, angle, off0=0):
  """Example:
  obj47 =  model_lens("lens01", 25, 50, 0, 10)
  obj42  = model_beam("laser1", 10, 200, 100)
  rotate(obj47, Vector(0, 0, 1), 55)
  """
  p0 = obj.Placement
  base = p0.Base
  vec = Vector(vec)
  off0 = Vector(off0)
  obj.Placement = Placement(Vector(0,0,0), Rotation(vec,angle), base-off0).multiply(p0)
  return obj.Placement

def set_normal(obj, normal, off0=0):
  default = Vector(1,0,0)
  angle = default.getAngle(normal)*180/np.pi
  vec = default.cross(normal)
  rotate(obj, vec, angle, off0)
  return obj.Placement

def set_z_normal(obj, normal, off0=0):
  default = Vector(0,0,1)
  angle = default.getAngle(normal)*180/np.pi
  vec = default.cross(normal)
  rotate(obj, vec, angle, off0)
  return obj.Placement

def update_geom_info(obj, geom_info, off0=0):
  if geom_info != None:
    pos = Vector(geom_info[0])
    normal = Vector(geom_info[1])
    # -----------------------------------
    if len(geom_info)>2:
      z_normal = Vector(geom_info[2])
      set_z_normal(obj, z_normal, off0)
    # -----------------------------------
    set_normal(obj, normal, off0)
    translate(obj, pos)
    
