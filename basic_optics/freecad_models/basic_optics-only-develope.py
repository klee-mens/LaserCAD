freecad_da = True

try:
  import FreeCAD
  from FreeCAD import Base, Vector, Placement, Rotation
  import Part
  import PartDesign
  import Sketcher
  from math import pi, sin, cos
  import time
except:
  freecad_da = False
  print("FreeCAD konnte nicht importiert werden")
import os
import numpy as np

# some basic functions, to open, clear, name and show the Document
# DOC = FreeCAD.activeDocument()
# DOC_NAME = "labor_116"

def clear_doc_old():
  """
  Clear the active document deleting all the objects
  """
  for obj in DOC.Objects:
    try:
      DOC.removeObject(obj.Name)
    except:
      continue

def clear_doc():
  """Close the <DOC_NAME> Document without saving and opens new one
  Currently not working"""
  FreeCAD.closeDocument(DOC_NAME)
  time.sleep(0.2)
  FreeCAD.newDocument(DOC_NAME)
  time.sleep(0.2)
  FreeCAD.setActiveDocument(DOC_NAME)
  DOC = FreeCAD.activeDocument()

def setview():
  """Rearrange View"""
  FreeCAD.Gui.SendMsgToActiveView("ViewFit")
  FreeCAD.Gui.activeDocument().activeView().viewAxometric()

def start_DOC(DOC):
  """Has to called to open the Document for the FreeCAD objects to show"""
  if DOC is None:
    FreeCAD.newDocument(DOC_NAME)
    FreeCAD.setActiveDocument(DOC_NAME)
    DOC = FreeCAD.activeDocument()
  else:
    clear_doc_old()
  return DOC

def warning(str):
  print(str)

DOC = FreeCAD.activeDocument()
DOC_NAME = "labor_116"
DOC = start_DOC(DOC)
# model_plate()

# EPS= tolerance to use to cut the parts (no clue, just copied)
EPS = 0.10
EPS_C = EPS * -0.5




def model_beam(name="beam", dia=10, prop=200,  f=130, clr="crimson", geom_info=None):
  """creates a red beam with length <prop>, diameter <dia>,
  fokus <f> and name ~
  example :  beam1 = model_beam("laser1", 10, 200, 100)
  beam1 = model_beam(name="laser1", dia=10, prop=200, f=-45)
  """
  if prop < f or f <= 0:
    # only one cone
    dia2 = dia*1.001 if f==0 else dia * (f-prop)/f
    obj = DOC.addObject("Part::Cone", name)
    obj.Height = prop
    obj.Radius1 = dia/2
    obj.Radius2 = dia2/2
  else:
    dia2 = 0 #1 altern
    obj1 = DOC.addObject("Part::Cone", name+"_1")
    obj1.Height = f
    obj1.Radius1 = dia/2
    obj1.Radius2 = dia2/2

    dia3 = dia * (prop-f)/f
    obj2 = DOC.addObject("Part::Cone", name+"_2")
    obj2.Height = prop-f
    obj2.Radius1 = dia2/2
    obj2.Radius2 = dia3/2
    obj2.Placement = FreeCAD.Placement(Vector(0,0,f), FreeCAD.Rotation(Vector(0,1,0),0), Vector(0,0,0))
    obj = DOC.addObject("Part::Fuse", name)
    obj.Base = obj1
    obj.Tool = obj2
    obj.Refine = True
    DOC.recompute()

  obj.Placement = FreeCAD.Placement(Vector(0,0,0), FreeCAD.Rotation(Vector(0,1,0),90), Vector(0,0,0))
  obj.ViewObject.ShapeColor = (0.86,0.08,0.24)
  obj.ViewObject.Transparency = 50
  update_geom_info(obj, geom_info)

  DOC.recompute()
  return obj



def model_lens(name="lens", dia=25, R1=50, R2=0, d=8, geom_info=None):
  """Beispiel
  #lens_1 = model_lens("lens01", 25, 50, 0, 10)
  #lens_1.Placement = FreeCAD.Placement(Vector(0,0,0), FreeCAD.Rotation(Vector(0,0,1),0), Vector(0,0,0))
  #lens_2 = model_lens("lens02", 25, 0, 150, 5)
  #lens_2.Placement = FreeCAD.Placement(Vector(0,50,0), FreeCAD.Rotation(Vector(0,0,1),0), Vector(0,0,0))
  #lens_3 = model_lens("lens03", 25, 100, -50, 10)
  #lens_3.Placement = FreeCAD.Placement(Vector(0,0,50), FreeCAD.Rotation(Vector(0,0,1),0), Vector(0,0,0))
  #lens_4 = model_lens("lens04", 25, -100, -50, 10)
  #lens_4.Placement = FreeCAD.Placement(Vector(0,50,50), FreeCAD.Rotation(Vector(0,0,1),0), Vector(0,0,0))
  """
  a = 1 if R1>0 else 0
  b = 1 if R2>=0 else 0

  obj = DOC.addObject('PartDesign::Body', name)
  sketch = obj.newObject('Sketcher::SketchObject', name+'_sketch')
  #sketch.Support = (DOC.getObject('XY_Plane'),[''])
  sketch.MapMode = 'FlatFace'

  sketch.addGeometry(Part.LineSegment(Vector(0,0,0),Vector(d,0,0)),False)
  sketch.addConstraint(Sketcher.Constraint('Coincident',0,1,-1,1))
  sketch.addConstraint(Sketcher.Constraint('PointOnObject',0,2,-1))
  sketch.addConstraint(Sketcher.Constraint('DistanceX',0,1,0,2,d))

  if R1 == 0:
    sketch.addGeometry(Part.LineSegment(Vector(0.000000,0.000000,0),Vector(0,10,0)),False)
    sketch.addConstraint(Sketcher.Constraint('Coincident',1,1,0,1))
    sketch.addConstraint(Sketcher.Constraint('PointOnObject',1,2,-2))
  else:
    sketch.addGeometry(Part.ArcOfCircle(Part.Circle(Vector(R1,0,0),Vector(0,0,1),abs(R1)),0.9*a*pi,0.9*a*pi+0.1*pi),False)
    sketch.addConstraint(Sketcher.Constraint('PointOnObject',1,3,-1))
    sketch.addConstraint(Sketcher.Constraint('Coincident',1,1+a,0,1))
    sketch.addConstraint(Sketcher.Constraint('Radius',1,abs(R1)))

  if R2 == 0:
    sketch.addGeometry(Part.LineSegment(Vector(5.000000,0.000000,0),Vector(5,10,0)),False)
    sketch.addConstraint(Sketcher.Constraint('Coincident',2,1,0,2))
    sketch.addConstraint(Sketcher.Constraint('Vertical',2))
  else:
    sketch.addGeometry(Part.ArcOfCircle(Part.Circle(Vector(d-R2,0,0),Vector(0,0,1),abs(R2)),0.9*pi-0.9*b*pi,pi-0.9*b*pi),False)
    sketch.addConstraint(Sketcher.Constraint('PointOnObject',2,3,-1))
    sketch.addConstraint(Sketcher.Constraint('Coincident',2,2-b,0,2))
    sketch.addConstraint(Sketcher.Constraint('Radius',2,abs(R2)))

  sketch.addGeometry(Part.LineSegment(Vector(0,10,0),Vector(10,10,0)),False)
  sketch.addConstraint(Sketcher.Constraint('Coincident',3,1,1,2-a))
  sketch.addConstraint(Sketcher.Constraint('Coincident',3,2,2,1+b))
  sketch.addConstraint(Sketcher.Constraint('Horizontal',3))
  sketch.addConstraint(Sketcher.Constraint('DistanceY',0,1,1,2-a,dia/2))

  rev = obj.newObject('PartDesign::Revolution',name+'_Revolution')
  rev.Profile = sketch
  rev.ReferenceAxis = (sketch,['H_Axis'])
  rev.Angle = 360.0
  rev.Reversed = 1
  sketch.Visibility = False

  obj.ViewObject.ShapeColor = (0.0, 0.32 , 0.0)
  obj.ViewObject.Transparency = 50
  update_geom_info(obj, geom_info)
  DOC.recompute()


  return obj





def model_cylincric_lens(name="cyl_lens", dia=25, h=30, R1=100, R2=-50, d=8, geom_info=None):
  """Example
  cyl_lens1 = model_cylincric_lens(name="cyl_len", dia=30, h=40, R1=100, R2=-50, d=8)
  cyl_lens2 = model_cylincric_lens(name="cyl_len", dia=30, h=40, R1=100, R2=0, d=8)
  """
  a = 1 if R1>=0 else 0
  b = 1 if R2>0 else 0

  obj = DOC.addObject('PartDesign::Body', name)
  sketch = obj.newObject('Sketcher::SketchObject', name+'_sketch')
  #sketch.Support = (DOC.getObject('XY_Plane'),[''])
  sketch.MapMode = 'FlatFace'


  sketch.addGeometry(Part.LineSegment(Vector(0.000000,0.000000,0),Vector(d,0,0)),True)
  sketch.addConstraint(Sketcher.Constraint('Coincident',0,1,-1,1))
  sketch.addConstraint(Sketcher.Constraint('PointOnObject',0,2,-1))
  sketch.addConstraint(Sketcher.Constraint('DistanceX',0,1,0,2,d))

  if R1 == 0:
    sketch.addGeometry(Part.LineSegment(Vector(0,10,0),Vector(0,-10,0)),False)
    sketch.addConstraint(Sketcher.Constraint('Symmetric',1,1,1,2,-1))
    sketch.addConstraint(Sketcher.Constraint('PointOnObject',-1,1,1))
  else:
    sketch.addGeometry(Part.ArcOfCircle(Part.Circle(Vector(R1,0,0),Vector(0,0,1),abs(R1)),-pi*a-0.1*pi,-pi*a+0.1*pi),False)
    sketch.addConstraint(Sketcher.Constraint('Symmetric',1,2-a,1,1+a,-1))
    sketch.addConstraint(Sketcher.Constraint('PointOnObject',-1,1,1))
    sketch.addConstraint(Sketcher.Constraint('Radius',1,abs(R1)))

  if R2 == 0:
    sketch.addGeometry(Part.LineSegment(Vector(10,10,0),Vector(10,-10,0)),False)
    sketch.addConstraint(Sketcher.Constraint('PointOnObject',0,2,2))
    sketch.addConstraint(Sketcher.Constraint('Symmetric',2,1,2,2,-1))
  else:
    sketch.addGeometry(Part.ArcOfCircle(Part.Circle(Vector(d-R2,0,0),Vector(0,0,1),abs(R2)),-1.1*pi+pi*b,-0.9*pi+pi*b),False)
    sketch.addConstraint(Sketcher.Constraint('Symmetric',2,1+b,2,2-b,-1))
    sketch.addConstraint(Sketcher.Constraint('PointOnObject',0,2,2))
    sketch.addConstraint(Sketcher.Constraint('Radius',2,abs(R2)))

  sketch.addGeometry(Part.LineSegment(Vector(0,10,0),Vector(10,10,0)),False)
  sketch.addConstraint(Sketcher.Constraint('Coincident',3,1,1,2-a))
  sketch.addConstraint(Sketcher.Constraint('Coincident',3,2,2,1+b))
  sketch.addConstraint(Sketcher.Constraint('Horizontal',3))

  sketch.addGeometry(Part.LineSegment(Vector(0,-10,0),Vector(10,-10,0)),False)
  sketch.addConstraint(Sketcher.Constraint('Coincident',4,1,1,1+a))
  sketch.addConstraint(Sketcher.Constraint('Coincident',4,2,2,2-b))

  sketch.addConstraint(Sketcher.Constraint('DistanceY',1,1+a,1,2-a,h))

  pad = obj.newObject('PartDesign::Pad',name+'_Pad')
  pad.Profile = sketch
  pad.Length = dia
  pad.Length2 = 100.000000
  pad.UseCustomVector = 0
  pad.Direction = (1, 1, 1)
  pad.Type = 0
  pad.UpToFace = None
  pad.Reversed = 0
  pad.Midplane = 0
  pad.Offset = 0
  sketch.Visibility = False
  DOC.recompute()
  obj.ViewObject.ShapeColor = (0.0, 0.32 , 0.0)
  obj.ViewObject.Transparency = 50
  obj.Placement = Placement = FreeCAD.Placement(Vector(0,0,-dia/2), FreeCAD.Rotation(Vector(0,0,1),0), Vector(0,0,0))
  update_geom_info(obj, geom_info)
  DOC.recompute()

  return obj


def model_mirror(name="mirror", dia=25, d=5, R=0, geom_info=None):
  """
  Example:
  mirror47 = mirror("mirror_47", dia=25, d=5, R=200)
  """
  obj = model_lens(name, dia, R1=-R, R2=0, d=d)
  obj.ViewObject.ShapeColor = (1.0,0.0,1.0)
  obj.ViewObject.Transparency = 50
  obj.Placement = FreeCAD.Placement(Vector(0,0,0), FreeCAD.Rotation(Vector(0,0,1),180), Vector(0,0,0))
  update_geom_info(obj, geom_info)

  DOC.recompute()
  return obj

def model_plate(name="plate", length=600, width=800, height=10, geom_info=None):
  mesh = True
  if mesh:
    obj = DOC.addObject("Mesh::Feature", name)
    #obj.Mesh = Mesh.Mesh(u"C:/Users/mens/Nextcloud/FreeCAD/opticslib/thorlabs/lochrasterplatte.stl")
    obj.Mesh = Mesh.Mesh(u"/home/mens/Nextcloud/FreeCAD/opticslib/thorlabs/lochrasterplatte.stl")
  else:
    obj = DOC.addObject("Part::Box",name)
    obj.Length = length
    obj.Width = width
    obj.Height = height
  obj.Placement = FreeCAD.Placement(Vector(-20,-20,-height),FreeCAD.Rotation(Vector(0,0,1),0))
  obj.Label = name
  DOC.recompute()
  return obj


if freecad_da:
  import ImportGui
  import Mesh

def lens_mount(name="lens_mount",  geom_info=None):
  mesh = True
  if mesh:
    obj = DOC.addObject("Mesh::Feature", name)
    obj.Mesh = Mesh.Mesh(u"C:/Users/mens/Nextcloud/FreeCAD/opticslib/thorlabs/LMR1_M-Step.stl")
  else:
    obj = ImportGui.insert(u"C:/Users/mens/Nextcloud/FreeCAD/opticslib/thorlabs/LMR1_M-Step.step","labor_116")
    #obj = ImportGui.insert(u"/home/mens/Nextcloud/FreeCAD/opticslib/thorlabs/LMR1_M-Step.step","labor_116")
    #obj = ImportGui.insert(u"/thorlabs/LMR1_M-Step.step","labor_116")
  rotate(obj, (0,1,0), -90)
  rotate(obj, (1,0,0), 90)
  offset = Vector(2,-9.5,-8.2)
  translate(obj, offset)
  update_geom_info(obj, geom_info, off0=offset)
  return obj

def mirror_mount(name="mirror_mount",  geom_info=None):
  mesh = True
  if mesh:
    obj = DOC.addObject("Mesh::Feature", name)
    obj.Mesh = Mesh.Mesh(u"C:/Users/mens/Nextcloud/FreeCAD/opticslib/thorlabs/POLARIS-K1-Step.stl")
    #obj.Mesh = Mesh.Mesh(u"/home/mens/Nextcloud/FreeCAD/opticslib/thorlabs/POLARIS-K1-Step.stl")
  else:
    obj = ImportGui.insert(u"C:/Users/mens/Nextcloud/FreeCAD/opticslib/thorlabs/POLARIS-K1-Step.step","labor_116")
    #obj = ImportGui.insert(u"C:/Users/mens/Nextcloud/FreeCAD/opticslib/thorlabs/KM100CP_M-Step.step","labor_116")
    #obj = ImportGui.insert(u"/home/mens/Nextcloud/FreeCAD/opticslib/thorlabs/LMR1_M-Step.step","labor_116")
    #obj = ImportGui.insert(u"/thorlabs/LMR1_M-Step.step","labor_116")
  rotate(obj, (0,1,0), 90)
  offset = Vector(-19,0,0)
  translate(obj, offset)
  update_geom_info(obj, geom_info, off0=offset)
  #obj.Label = name
  return obj


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
  DOC.recompute()
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

def update_geom_info(obj, geom_info, off0=0):
  if geom_info != None:
    pos = Vector(geom_info[0])
    normal = Vector(geom_info[1])
    set_normal(obj, normal, off0)
    translate(obj, pos)