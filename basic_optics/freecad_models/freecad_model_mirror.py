# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 16:28:18 2022

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
 
DEFAULT_COLOR_JOERG = (0.8,0.2,0.8)
DEFAULT_COLOR = (199/255, 144/255, 28/255) #Messing
DEFAULT_TRANSPARENCY = 50
DEFALUT_MAX_ANGULAR_OFFSET = 10


def model_mirror(model_type="DEFAULT", **kwargs):
  """
    bulid a mirror model

    Parameters
    ----------
    model_type : String, optional
        The type of the mirror.
        There are two options, Round mirror(DEFAULT) and Stripe mirror.
        The default is "DEFAULT".
    **kwargs : TYPE
        DESCRIPTION.

    Returns
    -------
    obj : TYPE
        object of mirror.
    Example:
    mirror47 = mirror("mirror_47", dia=25, d=5, R=200)
  """
  if model_type == "DEFAULT" or model_type == "Round" or model_type == "polarizer":
    obj = model_round_mirror(**kwargs)
  elif model_type == "Stripe":
    obj = model_stripe_mirror(**kwargs)
  elif model_type == "Rooftop":
    obj = model_rooftop_mirror(**kwargs)
     
  return obj


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


def model_stripe_mirror(name="Stripe_Mirror", dia=75, Radius1=250, thickness=25, 
                        height=10, geom=None, pos=0, axes = "somthing", **kwargs):
  """
    

    Parameters
    ----------
    name : String, optional
        The name of the mirror. The default is "Stripe_Mirror".
    dia : TYPE, optional
        The width of the mirror. The default is 75.
    Radius1 : TYPE, optional
        The curvature of the mirror. The default is 250.
    thickness : TYPE, optional
        The thickness of the mirror. The default is 25.
    height : TYPE, optional
        The height of the mirror. The default is 10.
    geom : TYPE, optional
        The geometrical parameter of the mirror. The default is None.
    **kwargs : TYPE
        DESCRIPTION.

    Returns
    -------
    obj : TYPE
        object of mirror.
   example:
       stripe_mirror=model_stripe_mirror(name="Stripe_Mirror", dia=60, 
                                         Radius1=300, thickness=30, height=15, 
                                         geom=None,)
   """
  DOC = get_DOC()
  """Beispiel
  s.o.
  """
  
  Radius1 *= -1
  a = 1 if Radius1>0 else -1

  obj = DOC.addObject('PartDesign::Body', name)
  sketch = obj.newObject('Sketcher::SketchObject', name+'_sketch')
  #sketch.Support = (DOC.getObject('XY_Plane'),[''])
  sketch.MapMode = 'FlatFace'
  if a == 1:
    sketch.addGeometry(Part.ArcOfCircle(Part.Circle(Vector(Radius1,0,0),Vector(0,0,1),abs(Radius1)),0.9*a*pi,0.9*a*pi+0.2*pi),False)
    sketch.addConstraint(Sketcher.Constraint('PointOnObject',-1,1,0)) 
    sketch.addConstraint(Sketcher.Constraint('Symmetric',0,1,0,2,-1)) 
    sketch.addConstraint(Sketcher.Constraint('Radius',0,Radius1)) 
    sketch.addConstraint(Sketcher.Constraint('DistanceY',0,2,0,1,dia)) 
  else:
    sketch.addGeometry(Part.ArcOfCircle(Part.Circle(Vector(Radius1,0,0),Vector(0,0,1),abs(Radius1)),np.arcsin(dia/(2*-Radius1)),-np.arcsin(dia/(2*-Radius1))),False)
    sketch.addConstraint(Sketcher.Constraint('DistanceX',0,3,-1,1,-Radius1)) 
    sketch.addConstraint(Sketcher.Constraint('PointOnObject',0,3,-1)) 
    sketch.addConstraint(Sketcher.Constraint('DistanceY',-1,1,0,2,dia/2)) 
    sketch.addConstraint(Sketcher.Constraint('DistanceY',0,1,-1,1,dia/2)) 
    sketch.addConstraint(Sketcher.Constraint('Radius',0,-Radius1)) 
  xx = Radius1-pow(Radius1**2-(dia/2)**2,0.5)
  sketch.addGeometry(Part.LineSegment(Vector(a*xx,dia/2,0.0),Vector(thickness,dia/2,0.0)),False)
  sketch.addConstraint(Sketcher.Constraint('Coincident',1,1,0,1)) 
  sketch.addConstraint(Sketcher.Constraint('Horizontal',1)) 
  sketch.addGeometry(Part.LineSegment(Vector(thickness,dia/2,0.0),Vector(thickness,-dia/2,0.0)),False)
  sketch.addConstraint(Sketcher.Constraint('Coincident',2,1,1,2)) 
  sketch.addConstraint(Sketcher.Constraint('Vertical',2)) 
  sketch.addGeometry(Part.LineSegment(Vector(thickness,-dia/2,0),Vector(a*xx,-dia/2,0)),False)
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
  # print("geom=",geom)
  # obj.Placement = Placement(Vector(0,0,0), Rotation(0,0,90), Vector(0,0,0))
  
  if "color" in kwargs.keys():
    obj.ViewObject.ShapeColor = kwargs["color"]
  else:
    # obj.ViewObject.ShapeColor = (204/255, 204/255, 204/255)
    obj.ViewObject.ShapeColor = DEFAULT_COLOR
  if "transparency" in kwargs.keys():
    obj.ViewObject.Transparency = kwargs["transparency"]
  else:
    obj.ViewObject.Transparency = DEFAULT_TRANSPARENCY
  update_geom_info(obj, geom)

  DOC = get_DOC()
  DOC.recompute()
  
  return obj


def model_rooftop_mirror(name="rooftop_mirror",dia=0, geom=None, **kwargs):
  """
  draw a rooftop mirror

  Parameters
  ----------
  name : TYPE, optional
    mirror name. The default is "rooftop_mirror".
  dia : TYPE, optional
    the periscope distance, which will deside the pos of mirror.
    The default is 0.
  geom : TYPE, optional
    DESCRIPTION. The default is None.
  **kwargs : TYPE
    DESCRIPTION.

  Returns
  -------
  obj : TYPE
    DESCRIPTION.
    
  example:
      stripe_mirror= model_rooftop_mirror(name="rooftop_mirror",dia=0, 
                                          geom=None, **kwargs)
  """

  DOC = get_DOC()
  obj = DOC.addObject('PartDesign::Body', name)
  sketch = obj.newObject('Sketcher::SketchObject', name+'_sketch')
  # sketch.Support = (DOC.getObject('XY_Plane'),[''])
  sketch.MapMode = 'FlatFace'

  sketch.addGeometry(Part.LineSegment(Vector(0,0,0),Vector(24.748737,24.748737,0)),False)
  sketch.addConstraint(Sketcher.Constraint('Coincident',-1,1,0,1)) 
  sketch.addGeometry(Part.LineSegment(Vector(24.748737,24.748737,0),Vector(24.748737,-24.748737,0)),False)
  sketch.addConstraint(Sketcher.Constraint('Coincident',0,2,1,1)) 
  sketch.addConstraint(Sketcher.Constraint('Vertical',1)) 
  sketch.addGeometry(Part.LineSegment(Vector(24.748737,-24.748737,0),Vector(0,0,0)),False)
  sketch.addConstraint(Sketcher.Constraint('Coincident',1,2,2,1)) 
  sketch.addConstraint(Sketcher.Constraint('Coincident',2,2,0,1)) 
  sketch.addConstraint(Sketcher.Constraint('Angle',-1,1,0,1,45/180*np.pi)) 
  sketch.addConstraint(Sketcher.Constraint('Angle',2,2,-1,1,45/180*np.pi)) 
  sketch.addConstraint(Sketcher.Constraint('Distance',0,35)) 
  

  pad = obj.newObject('PartDesign::Pad','Pad')
  pad.Profile = sketch
  pad.Length = 90
  pad.ReferenceAxis = (sketch,['N_Axis'])
  pad.Midplane = 1
  sketch.Visibility = False
  
  if "color" in kwargs.keys():
    obj.ViewObject.ShapeColor = kwargs["color"]
  else:
    # obj.ViewObject.ShapeColor = (204/255, 204/255, 204/255)
    obj.ViewObject.ShapeColor = DEFAULT_COLOR
  if "transparency" in kwargs.keys():
    obj.ViewObject.Transparency = kwargs["transparency"]
  else:
    obj.ViewObject.Transparency = DEFAULT_TRANSPARENCY+20
  offset=Vector(dia/2,0,0)
  obj.Placement = Placement(offset, Rotation(0,-180,90), Vector(0,0,0))
  update_geom_info(obj, geom, off0=offset)
  # DOC = get_DOC()
  DOC.recompute()
  
  return obj







# def mirror_mount(mount_name="mirror_mount",model_type="DEFAULT",
#                  mount_type="default", geom=None, only_info=False, 
#                  drawing_post=True,base_exists=False, dia=25.4,thickness=30, **kwargs):
#   """
#     Build the mirror mount, post, post holder and slotted bases of the mirror

#     Parameters
#     ----------
#     mount_name : String, optional
#         The name of the mount. The default is "mirror_mount".
#     model_type : String, optional
#         The tpye fo the mirror. There are some special mount for stripe mirror
#         and rooftop mirror.
#         Set the model_type as 'rooftop_mirror_mount' if you want to draw rooftop 
#         mirror mount.
#         Set the model_type as 'Stripe' if you want to draw stripe mirror mount.
#         The default is "DEFAULT".
#     mount_type : String, optional
#         The type of the mount.You can check 'mirrormounts.csv' to find mount in
#         the database.
#         If you want to select the appropriate mount automatically, please keep 
#         it as 'default'.
#         If you don't want to draw the mount, please set the mount_type 
#         as 'dont_draw'
#         DESCRIPTION. The default is "default".
#     geom : TYPE, optional
#         The geometrical parameter of the mirror. The default is None.
#     only_info : Boolean, optional
#         Set it as True if you only the the information. The default is False.
#     drawing_post : Boolean, optional
#         Determine if you want to draw the post.
#         Set it as True if you want to draw the post. The default is True.
#     dia : float/int, optional
#         The diameter of the mirror. Please input it correctly if you want to 
#         select the appropriate mount automatically.
#         In case of rooftop mirror, dia mean the periscope distance between rays.
#         Please check the Make_Stretcher() function in modults to get an example 
#         of how to use.
#         The default is 25.4.
#     thickness : float/int, optional
#         The thickness of mirror. The default is 30.
#     **kwargs : TYPE
#         DESCRIPTION.

#     Returns
#     -------
#     Part
#         A part which includes the mount, the post, the post holder and the 
#         slotted bases.
#   example:
#       mount64=mirror_mount(mount_name="mirror_mount",model_type="DEFAULT",
#                        mount_type="POLARIS-K1", geom=None, only_info=False, 
#                        drawing_post=True, dia=25.4*2,thickness=30)
#   """
#   if mount_type == "dont_draw":
#     return None
#   mesh = True
#   mount_adjusted = False
#   mount_in_database= False
#   mount_rotation = False
#   additional_mount = None
  
#   POS = geom[0]
#   AXES = geom[1]
#   NORMAL = AXES[:,0]
  
#   DOC = get_DOC()
#   if abs(NORMAL[2])<DEFALUT_MAX_ANGULAR_OFFSET/180*np.pi:
#     NORMAL[2]=0
#   else:
#     if mount_type!="rooftop_mirror_mount":
#       mount_rotation=True
#       print("this post should't be placed on the XY plane")
#   if abs(NORMAL[1])<DEFALUT_MAX_ANGULAR_OFFSET/180*np.pi:
#     NORMAL[1]=0
#   if abs(NORMAL[0])<DEFALUT_MAX_ANGULAR_OFFSET/180*np.pi:
#     NORMAL[0]=0
    
#   if model_type=="Stripe":
#     additional_mount = draw_stripe_mount(thickness=thickness,geom=geom)
#     xshift = thickness-7
#     yshift = 104.3
#     geom = (np.array((POS[0]+xshift*NORMAL[0]-yshift*NORMAL[1],
#                       POS[1]+yshift*NORMAL[0]+xshift*NORMAL[1],
#                       POS[2])),np.array((-NORMAL[0],-NORMAL[1],
#                       NORMAL[2])))
#     mount_type = "POLARIS-K2"
#     dia =25.4*2
#   if mount_type =="rooftop_mirror_mount":
#     additional_mount = draw_rooftop_mount(xxshift=dia/2,geom=geom)
#     xshift=57+dia/2-12.2
#     zshift=-5
#     shiftvec=Vector(xshift,0,zshift)
#     default=Vector(1,0,0)
#     default_axis=Vector(0,1,0)
#     normal=Vector(NORMAL)
#     angle = default.getAngle(normal)
#     if angle!=0:
#       vec = default.cross(normal)
#       vec = vec/np.linalg.norm(vec)
#       shiftvec = rotate_vector(shiftvec=shiftvec,vec=vec,angle=angle)
#       default_axis = rotate_vector(shiftvec=default_axis,vec=vec,angle=angle)
#       default_axis = default_axis/np.linalg.norm(default_axis)
#     if angle==np.pi/180:
#       shiftvec = -shiftvec
#     new_normal = Vector(NORMAL)
#     # new_normal = rotate_vector(shiftvec=new_normal,vec=default_axis,angle=45/180*np.pi)
#     new_pos = Vector(POS)+shiftvec
#     geom = (new_pos,new_normal)
#     mount_type = "POLARIS-K2"
#     dia =25.4*2
#     if abs(NORMAL[2])<DEFALUT_MAX_ANGULAR_OFFSET/180*np.pi:
#       NORMAL[2]=0
#   if mount_type == "default":
#     if dia<= 25.4/2:
#       mount_type = "POLARIS-K05"
#     elif dia <= 25.4:
#       mount_type = "POLARIS-K1"
#     elif dia <= 25.4*1.5:
#       mount_type = "POLARIS-K15S4"
#     elif dia <=25.4*2:
#       mount_type = "POLARIS-K2"
#     elif dia <=25.4*3:
#       mount_type = "POLARIS-K3S5"
#     elif dia <=25.4*4:
#       mount_type = "KS4"
#     elif dia <=160:
#       return draw_large_mount(thickness=thickness,geom=geom)
#     else:
#       print("there is no suitable default mount in the database. Going back to construct a new mount.")
#   buf = []
#   with open(thisfolder+"mirrormounts.csv") as csvfile:
#     reader = csv.DictReader(csvfile)
#     for row in reader:
#       buf.append(row)
  
#   for mount_loop in buf:
#     if mount_loop["name"] == mount_type:
#       mount_in_database = True
#       aperture = float(mount_loop["aperture"])
#       height = float(mount_loop["height"])
#       price = float(mount_loop["price"])
#       xshift = float(mount_loop["xshift"])
#       offset = Vector(float(mount_loop["offsetX"]),
#                       float(mount_loop["offsetY"]),
#                       float(mount_loop["offsetZ"]))
#       rotation = Rotation(float(mount_loop["rot_angleZ"]),
#                           float(mount_loop["rot_angleY"]),
#                           float(mount_loop["rot_angleX"]))
#       if not mount_adjusted:
#         place = Placement(offset, rotation, Vector(0,0,0))
#   if not mount_in_database:
#     if mount_type != "default":
#       print("This mount type is not in the database. Going back to construct a new mount.")
#     height=dia/2+10
#     xshift=0
#     new_mount = building_mount(Radius1=dia/2,height=height,geom=geom)
#     if  drawing_post:
#       post_part=draw_post_part(name="post_part",base_exists=base_exists,
#                                height=height,xshift=xshift, geom=geom)
#     else:
#       DOC.recompute()
#       return new_mount
#     part = initialize_composition_old(name="mount, post and base")
#     container = post_part,new_mount, additional_mount
#     add_to_composition(part, container)
#     return part

#   if only_info:
#     data = {"aperture":aperture, "height":height, "price":price}
#     return data
#   if mount_adjusted:
#     datei = thisfolder + "mount_meshes\\adjusted mirror mount\\" + mount_type
#   else:
#     datei = thisfolder + "mount_meshes\\mirror\\" + mount_type
#   if mesh:
#     obj = DOC.addObject("Mesh::Feature", mount_name)
#     datei += ".stl"
#     obj.Mesh = Mesh.Mesh(datei)
#   else:
#     datei += ".step"
#     obj = ImportGui.insert(datei, "labor_116")
    
#   if mount_rotation:
#     #obj.Placement = Placement(Vector(0,0,0), Rotation(0,0,90), Vector(0,0,0))
#     if  drawing_post:
#       post = draw_post_special(name="TR50_M", height=50+height,xshift=xshift,
#                         geom=geom)
#       post2 = draw_post_special(name="PH50_M", height=0,xshift=xshift, geom=geom)
#       post1 = draw_post_special(name="BA2_M", height=0,xshift=xshift, geom=geom)
#       if mount_adjusted:
#         rotate(obj,Vector(1,0,0),90)
#         update_geom_info(obj,geom)
#       else:
#         obj.Placement = place
#         rotate(obj,Vector(1,0,0),90)
#         update_geom_info(obj,geom,off0=offset)
        
#       obj.Label = mount_name
#       part = initialize_composition_old(name="mount, post and base")
#       container = post,post1,post2,obj, additional_mount
#       add_to_composition(part, container)
#       DOC.recompute()
#       return part
#   if not mount_adjusted:
#     obj.Placement = place
#     update_geom_info(obj, geom, off0=offset)

#   else:
#     update_geom_info(obj,geom)
#   obj.Label = mount_name
  
#   if  drawing_post:
#     post_part=draw_post_part(name="post_part",base_exists=base_exists,
#                              height=height,xshift=xshift, geom=geom)
#   else:
#     DOC.recompute()
#     return obj
#   part = initialize_composition_old(name="mount, post and base")
#   container = post_part,obj,additional_mount
#   add_to_composition(part, container)
#   DOC.recompute()
#   return part

# def draw_post_part(name="post_part", base_exists=False, height=12,xshift=0, geom=None):
#   """
#   Draw the post part, including post, post holder and base
#   Assuming that all optics are placed in the plane of z = 0.

#   Parameters
#   ----------
#   name : String, optional
#     The name of the part. The default is "post_part".
#   height : float/int, optional
#     distance from the center of the mirror to the bottom of the mount.
#     The default is 12.
#   xshift : float/int, optional
#     distance from the center of the mirror to the cavity at the bottom of the 
#     mount. The default is 0.
#   geom : TYPE, optional
#     mount geom. The default is None.

#   Returns
#   -------
#   part : TYPE
#     A part which includes the post, the post holder and the slotted bases.

#   """
#   POS = geom[0]
#   # AXES = geom[1]
#   # if np.shape(AXES)==(3,):
#   #   NORMAL=AXES
#   # else:
#   #   NORMAL=AXES[:,0]
#   if (POS[2]-height<34) or (POS[2]-height>190):
#     print("Warning, there is no suitable post holder and slotted base at this height")
#   post_length=50
#   if base_exists:
#       if POS[2]-height>110:
#         post_length=100
#       elif POS[2]-height>90:
#         post_length=75
#       elif POS[2]-height>65:
#         post_length=50
#       elif POS[2]-height>55:
#         post_length=40
#       elif POS[2]-height>40:
#         post_length=30
#       else:
#         post_length=20
#         post2 = draw_post_holder(name="PH20E_M", height=0,xshift=xshift, geom=geom)
#       post = draw_post(name="TR"+str(post_length)+"_M", height=height,
#                        xshift=xshift,geom=geom)
#       if post_length>20:
#         post2 = draw_post_holder(name="PH"+str(post_length)+"_M", height=0,
#                                  xshift=xshift, geom=geom)
#   else:
#       if POS[2]-height>105:
#         post_length=100
#       elif POS[2]-height>85:
#         post_length=75
#       elif POS[2]-height>60:
#         post_length=50
#       elif POS[2]-height>50:
#         post_length=40
#       elif POS[2]-height>35:
#         post_length=30
#       else:
#         post_length=20
#         post2 = draw_post_holder(name="PH"+str(post_length)+"E_M", height=0,
#                                  xshift=xshift, geom=geom)
#       post = draw_post(name="TR"+str(post_length)+"_M", height=height,
#                        xshift=xshift,geom=geom)
#       post2 = draw_post_holder(name="PH"+str(post_length)+"E_M", height=0,
#                                xshift=xshift, geom=geom)
#   if base_exists:
#     if post_length>90 or post_length<31:
#         post1 = draw_post_base(name="BA2_M", height=0,xshift=xshift, geom=geom)
#     else:
#         post1 = draw_post_base(name="BA1L", height=0,xshift=xshift, geom=geom)
#   else:
#     post1 = None
  
#   part = initialize_composition_old(name=name)
#   container = post,post1,post2
#   add_to_composition(part, container)
#   return part

# def draw_post(name="TR50_M", height=12,xshift=0, geom=None):
#   """
#   draw a post
#   Normally, this function is not called separately.

#   Parameters
#   ----------
#   name : String, optional
#     THe type of the post. The default is "TR50_M".
#   height : float/int, optional
#     distance from the center of the mirror to the bottom of the mount.
#     The default is 12.
#   xshift : float/int, optional
#     distance from the center of the mirror to the cavity at the bottom of the 
#     mount. The default is 0.
#   geom : TYPE, optional
#     mount geom. The default is None.

#   Returns
#   -------
#   obj : TYPE
#     DESCRIPTION.

#   """
  
#   datei1 = thisfolder + "post\\" + name
#   DOC = get_DOC()
#   obj = DOC.addObject("Mesh::Feature", name)
#   datei1 += ".stl"
#   obj.Mesh = Mesh.Mesh(datei1)
#   obj.Label = name
#   post_length= int("".join(list(filter(str.isdigit,name))))
#   height=-post_length-height
#   offset=Vector(xshift,0,height)
#   obj.Placement = Placement(offset, Rotation(90,0,90), Vector(0,0,0))
#   update_geom_info(obj, geom, off0=offset)
#   return obj

# def draw_post_holder (name="PH50_M", height=0,xshift=0, geom=None):
#   """
#   draw the post holder
#   Normally, this function is not called separately.

#   Parameters
#   ----------
#   name : String, optional
#     The type of the post holder. The default is "PH50_M".
#   height : float/int, optional
#     The height of the table for placing optical elements. The default is 0.
#   xshift : float/int, optional
#     distance from the center of the mirror to the cavity at the bottom of the 
#     mount. The default is 0.
#   geom : TYPE, optional
#     mount geom. The default is None.

#   Returns
#   -------
#   obj : TYPE
#     DESCRIPTION.

#   """
  
#   POS = geom[0]
#   AXES = geom[1]
#   if np.shape(AXES)==(3,):
#     NORMAL=AXES
#   else:
#     NORMAL=AXES[:,0]
#   # NORMAL = AXES[:,0]
  
#   datei1 = thisfolder + "post\\post_holder\\" + name
#   DOC = get_DOC()
#   obj = DOC.addObject("Mesh::Feature", name)
#   datei1 += ".stl"
#   obj.Mesh = Mesh.Mesh(datei1)
#   obj.Label = name
#   Geom_ground = (np.array((POS[0],POS[1],0)), np.array((NORMAL)))
#   if name =="PH100_M":
#     offset=Vector(xshift+4.3,-1.5,height+54)
#     obj.Placement = Placement(offset, Rotation(90,0,90), Vector(0,0,0))
#     update_geom_info(obj, Geom_ground, off0=offset)
#   elif name =="PH75_M":
#     offset=Vector(xshift+4.75,-1.35,height+41.5)
#     obj.Placement = Placement(offset, Rotation(90,0,90), Vector(0,0,0))
#     update_geom_info(obj, Geom_ground, off0=offset)
#   elif name =="PH50_M":
#     offset=Vector(xshift+5.25,0.25,height+28.5)
#     obj.Placement = Placement(offset, Rotation(90,0,90), Vector(0,0,0))
#     update_geom_info(obj, Geom_ground, off0=offset)
#   elif name =="PH40_M":
#     offset=Vector(xshift+4.75,-1.45,height+24)
#     obj.Placement = Placement(offset, Rotation(90,0,90), Vector(0,0,0))
#     update_geom_info(obj, Geom_ground, off0=offset)
#   elif name =="PH30_M":
#     offset=Vector(xshift+4.75,-1.45,height+19.85)
#     obj.Placement = Placement(offset, Rotation(90,0,90), Vector(0,0,0))
#     update_geom_info(obj, Geom_ground, off0=offset)
#   elif name =="PH20E_M":
#     offset = Vector(xshift-11.75,16.8,height+29)
#     obj.Placement = Placement(offset, Rotation(90,0,90), Vector(0,0,0))
#     update_geom_info(obj, Geom_ground, off0=offset)
# #----------------------------------------------------------------------------
#   elif name =="PH100E_M":
#     offset=Vector(xshift+6.25,6.75,height+40.4)
#     obj.Placement = Placement(offset, Rotation(90,0,90), Vector(0,0,0))
#     update_geom_info(obj, Geom_ground, off0=offset)
#   elif name =="PH75E_M":
#     offset=Vector(xshift-8,10.5,height+46.5)
#     obj.Placement = Placement(offset, Rotation(90,0,90), Vector(0,0,0))
#     update_geom_info(obj, Geom_ground, off0=offset)
#   elif name =="PH50E_M":
#     offset=Vector(xshift-4.5,18,height+22.6)
#     obj.Placement = Placement(offset, Rotation(90,0,90), Vector(0,0,0))
#     update_geom_info(obj, Geom_ground, off0=offset)
#   elif name =="PH40E_M":
#     offset=Vector(xshift-2,2.7,height+25.7)
#     obj.Placement = Placement(offset, Rotation(90,0,90), Vector(0,0,0))
#     update_geom_info(obj, Geom_ground, off0=offset)
#   elif name =="PH30E_M":
#     offset=Vector(xshift-4.5,-5.5,height+31.25)
#     obj.Placement = Placement(offset, Rotation(90,0,90), Vector(0,0,0))
#     update_geom_info(obj, Geom_ground, off0=offset)

#   return obj

# def draw_post_base(name="BA1L", height=0,xshift=0, geom=None):
#   """
#   draw the base of the post
#   Normally, this function is not called separately.

#   Parameters
#   ----------
#   name : String, optional
#     base type. The default is "BA1L".
#   height : float/int, optional
#     The height of the table for placing optical elements. The default is 0.
#   xshift : float/int, optional
#     distance from the center of the mirror to the cavity at the bottom of the 
#     mount. The default is 0.
#   geom : TYPE, optional
#     mount geom. The default is None.

#   Returns
#   -------
#   obj : TYPE
#     DESCRIPTION.

#   """
  
#   POS = geom[0]
#   AXES = geom[1]
#   if np.shape(AXES)==(3,):
#     NORMAL=AXES
#   else:
#     NORMAL=AXES[:,0]
  
#   datei1 = thisfolder + "post\\base\\" + name
#   DOC = get_DOC()
#   obj = DOC.addObject("Mesh::Feature", name)
#   datei1 += ".stl"
#   obj.Mesh = Mesh.Mesh(datei1)
#   obj.Label = name
#   Geom_ground = (np.array((POS[0],POS[1],0)), np.array((NORMAL)))
#   if name == "BA1L":
#     offset=Vector(xshift,0,height)
#     obj.Placement = Placement(offset, Rotation(90,0,90), Vector(0,0,0))
#     update_geom_info(obj, Geom_ground, off0=offset)
#   elif name =="BA2_M":
#     offset=Vector(xshift,0,height+5.6)
#     obj.Placement = Placement(offset, Rotation(0,0,90), Vector(0,0,0))
#     update_geom_info(obj, Geom_ground, off0=offset)
#   elif name == "BA3_M":
#     offset=Vector(xshift,0,height+4.5)
#     obj.Placement = Placement(offset, Rotation(90,0,90), Vector(0,0,0))
#     update_geom_info(obj, Geom_ground, off0=offset)
#   # obj.ViewObject.ShapeColor = (0.86,0.08,0.24)
#   # obj.ViewObject.Transparency = 50
#   DOC.recompute()
#   return obj

# def draw_post_special(name="TR50_M", height=12,xshift=0, geom=None):
#   """
#   draw the special post only for periscope
#   Normally, this function is not called separately.

#   Parameters
#   ----------
#   name : String, optional
#     The type of the elements that needs to be drawed. The default is "TR50_M".
#   height : float/int, optional
#     distance from the center of the mirror to the bottom of the mount.
#     The default is 12.
#   xshift : float/int, optional
#     distance from the center of the mirror to the cavity at the bottom of the 
#     mount. The default is 0.
#   geom : TYPE, optional
#     mirror geom. The default is None.

#   Returns
#   -------
#   None.

#   """
  
#   # POS = geom[0]
#   AXES = geom[1]
#   if np.shape(AXES)==(3,):
#     NORMAL=AXES
#   else:
#     NORMAL=AXES[:,0]
  
#   datei1 = thisfolder + "post\\" + name
#   DOC = get_DOC()
#   ground = np.array((NORMAL[0],NORMAL[1],0))
#   ground = ground/(pow(NORMAL[0]**2+NORMAL[1]**2,0.5))
#   obj = DOC.addObject("Mesh::Feature", name)
#   datei1 += ".stl"
#   obj.Mesh = Mesh.Mesh(datei1)
#   obj.Label = name
#   if name =="TR50_M":
#     offset=Vector(xshift,height,0)
#     obj.Placement = Placement(offset, Rotation(90,-90,90), Vector(0,0,0))
#     update_geom_info(obj, geom, off0=offset)
#   elif name =="PH50_M":
#     offset=Vector(xshift+5.25,71,0) #80.8
#     obj.Placement=Placement(Vector(offset), Rotation(0,-90,180), Vector(0,0,0))
#     update_geom_info(obj, geom, off0=offset)
#   elif name =="BA2_M":
#     offset=Vector(xshift,94.4,0)
#     obj.Placement=Placement(Vector(offset), Rotation(0,-0,180), Vector(0,0,0))
#     update_geom_info(obj, geom, off0=offset)
#     rotate(obj,Vector(0,1,0),180/pi*np.arctan(NORMAL[2]/(pow(NORMAL[0]**2+NORMAL[1]**2,0.5))))
#   DOC.recompute()
#   return obj

# def building_mount(name="mount",  Radius1=13, Hole_Radius=2, thickness=10, 
#                         height=20, geom=None, **kwargs):
#   """
#   make a custom mount
#   Normally, this function is not called separately.
#   Parameters
#   ----------
#   name : String, optional
#     DESCRIPTION. The default is "mount".
#   Radius1 : float/int, optional
#     aperture of the mount. The default is 13.
#   Hole_Radius : float/int, optional
#     radious of the fixed hole at the button of the mount. The default is 1.5.
#   thickness : float/int, optional
#     DESCRIPTION. The default is 10.
#   height : float/int, optional
#     the distance between the button of the mount and the center of the mirror.
#     The default is 20.
#   geom : TYPE, optional
#     mirror geom. The default is None.
#   **kwargs : TYPE
#     DESCRIPTION.
#   """
#   DOC = get_DOC()
#   obj = DOC.addObject('PartDesign::Body', name)
#   sketch = obj.newObject('Sketcher::SketchObject', name+'_sketch')
#   #sketch.Support = (DOC.getObject('YZ_Plane002'),[''])
#   sketch.MapMode = 'FlatFace'
  
#   sketch.addGeometry(Part.Circle(Vector(0,0,0),Vector(0,0,1),abs(Radius1)),
#                      False)
#   sketch.addConstraint(Sketcher.Constraint('Coincident',0,3,-1,1))
#   sketch.addConstraint(Sketcher.Constraint('Diameter',0,Radius1*2)) 
#   sketch.addGeometry(Part.ArcOfCircle(Part.Circle(Vector(0,0,0),Vector(0,0,1),
#                                                   Radius1+5),0,pi),False)
#   sketch.addConstraint(Sketcher.Constraint('Coincident',1,3,0,3)) 
#   sketch.addConstraint(Sketcher.Constraint('PointOnObject',1,1,-1)) 
#   sketch.addConstraint(Sketcher.Constraint('PointOnObject',1,2,-1))
#   sketch.addConstraint(Sketcher.Constraint('Radius',1,Radius1+5)) 
#   sketch.addGeometry(Part.LineSegment(Vector(-Radius1-5,0,0),
#                                       Vector(-Radius1-5,-height,0)),False)
#   sketch.addConstraint(Sketcher.Constraint('Coincident',2,1,1,2)) 
#   sketch.addConstraint(Sketcher.Constraint('Vertical',2)) 
#   sketch.addGeometry(Part.LineSegment(Vector(Radius1+5,0,0),
#                                       Vector(Radius1+5,-height,0)),False)
#   sketch.addConstraint(Sketcher.Constraint('Coincident',3,1,1,1)) 
#   sketch.addConstraint(Sketcher.Constraint('Vertical',3)) 
#   sketch.addGeometry(Part.LineSegment(Vector(-Radius1-5,-height,0),
#                                       Vector(Radius1+5,-height,0)),False)
#   sketch.addConstraint(Sketcher.Constraint('Coincident',4,1,2,2)) 
#   sketch.addConstraint(Sketcher.Constraint('Coincident',4,2,3,2)) 
#   sketch.addConstraint(Sketcher.Constraint('Horizontal',4)) 
#   sketch.addConstraint(Sketcher.Constraint('DistanceY',3,2,3,1,height)) 
  
#   pad = obj.newObject('PartDesign::Pad','Pad')
#   pad.Profile = sketch
#   pad.Length = thickness
#   pad.ReferenceAxis = (sketch,['N_Axis'])
#   pad.Midplane = 1
#   sketch.Visibility = False
  
  
#   DOC.recompute()
#   sketch001 = obj.newObject('Sketcher::SketchObject', name+'_sketch001')
#   sketch001.Support = (pad,['Face3',])
#   sketch001.MapMode = 'FlatFace'
  
#   sketch001.addGeometry(Part.Circle(Vector(0,0,0),Vector(0,0,1),Hole_Radius),
#                         False)
#   sketch001.addConstraint(Sketcher.Constraint('Coincident',0,3,-1,1))
#   sketch001.addConstraint(Sketcher.Constraint('Diameter',0,Hole_Radius*2)) 
  
#   Pocket = obj.newObject('PartDesign::Pocket','Pocket')
#   Pocket.Profile = sketch001
#   Pocket.Length = 10
#   Pocket.ReferenceAxis = (sketch001,['N_Axis'])
#   sketch001.Visibility = False
  
#   obj.ViewObject.ShapeColor = (204/255, 204/255, 204/255)
#   if "transparency" in kwargs.keys():
#     obj.ViewObject.Transparency = kwargs["transparency"]
#   else:
#     obj.ViewObject.Transparency = 0
#   obj.Placement=Placement(Vector(0,0,0), Rotation(90,0,90), Vector(0,0,0))
#   update_geom_info(obj, geom)
  
#   DOC.recompute()
#   return obj

# def draw_large_mount(thickness=30,geom=None):
#   """
#   draw a large mount
#   Normally, this function is not called separately.

#   Parameters
#   ----------
#   thickness : float/int, optional
#     the thickness of the large mirror. The default is 30.
#   geom : TYPE, optional
#     mirror geom. The default is None.

#   Returns
#   -------
#   TYPE
#     DESCRIPTION.

#   """
  
#   POS = geom[0]
#   AXES = geom[1]
#   if np.shape(AXES)==(3,):
#     NORMAL=AXES
#   else:
#     NORMAL=AXES[:,0]
  
#   mesh = True
#   datei = thisfolder + "mount_meshes\\special mount\\large mirror mount"
#   if mesh:
#     DOC = get_DOC()
#     obj = DOC.addObject("Mesh::Feature", "large mirror mount")
#     datei += ".stl"
#     obj.Mesh = Mesh.Mesh(datei)
#   else:
#     datei += ".step"
#     obj = ImportGui.insert(datei, "labor_116")
#   offset=Vector(thickness-30,0,0)
#   obj.Placement = Placement(offset, Rotation(0,0,0), Vector(0,0,0))
#   update_geom_info(obj,geom,off0=offset)
#   if POS[2]>70:
#     Geom_ground = (np.array((POS[0],POS[1],0)), np.array((NORMAL)))
#     obj1 = DOC.addObject("Part::Cylinder","Cylinder")
#     obj1.Label = "Post"
#     obj1.Radius = 38 #35.05
#     obj1.Height = POS[2]-70
#     offset1 = Vector(78.95+thickness-30,0,0)
#     obj1.Placement = Placement(offset1, Rotation(0,0,0), Vector(0,0,0))
#     update_geom_info(obj1, Geom_ground,off0=offset1)
#     part = initialize_composition_old(name="mount and post")
#     container = obj,obj1
#     add_to_composition(part, container)
#     return part
#   else:
#     print("this mirror shouldn't be placed at this height.")
  
  
#   return obj

# def draw_stripe_mount(thickness=25,geom=None):
#   """
#   draw a stripe mount
#   Normally, this function is not called separately.

#   Parameters
#   ----------
#   thickness : float/int, optional
#     the thickness of the stripe mirror. The default is 25.
#   geom : TYPE, optional
#     mirror geom. The default is None.

#   Returns
#   -------
#   obj : TYPE
#     DESCRIPTION.

#   """
#   mesh = True
#   datei = thisfolder + "mount_meshes\\special mount\\Stripe mirror mount"
#   if mesh:
#     DOC = get_DOC()
#     obj = DOC.addObject("Mesh::Feature", "Stripe mirror mount")
#     datei += ".stl"
#     obj.Mesh = Mesh.Mesh(datei)
#   else:
#     datei += ".step"
#     obj = ImportGui.insert(datei, "labor_116")
#   offset=Vector(thickness-25,0,0)
#   obj.Placement = Placement(offset, Rotation(0,0,0), Vector(0,0,0))
#   update_geom_info(obj,geom,off0=offset)
#   return obj

# def draw_rooftop_mount(xxshift=0,geom=None):
#   """
#   draw a rooftop mount

#   Parameters
#   ----------
#   xxshift : TYPE, optional
#     a shift to fit the mirror, which is related to the periscope_distance.
#     The default is 0.
#   geom : TYPE, optional
#     DESCRIPTION. The default is None.

#   Returns
#   -------
#   obj : TYPE
#     DESCRIPTION.

#   """
#   mesh = True
#   datei = thisfolder + "mount_meshes\\special mount\\rooftop mirror mount"
#   if mesh:
#     DOC = get_DOC()
#     obj = DOC.addObject("Mesh::Feature", "rooftop mirror mount")
#     datei += ".stl"
#     obj.Mesh = Mesh.Mesh(datei)
#   else:
#     datei += ".step"
#     obj = ImportGui.insert(datei, "labor_116")
#   offset=Vector(xxshift,0,0)
#   obj.Placement = Placement(offset, Rotation(0,0,0), Vector(0,0,0))
#   update_geom_info(obj,geom,off0=offset)
#   return obj

# def rotate_vector(shiftvec=np.array((1.0,0,0)),vec=np.array((1.0,0,0)),angle=0):
#   """
#   rotates the shiftvec around vec with angle 

#   Parameters
#   ----------
#   shiftvec : np.array(), optional
#     The vector needs to be rotated. The default is np.array((1,0,0)).
#   vec : np.array(), optional
#     The rotating axis. The default is np.array((1,0,0)).
#   angle : float/int, optional
#     The angle. The default is 0.

#   Returns
#   -------
#   TYPE
#     DESCRIPTION.

#   """
#   shiftvec = Vector(shiftvec)
#   vec = Vector(vec)
#   return shiftvec*math.cos(angle)+vec.cross(shiftvec)*math.sin(angle)+vec*(vec*shiftvec)*(1-math.cos(angle))

# def model_table():
#   datei1 = thisfolder + "post\\optical breadboard.stl" 
#   DOC = get_DOC()
#   obj = DOC.addObject("Mesh::Feature", "optical breadboard")
#   obj.Mesh = Mesh.Mesh(datei1)
#   obj.Label = "optical breadboard"
#   obj.Placement =Placement(Vector(-750,-400,0),Rotation(0,0,0), Vector(0,0,0))
  
#   DOC.recompute()
#   return obj




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
