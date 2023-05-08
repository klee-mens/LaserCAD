# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 12:14:01 2023

@author: mens
"""


from .utils import freecad_da, update_geom_info, get_DOC, GEOM0, thisfolder
from .freecad_model_composition import initialize_composition_old, add_to_composition
from .freecad_model_mounts import  mirror_mount
import numpy as np
import math
if freecad_da:
  from FreeCAD import Vector, Placement, Rotation
  import Part
  import Mesh
  import ImportGui
  
DEFUALT_DIM = (50, 50, 8)
DEFUALT_COLOR = (170/255, 170/255, 1.0)  

def model_grating(name="grating", dimensions=DEFUALT_DIM, geom=GEOM0, 
                  color=DEFUALT_COLOR):
  """
  kreiert das Model eines Gitters durch simples Erzeugen eines Quaders
  creates the model of a grid by simply creating a box

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
  obj.Height = dimensions[1]
  obj.Width = dimensions[0]
  obj.Length = dimensions[2]
  obj.ViewObject.ShapeColor = color
  offset = Vector(0, -obj.Width/2,-obj.Height/2)
  obj.Placement = Placement(offset, Rotation(0,0,0), Vector(0,0,0))

  update_geom_info(obj, geom, off0=offset)
  DOC.recompute()
  return obj

def grating_mount(name="grating_mount",height=50,thickness=8,base_exists=False,geom=None, **kwargs):
  """
    Build the mount of the grating.

    Parameters
    ----------
    name : String, optional
        The name of the mount. The default is "grating_mount".
    height : float/int, optional
        The height of the grating. The default is 50.
    thickness : float/int, optional
        The thickness of the grating. The default is 8.
    geom : TYPE, optional
        geom info. The default is None.
    **kwargs : TYPE
        DESCRIPTION.

    Returns
    -------
    part : TYPE
        DESCRIPTION.

    """
  if height<=20:
    grating_mount_name="KGM20"
  elif height<=40:
    grating_mount_name="KGM40"
  elif height<=60:
    grating_mount_name="KGM60"
  else:
    print("there is no suitable mount for this grating")
    return None
  mount1 = draw_mount(name=grating_mount_name+"_base",height=height,thickness=thickness,geom=geom)
  mount2 = draw_mount(name=grating_mount_name+"_buttom_half",height=height,thickness=thickness,geom=geom)
  mount3 = draw_mount(name=grating_mount_name+"_top_half",height=height,thickness=thickness,geom=geom)
  
  xshift=17
  shiftvec=Vector(xshift,0,0)
  default=Vector(1,0,0)
  default_axis=Vector(0,1,0)
  # normal=Vector(geom[1])
  axes = geom[1]
  normal = Vector(axes[:,0])
  angle = default.getAngle(normal)
  if angle!=0:
    vec = default.cross(normal)
    vec = vec/np.linalg.norm(vec)
    shiftvec = rotate_vector(shiftvec=shiftvec,vec=vec,angle=angle)
    default_axis = rotate_vector(shiftvec=default_axis,vec=vec,angle=angle)
    default_axis = default_axis/np.linalg.norm(default_axis)
  if angle==np.pi/180:
    shiftvec = -shiftvec
  new_normal = Vector(normal)
  new_pos = Vector(geom[0])+shiftvec
  # geom = (new_pos,new_normal)
  newaxs = np.array(axes)
  newaxs[:,0] = new_normal
  geom = (new_pos, newaxs)
  other_mount = mirror_mount(mount_name="mirror_mount",mount_type="default",base_exists=base_exists, geom=geom, dia=25.4)
  part = initialize_composition_old(name="Grating mount, post and base")
  container = mount1,mount2,mount3,other_mount
  add_to_composition(part, container)

  return part

def draw_mount(name="KGM60_base",height=50,thickness=8,geom=None):
  """
    Draw the part of the mount.
    Since the grating mount is divided into three parts, this function will 
    draw one part of the mount. 

    Parameters
    ----------
    name : TYPE, optional
        Part name. The default is "KGM60_base".
    height : float/int, optional
        The height of the grating. The default is 50.
    thickness : float/int, optional
        The thickness of the grating. The default is 8.
    geom : TYPE, optional
        geom info. The default is None.

    Returns
    -------
    obj : TYPE
        DESCRIPTION.

    """
  mesh = True
  xshift = thickness-8
  if "60" in name:
    zshift = (height-50)/2
  elif "40" in name:
    zshift = (height-30)/2
  elif "20" in name:
    zshift = (height-10)/2
  datei = thisfolder + "mount_meshes\\Grating\\" + name
  if mesh:
    DOC = get_DOC()
    obj = DOC.addObject("Mesh::Feature", name)
    datei += ".stl"
    obj.Mesh = Mesh.Mesh(datei)
  else:
    datei += ".step"
    obj = ImportGui.insert(datei, "labor_116")
  if "base" in name:
    offset=Vector(xshift,0,0)
    obj.Placement = Placement(offset, Rotation(0,0,0), Vector(0,0,0))
  elif "top" in name:
    offset=Vector(xshift,0,zshift)
    obj.Placement = Placement(offset, Rotation(0,0,0), Vector(0,0,0))
  elif "buttom" in name:
    offset=Vector(xshift,0,-zshift)
    obj.Placement = Placement(offset, Rotation(0,0,0), Vector(0,0,0))
  update_geom_info(obj,geom, off0=offset)
  return obj
  
def rotate_vector(shiftvec=np.array((1.0,0,0)),vec=np.array((1.0,0,0)),angle=0):
  """
  rotates the shiftvec around vec with angle 

  Parameters
  ----------
  shiftvec : np.array(), optional
    The vector needs to be rotated. The default is np.array((1,0,0)).
  vec : np.array(), optional
    The rotating axis. The default is np.array((1,0,0)).
  angle : TYPE, optional
    The angle. The default is 0.

  Returns
  -------
  TYPE
    DESCRIPTION.

  """
  shiftvec = Vector(shiftvec)
  vec = Vector(vec)
  return shiftvec*math.cos(angle)+vec.cross(shiftvec)*math.sin(angle)+vec*(vec*shiftvec)*(1-math.cos(angle))