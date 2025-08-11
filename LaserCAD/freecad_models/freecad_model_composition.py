# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 12:48:34 2022

@author: mens
"""


# import sys
# sys.path.append(u'/home/mens/Nextcloud/FreeCAD/opticslib2/basic_objects/freecad_models')
# sys.path.append(u"C:/Users/mens/Nextcloud/FreeCAD/opticslib2/basic_objects/freecad_models")

# from .utils import freecad_da, update_geom_info
from .utils import get_DOC
# if freecad_da:
  # from FreeCAD import Vector
  # import Part
  # import Sketcher
  # from math import pi
  
  
def initialize_composition_old(name="compostion"):
  DOC = get_DOC()
  part = DOC.addObject('App::Part', name)
  part.Label = name
  return part

def initialize_composition(name="compostion"):
  DOC = get_DOC()
  mainpart = DOC.addObject('App::Part', name)
  mainpart.Label = name
  
  elements_part = DOC.addObject('App::Part', name+"_elements")
  elements_part.Label = name+"_elements"
  elements_part.adjustRelativeLinks(mainpart)
  mainpart.addObject(elements_part)
  
  mounts_part = DOC.addObject('App::Part', name+"_mounts")
  mounts_part.Label = name+"_mounts"
  mounts_part.adjustRelativeLinks(mainpart)
  mainpart.addObject(mounts_part)
  
  beams_part = DOC.addObject('App::Part', name+"_beams")
  beams_part.Label = name+"_beams"
  beams_part.adjustRelativeLinks(mainpart)
  mainpart.addObject(beams_part)
  
  alignment_post_part = DOC.addObject('App::Part', name+"_alignment_post")
  alignment_post_part.Label = name+"_alignment_post"
  alignment_post_part.adjustRelativeLinks(mainpart)
  mainpart.addObject(alignment_post_part)
  
  # rays_part = DOC.addObject('App::Part', name+"_rays")
  # rays_part.Label = name+"_rays"
  # rays_part.adjustRelativeLinks(mainpart)
  # mainpart.addObject(rays_part)
  # return (mainpart, elements_part, mounts_part, beams_part, rays_part)
  return (mainpart, elements_part, mounts_part, beams_part,alignment_post_part)


def add_to_composition(part, container):
  # print("add_comp called")
  for obj in container:
    # print("obj z.z.", obj)
    if obj: #manche sind auch None, z.B. Propagation
      # print("obj hinzugefuegt:", obj)
      obj.adjustRelativeLinks(part)
      part.addObject(obj)

# def make_to_ray_part(name, part, container):
#   DOC = get_DOC()
#   name += "_rays"
#   counter = 0
#   sub_parts= []
#   for raygroup in container:
#     counter += 1
#     subpart = DOC.addObject("App::Part", name+"_"+str(counter))
#     add_to_composition(subpart, raygroup)
#     sub_parts.append(subpart)
#   add_to_composition(part, sub_parts)