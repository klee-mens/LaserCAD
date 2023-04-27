#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 18 19:55:00 2022

@author: mens
"""
import sys
sys.path.append(u'/home/mens/Nextcloud/FreeCAD/opticslib2/basic_objects/freecad_models')
sys.path.append(u"C:/Users/mens/Nextcloud/FreeCAD/opticslib2/basic_objects/freecad_models")

# from .utils import freecad_da, update_geom_info
from .utils import freecad_da, update_geom_info, get_DOC, thisfolder#, inch
from .freecad_model_composition import initialize_composition_old, add_to_composition
import numpy as np
#import math

DEFALUT_MAX_ANGULAR_OFFSET = 10

import csv
if freecad_da:
  from FreeCAD import Vector, Placement, Rotation
  import Mesh
  import ImportGui
  import Part
  import Sketcher
  from math import pi


def model_lens(name="lens", dia=25, Radius1=300, Radius2=0, thickness=3, geom=None, **kwargs):
  """
    Build a lens.

    Parameters
    ----------
    name : String, optional
        The name of the lens. The default is "lens".
    dia : float/int, optional
        The diameter of the lens. The default is 25.
    Radius1 : float/int, optional
        The curvature of the first serface. The default is 300.
    Radius2 : float/int, optional
        The curvature of the second serface. The default is 0.
    Radius = 0 means the flat serface.
    thickness : float/int, optional
        The thickness of the lens. The default is 3.
    geom : TYPE, optional
        geom info. The default is None.
    **kwargs : TYPE
        DESCRIPTION.

    Returns
    -------
    obj : TYPE
        DESCRIPTION.
    example:
        lens64 = model_lens("Lens64", dia=25.4, Radius1=250, Radius2=500, thickness=3, geom=None)

    """
  DOC = get_DOC()
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
  a = 1 if Radius1>0 else 0
  b = 1 if Radius2>=0 else 0

  obj = DOC.addObject('PartDesign::Body', name)
  sketch = obj.newObject('Sketcher::SketchObject', name+'_sketch')
  #sketch.Support = (DOC.getObject('XY_Plane'),[''])
  sketch.MapMode = 'FlatFace'

  sketch.addGeometry(Part.LineSegment(Vector(0,0,0),Vector(thickness,0,0)),
                     False)
  sketch.addConstraint(Sketcher.Constraint('Coincident',0,1,-1,1))
  sketch.addConstraint(Sketcher.Constraint('PointOnObject',0,2,-1))
  sketch.addConstraint(Sketcher.Constraint('DistanceX',0,1,0,2,thickness))

  if Radius1 == 0:
    sketch.addGeometry(Part.LineSegment(Vector(0.0,0.0,0),Vector(0,10,0)),
                       False)
    sketch.addConstraint(Sketcher.Constraint('Coincident',1,1,0,1))
    sketch.addConstraint(Sketcher.Constraint('PointOnObject',1,2,-2))
  else:
    sketch.addGeometry(Part.ArcOfCircle(Part.Circle(Vector(Radius1,0,0),
                                        Vector(0,0,1),abs(Radius1)),0.9*a*pi,
                                        0.9*a*pi+0.1*pi),False)
    sketch.addConstraint(Sketcher.Constraint('PointOnObject',1,3,-1))
    sketch.addConstraint(Sketcher.Constraint('Coincident',1,1+a,0,1))
    sketch.addConstraint(Sketcher.Constraint('Radius',1,abs(Radius1)))

  if Radius2 == 0:
    sketch.addGeometry(Part.LineSegment(Vector(5.0,0.0,0),Vector(5,10,0)),
                       False)
    sketch.addConstraint(Sketcher.Constraint('Coincident',2,1,0,2))
    sketch.addConstraint(Sketcher.Constraint('Vertical',2))
  else:
    sketch.addGeometry(Part.ArcOfCircle(Part.Circle(
                                        Vector(thickness-Radius2,0,0),
                                        Vector(0,0,1),abs(Radius2)),
                                        0.9*pi-0.9*b*pi,pi-0.9*b*pi),False)
    sketch.addConstraint(Sketcher.Constraint('PointOnObject',2,3,-1))
    sketch.addConstraint(Sketcher.Constraint('Coincident',2,2-b,0,2))
    sketch.addConstraint(Sketcher.Constraint('Radius',2,abs(Radius2)))

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
  update_geom_info(obj, geom)
  DOC.recompute()

  return obj
"""

def lens_mount(mount_name="mirror_mount", dia=inch,  geom=None,
               mount_type="DEFAULT", mesh=True, **kwargs):
  
  
  if dia <= 0.51*inch:
    kind = "MLH05_M"
    offset = Vector(1,-9.5,-8.2)
    place = Placement(offset, Rotation(Vector(-0.57735,0.57735,0.57735),240), Vector(0,0,0))
  elif dia <= 1.01*inch:
    kind = "LMR1_M"
    offset = Vector(1,-9.5,-8.2)
    place = Placement(offset, Rotation(Vector(-0.57735,0.57735,0.57735),240), Vector(0,0,0))
  elif dia <= 1.51*inch:
    kind = "LMR1.5_M"
    offset = Vector(1,-9.5,-8.2)
    place = Placement(offset, Rotation(Vector(-0.57735,0.57735,0.57735),240), Vector(0,0,0))
  elif dia <= 2.01*inch:
    kind = "LMR2_M"
    offset = Vector(13,-31.2,32.4)
    place = Placement(offset, Rotation(-90,2.22639e-14,90), Vector(0,0,0))
  
  if not mount_type == "DEFAULT":
    kind = mount_type #kind kann auf expliziten Wunsch überschireben werden
    offset = Vector(13,-31.2,112.5)
    place = Placement(offset, Rotation(-90,2.22639e-14,90), Vector(0,0,0))
    
  # if kind == "LMR2_M":
  datei = thisfolder + "mount_meshes\\lens\\" + kind
  if mesh:
    DOC = get_DOC()
    obj = DOC.addObject("Mesh::Feature", mount_name)
    datei += ".stl"
    # obj.Mesh = Mesh.Mesh("/home/mens/projects/optics-workbench/basic_optics/freecad_models/mount_meshes/POLARIS-K1-Step.stl")
    obj.Mesh = Mesh.Mesh(datei)
  else:
    datei += ".step"
    # obj = ImportGui.insert(u"C:/Users/mens/Nextcloud/FreeCAD/opticslib/thorlabs/POLARIS-K1-Step.step","labor_116")
    obj = ImportGui.insert(datei, "labor_116")

  obj.Placement = place
  update_geom_info(obj, geom, off0=offset)
  obj.Label = mount_name

  DOC.recompute()
  return obj

"""

def lens_mount(mount_name="lens_mount", mount_type="MLH05_M",  
                 geom=None, only_info=False, drawing_post=True,
                 dia=25.4, **kwargs):
  """
    Build the lens mount, post, post holder and slotted bases of the lens

    Parameters
    ----------
    mount_name : String, optional
        The name of the mount. The default is "lens_mount".
    mount_type : String, optional
        The type of the mount.You can check 'lensmounts.csv' to find mount in
        the database.
        If you want to select the appropriate mount automatically, please keep 
        it as 'default'.
        If you don't want to draw the mount, please set the mount_type 
        as 'dont_draw'
         The default is "MLH05_M".
    geom : TYPE, optional
        The geometrical parameter of the lens. The default is None.
    only_info : Boolean, optional
        Set it as True if you only the the information. The default is False.
    drawing_post : Boolean, optional
        Determine if you want to draw the post.
        Set it as True if you want to draw the post. The default is True.
    dia : float/int, optional
        The diameter of the lens. Please input it correctly if you want to 
        select the appropriate mount automatically.
        The default is 25.4.
    thickness : float/int, optional
        The thickness of lens. The default is 30.
    **kwargs : TYPE
        DESCRIPTION.

    Returns
    -------
    Part
        A part which includes the mount, the post, the post holder and the 
        slotted bases.
    examples:
        mount64 = lens_mount(mount_name="mount64", mount_type="default",  
                         geom=None, only_info=False, drawing_post=True,
                         dia=25.4*1.5)

  """
  if mount_type == "dont_draw":
    return None
  mesh = True
  mount_adjusted = False
  mount_in_database = False
  
  DOC = get_DOC()
  POS = geom[0]
  AXES = geom[1]
  NORMAL = AXES[:,0]
  
  if abs(NORMAL[2])<DEFALUT_MAX_ANGULAR_OFFSET/180*pi:
    NORMAL[2]=0
  else:
    print("this post should't be placed on the XY plane")
  if mount_type == "default":
    if dia<= 25.4/2:
      mount_type = "MLH05_M"
    elif dia <= 25.4:
      mount_type = "LMR1_M"
    elif dia <= 25.4*1.5:
      mount_type = "LMR1.5_M"
    elif dia <=25.4*2:
      mount_type = "LMR2_M"
    else:
      print("there is no suitable default mount in the database. Going back to construct a new mount.")
  buf = []
  with open(thisfolder+"lensmounts.csv") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
      buf.append(row)
  
  for mount_loop in buf:
    if mount_loop["name"] == mount_type:
      mount_in_database = True
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
      if not mount_adjusted:
        place = Placement(offset, rotation, Vector(0,0,0))
  if not mount_in_database:
    if mount_type != "default":
      print("This mount type is not in the database. Going back to construct a new mount.")
    height = dia/2+10
    xshift = 0
    if  drawing_post:
      post_part=draw_post_part(name="post_part", height=height,xshift=xshift, geom=geom)
    else:
      
      DOC.recompute()
      return building_mount(Radius1=dia/2,height=height,geom=geom)
    new_mount = building_mount(Radius1=dia/2,height=height,geom=geom)

    part = initialize_composition_old(name="mount, post and base")
    container = post_part,new_mount
    add_to_composition(part, container)
    DOC.recompute()
    return part

  if only_info:
    data = {"aperture":aperture, "height":height, "price":price}
    return data
    
  if mount_adjusted:
    datei = thisfolder + "mount_meshes\\adjusted lens mount\\" + mount_type
  else:
    datei = thisfolder + "mount_meshes\\lens\\" + mount_type
  if mesh:
    
    obj = DOC.addObject("Mesh::Feature", mount_name)
    datei += ".stl"
    obj.Mesh = Mesh.Mesh(datei)
  else:
    datei += ".step"
    obj = ImportGui.insert(datei, "labor_116")

  if not mount_adjusted:
    obj.Placement = place
  update_geom_info(obj, geom, off0=offset)
  obj.Label = mount_name
  if  drawing_post:
    post_part=draw_post_part(name="post_part", height=height,xshift=xshift, geom=geom)
  else:
    DOC.recompute()
    return obj
  part = initialize_composition_old(name="mount, post and base")
  container = post_part,obj
  add_to_composition(part, container)
  DOC.recompute()
  return part

def draw_post_part(name="post_part", height=12,xshift=0, geom=None):
  """
  Draw the post part, including post, post holder and base
  Assuming that all optics are placed in the plane of z = 0.

  Parameters
  ----------
  name : String, optional
    The name of the part. The default is "post_part".
  height : float/int, optional
    distance from the center of the mirror to the bottom of the mount.
    The default is 12.
  xshift : float/int, optional
    distance from the center of the mirror to the cavity at the bottom of the 
    mount. The default is 0.
  geom : TYPE, optional
    mount geom. The default is None.

  Returns
  -------
  part : TYPE
    A part which includes the post, the post holder and the slotted bases.

  """
  
  POS = geom[0]
  AXES = geom[1]
  NORMAL = AXES[:,0]
  
  if (POS[2]-height<34) or (POS[2]-height>190):
    print("Warning, there is no suitable post holder and slotted base at this height")
  post_length=50
  if POS[2]-height>110:
    post_length=100
  elif POS[2]-height>85:
    post_length=75
  elif POS[2]-height>60:
    post_length=50
  elif POS[2]-height>50:
    post_length=40
  elif POS[2]-height>40:
    post_length=30
  else:
    post_length=20
    post2 = draw_post_holder(name="PH20E_M", height=0,xshift=xshift, geom=geom)
  post = draw_post(name="TR"+str(post_length)+"_M", height=height,
                   xshift=xshift,geom=geom)
  if post_length>90 or post_length<31:
    post1 = draw_post_base(name="BA2_M", height=0,xshift=xshift, geom=geom)
  else:
    post1 = draw_post_base(name="BA1L", height=0,xshift=xshift, geom=geom)
  if post_length>20:
    post2 = draw_post_holder(name="PH"+str(post_length)+"_M", height=0,
                             xshift=xshift, geom=geom)
  part = initialize_composition_old(name=name)
  container = post,post1,post2
  add_to_composition(part, container)
  return part

def draw_post(name="TR50_M", height=12,xshift=0, geom=None):
  """
  draw a post
  Normally, this function is not called separately.

  Parameters
  ----------
  name : String, optional
    THe type of the post. The default is "TR50_M".
  height : float/int, optional
    distance from the center of the mirror to the bottom of the mount.
    The default is 12.
  xshift : float/int, optional
    distance from the center of the mirror to the cavity at the bottom of the 
    mount. The default is 0.
  geom : TYPE, optional
    mount geom. The default is None.

  Returns
  -------
  obj : TYPE
    post object.

  """
  datei1 = thisfolder + "post\\" + name
  DOC = get_DOC()
  obj = DOC.addObject("Mesh::Feature", name)
  datei1 += ".stl"
  obj.Mesh = Mesh.Mesh(datei1)
  obj.Label = name
  post_length= int("".join(list(filter(str.isdigit,name))))
  height=-post_length-height
  offset=Vector(xshift,0,height)
  obj.Placement = Placement(offset, Rotation(90,0,90), Vector(0,0,0))
  update_geom_info(obj, geom, off0=offset)
  return obj

def draw_post_holder (name="PH50_M", height=12,xshift=0, geom=None):
  """
  draw the post holder
  Normally, this function is not called separately.

  Parameters
  ----------
  name : String, optional
    The type of the post holder. The default is "PH50_M".
  height : float/int, optional
    The height of the table for placing optical elements. The default is 0.
  xshift : float/int, optional
    distance from the center of the mirror to the cavity at the bottom of the 
    mount. The default is 0.
  geom : TYPE, optional
    mount geom. The default is None.

  Returns
  -------
  obj : TYPE
    DESCRIPTION.

  """
  POS = geom[0]
  AXES = geom[1]
  NORMAL = AXES[:,0]
  
  datei1 = thisfolder + "post\\post_holder\\" + name
  DOC = get_DOC()
  obj = DOC.addObject("Mesh::Feature", name)
  datei1 += ".stl"
  obj.Mesh = Mesh.Mesh(datei1)
  obj.Label = name
  # Geom_ground = (np.array((POS[0],POS[1],0)), np.array((NORMAL)))
  Geom_ground = (np.array((POS[0],POS[1],0)), np.eye(3))
  if name =="PH100_M":
    offset=Vector(xshift+4.3,-1.5,height+54)
    obj.Placement = Placement(offset, Rotation(90,0,90), Vector(0,0,0))
    update_geom_info(obj, Geom_ground, off0=offset)
  elif name =="PH75_M":
    offset=Vector(xshift+4.75,-1.35,height+41.5)
    obj.Placement = Placement(offset, Rotation(90,0,90), Vector(0,0,0))
    update_geom_info(obj, Geom_ground, off0=offset)
  elif name =="PH50_M":
    offset=Vector(xshift+5.25,0.25,height+28.5)
    obj.Placement = Placement(offset, Rotation(90,0,90), Vector(0,0,0))
    update_geom_info(obj, Geom_ground, off0=offset)
  elif name =="PH40_M":
    offset=Vector(xshift+4.75,-1.45,height+24)
    obj.Placement = Placement(offset, Rotation(90,0,90), Vector(0,0,0))
    update_geom_info(obj, Geom_ground, off0=offset)
  elif name =="PH30_M":
    offset=Vector(xshift+4.75,-1.45,height+19.85)
    obj.Placement = Placement(offset, Rotation(90,0,90), Vector(0,0,0))
    update_geom_info(obj, Geom_ground, off0=offset)
  elif name =="PH20E_M":
    offset = Vector(xshift-11.75,16.8,height+29)
    obj.Placement = Placement(offset, Rotation(90,0,90), Vector(0,0,0))
    update_geom_info(obj, Geom_ground, off0=offset)
  return obj

def draw_post_base(name="BA1L", height=12,xshift=0, geom=None):
  """
  draw the base of the post
  Normally, this function is not called separately.

  Parameters
  ----------
  name : String, optional
    base type. The default is "BA1L".
  height : float/int, optional
    The height of the table for placing optical elements. The default is 0.
  xshift : float/int, optional
    distance from the center of the mirror to the cavity at the bottom of the 
    mount. The default is 0.
  geom : TYPE, optional
    mount geom. The default is None.

  Returns
  -------
  obj : TYPE
    DESCRIPTION.

  """

  datei1 = thisfolder + "post\\base\\" + name
  DOC = get_DOC()
  obj = DOC.addObject("Mesh::Feature", name)
  datei1 += ".stl"
  obj.Mesh = Mesh.Mesh(datei1)
  obj.Label = name
  
  POS = geom[0]
  AXES = geom[1]
  NORMAL = AXES[:,0]
  
  # Geom_ground = (np.array((POS[0],POS[1],0)), np.array((NORMAL)))
  Geom_ground = (np.array((POS[0],POS[1],0)), np.eye(3))
  if name == "BA1L":
    offset=Vector(xshift,0,height)
    obj.Placement = Placement(offset, Rotation(90,0,90), Vector(0,0,0))
    update_geom_info(obj, Geom_ground, off0=offset)
  elif name =="BA2_M":
    offset=Vector(xshift,0,height+5.6)
    obj.Placement = Placement(offset, Rotation(0,0,90), Vector(0,0,0))
    update_geom_info(obj, Geom_ground, off0=offset)
  elif name == "BA3_M":
    offset=Vector(xshift,0,height+4.5)
    obj.Placement = Placement(offset, Rotation(90,0,90), Vector(0,0,0))
    update_geom_info(obj, Geom_ground, off0=offset)
  # obj.ViewObject.ShapeColor = (0.86,0.08,0.24)
  # obj.ViewObject.Transparency = 50
  DOC.recompute()
  return obj

def building_mount(name="mount",  Radius1=13, Hole_Radius=2, thickness=10, 
                        height=20, geom=None, **kwargs):
  """
  make a custom mount
  Normally, this function is not called separately.
  Parameters
  ----------
  name : String, optional
    DESCRIPTION. The default is "mount".
  Radius1 : float/int, optional
    aperture of the mount. The default is 13.
  Hole_Radius : float/int, optional
    radious of the fixed hole at the button of the mount. The default is 1.5.
  thickness : float/int, optional
    DESCRIPTION. The default is 10.
  height : float/int, optional
    the distance between the button of the mount and the center of the mirror.
    The default is 20.
  geom : TYPE, optional
    mirror geom. The default is None.
  **kwargs : TYPE
    DESCRIPTION.
  """
  DOC = get_DOC()
  obj = DOC.addObject('PartDesign::Body', name)
  sketch = obj.newObject('Sketcher::SketchObject', name+'_sketch')
  #sketch.Support = (DOC.getObject('YZ_Plane001'),[''])
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
  
  sketch001.addGeometry(Part.Circle(Vector(0,0,0),Vector(0,0,1),Hole_Radius),False)
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




# Test
if __name__ == "__main__":
  from utils import start_DOC
  DOC = None
  start_DOC(DOC)
  model_lens()