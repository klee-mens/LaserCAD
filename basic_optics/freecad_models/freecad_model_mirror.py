# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 16:28:18 2022

@author: mens
"""


from .utils import freecad_da, update_geom_info, get_DOC, rotate, translate, thisfolder
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
 
DEFAULT_COLOR_JOERG = (0.8,0.2,0.8)
DEFAULT_COLOR = (199/255, 144/255, 28/255) #Messing
DEFAULT_TRANSPARENCY = 50
DEFALUT_MAX_ANGULAR_OFFSET = 10


def model_mirror(model_type="DEFAULT", **kwargs):
  """
  Example:
  mirror47 = mirror("mirror_47", dia=25, d=5, R=200)
  """
    
  if model_type == "DEFAULT" or model_type == "Round":
    obj = model_round_mirror(**kwargs)
  elif model_type == "Stripe":
    obj = model_stripe_mirror(**kwargs)
     
  return obj


def model_round_mirror(name="mirror", dia=25, thickness=5, Radius=0, geom=None, **kwargs):
  """
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


def model_stripe_mirror(name="Stripe_Mirror", dia=75, Radius1=250, thickness=25, 
                        height=10, geom=None, **kwargs):
  DOC = get_DOC()
  """Beispiel
  s.o.
  """
  
  Radius1 *= -1
  a = 1 if Radius1>0 else 0

  obj = DOC.addObject('PartDesign::Body', name)
  sketch = obj.newObject('Sketcher::SketchObject', name+'_sketch')
  #sketch.Support = (DOC.getObject('XY_Plane'),[''])
  sketch.MapMode = 'FlatFace'

  sketch.addGeometry(Part.ArcOfCircle(Part.Circle(Vector(Radius1,0,0),Vector(0,0,1),abs(Radius1)),0.9*a*pi,0.9*a*pi+0.2*pi),False)
  sketch.addConstraint(Sketcher.Constraint('PointOnObject',-1,1,0)) 
  sketch.addConstraint(Sketcher.Constraint('Symmetric',0,1,0,2,-1)) 
  sketch.addConstraint(Sketcher.Constraint('Radius',0,Radius1)) 
  sketch.addConstraint(Sketcher.Constraint('DistanceY',0,2,0,1,dia)) 


  sketch.addGeometry(Part.LineSegment(Vector(1.0,dia/2,0.0),Vector(thickness,dia/2,0.0)),False)
  sketch.addConstraint(Sketcher.Constraint('Coincident',1,1,0,1)) 
  sketch.addConstraint(Sketcher.Constraint('Horizontal',1)) 
  sketch.addGeometry(Part.LineSegment(Vector(thickness,dia/2,0.0),Vector(thickness,-dia/2,0.0)),False)
  sketch.addConstraint(Sketcher.Constraint('Coincident',2,1,1,2)) 
  sketch.addConstraint(Sketcher.Constraint('Vertical',2)) 
  sketch.addGeometry(Part.LineSegment(Vector(thickness,-dia/2,0),Vector(1,-dia/2,0)),False)
  sketch.addConstraint(Sketcher.Constraint('Coincident',3,1,2,2)) 
  sketch.addConstraint(Sketcher.Constraint('Coincident',3,2,0,2)) 
  sketch.addConstraint(Sketcher.Constraint('Horizontal',3)) 
  sketch.addConstraint(Sketcher.Constraint('DistanceX',-1,1,2,2,thickness)) 

  pad = obj.newObject('PartDesign::Pad','Pad')
  pad.Profile = sketch
  pad.Length = height
  pad.ReferenceAxis = (sketch,['N_Axis'])
  pad.Midplane = 1
  sketch.Visibility = False
  
  if "color" in kwargs.keys():
    obj.ViewObject.ShapeColor = kwargs["color"]
  else:
    obj.ViewObject.ShapeColor = (204/255, 204/255, 204/255)
  if "transparency" in kwargs.keys():
    obj.ViewObject.Transparency = kwargs["transparency"]
  else:
    obj.ViewObject.Transparency = 0
  update_geom_info(obj, geom)

  DOC = get_DOC()
  DOC.recompute()
  
  return obj








# =============================================================================
# Begin Working area of He Zhuang
# =============================================================================


def mirror_mount(mount_name="mirror_mount", mount_type="default",  
                 geom=None, only_info=False, drawing_post=True, 
                 dia=25.4, **kwargs):
  mesh = True
  mount_fix = True
  flag_new= False
  mount_rotation = False
  if abs(geom[1][2])<DEFALUT_MAX_ANGULAR_OFFSET/180*pi:
    geom[1][2]=0
  else:
    print("this post should't be placed on the XY plane")
    mount_rotation=True
  if mount_type == "default":
    if dia<= 25.4/2:
      mount_type = "POLARIS-K05"
    elif dia <= 25.4:
      mount_type = "POLARIS-K1"
    elif dia <= 25.4*1.5:
      mount_type = "POLARIS-K15S4"
    elif dia <=25.4*2:
      mount_type = "POLARIS-K2"
    elif dia <=25.4*3:
      mount_type = "POLARIS-K3S5"
    elif dia <=25.4*4:
      mount_type = "KS4"
    else:
      print("there is no suitable default mount in the database. Going back to construct a new mount.")
  buf = []
  with open(thisfolder+"mirrormounts.csv") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
      buf.append(row)
  
  for mount_loop in buf:
    if mount_loop["name"] == mount_type:
      flag_new = True
      aperture = float(mount_loop["aperture"])
      height = float(mount_loop["height"])
      price = float(mount_loop["price"])
      xshift = float(mount_loop["xshift"])
      offset = Vector(float(mount_loop["offsetX"]),
                      float(mount_loop["offsetY"]),
                      float(mount_loop["offsetZ"]))
      rotation = Rotation(float(mount_loop["rot_angleZ"]),
                          float(mount_loop["rot_angleY"]),
                          float(mount_loop["rot_angleX"]))
      if not mount_fix:
        place = Placement(offset, rotation, Vector(0,0,0))
  if not flag_new:
    if mount_type != "default":
      print("This mount type is not in the database. Going back to construct a new mount.")
    height=dia/2+10
    xshift=0
    new_mount = building_mount(Radius1=dia/2,height=height,geom=geom)
    if  drawing_post:
      if (geom[0][2]-height<39) or (geom[0][2]-height>101):
        print("Warning, there is no suitable post holder and slotted base at this height")

      if height < geom[0][2]-59:
        post = draw_post2(name="TR50_M", height=-50-height,xshift=xshift, 
                          geom=geom)
        post1 = draw_post2(name="BA1L", height=0,xshift=xshift, geom=geom)
        post2 = draw_post2(name="PH50_M", height=0,xshift=xshift, geom=geom)
      else:
        post = draw_post2(name="TR30_M", height=-30-height,xshift=xshift, 
                          geom=geom)
        post1 = draw_post2(name="BA2_M", height=0,xshift=xshift, geom=geom)
        post2 = draw_post2(name="PH20E_M", height=0,xshift=xshift, geom=geom)
    else:
      DOC = get_DOC()
      DOC.recompute()
      return new_mount
    part = initialize_composition_old(name="mount, post and base")
    container = post,post1,post2,new_mount
    add_to_composition(part, container)

    return part

  if only_info:
    data = {"aperture":aperture, "height":height, "price":price}
    return data
  if mount_fix:
    datei = thisfolder + "mount_meshes\\adjusted mirror mount\\" + mount_type
  else:
    datei = thisfolder + "mount_meshes\\mirror\\" + mount_type
  if mesh:
    DOC = get_DOC()
    obj = DOC.addObject("Mesh::Feature", mount_name)
    datei += ".stl"
    obj.Mesh = Mesh.Mesh(datei)
  else:
    datei += ".step"
    obj = ImportGui.insert(datei, "labor_116")
    
  # if mount_rotation and mount_fix:
  #   obj.Placement = Placement(Vector(0,0,0), Rotation(0,0,90), Vector(0,0,0))
  #   if  drawing_post:
  #     post = draw_post_special(name="TR50_M", height=50+height,xshift=xshift,
  #                       geom=geom)
  #     post2 = draw_post_special(name="PH50_M", height=0,xshift=xshift, geom=geom)
  #     post1 = draw_post_special(name="new", height=0,xshift=xshift, geom=geom)
  #     update_geom_info(obj,geom)
  #     obj.Label = mount_name
  #     part = initialize_composition_old(name="mount, post and base")
  #     container = post,post1,post2,obj
  #     add_to_composition(part, container)
  #     DOC.recompute()
  #     return part
  if not mount_fix:
    obj.Placement = place
    update_geom_info(obj, geom, off0=offset)
  else:
    update_geom_info(obj,geom)
  obj.Label = mount_name
  
  if  drawing_post:
    if (geom[0][2]-height<39) or (geom[0][2]-height>101):
      print("Warning, there is no suitable post holder and slotted base at this height")

    if height < geom[0][2]-59:
      post = draw_post2(name="TR50_M", height=-50-height,xshift=xshift,
                        geom=geom)
      post1 = draw_post2(name="BA1L", height=0,xshift=xshift, geom=geom)
      post2 = draw_post2(name="PH50_M", height=0,xshift=xshift, geom=geom)
    else:
      post = draw_post2(name="TR30_M", height=-30-height,xshift=xshift,
                        geom=geom)
      post1 = draw_post2(name="BA2_M", height=0,xshift=xshift, geom=geom)
      post2 = draw_post2(name="PH20E_M", height=0,xshift=xshift, geom=geom)
  else:
    DOC = get_DOC()
    DOC.recompute()
    return obj
  DOC = get_DOC()
  
  part = initialize_composition_old(name="mount, post and base")
  container = post,post1,post2,obj
  add_to_composition(part, container)

  DOC.recompute()
  return part

def draw_post2(name="TR50_M", height=12,xshift=0, geom=None):

  datei1 = thisfolder + "post\\" + name
  DOC = get_DOC()
  obj = DOC.addObject("Mesh::Feature", name)
  datei1 += ".stl"
  obj.Mesh = Mesh.Mesh(datei1)
  
  obj.Label = name
  Geom_ground = (np.array((geom[0][0],geom[0][1],0)), np.array((geom[1])))
  if name == "BA1L":
    offset=Vector(xshift,0,height)
    obj.Placement = Placement(offset, Rotation(90,0,90), Vector(0,0,0))
    update_geom_info(obj, Geom_ground, off0=offset)
  elif name =="PH50_M":
    offset=Vector(xshift+5.25,0.25,height+28.5)
    obj.Placement = Placement(offset, Rotation(90,0,90), Vector(0,0,0))
    update_geom_info(obj, Geom_ground, off0=offset)
  elif name =="TR50_M":
    offset=Vector(xshift,0,height)
    obj.Placement = Placement(offset, Rotation(90,0,90), Vector(0,0,0))
    update_geom_info(obj, geom, off0=offset)
  elif name =="TR30_M":
    offset=Vector(xshift,0,height)
    obj.Placement = Placement(offset, Rotation(90,0,90), Vector(0,0,0))
    update_geom_info(obj, geom, off0=offset)
  elif name =="PH20E_M":
    offset = Vector(xshift-11.75,16.8,height+29)
    obj.Placement = Placement(offset, Rotation(90,0,90), Vector(0,0,0))
    update_geom_info(obj, Geom_ground, off0=offset)
  elif name =="BA2_M":
    offset=Vector(xshift,0,height+5.6)
    obj.Placement = Placement(offset, Rotation(0,0,90), Vector(0,0,0))
    update_geom_info(obj, Geom_ground, off0=offset)
  # obj.ViewObject.ShapeColor = (0.86,0.08,0.24)
  # obj.ViewObject.Transparency = 50
  DOC.recompute()
  return obj

def draw_post_special(name="TR50_M", height=12,xshift=0, geom=None):
  datei1 = thisfolder + "post\\" + name
  DOC = get_DOC()
  ground=np.array((geom[1][0],geom[1][1],0))
  ground= ground/(pow(geom[1][0]**2+geom[1][1]**2,0.5))
  Geom_ground = (np.array((geom[0])), np.array((geom[1][0],geom[1][1],0)))
  if name =="new":
    offset=Vector(xshift-56,100,-50)
    obj = DOC.addObject("Part::Box","Box")
    obj.Label = "Mount_base"
    obj.Length = '100.00 mm'
    obj.Height = '100.00 mm'
    obj.Placement=Placement(Vector(offset), Rotation(0,0,0), Vector(0,0,0))
    update_geom_info(obj, Geom_ground, off0=offset)
    return obj
  obj = DOC.addObject("Mesh::Feature", name)
  datei1 += ".stl"
  obj.Mesh = Mesh.Mesh(datei1)
  obj.Label = name
  if name =="TR50_M":
    offset=Vector(xshift,height,0)
    obj.Placement = Placement(offset, Rotation(90,-90,90), Vector(0,0,0))
    update_geom_info(obj, geom, off0=offset)
  elif name =="PH50_M":
    offset=Vector(xshift+5.25,80.8,0)
    obj.Placement=Placement(Vector(offset), Rotation(0,-90,180), Vector(0,0,0))
    update_geom_info(obj, geom, off0=offset)
  elif name =="BA2_M":
    offset=Vector(xshift,100-5.6,0)
    obj.Placement=Placement(Vector(offset), Rotation(0,-0,180), Vector(0,0,0))
    update_geom_info(obj, Geom_ground, off0=offset)
  DOC.recompute()
  return obj
def building_mount(name="mount",  Radius1=13, Hole_Radius=2, thickness=10, 
                        height=20, geom=None, **kwargs):
  """
  Parameters
  ----------
  name : TYPE, optional
    DESCRIPTION. The default is "mount".
  Radius1 : TYPE, optional
    aperture of the mount. The default is 13.
  Hole_Radius : TYPE, optional
    radious of the fixed hole at the button of the mount. The default is 1.5.
  thickness : TYPE, optional
    DESCRIPTION. The default is 10.
  height : TYPE, optional
    the distance between the button of the mount and the center of the mirror.
    The default is 20.
  geom : TYPE, optional
    DESCRIPTION. The default is None.
  **kwargs : TYPE
    DESCRIPTION.
  """
  DOC = get_DOC()
  obj = DOC.addObject('PartDesign::Body', name)
  sketch = obj.newObject('Sketcher::SketchObject', name+'_sketch')
  #sketch.Support = (DOC.getObject('YZ_Plane002'),[''])
  sketch.MapMode = 'FlatFace'
  
  sketch.addGeometry(Part.Circle(Vector(0,0,0),Vector(0,0,1),abs(Radius1)),
                     False)
  sketch.addConstraint(Sketcher.Constraint('Coincident',0,3,-1,1))
  sketch.addConstraint(Sketcher.Constraint('Diameter',0,Radius1*2)) 
  sketch.addGeometry(Part.ArcOfCircle(Part.Circle(Vector(0,0,0),Vector(0,0,1),
                                                  Radius1+5),0,pi),False)
  sketch.addConstraint(Sketcher.Constraint('Coincident',1,3,0,3)) 
  sketch.addConstraint(Sketcher.Constraint('PointOnObject',1,1,-1)) 
  sketch.addConstraint(Sketcher.Constraint('PointOnObject',1,2,-1))
  sketch.addConstraint(Sketcher.Constraint('Radius',1,Radius1+5)) 
  sketch.addGeometry(Part.LineSegment(Vector(-Radius1-5,0,0),
                                      Vector(-Radius1-5,-height,0)),False)
  sketch.addConstraint(Sketcher.Constraint('Coincident',2,1,1,2)) 
  sketch.addConstraint(Sketcher.Constraint('Vertical',2)) 
  sketch.addGeometry(Part.LineSegment(Vector(Radius1+5,0,0),
                                      Vector(Radius1+5,-height,0)),False)
  sketch.addConstraint(Sketcher.Constraint('Coincident',3,1,1,1)) 
  sketch.addConstraint(Sketcher.Constraint('Vertical',3)) 
  sketch.addGeometry(Part.LineSegment(Vector(-Radius1-5,-height,0),
                                      Vector(Radius1+5,-height,0)),False)
  sketch.addConstraint(Sketcher.Constraint('Coincident',4,1,2,2)) 
  sketch.addConstraint(Sketcher.Constraint('Coincident',4,2,3,2)) 
  sketch.addConstraint(Sketcher.Constraint('Horizontal',4)) 
  sketch.addConstraint(Sketcher.Constraint('DistanceY',3,2,3,1,height)) 
  
  pad = obj.newObject('PartDesign::Pad','Pad')
  pad.Profile = sketch
  pad.Length = thickness
  pad.ReferenceAxis = (sketch,['N_Axis'])
  pad.Midplane = 1
  sketch.Visibility = False
  
  
  DOC.recompute()
  sketch001 = obj.newObject('Sketcher::SketchObject', name+'_sketch001')
  sketch001.Support = (pad,['Face3',])
  sketch001.MapMode = 'FlatFace'
  
  sketch001.addGeometry(Part.Circle(Vector(0,0,0),Vector(0,0,1),Hole_Radius),
                        False)
  sketch001.addConstraint(Sketcher.Constraint('Coincident',0,3,-1,1))
  sketch001.addConstraint(Sketcher.Constraint('Diameter',0,Hole_Radius*2)) 
  
  Pocket = obj.newObject('PartDesign::Pocket','Pocket')
  Pocket.Profile = sketch001
  Pocket.Length = 10
  Pocket.ReferenceAxis = (sketch001,['N_Axis'])
  sketch001.Visibility = False
  
  obj.ViewObject.ShapeColor = (204/255, 204/255, 204/255)
  if "transparency" in kwargs.keys():
    obj.ViewObject.Transparency = kwargs["transparency"]
  else:
    obj.ViewObject.Transparency = 0
  obj.Placement=Placement(Vector(0,0,0), Rotation(90,0,90), Vector(0,0,0))
  update_geom_info(obj, geom)
  
  DOC.recompute()
  return obj

# =============================================================================
# End Working area of He Zhuang
# =============================================================================






# def mirror_mount(mount_name="mirror_mount", mount_type="POLARIS-K1",  geom=None, **kwargs):
#   mesh = True
#   if mount_type == "POLARIS-K1":
#     datei = thisfolder + "mount_meshes\\mirror\\" + mount_type
#     if mesh:
#       DOC = get_DOC()
#       obj = DOC.addObject("Mesh::Feature", mount_name)
#       datei += ".stl"
#       # obj.Mesh = Mesh.Mesh("/home/mens/projects/optics-workbench/basic_optics/freecad_models/mount_meshes/POLARIS-K1.stl")
#       obj.Mesh = Mesh.Mesh(datei)
#     else:
#       datei += ".step"
#       # obj = ImportGui.insert(u"C:/Users/mens/Nextcloud/FreeCAD/opticslib/thorlabs/POLARIS-K1.step","labor_116")
#       obj = ImportGui.insert(datei, "labor_116")

#     rotate(obj, (0,1,0), -90)
#     rotate(obj, (1,0,0), 180)
#     offset = Vector(19,0,0)
#     translate(obj, offset)
#     update_geom_info(obj, geom, off0=offset)
#     obj.Label = mount_name

#   DOC.recompute()
#   return obj
