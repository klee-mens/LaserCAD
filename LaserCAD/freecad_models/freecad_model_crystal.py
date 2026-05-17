#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 18 19:55:00 2022

@author: mens
"""

from .utils import freecad_da, update_geom_info, get_DOC
from .freecad_model_composition import initialize_composition_old, add_to_composition
from .freecad_model_lens import model_lens
from .freecad_model_mounts import draw_post_part

DEFALUT_MAX_ANGULAR_OFFSET = 10
DEFAULT_COLOR_LENS = (0/84,0/255,255/255)
DEFAULT_COLOR_CRYSTAL = (131/255,27/255,44/255)
DEFALUT_MOUNT_COLOR = (207/255,138/255,0/255)
if freecad_da:
  from FreeCAD import Vector, Placement, Rotation
  import Part
  import Sketcher



def model_crystal(name="crystal",model="cube", width=50, height=10, thickness=25, color=DEFAULT_COLOR_CRYSTAL,Transparency=50, geom=None, **kwargs):
  """
  Parameters
  ----------
  name : string, optional
    crystal name. The default is "crystal".
  model : string, optional
    The model of crystal. It can be "cube" or "round" for cubic crystal and 
    circular crystal. The default is "cube".
  width : float, optional
    The width or radius of the crystal. The default is 50.
  height : float, optional
    The height of the crystal (cube only). The default is 10.
  thickness : float, optional
    The thickness of the crystal. The default is 25.
  color : TYPE, optional
    The color of the crystal. The default is DEFAULT_COLOR_CRYSTAL.
  Transparency : float, optional
    The Transparency of the crystal. The default is 50.
  geom : TYPE, optional
    DESCRIPTION. The default is None.
  **kwargs : TYPE
    DESCRIPTION.

  Returns
  -------
  obj : TYPE
    DESCRIPTION.

  """
  # print(geom)
  DOC = get_DOC()
  if model== "round":
    obj = model_lens(name, dia=width, Radius1=0, Radius2=0, thickness=thickness)
    obj.ViewObject.ShapeColor = color
    obj.ViewObject.Transparency = Transparency
    update_geom_info(obj, geom)
    DOC.recompute()
    return obj
  obj = DOC.addObject('PartDesign::Body', name)
  sketch = obj.newObject('Sketcher::SketchObject', name+'_sketch')
  sketch.MapMode = 'FlatFace'
  
  geoList = []
  geoList.append(Part.LineSegment(Vector(-width/2,height/2,0),Vector(width/2,height/2,0)))
  geoList.append(Part.LineSegment(Vector(width/2,height/2,0),Vector(width/2,-height/2,0)))
  geoList.append(Part.LineSegment(Vector(width/2,-height/2,0),Vector(-width/2,-height/2,0)))
  geoList.append(Part.LineSegment(Vector(-width/2,-height/2,0),Vector(-width/2,height/2,0)))
  sketch.addGeometry(geoList,False)
  conList = []
  conList.append(Sketcher.Constraint('Coincident',0,2,1,1))
  conList.append(Sketcher.Constraint('Coincident',1,2,2,1))
  conList.append(Sketcher.Constraint('Coincident',2,2,3,1))
  conList.append(Sketcher.Constraint('Coincident',3,2,0,1))
  conList.append(Sketcher.Constraint('Horizontal',0))
  conList.append(Sketcher.Constraint('Horizontal',2))
  conList.append(Sketcher.Constraint('Vertical',1))
  conList.append(Sketcher.Constraint('Vertical',3))
  sketch.addConstraint(conList)
  del geoList, conList
  sketch.addConstraint(Sketcher.Constraint('DistanceX',0,1,0,2,width))
  sketch.addConstraint(Sketcher.Constraint('DistanceY',1,2,1,1,height)) 
  sketch.addConstraint(Sketcher.Constraint('DistanceY',-1,1,0,2,height/2))
  sketch.addConstraint(Sketcher.Constraint('DistanceX',-1,1,0,2,width/2)) 
  
  pad = obj.newObject('PartDesign::Pad','Pad')
  pad.Profile = sketch
  pad.Length = thickness
  # pad.ReferenceAxis = (sketch,['N_Axis'])
  sketch.Visibility = False
  
  obj.ViewObject.ShapeColor = color
  obj.ViewObject.Transparency = Transparency
  obj.Placement=Placement(Vector(0,0,0), Rotation(90,0,90), Vector(0,0,0))
  update_geom_info(obj, geom)
  DOC.recompute()
  # print(obj.Placement)
  return obj



# =============================================================================
# round crystal mount
# =============================================================================

#  App.activeDocument().addObject('PartDesign::Body','Body')
# >>> App.ActiveDocument.getObject('Body').Label = 'Body'
# >>> App.ActiveDocument.getObject('Body').AllowCompound = False
# >>> # import PartDesignGui
# >>> # Gui.activateView('Gui::View3DInventor', True)
# >>> # Gui.activeView().setActiveObject('pdbody', App.activeDocument().Body)
# >>> # Gui.Selection.clearSelection()
# >>> # Gui.Selection.addSelection(App.ActiveDocument.Body)
# >>> App.ActiveDocument.recompute()
# >>> ### End command PartDesign_Body
# >>> # Gui.Selection.addSelection('labor_116','Body')
# >>> # Gui.runCommand('PartDesign_CompSketches',0)
# >>> # Gui.Selection.clearSelection()
# >>> # Gui.Selection.addSelection('labor_116','Body','Origin002.YZ_Plane001.')
# >>> App.getDocument('labor_116').getObject('Body').newObject('Sketcher::SketchObject','Sketch')
# >>> App.getDocument('labor_116').getObject('Sketch').AttachmentSupport = (App.getDocument('labor_116').getObject('Origin002'),['YZ_Plane001'])
# >>> App.getDocument('labor_116').getObject('Sketch').MapMode = 'FlatFace'
# >>> App.ActiveDocument.recompute()
# >>> # Gui.getDocument('labor_116').setEdit(App.getDocument('labor_116').getObject('Body'), 0, 'Sketch.')
# >>> # import Show
# >>> # ActiveSketch = App.getDocument('labor_116').getObject('Sketch')
# >>> # tv = Show.TempoVis(App.ActiveDocument, tag= ActiveSketch.ViewObject.TypeId)
# >>> # ActiveSketch.ViewObject.TempoVis = tv
# >>> # if ActiveSketch.ViewObject.EditingWorkbench:
# >>> #   tv.activateWorkbench(ActiveSketch.ViewObject.EditingWorkbench)
# >>> # if ActiveSketch.ViewObject.HideDependent:
# >>> #   tv.hide(tv.get_all_dependent(App.getDocument('labor_116').getObject('Body'), 'Sketch.'))
# >>> # if ActiveSketch.ViewObject.ShowSupport:
# >>> #   tv.show([ref[0] for ref in ActiveSketch.AttachmentSupport if not (ref[0].isDerivedFrom("App::Plane") or ref[0].isDerivedFrom("App::LocalCoordinateSystem"))])
# >>> # if ActiveSketch.ViewObject.ShowLinks:
# >>> #   tv.show([ref[0] for ref in ActiveSketch.ExternalGeometry])
# >>> # tv.sketchClipPlane(ActiveSketch, ActiveSketch.ViewObject.SectionView)
# >>> # tv.hide(ActiveSketch)
# >>> # del(tv)
# >>> # del(ActiveSketch)
# >>> # 
# >>> import PartDesignGui
# >>> # ActiveSketch = App.getDocument('labor_116').getObject('Sketch')
# >>> # if ActiveSketch.ViewObject.RestoreCamera:
# >>> #   ActiveSketch.ViewObject.TempoVis.saveCamera()
# >>> #   if ActiveSketch.ViewObject.ForceOrtho:
# >>> #     ActiveSketch.ViewObject.Document.ActiveView.setCameraType('Orthographic')
# >>> # 
# >>> # Gui.Selection.clearSelection()
# >>> # Gui.Selection.addSelection('labor_116','NewCrystal')
# >>> # Gui.runCommand('Std_ToggleVisibility',0)
# >>> # Gui.Selection.clearSelection()
# >>> # Gui.Selection.addSelection('labor_116','Sphere')
# >>> # Gui.runCommand('Std_ToggleVisibility',0)
# >>> # Gui.runCommand('Sketcher_CompCreateConic',0)
# >>> # Gui.Selection.clearSelection()
# >>> ActiveSketch = App.getDocument('labor_116').getObject('Sketch')
# >>> 
# >>> lastGeoId = len(ActiveSketch.Geometry)
# >>> 
# >>> geoList = []
# >>> geoList.append(Part.Circle(App.Vector(0.000000, 0.000000, 0.000000), App.Vector(0.000000, 0.000000, 1.000000), 10.921819))
# >>> App.getDocument('labor_116').getObject('Sketch').addGeometry(geoList,False)
# >>> del geoList
# >>> 
# >>> constraintList = []
# >>> App.getDocument('labor_116').getObject('Sketch').addConstraint(Sketcher.Constraint('Coincident', 0, 3, -1, 1))
# >>> 
# >>> 
# >>> # Gui.runCommand('Sketcher_CompDimensionTools',0)
# >>> App.getDocument('labor_116').getObject('Sketch').addConstraint(Sketcher.Constraint('Diameter',0,21.843638)) 
# >>> # Gui.Selection.addSelection('labor_116','Body','Sketch.Edge1',-8.78457,6.48979,0,False)
# >>> App.getDocument('labor_116').getObject('Sketch').deleteAllGeometry(True)
# >>> ActiveSketch = App.getDocument('labor_116').getObject('Sketch')
# >>> 
# >>> lastGeoId = len(ActiveSketch.Geometry)
# >>> 
# >>> geoList = []
# >>> geoList.append(Part.Circle(App.Vector(0.000000, 0.000000, 0.000000), App.Vector(0.000000, 0.000000, 1.000000), 25.000000))
# >>> App.getDocument('labor_116').getObject('Sketch').addGeometry(geoList,False)
# >>> del geoList
# >>> 
# >>> constraintList = []
# >>> constraintList.append(Sketcher.Constraint('Coincident', 0, 3, -1, 1))
# >>> constraintList.append(Sketcher.Constraint('Diameter', 0, 50.000000))
# >>> App.getDocument('labor_116').getObject('Sketch').addConstraint(constraintList)
# >>> del constraintList
# >>> 
# >>> App.getDocument('labor_116').getObject('Sketch').setGeometryIds([(0,1)])
# >>> App.getDocument('labor_116').getObject('Sketch').setDatum(1,App.Units.Quantity('50.000000 mm'))
# >>> # Gui.Selection.clearSelection()
# >>> # Gui.getDocument('labor_116').resetEdit()
# >>> App.ActiveDocument.recompute()
# >>> # ActiveSketch = App.getDocument('labor_116').getObject('Sketch')
# >>> # tv = ActiveSketch.ViewObject.TempoVis
# >>> # if tv:
# >>> #   tv.restore()
# >>> # ActiveSketch.ViewObject.TempoVis = None
# >>> # del(tv)
# >>> # del(ActiveSketch)
# >>> # 
# >>> # Gui.Selection.addSelection('labor_116','Body','Sketch.')
# >>> App.getDocument('labor_116').recompute()
# >>> ### Begin command PartDesign_Pad
# >>> App.getDocument('labor_116').getObject('Body').newObject('PartDesign::Pad','Pad001')
# >>> App.getDocument('labor_116').getObject('Pad001').Profile = (App.getDocument('labor_116').getObject('Sketch'), ['',])
# >>> App.getDocument('labor_116').getObject('Pad001').Length = 10
# >>> App.ActiveDocument.recompute()
# >>> App.getDocument('labor_116').getObject('Pad001').ReferenceAxis = (App.getDocument('labor_116').getObject('Sketch'),['N_Axis'])
# >>> App.getDocument('labor_116').getObject('Sketch').Visibility = False
# >>> App.ActiveDocument.recompute()
# >>> # App.getDocument('labor_116').getObject('Pad001').ViewObject.ShapeAppearance=getattr(App.getDocument('labor_116').getObject('Body').getLinkedObject(True).ViewObject,'ShapeAppearance',App.getDocument('labor_116').getObject('Pad001').ViewObject.ShapeAppearance)
# >>> # App.getDocument('labor_116').getObject('Pad001').ViewObject.LineColor=getattr(App.getDocument('labor_116').getObject('Body').getLinkedObject(True).ViewObject,'LineColor',App.getDocument('labor_116').getObject('Pad001').ViewObject.LineColor)
# >>> # App.getDocument('labor_116').getObject('Pad001').ViewObject.PointColor=getattr(App.getDocument('labor_116').getObject('Body').getLinkedObject(True).ViewObject,'PointColor',App.getDocument('labor_116').getObject('Pad001').ViewObject.PointColor)
# >>> # App.getDocument('labor_116').getObject('Pad001').ViewObject.Transparency=getattr(App.getDocument('labor_116').getObject('Body').getLinkedObject(True).ViewObject,'Transparency',App.getDocument('labor_116').getObject('Pad001').ViewObject.Transparency)
# >>> # App.getDocument('labor_116').getObject('Pad001').ViewObject.DisplayMode=getattr(App.getDocument('labor_116').getObject('Body').getLinkedObject(True).ViewObject,'DisplayMode',App.getDocument('labor_116').getObject('Pad001').ViewObject.DisplayMode)
# >>> # Gui.getDocument('labor_116').setEdit(App.getDocument('labor_116').getObject('Body'), 0, 'Pad001.')
# >>> # Gui.Selection.clearSelection()
# >>> ### End command PartDesign_Pad
# >>> # Gui.Selection.clearSelection()
# >>> App.getDocument('labor_116').getObject('Pad001').Length = 10.000000
# >>> App.getDocument('labor_116').getObject('Pad001').TaperAngle = 0.000000
# >>> App.getDocument('labor_116').getObject('Pad001').UseCustomVector = 0
# >>> App.getDocument('labor_116').getObject('Pad001').Direction = (1, 0, 0)
# >>> App.getDocument('labor_116').getObject('Pad001').ReferenceAxis = (App.getDocument('labor_116').getObject('Sketch'), ['N_Axis'])
# >>> App.getDocument('labor_116').getObject('Pad001').AlongSketchNormal = 1
# >>> App.getDocument('labor_116').getObject('Pad001').SideType = 0
# >>> App.getDocument('labor_116').getObject('Pad001').Type = 0
# >>> App.getDocument('labor_116').getObject('Pad001').Type2 = 0
# >>> App.getDocument('labor_116').getObject('Pad001').UpToFace = None
# >>> App.getDocument('labor_116').getObject('Pad001').UpToFace2 = None
# >>> App.getDocument('labor_116').getObject('Pad001').Reversed = 0
# >>> App.getDocument('labor_116').getObject('Pad001').Offset = 0
# >>> App.getDocument('labor_116').getObject('Pad001').Offset2 = 0
# >>> App.getDocument('labor_116').purgeTouched()
# >>> App.getDocument('labor_116').recompute()
# >>> # Gui.getDocument('labor_116').resetEdit()
# >>> App.getDocument('labor_116').getObject('Sketch').Visibility = False
# >>> # Gui.Selection.addSelection('labor_116','Body','Pad001.Face2',1.77636e-15,-9.39204,6.14509)
# >>> ### Begin command PartDesign_CompSketches
# >>> App.getDocument('labor_116').getObject('Body').newObject('Sketcher::SketchObject','Sketch001')
# >>> App.getDocument('labor_116').getObject('Sketch001').AttachmentSupport = (App.getDocument('labor_116').getObject('Pad001'),['Face2',])
# >>> App.getDocument('labor_116').getObject('Sketch001').MapMode = 'FlatFace'
# >>> App.ActiveDocument.recompute()
# >>> # Gui.getDocument('labor_116').setEdit(App.getDocument('labor_116').getObject('Body'), 0, 'Sketch001.')
# >>> # ActiveSketch = App.getDocument('labor_116').getObject('Sketch001')
# >>> # tv = Show.TempoVis(App.ActiveDocument, tag= ActiveSketch.ViewObject.TypeId)
# >>> # ActiveSketch.ViewObject.TempoVis = tv
# >>> # if ActiveSketch.ViewObject.EditingWorkbench:
# >>> #   tv.activateWorkbench(ActiveSketch.ViewObject.EditingWorkbench)
# >>> # if ActiveSketch.ViewObject.HideDependent:
# >>> #   tv.hide(tv.get_all_dependent(App.getDocument('labor_116').getObject('Body'), 'Sketch001.'))
# >>> # if ActiveSketch.ViewObject.ShowSupport:
# >>> #   tv.show([ref[0] for ref in ActiveSketch.AttachmentSupport if not (ref[0].isDerivedFrom("App::Plane") or ref[0].isDerivedFrom("App::LocalCoordinateSystem"))])
# >>> # if ActiveSketch.ViewObject.ShowLinks:
# >>> #   tv.show([ref[0] for ref in ActiveSketch.ExternalGeometry])
# >>> # tv.sketchClipPlane(ActiveSketch, ActiveSketch.ViewObject.SectionView)
# >>> # tv.hide(ActiveSketch)
# >>> # del(tv)
# >>> # del(ActiveSketch)
# >>> # 
# >>> import PartDesignGui
# >>> # ActiveSketch = App.getDocument('labor_116').getObject('Sketch001')
# >>> # if ActiveSketch.ViewObject.RestoreCamera:
# >>> #   ActiveSketch.ViewObject.TempoVis.saveCamera()
# >>> #   if ActiveSketch.ViewObject.ForceOrtho:
# >>> #     ActiveSketch.ViewObject.Document.ActiveView.setCameraType('Orthographic')
# >>> # 
# >>> ### End command PartDesign_CompSketches
# >>> # Gui.Selection.clearSelection()
# >>> # Gui.runCommand('Sketcher_CompCreateConic',0)
# >>> ActiveSketch = App.getDocument('labor_116').getObject('Sketch001')
# >>> 
# >>> lastGeoId = len(ActiveSketch.Geometry)
# >>> 
# >>> geoList = []
# >>> geoList.append(Part.Circle(App.Vector(0.000000, 0.000000, 0.000000), App.Vector(0.000000, 0.000000, 1.000000), 9.791914))
# >>> App.getDocument('labor_116').getObject('Sketch001').addGeometry(geoList,False)
# >>> del geoList
# >>> 
# >>> constraintList = []
# >>> App.getDocument('labor_116').getObject('Sketch001').addConstraint(Sketcher.Constraint('Coincident', 0, 3, -1, 1))
# >>> 
# >>> 
# >>> # Gui.runCommand('Sketcher_CompDimensionTools',0)
# >>> App.getDocument('labor_116').getObject('Sketch001').addConstraint(Sketcher.Constraint('Diameter',0,19.583828)) 
# >>> # Gui.Selection.addSelection('labor_116','Body','Sketch001.Edge1',5.10428,8.35631,0,False)
# >>> App.getDocument('labor_116').getObject('Sketch001').deleteAllGeometry(True)
# >>> ActiveSketch = App.getDocument('labor_116').getObject('Sketch001')
# >>> 
# >>> lastGeoId = len(ActiveSketch.Geometry)
# >>> 
# >>> geoList = []
# >>> geoList.append(Part.Circle(App.Vector(0.000000, 0.000000, 0.000000), App.Vector(0.000000, 0.000000, 1.000000), 7.500000))
# >>> App.getDocument('labor_116').getObject('Sketch001').addGeometry(geoList,False)
# >>> del geoList
# >>> 
# >>> constraintList = []
# >>> constraintList.append(Sketcher.Constraint('Coincident', 0, 3, -1, 1))
# >>> constraintList.append(Sketcher.Constraint('Diameter', 0, 15.000000))
# >>> App.getDocument('labor_116').getObject('Sketch001').addConstraint(constraintList)
# >>> del constraintList
# >>> 
# >>> App.getDocument('labor_116').getObject('Sketch001').setGeometryIds([(0,1)])
# >>> App.getDocument('labor_116').getObject('Sketch001').setDatum(1,App.Units.Quantity('15.000000 mm'))
# >>> # Gui.Selection.clearSelection()
# >>> # Gui.getDocument('labor_116').resetEdit()
# >>> App.ActiveDocument.recompute()
# >>> # ActiveSketch = App.getDocument('labor_116').getObject('Sketch001')
# >>> # tv = ActiveSketch.ViewObject.TempoVis
# >>> # if tv:
# >>> #   tv.restore()
# >>> # ActiveSketch.ViewObject.TempoVis = None
# >>> # del(tv)
# >>> # del(ActiveSketch)
# >>> # 
# >>> # Gui.Selection.addSelection('labor_116','Body','Sketch001.')
# >>> App.getDocument('labor_116').recompute()
# >>> ### Begin command PartDesign_Pocket
# >>> App.getDocument('labor_116').getObject('Body').newObject('PartDesign::Pocket','Pocket')
# >>> App.getDocument('labor_116').getObject('Pocket').Profile = (App.getDocument('labor_116').getObject('Sketch001'), ['',])
# >>> App.getDocument('labor_116').getObject('Pocket').Length = 5
# >>> App.ActiveDocument.recompute()
# >>> App.getDocument('labor_116').getObject('Pocket').ReferenceAxis = (App.getDocument('labor_116').getObject('Sketch001'),['N_Axis'])
# >>> App.getDocument('labor_116').getObject('Sketch001').Visibility = False
# >>> App.ActiveDocument.recompute()
# >>> # App.getDocument('labor_116').getObject('Pocket').ViewObject.ShapeAppearance=getattr(App.getDocument('labor_116').getObject('Pad001').getLinkedObject(True).ViewObject,'ShapeAppearance',App.getDocument('labor_116').getObject('Pocket').ViewObject.ShapeAppearance)
# >>> # App.getDocument('labor_116').getObject('Pocket').ViewObject.LineColor=getattr(App.getDocument('labor_116').getObject('Pad001').getLinkedObject(True).ViewObject,'LineColor',App.getDocument('labor_116').getObject('Pocket').ViewObject.LineColor)
# >>> # App.getDocument('labor_116').getObject('Pocket').ViewObject.PointColor=getattr(App.getDocument('labor_116').getObject('Pad001').getLinkedObject(True).ViewObject,'PointColor',App.getDocument('labor_116').getObject('Pocket').ViewObject.PointColor)
# >>> # App.getDocument('labor_116').getObject('Pocket').ViewObject.Transparency=getattr(App.getDocument('labor_116').getObject('Pad001').getLinkedObject(True).ViewObject,'Transparency',App.getDocument('labor_116').getObject('Pocket').ViewObject.Transparency)
# >>> # App.getDocument('labor_116').getObject('Pocket').ViewObject.DisplayMode=getattr(App.getDocument('labor_116').getObject('Pad001').getLinkedObject(True).ViewObject,'DisplayMode',App.getDocument('labor_116').getObject('Pocket').ViewObject.DisplayMode)
# >>> # Gui.getDocument('labor_116').setEdit(App.getDocument('labor_116').getObject('Body'), 0, 'Pocket.')
# >>> # Gui.Selection.clearSelection()
# >>> ### End command PartDesign_Pocket
# >>> # Gui.Selection.clearSelection()
# >>> App.getDocument('labor_116').getObject('Pocket').TaperAngle = 0.000000
# >>> App.getDocument('labor_116').getObject('Pocket').UseCustomVector = 0
# >>> App.getDocument('labor_116').getObject('Pocket').Direction = (1, 0, 0)
# >>> App.getDocument('labor_116').getObject('Pocket').ReferenceAxis = (App.getDocument('labor_116').getObject('Sketch001'), ['N_Axis'])
# >>> App.getDocument('labor_116').getObject('Pocket').AlongSketchNormal = 1
# >>> App.getDocument('labor_116').getObject('Pocket').SideType = 0
# >>> App.getDocument('labor_116').getObject('Pocket').Type = 1
# >>> App.getDocument('labor_116').getObject('Pocket').Type2 = 0
# >>> App.getDocument('labor_116').getObject('Pocket').UpToFace = None
# >>> App.getDocument('labor_116').getObject('Pocket').UpToFace2 = None
# >>> App.getDocument('labor_116').getObject('Pocket').Reversed = 0
# >>> App.getDocument('labor_116').getObject('Pocket').Offset = 0
# >>> App.getDocument('labor_116').getObject('Pocket').Offset2 = 0
# >>> App.getDocument('labor_116').purgeTouched()
# >>> App.getDocument('labor_116').recompute()
# >>> App.getDocument('labor_116').getObject('Pad001').Visibility = False
# >>> # Gui.getDocument('labor_116').resetEdit()
# >>> App.getDocument('labor_116').getObject('Sketch001').Visibility = False
# >>> 



















# def model_crystal_mount(name="crystal_mount",model="cube", width=50, height=10, thickness=25, geom=None, **kwargs):
#   """
#   Parameters
#   ----------
#   name : string, optional
#     crystal name. The default is "crystal".
#   model : string, optional
#     The model of crystal. It can be "cube" or "round" for cubic crystal and 
#     circular crystal. The default is "cube".
#   width : float, optional
#     The width or radius of the crystal. The default is 50.
#   height : float, optional
#     The height of the crystal (cube only). The default is 10.
#   thickness : float, optional
#     The thickness of the crystal. The default is 25.
#   geom : TYPE, optional
#     DESCRIPTION. The default is None.
#   **kwargs : TYPE
#     DESCRIPTION.

#   Returns
#   -------
#   obj : TYPE
#     DESCRIPTION.

#   """
#   DOC = get_DOC()
#   obj = DOC.addObject('PartDesign::Body', name)
#   sketch = obj.newObject('Sketcher::SketchObject', name+'_sketch')
#   sketch.MapMode = 'FlatFace'
#   if model== "cube":
#     geoList = []
#     geoList.append(Part.LineSegment(Vector(-width/2,height/2,0),Vector(width/2,height/2,0)))
#     geoList.append(Part.LineSegment(Vector(width/2,height/2,0),Vector(width/2,-height/2,0)))
#     geoList.append(Part.LineSegment(Vector(width/2,-height/2,0),Vector(-width/2,-height/2,0)))
#     geoList.append(Part.LineSegment(Vector(-width/2,-height/2,0),Vector(-width/2,height/2,0)))
#     sketch.addGeometry(geoList,False)
#     conList = []
#     conList.append(Sketcher.Constraint('Coincident',0,2,1,1))
#     conList.append(Sketcher.Constraint('Coincident',1,2,2,1))
#     conList.append(Sketcher.Constraint('Coincident',2,2,3,1))
#     conList.append(Sketcher.Constraint('Coincident',3,2,0,1))
#     conList.append(Sketcher.Constraint('Horizontal',0))
#     conList.append(Sketcher.Constraint('Horizontal',2))
#     conList.append(Sketcher.Constraint('Vertical',1))
#     conList.append(Sketcher.Constraint('Vertical',3))
#     sketch.addConstraint(conList)
#     del geoList, conList
#     sketch.addConstraint(Sketcher.Constraint('DistanceX',0,1,0,2,width))
#     sketch.addConstraint(Sketcher.Constraint('DistanceY',1,2,1,1,height)) 
#     sketch.addConstraint(Sketcher.Constraint('DistanceY',-1,1,0,2,height/2))
#     sketch.addConstraint(Sketcher.Constraint('DistanceX',-1,1,0,2,width/2)) 
#     geoList = []
#     geoList.append(Part.LineSegment(Vector(-20,20,0),Vector(20,20,0)))
#     geoList.append(Part.LineSegment(Vector(20,20,0),Vector(20,-20,0)))
#     geoList.append(Part.LineSegment(Vector(20,-20,0),Vector(-20,-20,0)))
#     geoList.append(Part.LineSegment(Vector(-20,-20,0),Vector(-20,20,0)))
#     sketch.addGeometry(geoList,False)
#     conList = []
#     conList.append(Sketcher.Constraint('Coincident',4,2,5,1))
#     conList.append(Sketcher.Constraint('Coincident',5,2,6,1))
#     conList.append(Sketcher.Constraint('Coincident',6,2,7,1))
#     conList.append(Sketcher.Constraint('Coincident',7,2,4,1))
#     conList.append(Sketcher.Constraint('Horizontal',4))
#     conList.append(Sketcher.Constraint('Horizontal',6))
#     conList.append(Sketcher.Constraint('Vertical',5))
#     conList.append(Sketcher.Constraint('Vertical',7))
#     sketch.addConstraint(conList)
#     del geoList, conList
#     sketch.addConstraint(Sketcher.Constraint('DistanceX',4,1,4,2,40))
#     sketch.addConstraint(Sketcher.Constraint('DistanceY',5,2,5,1,40)) 
#     sketch.addConstraint(Sketcher.Constraint('DistanceY',-1,1,4,2,20))
#     sketch.addConstraint(Sketcher.Constraint('DistanceX',-1,1,4,2,20)) 
#   else:
#     sketch.addGeometry(Part.Circle(Vector(0,0,0),Vector(0,0,1),width/2),False)
#     sketch.addConstraint(Sketcher.Constraint('Coincident',0,3,-1,1)) 
#     sketch.addConstraint(Sketcher.Constraint('Diameter',0,width)) 
#     geoList = []
#     geoList.append(Part.LineSegment(Vector(-20,20,0),Vector(20,20,0)))
#     geoList.append(Part.LineSegment(Vector(20,20,0),Vector(20,-20,0)))
#     geoList.append(Part.LineSegment(Vector(20,-20,0),Vector(-20,-20,0)))
#     geoList.append(Part.LineSegment(Vector(-20,-20,0),Vector(-20,20,0)))
#     sketch.addGeometry(geoList,False)
#     conList = []
#     conList.append(Sketcher.Constraint('Coincident',1,2,2,1))
#     conList.append(Sketcher.Constraint('Coincident',2,2,3,1))
#     conList.append(Sketcher.Constraint('Coincident',3,2,4,1))
#     conList.append(Sketcher.Constraint('Coincident',4,2,1,1))
#     conList.append(Sketcher.Constraint('Horizontal',1))
#     conList.append(Sketcher.Constraint('Horizontal',3))
#     conList.append(Sketcher.Constraint('Vertical',2))
#     conList.append(Sketcher.Constraint('Vertical',4))
#     sketch.addConstraint(conList)
#     del geoList, conList
#     sketch.addConstraint(Sketcher.Constraint('DistanceX',1,1,1,2,40))
#     sketch.addConstraint(Sketcher.Constraint('DistanceY',2,2,2,1,40)) 
#     sketch.addConstraint(Sketcher.Constraint('DistanceY',0,3,1,2,20))
#     sketch.addConstraint(Sketcher.Constraint('DistanceX',0,3,1,2,20)) 
  
  
#   pad = obj.newObject('PartDesign::Pad','Pad')
#   pad.Profile = sketch
#   pad.Length = thickness + 2
#   # pad.ReferenceAxis = (sketch,['N_Axis'])
#   sketch.Visibility = False
  
#   DOC.recompute()
#   sketch001 = obj.newObject('Sketcher::SketchObject', name+'_sketch001')
#   sketch001.Support = (pad,['Face3',])
#   sketch001.MapMode = 'FlatFace'
  
#   sketch001.addGeometry(Part.Circle(Vector(0,(thickness + 2)/2,0),Vector(0,0,1),2),
#                         False)
#   sketch001.addConstraint(Sketcher.Constraint('PointOnObject',0,3,-2)) 
#   sketch001.addConstraint(Sketcher.Constraint('Diameter',0,2*2)) 
#   sketch001.addConstraint(Sketcher.Constraint('DistanceY',-1,1,0,3,(thickness + 2)/2)) 
  
#   Pocket = obj.newObject('PartDesign::Pocket','Pocket')
#   Pocket.Profile = sketch001
#   Pocket.Length = 10
#   Pocket.ReferenceAxis = (sketch001,['N_Axis'])
#   sketch001.Visibility = False
  
#   obj.ViewObject.ShapeColor = DEFALUT_MOUNT_COLOR
#   obj.ViewObject.Transparency = 0
#   obj.Placement=Placement(Vector(0,0,0), Rotation(90,0,90), Vector(0,0,0))
#   update_geom_info(obj, geom)
#   DOC.recompute()
#   post_part=draw_post_part(name="post_part",
#                             height=20,xshift=(thickness + 2)/2, geom=geom)
#   part = initialize_composition_old(name="mount, post and base")
#   container = post_part,obj
#   add_to_composition(part, container)
#   return part
def model_crystal_mount(name="crystal_mount",model="cube", width=50, height=10, thickness=25, geom=None, **kwargs):
  """
  Parameters
  ----------
  name : string, optional
    crystal name. The default is "crystal".
  model : string, optional
    The model of crystal. It can be "cube" or "round" for cubic crystal and 
    circular crystal. The default is "cube".
  width : float, optional
    The width or radius of the crystal. The default is 50.
  height : float, optional
    The height of the crystal (cube only). The default is 10.
  thickness : float, optional
    The thickness of the crystal. The default is 25.
  geom : TYPE, optional
    DESCRIPTION. The default is None.
  **kwargs : TYPE
    DESCRIPTION.

  Returns
  -------
  obj : TYPE
    DESCRIPTION.

  """
  DOC = get_DOC()
  obj = DOC.addObject('PartDesign::Body', name)
  sketch = obj.newObject('Sketcher::SketchObject', name+'_sketch')
  sketch.MapMode = 'FlatFace'
  if model== "cube":
    geoList = []
    geoList.append(Part.LineSegment(Vector(-width/2,height/2,0),Vector(width/2,height/2,0)))
    geoList.append(Part.LineSegment(Vector(width/2,height/2,0),Vector(width/2,-height/2,0)))
    geoList.append(Part.LineSegment(Vector(width/2,-height/2,0),Vector(-width/2,-height/2,0)))
    geoList.append(Part.LineSegment(Vector(-width/2,-height/2,0),Vector(-width/2,height/2,0)))
    sketch.addGeometry(geoList,False)
    conList = []
    conList.append(Sketcher.Constraint('Coincident',0,2,1,1))
    conList.append(Sketcher.Constraint('Coincident',1,2,2,1))
    conList.append(Sketcher.Constraint('Coincident',2,2,3,1))
    conList.append(Sketcher.Constraint('Coincident',3,2,0,1))
    conList.append(Sketcher.Constraint('Horizontal',0))
    conList.append(Sketcher.Constraint('Horizontal',2))
    conList.append(Sketcher.Constraint('Vertical',1))
    conList.append(Sketcher.Constraint('Vertical',3))
    sketch.addConstraint(conList)
    del geoList, conList
    sketch.addConstraint(Sketcher.Constraint('DistanceX',0,1,0,2,width))
    sketch.addConstraint(Sketcher.Constraint('DistanceY',1,2,1,1,height)) 
    sketch.addConstraint(Sketcher.Constraint('DistanceY',-1,1,0,2,height/2))
    sketch.addConstraint(Sketcher.Constraint('DistanceX',-1,1,0,2,width/2)) 
    geoList = []
    geoList.append(Part.LineSegment(Vector(-20,20,0),Vector(20,20,0)))
    geoList.append(Part.LineSegment(Vector(20,20,0),Vector(20,-20,0)))
    geoList.append(Part.LineSegment(Vector(20,-20,0),Vector(-20,-20,0)))
    geoList.append(Part.LineSegment(Vector(-20,-20,0),Vector(-20,20,0)))
    sketch.addGeometry(geoList,False)
    conList = []
    conList.append(Sketcher.Constraint('Coincident',4,2,5,1))
    conList.append(Sketcher.Constraint('Coincident',5,2,6,1))
    conList.append(Sketcher.Constraint('Coincident',6,2,7,1))
    conList.append(Sketcher.Constraint('Coincident',7,2,4,1))
    conList.append(Sketcher.Constraint('Horizontal',4))
    conList.append(Sketcher.Constraint('Horizontal',6))
    conList.append(Sketcher.Constraint('Vertical',5))
    conList.append(Sketcher.Constraint('Vertical',7))
    sketch.addConstraint(conList)
    del geoList, conList
    sketch.addConstraint(Sketcher.Constraint('DistanceX',4,1,4,2,40))
    sketch.addConstraint(Sketcher.Constraint('DistanceY',5,2,5,1,40)) 
    sketch.addConstraint(Sketcher.Constraint('DistanceY',-1,1,4,2,20))
    sketch.addConstraint(Sketcher.Constraint('DistanceX',-1,1,4,2,20)) 
  else:
    sketch.addGeometry(Part.Circle(Vector(0,0,0),Vector(0,0,1),width/2),False)
    sketch.addConstraint(Sketcher.Constraint('Coincident',0,3,-1,1)) 
    sketch.addConstraint(Sketcher.Constraint('Diameter',0,width)) 
    geoList = []
    geoList.append(Part.LineSegment(Vector(-20,20,0),Vector(20,20,0)))
    geoList.append(Part.LineSegment(Vector(20,20,0),Vector(20,-20,0)))
    geoList.append(Part.LineSegment(Vector(20,-20,0),Vector(-20,-20,0)))
    geoList.append(Part.LineSegment(Vector(-20,-20,0),Vector(-20,20,0)))
    sketch.addGeometry(geoList,False)
    conList = []
    conList.append(Sketcher.Constraint('Coincident',1,2,2,1))
    conList.append(Sketcher.Constraint('Coincident',2,2,3,1))
    conList.append(Sketcher.Constraint('Coincident',3,2,4,1))
    conList.append(Sketcher.Constraint('Coincident',4,2,1,1))
    conList.append(Sketcher.Constraint('Horizontal',1))
    conList.append(Sketcher.Constraint('Horizontal',3))
    conList.append(Sketcher.Constraint('Vertical',2))
    conList.append(Sketcher.Constraint('Vertical',4))
    sketch.addConstraint(conList)
    del geoList, conList
    sketch.addConstraint(Sketcher.Constraint('DistanceX',1,1,1,2,40))
    sketch.addConstraint(Sketcher.Constraint('DistanceY',2,2,2,1,40)) 
    sketch.addConstraint(Sketcher.Constraint('DistanceY',0,3,1,2,20))
    sketch.addConstraint(Sketcher.Constraint('DistanceX',0,3,1,2,20)) 
  
  
  pad = obj.newObject('PartDesign::Pad','Pad')
  pad.Profile = sketch
  pad.Length = thickness + 2
  # pad.ReferenceAxis = (sketch,['N_Axis'])
  sketch.Visibility = False
  
  DOC.recompute()
  sketch001 = obj.newObject('Sketcher::SketchObject', name+'_sketch001')
  sketch001.Support = (pad,['Face3',])
  sketch001.MapMode = 'FlatFace'
  
  sketch001.addGeometry(Part.Circle(Vector(0,(thickness + 2)/2,0),Vector(0,0,1),2),
                        False)
  sketch001.addConstraint(Sketcher.Constraint('PointOnObject',0,3,-2)) 
  sketch001.addConstraint(Sketcher.Constraint('Diameter',0,2*2)) 
  sketch001.addConstraint(Sketcher.Constraint('DistanceY',-1,1,0,3,(thickness + 2)/2)) 
  
  Pocket = obj.newObject('PartDesign::Pocket','Pocket')
  Pocket.Profile = sketch001
  Pocket.Length = 10
  Pocket.ReferenceAxis = (sketch001,['N_Axis'])
  sketch001.Visibility = False
  
  obj.ViewObject.ShapeColor = DEFALUT_MOUNT_COLOR
  obj.ViewObject.Transparency = 0
  obj.Placement=Placement(Vector(0,0,0), Rotation(90,0,90), Vector(0,0,0))
  update_geom_info(obj, geom)
  DOC.recompute()
  post_part=draw_post_part(name="post_part",
                            height=20,xshift=(thickness + 2)/2, geom=geom)
  part = initialize_composition_old(name="mount, post and base")
  container = post_part,obj
  add_to_composition(part, container)
  return part

# Test
if __name__ == "__main__":
  from utils import start_DOC
  DOC = None
  start_DOC(DOC)
  model_crystal()