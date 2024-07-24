#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 01:31:42 2022

@author: mens
"""

from .utils import freecad_da, update_geom_info, get_DOC, GEOM0
from .freecad_model_composition import initialize_composition_old, add_to_composition
import numpy as np
if freecad_da:
  import FreeCAD
  from FreeCAD import Vector, Placement, Rotation
  import Part
  import Sketcher

DEFAULT_COLOR_CRIMSON = (0.86,0.08,0.24) #crimson
MIN_RADIUS =0.5
BEAM_TRANSPARENCY = 50
# BEAM_TRANSPARENCY = 0




def model_beam(name="beam", radius=5, length=200,  angle=0.02,
                   color=DEFAULT_COLOR_CRIMSON,geom=GEOM0, **kwargs):
  DOC = get_DOC()

  if abs(angle) < 1E-9:
    obj = DOC.addObject("Part::Cylinder", name)
    obj.Height = length
    obj.Radius = radius
  else:
    f = - radius/np.tan(angle)
    if f == 0:
      radius2 = length * np.tan(angle)
      obj = DOC.addObject("Part::Cone", name)
      obj.Height = length
      obj.Radius1 = radius
      obj.Radius2 = radius2
    elif length <= f or f < 0:
      radius2 = radius * (f-length)/f
      obj = DOC.addObject("Part::Cone", name)
      obj.Height = length
      obj.Radius1 = radius
      obj.Radius2 = radius2
    else:
      radius2 = 0
      obj1 = DOC.addObject("Part::Cone", name+"_1")
      obj1.Height = f
      obj1.Radius1 = radius
      obj1.Radius2 = radius2
      radius3 =  radius * (length-f)/f
      obj2 = DOC.addObject("Part::Cone", name+"_2")
      obj2.Height = length - f
      obj2.Radius1 = radius2
      obj2.Radius2 = radius3
      obj2.Placement = FreeCAD.Placement(Vector(0,0,f), FreeCAD.Rotation(Vector(0,1,0),0), Vector(0,0,0))
      obj = DOC.addObject("Part::Fuse", name)
      obj.Base = obj1
      obj.Tool = obj2
      obj.Refine = True
      DOC.recompute()
  obj.Placement = FreeCAD.Placement(Vector(0,0,0), FreeCAD.Rotation(Vector(0,1,0),90), Vector(0,0,0))
  obj.ViewObject.ShapeColor = color
  # obj.ViewObject.Transparency = 50
  obj.Label = name
  update_geom_info(obj, geom)

  DOC.recompute()
  return obj

def model_asti_beam (name="beam", dia_l=10,dia_s=10, prop=200,  f_l=100,f_s=150,rot_angle=0, color=DEFAULT_COLOR_CRIMSON,
               geom=None):
  """
  creates a beam that take astigmatism account
  Parameters
  ----------
  name : string,
    beams name. The default is "beam".
  dia_l : float,
    diameter of one direction. The default is 10.
  dia_s : float, optional
    diameter of the other direction. The default is 10.
  prop : float, optional
    Propagation length. The default is 200.
  f_l : float, optional
    The first Focal length. The default is 100.
  f_s : float, optional
    The second focal length. The default is 150.
  rot_angle : float, optional
    rotation angle. The default is 0.
  color : float, optional
    The color of beam. The default is DEFAULT_COLOR_CRIMSON.
  geom : float, optional
    The default is None.

  Returns
  -------
  part : TYPE
    DESCRIPTION.
  example: beam1=model_asti_beam(name="beam", dia_l=20,dia_s=10, prop=150,  f_l=-100,f_s=-100,rot_angle=0)
  """
  DOC = get_DOC()
  obj = DOC.addObject('PartDesign::Body', name)
  sketch = obj.newObject('Sketcher::SketchObject', name+'_sketch')
  sketch.MapMode = 'FlatFace'
  sketch.addGeometry(Part.Ellipse(Vector(dia_l,-0,0),Vector(0,dia_s,0),Vector(0,0,0)),False)
  sketch.Placement=Placement(Vector(0,0,0), Rotation(Vector(0,0,1),rot_angle), Vector(0,0,0))
  if f_l>0 and f_s>0:
    if f_l!=f_s:
      if prop <= min(f_l,f_s):
        sketch_end = obj.newObject('Sketcher::SketchObject', name+'_sketch_end')
        sketch_end.MapMode = 'FlatFace'
        if abs(dia_l/f_l*(prop-f_l))>abs(dia_s/f_s*(f_s-prop)):
          sketch_end.addGeometry(Part.Ellipse(Vector(max(abs(dia_l/f_l*(f_l-prop)),MIN_RADIUS),-0,0),Vector(0,max(abs(dia_s/f_s*(f_s-prop)),0),MIN_RADIUS),Vector(0,0,0)),False)
        else:
          sketch_end.addGeometry(Part.Ellipse(Vector(0,max(abs(dia_s/f_s*(f_s-prop)),MIN_RADIUS),0),Vector(max(abs(dia_l/f_l*(f_l-prop)),MIN_RADIUS),0,0),Vector(0,0,0)),False)
        sketch_end.Placement=Placement(Vector(0,0,prop), Rotation(Vector(0,0,1),rot_angle), Vector(0,0,0))
        addi=obj.newObject('PartDesign::AdditiveLoft','AdditiveLoft')
        addi.Profile = sketch
        addi.Sections = sketch_end
        sketch.Visibility = False
        sketch_end.Visibility = False
        obj.ViewObject.ShapeColor = color
        obj.ViewObject.Transparency = 50
        update_geom_info(obj, geom)
        obj1=obj2=None
      else:
        sketch_f1 = obj.newObject('Sketcher::SketchObject', name+'_sketch_f1')
        sketch_f1.MapMode = 'FlatFace'
        if f_l<f_s:
          sketch_f1.addGeometry(Part.Ellipse(Vector(0.0,max(abs(dia_s/f_s*(f_s-f_l)),0),MIN_RADIUS),Vector(MIN_RADIUS,0,0),Vector(0,0,0)),False)
          sketch_f1.Placement=Placement(Vector(0,0,f_l), Rotation(Vector(0,0,1),rot_angle), Vector(0,0,0))
        else:
          sketch_f1.addGeometry(Part.Ellipse(Vector(max(abs(dia_l/f_l*(f_l-f_s)),MIN_RADIUS),0,0),Vector(0,MIN_RADIUS,0),Vector(0,0,0)),False)
          sketch_f1.Placement=Placement(Vector(0,0,f_s), Rotation(Vector(0,0,1),rot_angle), Vector(0,0,0))
        addi=obj.newObject('PartDesign::AdditiveLoft','AdditiveLoft')
        addi.Profile = sketch
        addi.Sections = sketch_f1
        sketch.Visibility = False
        sketch_f1.Visibility = False
        obj.ViewObject.ShapeColor = color
        obj.ViewObject.Transparency = 50
        update_geom_info(obj, geom)
        obj1 = DOC.addObject('PartDesign::Body', name+'1')
        if prop < max(f_s,f_l):
          sketch_end = obj1.newObject('Sketcher::SketchObject', name+'_sketch_end')
          sketch_end.MapMode = 'FlatFace'
          if abs(dia_l/f_l*(prop-f_l))>abs(dia_s/f_s*(f_s-prop)):
            sketch_end.addGeometry(Part.Ellipse(Vector(max(abs(dia_l/f_l*(prop-f_l)),MIN_RADIUS),-0,0),Vector(0,max(abs(dia_s/f_s*(f_s-prop)),MIN_RADIUS),0),Vector(0,0,0)),False)
          else:
            sketch_end.addGeometry(Part.Ellipse(Vector(0,max(abs(dia_s/f_s*(f_s-prop)),MIN_RADIUS),0),Vector(max(abs(dia_l/f_l*(prop-f_l)),MIN_RADIUS),0,0),Vector(0,0,0)),False)
          sketch_end.Placement=Placement(Vector(0,0,prop), Rotation(Vector(0,0,1),rot_angle), Vector(0,0,0))
          addi=obj1.newObject('PartDesign::AdditiveLoft','AdditiveLoft1')
          addi.Profile = sketch_f1
          addi.Sections = sketch_end
          sketch_f1.Visibility = False
          sketch_end.Visibility = False
          obj.ViewObject.ShapeColor = color
          obj.ViewObject.Transparency = 50
          update_geom_info(obj, geom)
          obj1.ViewObject.ShapeColor = color
          obj1.ViewObject.Transparency = 50
          update_geom_info(obj1, geom)
          obj2=None
        else:
          sketch_f2 = obj1.newObject('Sketcher::SketchObject', name+'_sketch_f2')
          sketch_f2.MapMode = 'FlatFace'
          if f_l<f_s:
            sketch_f2.addGeometry(Part.Ellipse(Vector(max(abs(dia_l/f_l*(f_s-f_l)),MIN_RADIUS),-0,0),Vector(0,MIN_RADIUS,0),Vector(0,0,0)),False)
            sketch_f2.Placement=Placement(Vector(0,0,f_s), Rotation(Vector(0,0,1),rot_angle), Vector(0,0,0))
          else:
            sketch_f2.addGeometry(Part.Ellipse(Vector(0,max(abs(dia_s/f_s*(f_l-f_s)),MIN_RADIUS),0),Vector(MIN_RADIUS,0,0),Vector(0,0,0)),False)
            sketch_f2.Placement=Placement(Vector(0,0,f_l), Rotation(Vector(0,0,1),rot_angle), Vector(0,0,0))
          addi=obj1.newObject('PartDesign::AdditiveLoft','AdditiveLoft1')
          addi.Profile = sketch_f1
          addi.Sections = sketch_f2
          sketch_f1.Visibility = False
          sketch_f2.Visibility = False
          if prop == max(f_l,f_s):
            obj2=None
            obj.ViewObject.ShapeColor = color
            obj.ViewObject.Transparency = 50
            update_geom_info(obj, geom)
            obj1.ViewObject.ShapeColor = color
            obj1.ViewObject.Transparency = 50
            update_geom_info(obj1, geom)
          else:
            obj2 = DOC.addObject('PartDesign::Body', name+'2')
            sketch_end = obj2.newObject('Sketcher::SketchObject', name+'_sketch_end')
            sketch_end.MapMode = 'FlatFace'
            if abs(dia_l/f_l*(f_l-prop))>abs(dia_s/f_s*(f_s-prop)):
              sketch_end.addGeometry(Part.Ellipse(Vector(max(abs(dia_l/f_l*(f_l-prop)),MIN_RADIUS),-0,0),Vector(0,max(abs(dia_s/f_s*(f_s-prop)),MIN_RADIUS),0),Vector(0,0,0)),False)
            else:
              sketch_end.addGeometry(Part.Ellipse(Vector(0,max(abs(dia_s/f_s*(f_s-prop)),MIN_RADIUS),0),Vector(max(abs(dia_l/f_l*(f_l-prop)),MIN_RADIUS),-0,0),Vector(0,0,0)),False)
            sketch_end.Placement=Placement(Vector(0,0,prop), Rotation(Vector(0,0,1),rot_angle), Vector(0,0,0))
            addi=obj2.newObject('PartDesign::AdditiveLoft','AdditiveLoft2')
            addi.Profile = sketch_f2
            addi.Sections = sketch_end
            sketch_f2.Visibility = False
            sketch_end.Visibility = False
            obj.ViewObject.ShapeColor = color
            obj.ViewObject.Transparency = 50
            update_geom_info(obj, geom)
            obj1.ViewObject.ShapeColor = color
            obj1.ViewObject.Transparency = 50
            update_geom_info(obj1, geom)
            obj2.ViewObject.ShapeColor = color
            obj2.ViewObject.Transparency = 50
            update_geom_info(obj2, geom)
    else:
      if prop < f_l:
        sketch_end = obj.newObject('Sketcher::SketchObject', name+'_sketch_end')
        sketch_end.MapMode = 'FlatFace'
        if dia_l/f_l*(f_l-prop)>dia_s/f_s*(f_s-prop):
          sketch_end.addGeometry(Part.Ellipse(Vector(max(abs(dia_l/f_l*(f_l-prop)),MIN_RADIUS),-0,0),Vector(0,max(abs(dia_s/f_s*(f_s-prop)),MIN_RADIUS),0),Vector(0,0,0)),False)
        else:
          sketch_end.addGeometry(Part.Ellipse(Vector(0,max(abs(dia_s/f_s*(f_s-prop)),MIN_RADIUS),0),Vector(max(abs(dia_l/f_l*(f_l-prop)),MIN_RADIUS),0,0),Vector(0,0,0)),False)
        sketch_end.Placement=Placement(Vector(0,0,prop), Rotation(Vector(0,0,1),rot_angle), Vector(0,0,0))
        addi=obj.newObject('PartDesign::AdditiveLoft','AdditiveLoft')
        addi.Profile = sketch
        addi.Sections = sketch_end
        sketch.Visibility = False
        sketch_end.Visibility = False
        obj.ViewObject.ShapeColor = color
        obj.ViewObject.Transparency = 50
        update_geom_info(obj, geom)
        obj1=obj2=None
      else:
        sketch_f_l = obj.newObject('Sketcher::SketchObject', name+'_sketch_f_l')
        sketch_f_l.MapMode = 'FlatFace'
        sketch_f_l.addGeometry(Part.Ellipse(Vector(0.0,MIN_RADIUS,0),Vector(MIN_RADIUS,0,0),Vector(0,0,0)),False)
        sketch_f_l.Placement=Placement(Vector(0,0,f_l), Rotation(Vector(0,0,1),rot_angle), Vector(0,0,0))
        addi=obj.newObject('PartDesign::AdditiveLoft','AdditiveLoft')
        addi.Profile = sketch
        addi.Sections = sketch_f_l
        sketch.Visibility = False
        sketch_f_l.Visibility = False
        obj1 = DOC.addObject('PartDesign::Body', name+'1')
        sketch_end = obj1.newObject('Sketcher::SketchObject', name+'_sketch_end')
        sketch_end.MapMode = 'FlatFace'
        if dia_l/f_l*(f_l-prop)<dia_s/f_s*(f_s-prop):
          sketch_end.addGeometry(Part.Ellipse(Vector(max(abs(dia_l/f_l*(f_l-prop)),MIN_RADIUS),-0,0),Vector(0,max(abs(dia_s/f_s*(f_s-prop)),MIN_RADIUS),0),Vector(0,0,0)),False)
        else:
          sketch_end.addGeometry(Part.Ellipse(Vector(0,max(abs(dia_s/f_s*(f_s-prop)),MIN_RADIUS),0),Vector(max(abs(dia_l/f_l*(f_l-prop)),MIN_RADIUS),0,0),Vector(0,0,0)),False)
        sketch_end.Placement=Placement(Vector(0,0,prop), Rotation(Vector(0,0,1),rot_angle), Vector(0,0,0))
        addi=obj1.newObject('PartDesign::AdditiveLoft','AdditiveLoft')
        addi.Profile = sketch_f_l
        addi.Sections = sketch_end
        sketch_f_l.Visibility = False
        sketch_end.Visibility = False
        obj.ViewObject.ShapeColor = color
        obj.ViewObject.Transparency = 50
        update_geom_info(obj, geom)
        obj1.ViewObject.ShapeColor = color
        obj1.ViewObject.Transparency = 50
        update_geom_info(obj1, geom)
        obj2=None
  elif f_s<0 and f_l<0:
    sketch_end = obj.newObject('Sketcher::SketchObject', name+'_sketch_end')
    sketch_end.MapMode = 'FlatFace'
    if dia_l/f_l*(f_l-prop)>dia_s/f_s*(f_s-prop):
      sketch_end.addGeometry(Part.Ellipse(Vector(max(abs(dia_l/f_l*(f_l-prop)),MIN_RADIUS),-0,0),Vector(0,max(abs(dia_s/f_s*(f_s-prop)),MIN_RADIUS),0),Vector(0,0,0)),False)
    else:
      sketch_end.addGeometry(Part.Ellipse(Vector(0,max(abs(dia_s/f_s*(f_s-prop)),MIN_RADIUS),0),Vector(max(abs(dia_l/f_l*(f_l-prop)),MIN_RADIUS),0,0),Vector(0,0,0)),False)
    sketch_end.Placement=Placement(Vector(0,0,prop), Rotation(Vector(0,0,1),rot_angle), Vector(0,0,0))
    addi=obj.newObject('PartDesign::AdditiveLoft','AdditiveLoft')
    addi.Profile = sketch
    addi.Sections = sketch_end
    sketch.Visibility = False
    sketch_end.Visibility = False
    obj.ViewObject.ShapeColor = color
    obj.ViewObject.Transparency = 50
    update_geom_info(obj, geom)
    obj1=obj2=None
  else:
    if max(f_l,f_s)>=prop:
      sketch_end = obj.newObject('Sketcher::SketchObject', name+'_sketch_end')
      sketch_end.MapMode = 'FlatFace'
      if dia_l/f_l*(f_l-prop)>dia_s/f_s*(f_s-prop):
        sketch_end.addGeometry(Part.Ellipse(Vector(max(abs(dia_l/f_l*(f_l-prop)),MIN_RADIUS),-0,0),Vector(0,max(abs(dia_s/f_s*(f_s-prop)),0),MIN_RADIUS),Vector(0,0,0)),False)
      else:
        sketch_end.addGeometry(Part.Ellipse(Vector(0,max(abs(dia_s/f_s*(f_s-prop)),MIN_RADIUS),0),Vector(max(abs(dia_l/f_l*(f_l-prop)),MIN_RADIUS),0,0),Vector(0,0,0)),False)
      sketch_end.Placement=Placement(Vector(0,0,prop), Rotation(Vector(0,0,1),rot_angle), Vector(0,0,0))
      addi=obj.newObject('PartDesign::AdditiveLoft','AdditiveLoft')
      addi.Profile = sketch
      addi.Sections = sketch_end
      sketch.Visibility = False
      sketch_end.Visibility = False
      obj.ViewObject.ShapeColor = color
      obj.ViewObject.Transparency = 50
      update_geom_info(obj, geom)
      obj1=obj2=None
    else:
      sketch_f =  obj.newObject('Sketcher::SketchObject', name+'_sketch_end')
      sketch_f.MapMode = 'FlatFace'
      if f_l<f_s:
        sketch_f.addGeometry(Part.Ellipse(Vector(max(abs(dia_l/f_l*(f_s-f_l)),MIN_RADIUS),-0,0),Vector(0,MIN_RADIUS,0),Vector(0,0,0)),False)
        sketch_f.Placement=Placement(Vector(0,0,f_s), Rotation(Vector(0,0,1),rot_angle), Vector(0,0,0))
      else:
        sketch_f.addGeometry(Part.Ellipse(Vector(0.0,max(abs(dia_s/f_s*(f_s-f_l)),MIN_RADIUS),0),Vector(MIN_RADIUS,0,0),Vector(0,0,0)),False)
        sketch_f.Placement=Placement(Vector(0,0,f_l), Rotation(Vector(0,0,1),rot_angle), Vector(0,0,0))
      addi=obj.newObject('PartDesign::AdditiveLoft','AdditiveLoft')
      addi.Profile = sketch
      addi.Sections = sketch_f
      sketch.Visibility = False
      sketch_f.Visibility = False
      obj1 = DOC.addObject('PartDesign::Body', name+'1')
      sketch_end = obj1.newObject('Sketcher::SketchObject', name+'_sketch_end')
      sketch_end.MapMode = 'FlatFace'
      if dia_l/f_l*(f_l-prop)>dia_s/f_s*(f_s-prop):
        sketch_end.addGeometry(Part.Ellipse(Vector(max(abs(dia_l/f_l*(f_l-prop)),MIN_RADIUS),-0,0),Vector(0,max(abs(dia_s/f_s*(f_s-prop)),MIN_RADIUS),0),Vector(0,0,0)),False)
      else:
        sketch_end.addGeometry(Part.Ellipse(Vector(0,max(abs(dia_s/f_s*(f_s-prop)),MIN_RADIUS),0),Vector(max(abs(dia_l/f_l*(f_l-prop)),MIN_RADIUS),0,0),Vector(0,0,0)),False)
      sketch_end.Placement=Placement(Vector(0,0,prop), Rotation(Vector(0,0,1),rot_angle), Vector(0,0,0))
      addi=obj1.newObject('PartDesign::AdditiveLoft','AdditiveLoft')
      addi.Profile = sketch_f
      addi.Sections = sketch_end
      sketch_f.Visibility = False
      sketch_end.Visibility = False
      obj.ViewObject.ShapeColor = color
      obj.ViewObject.Transparency = 50
      update_geom_info(obj, geom)
      obj1.ViewObject.ShapeColor = color
      obj1.ViewObject.Transparency = 50
      update_geom_info(obj1, geom)
      obj2=None

  part = initialize_composition_old(name="asti beam")
  container = obj,obj1,obj2
  add_to_composition(part, container)
  part.Placement = FreeCAD.Placement(Vector(0,0,0), FreeCAD.Rotation(Vector(0,1,0),90), Vector(0,0,0))
  DOC.recompute()
  return part

def model_Gaussian_beam (name="Gaussian_beam",q_para=-100+200j,prop=200,wavelength=650E-6,
                          color=DEFAULT_COLOR_CRIMSON,beam_count=1, geom=None):
    """
    creates a Gaussian beam.
    Parameters
    ----------
    name : TYPE, optional
        beam name. The default is "Gaussian_beam".
    q : TYPE, optional
        q-parameter. The default is -100+200j.
    prop : TYPE, optional
        propgation length. The default is 200.
    wavelength : TYPE, optional
        wavelength. The default is 650E-9.
    color : TYPE, optional
        beam color. The default is DEFAULT_COLOR_CRIMSON.
    geom : TYPE, optional
        DESCRIPTION. The default is None.

    Returns
    -------
    obj : TYPE
        DESCRIPTION.
    example: beam1 = model_beam("laser1", -100+200j, 200, 650E-6)
    """
    DOC = get_DOC()
    # obj = DOC.addObject('PartDesign::Body', name)
    # sketch = obj.newObject('Sketcher::SketchObject', name+'_sketch')
    # # sketch.Support = (DOC.getObject('XY_Plane'),[''])
    # sketch.MapMode = 'FlatFace'
    z0 = np.imag(q_para)
    z_start=np.real(q_para)
    z_end = z_start+prop
    w0 = pow(wavelength*z0/np.pi,0.5)
    w_start = w0 * pow(1+(z_start/z0)**2,0.5)
    # print("w_sart=",w_start)
    w_end = w0 * pow(1+(z_end/z0)**2,0.5)

    obj = DOC.addObject('PartDesign::Body', name)
    sketch = obj.newObject('Sketcher::SketchObject', name+'_sketch')
    # sketch.Support = (DOC.getObject('XY_Plane'),[''])
    sketch.MapMode = 'FlatFace'
    sketch.addGeometry(Part.LineSegment(Vector(0,0,0),Vector(0,w_start,0)),False)
    sketch.addConstraint(Sketcher.Constraint('Coincident',-1,1,0,1))
    sketch.addConstraint(Sketcher.Constraint('PointOnObject',0,2,-2))
    sketch.addConstraint(Sketcher.Constraint('DistanceY',0,1,0,2,w_start))
    sketch.addGeometry(Part.LineSegment(Vector(0,0,0),Vector(prop,0,0)),False)
    sketch.addConstraint(Sketcher.Constraint('Coincident',1,1,0,1))
    sketch.addConstraint(Sketcher.Constraint('PointOnObject',1,2,-1))
    sketch.addConstraint(Sketcher.Constraint('DistanceX',1,1,1,2,prop))
    sketch.addGeometry(Part.LineSegment(Vector(prop,0,0),Vector(prop,w_end,0)),False)
    sketch.addConstraint(Sketcher.Constraint('Coincident',2,1,1,2))
    sketch.addConstraint(Sketcher.Constraint('Vertical',2))
    ii = 0
    for ii in range(int(prop)):
      new_pos = ii*10
      new_w = w0 * pow(1+((z_start+new_pos)/z0)**2,0.5)
      next_w = w0 * pow(1+((z_start+new_pos+10)/z0)**2,0.5)
      if new_pos+10>=prop:
        sketch.addGeometry(Part.LineSegment(Vector(new_pos,new_w,0),Vector(prop,w_end,0)),False)
        if ii == 0:
          sketch.addConstraint(Sketcher.Constraint('Coincident',3,1,0,2))
        else:
          sketch.addConstraint(Sketcher.Constraint('Coincident',int(ii+3),1,int(ii+2),2))
        sketch.addConstraint(Sketcher.Constraint('Coincident',int(ii+3),2,2,2))
        break
      else:
        sketch.addGeometry(Part.LineSegment(Vector(new_pos,new_w,0),Vector(new_pos+10,next_w,0)),False)
        if ii == 0:
          sketch.addConstraint(Sketcher.Constraint('Coincident',3,1,0,2))
        else:
          sketch.addConstraint(Sketcher.Constraint('Coincident',int(ii+3),1,int(ii+2),2))
        sketch.addConstraint(Sketcher.Constraint('DistanceX',int(ii+3),2,new_pos+10))
        sketch.addConstraint(Sketcher.Constraint('DistanceY',int(ii+3),2,next_w))

    rev = obj.newObject('PartDesign::Revolution',name+'_Revolution')
    rev.Profile = sketch
    rev.Angle = 360
    rev.ReferenceAxis = (sketch,'H_Axis')
    rev.Midplane = 0
    rev.Reversed = 1
    sketch.Visibility = False
    """
    if z_start>z0 or z_end<-z0:
      obj = DOC.addObject("Part::Cone", name)
      obj.Height = prop
      obj.Radius1 = z_start/z0*w0
      obj.Radius2 = z_end/z0*w0
    elif z_start>-z0:
      obj1 = DOC.addObject("Part::Cylinder", name+"_1")
      obj1.Height = prop
      obj1.Radius = w0
      if z_end<z0:
        obj=obj1
      else:
        obj2 = DOC.addObject("Part::Cone", name+"_2")
        obj2.Height = prop-(z0-z_start)
        obj2.Radius1=w0
        obj2.Radius2=z_end/z0*w0
        obj2.Placement = FreeCAD.Placement(Vector(0,0,z0-z_start), FreeCAD.Rotation(Vector(0,1,0),0), Vector(0,0,0))
        obj = DOC.addObject("Part::Fuse", name)
        obj.Base = obj1
        obj.Tool = obj2
        obj.Refine = True
        DOC.recompute()
    else:
      if z_end<z0:
        obj1 = DOC.addObject("Part::Cylinder", name+"_1")
        obj1.Height = prop
        obj1.Radius = w0
        obj2 = DOC.addObject("Part::Cone", name+"_2")
        obj2.Height = -z_start-z0
        obj2.Radius1=z_start/z0*w0
        obj2.Radius2=w0
        obj = DOC.addObject("Part::Fuse", name)
        obj.Base = obj1
        obj.Tool = obj2
        obj.Refine = True
        DOC.recompute()
      else:
        obj = DOC.addObject('PartDesign::Body', name)
        sketch = obj.newObject('Sketcher::SketchObject', name+'_sketch')
        # sketch.Support = (DOC.getObject('XY_Plane'),[''])
        sketch.MapMode = 'FlatFace'
        sketch.addGeometry(Part.LineSegment(Vector(0,0,0),Vector(0,-z_start/z0*w0,0)),False)
        sketch.addConstraint(Sketcher.Constraint('Coincident',-1,1,0,1))
        sketch.addConstraint(Sketcher.Constraint('PointOnObject',0,2,-2))
        sketch.addGeometry(Part.LineSegment(Vector(0,-z_start/z0*w0,0),Vector(-z_start-z0,w0,0)),False)
        sketch.addConstraint(Sketcher.Constraint('Coincident',0,2,1,1))
        sketch.addGeometry(Part.LineSegment(Vector(-z_start-z0,w0,0),Vector(z0-z_start,w0,0)),False)
        sketch.addConstraint(Sketcher.Constraint('Coincident',1,2,2,1))
        sketch.addConstraint(Sketcher.Constraint('Horizontal',2))
        sketch.addGeometry(Part.LineSegment(Vector(z0-z_start,w0,0),Vector(prop,z_end/z0*w0,0)),False)
        sketch.addConstraint(Sketcher.Constraint('Coincident',2,2,3,1))
        sketch.addGeometry(Part.LineSegment(Vector(prop,z_end/z0*w0,0),Vector(prop,0,0)),False)
        sketch.addConstraint(Sketcher.Constraint('Coincident',3,2,4,1))
        sketch.addConstraint(Sketcher.Constraint('PointOnObject',4,2,-1))
        sketch.addConstraint(Sketcher.Constraint('Vertical',4))
        sketch.addGeometry(Part.LineSegment(Vector(prop,0,0),Vector(0,0,0)),False)
        sketch.addConstraint(Sketcher.Constraint('Coincident',4,2,5,1))
        sketch.addConstraint(Sketcher.Constraint('Coincident',5,2,0,1))
        sketch.addConstraint(Sketcher.Constraint('DistanceY',0,1,0,2,-z_start/z0*w0))
        sketch.addConstraint(Sketcher.Constraint('DistanceY',4,2,4,1,z_end/z0*w0))
        sketch.addConstraint(Sketcher.Constraint('DistanceX',5,2,5,1,prop))
        sketch.addConstraint(Sketcher.Constraint('DistanceX',2,1,2,2,z0*2))
        sketch.addConstraint(Sketcher.Constraint('DistanceX',1,2,-z_start-z0))
        sketch.addConstraint(Sketcher.Constraint('DistanceY',1,2,w0))
        rev = obj.newObject('PartDesign::Revolution',name+'_Revolution')
        rev.Profile = sketch
        rev.Angle = 360
        rev.ReferenceAxis = (sketch,'H_Axis')
        rev.Midplane = 0
        rev.Reversed = 1
        sketch.Visibility = False


    sketch.addGeometry(Part.ArcOfHyperbola(Part.Hyperbola(Vector(-z_start,w0,0),Vector(-z_start-z0,0,0),Vector(-z_start,0,0)),z_start/z0,z_end/z0),False)
    sketch.exposeInternalGeometry(0)

    sketch.addConstraint(Sketcher.Constraint('DistanceX',-1,1,1,1,-z_start))

    sketch.addConstraint(Sketcher.Constraint('DistanceX',-1,1,0,1,prop))
    sketch.addConstraint(Sketcher.Constraint('DistanceX',-1,1,0,2,0.0))

    # sketch.addGeometry(Part.Point(Vector(-z_start,w0,0)))
    # sketch.addConstraint(Sketcher.Constraint('PointOnObject',1,1,0))
    sketch.addConstraint(Sketcher.Constraint('DistanceY',-1,1,1,1,w0))
    sketch.addConstraint(Sketcher.Constraint('DistanceY',-1,1,0,2,w_start))
    sketch.addConstraint(Sketcher.Constraint('DistanceY',-1,1,0,1,w_end))
    # sketch.addConstraint(Sketcher.Constraint('DistanceY',0,3,-1,1,0.0))

    sketch.addGeometry(Part.LineSegment(Vector(0,w_start,0),Vector(0,0,0)),False)
    sketch.addConstraint(Sketcher.Constraint('Coincident',4,1,0,2))
    sketch.addConstraint(Sketcher.Constraint('Coincident',4,2,-1,1))
    # sketch.addConstraint(Sketcher.Constraint('Vertical',4))

    sketch.addGeometry(Part.LineSegment(Vector(prop,w_end,0),Vector(prop,0,0)),False)
    sketch.addConstraint(Sketcher.Constraint('Coincident',5,1,0,1))
    sketch.addConstraint(Sketcher.Constraint('PointOnObject',5,2,-1))
    sketch.addConstraint(Sketcher.Constraint('Vertical',5))
    sketch.addGeometry(Part.LineSegment(Vector(0,0,0),Vector(prop,0,0)),False)
    sketch.addConstraint(Sketcher.Constraint('Coincident',6,1,4,2))
    sketch.addConstraint(Sketcher.Constraint('Coincident',6,2,5,2))
    # sketch.addConstraint(Sketcher.Constraint('Horizontal',6))

    rev = obj.newObject('PartDesign::Revolution',name+'_Revolution')
    rev.Profile = sketch
    rev.Angle = 360
    rev.ReferenceAxis = (sketch,'H_Axis')
    rev.Midplane = 0
    rev.Reversed = 1
    sketch.Visibility = False
    """
    """
    if z_start>-z0 or z_end<z0:
      obj.Placement = FreeCAD.Placement(Vector(0,0,0), FreeCAD.Rotation(Vector(0,1,0),90), Vector(0,0,0))
    """
    obj.ViewObject.ShapeColor = color
    obj.ViewObject.LineColor = color
    obj.ViewObject.PointColor = color
    obj.ViewObject.Transparency = 50
    obj.Label = name
    update_geom_info(obj, geom)
    DOC.recompute()
    return obj

# def model_beam(name="beam", dia=10, prop=200,  f=130, color=DEFAULT_COLOR_CRIMSON,
#                 geom=GEOM0, **kwargs):
#   """creates a red beam with length <prop>, diameter <dia>,
#   fokus <f> and name ~
#   example :  beam1 = model_beam("laser1", 10, 200, 100)
#   beam1 = model_beam(name="laser1", dia=10, prop=200, f=-45)
#   """
#   DOC = get_DOC()
#   if f==0 or abs(f) > 1e4:
#     # wenn die Brennweite unendlich oder zu groß (10m) ist
#       obj = DOC.addObject("Part::Cylinder", name)
#       obj.Height = prop
#       obj.Radius = dia/2
#   elif prop < f or f < 0:
#     # only one cone
#     dia2 = dia * (f-prop)/f
#     obj = DOC.addObject("Part::Cone", name)
#     obj.Height = prop
#     obj.Radius1 = dia/2
#     obj.Radius2 = dia2/2
#   else:
#     dia2 = 0 #1 altern
#     obj1 = DOC.addObject("Part::Cone", name+"_1")
#     obj1.Height = f
#     obj1.Radius1 = dia/2
#     obj1.Radius2 = dia2/2

#     dia3 = dia * (prop-f)/f
#     obj2 = DOC.addObject("Part::Cone", name+"_2")
#     obj2.Height = prop-f
#     obj2.Radius1 = dia2/2
#     obj2.Radius2 = dia3/2
#     obj2.Placement = FreeCAD.Placement(Vector(0,0,f), FreeCAD.Rotation(Vector(0,1,0),0), Vector(0,0,0))
#     obj = DOC.addObject("Part::Fuse", name)
#     obj.Base = obj1
#     obj.Tool = obj2
#     obj.Refine = True
#     DOC.recompute()

#   obj.Placement = FreeCAD.Placement(Vector(0,0,0), FreeCAD.Rotation(Vector(0,1,0),90), Vector(0,0,0))
#   obj.ViewObject.ShapeColor = color
#   obj.ViewObject.Transparency = BEAM_TRANSPARENCY
#   obj.Label = name
#   update_geom_info(obj, geom)

#   DOC.recompute()
#   return obj

# Test
if __name__ == "__main__":
  from utils import start_DOC
  DOC = None
  start_DOC(DOC)
  model_beam()