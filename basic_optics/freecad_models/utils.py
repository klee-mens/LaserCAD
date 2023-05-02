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

# def update_geom_info(obj, geom_info, off0=0):
#   if geom_info != None:
#     pos = Vector(geom_info[0])
#     normal = Vector(geom_info[1])
#     set_normal(obj, normal, off0)
#     translate(obj, pos)

def update_pos_norm(obj, pos_norm=None, off0=0):
  # if pos_norm != None:
    pos = Vector(pos_norm[0])
    normal = Vector(pos_norm[1])
    set_normal(obj, normal, off0)
    translate(obj, pos)


def vec_phi_from_matrix(matrix):
  """
  Computes the rotation vector <vec> and angle <phi> from a given rotation 
  matrix. See "https://en.wikipedia.org/wiki/Rotation_matrix"

  Parameters
  ----------
  matrix : TYPE rotation matrix

  Returns
  -------
  phi, vec
  """
  val, vecs = np.linalg.eig(matrix)
  arg = ( np.trace(matrix)-1 ) / 2
  if arg > 1:
    # print("arg-gedöns:", arg)
    arg = 1
  elif arg < -1:
    # print("arg-gedöns:", arg)
    arg = -1
  phi = np.arccos(arg)
  for n in range(3):
    vec = vecs[:,n]
    if np.all(np.isreal(vec)):
      vec = np.real(vec)
      break
  # determine sign of phi
  a = vec[0]*vec[1]*(1-np.cos(phi)) - vec[2]*np.sin(phi)
  b = matrix[0,1]
  if np.isclose(a, b):
    return vec, phi
  else:
    return vec, -phi
  # print("something is strange with this rotation matrix")
  # return None0

def rotation_to_axis_angle(R):
    """
    Computes the rotation vector and angle from a given rotation matrix.

    Args:
        R (numpy.ndarray): A 3x3 rotation matrix.

    Returns:
        Tuple of a numpy.ndarray (rotation vector) and a float (rotation angle).

    Raises:
        ValueError: If the input matrix is not a valid rotation matrix.
    """

    # Check that R is a valid rotation matrix
    # if not np.allclose(np.dot(R.T, R), np.identity(3)):
    #     raise ValueError("Input matrix is not a valid rotation matrix.")

    # Compute the angle of rotation
    phi = (np.trace(R) - 1) / 2
    if phi>1:
      phi = 1 
    if phi<-1:
      phi=-1
    phi = np.arccos(phi)

    # Compute the rotation vector
    if np.abs(phi) < 1e-6:
        vec = (1,0,0)
    elif np.abs(phi - np.pi) < 1e-6:
        # In the case of a 180 degree rotation, the axis of rotation can be any vector
        # perpendicular to any of the columns of R that correspond to an eigenvalue of -1.
        eigenvalues, eigenvectors = np.linalg.eig(R)
        eigenvectors = eigenvectors.T
        mask = np.isclose(eigenvalues, -1)
        if np.count_nonzero(mask) == 0:
            raise ValueError("Input matrix is not a valid rotation matrix.")
        elif np.count_nonzero(mask) == 1:
            i = np.argmax(mask)
            vec = eigenvectors[i]
        else:
            # There are two possible axes of rotation
            i, j = np.where(mask)[0]
            vec1 = eigenvectors[i]
            vec2 = eigenvectors[j]
            vec = np.cross(vec1, vec2)
            vec /= np.linalg.norm(vec)
    else:
        vec = np.array([R[2, 1] - R[1, 2], R[0, 2] - R[2, 0], R[1, 0] - R[0, 1]])
        vec /= (2 * np.sin(phi))

    return vec, phi

def update_geom_info(obj, geom_info, off0=0):
  if geom_info != None:
    pos = Vector(geom_info[0])
    axes = geom_info[1]
    if off0!=0 or np.shape(axes)==(3,):
      if np.shape(axes)==(3,):
        normal=axes
      else:
        normal=axes[:,0]
      pos_norm=np.array((geom_info[0],normal))
      update_pos_norm(obj,pos_norm,off0=off0)
    else:
      # print(axes)
      rotvec, phi = rotation_to_axis_angle(axes)
      rotvec = Vector(rotvec)
      phi *= 180/np.pi
      # print(rotvec, phi)
      # print(rotvec,phi)
      place0 = obj.Placement
      obj.Placement = Placement(pos, Rotation(rotvec,phi), Vector(0,0,0)).multiply(place0)
