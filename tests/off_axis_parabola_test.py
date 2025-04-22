#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 16 12:18:45 2025

@author: mens
"""

# from LaserCAD.basic_optics.off_axis_parabola import Off_Axis_Parabola_Focus
# from LaserCAD.basic_optics.beam import SquareBeam
# import numpy as np

# oapf = Off_Axis_Parabola_Focus()

# sb = SquareBeam(radius=20, ray_in_line=20)
# sb.pos += (-50, 0, 0)

# # oapf.rotate(vec=oapf.normal, phi=np.pi)

# nb = oapf.next_beam(sb)


# sb.draw()
# nb.draw()



#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 17 10:45:09 2025

@author: mens
"""
# from .utils import freecad_da, update_geom_info, get_DOC
from LaserCAD.freecad_models.utils import freecad_da, update_geom_info, get_DOC
#import math

DEFALUT_MAX_ANGULAR_OFFSET = 10
# DEFAULT_COLOR_LENS = (0/255,170/255,124/2parent_focal_length
LENS_TRANSPARENCY = 50
# LENS_TRANSPARENCY = 0

if freecad_da:
  from FreeCAD import Vector, Rotation, Placement
  from BOPTools import BOPFeatures
  import Part
  import Sketcher
  # from math import pi
  

parent_pos = (50, 100)
parent_focal_length = 50
thickness = 31.7
diameter = 25.4

parent_curvature = 1/4 / parent_focal_length
cylinder_shift = parent_curvature * (diameter*parent_pos[1] + diameter**2/4)


DOC = get_DOC()  


rotparab = DOC.addObject('PartDesign::Body','Body')
rotparab.Label = 'Body'
sketch = rotparab.newObject('Sketcher::SketchObject','Sketch')
sketch.AttachmentSupport = (DOC.getObject('XY_Plane'),[''])
sketch.MapMode = 'FlatFace'

sketch.addGeometry(Part.ArcOfParabola(Part.Parabola(Vector(-22.913216,14.395430,0),Vector(25.979458,23.765106,0),Vector(0,0,1)),10.950560,53.375814),False)
sketch.exposeInternalGeometry(0)

sketch.addConstraint(Sketcher.Constraint('DistanceX',-1,1,0,3,25.979458))
# sketch.setDatum(2,App.Units.Quantity('22.000000 mm'))
sketch.setDatum(2, parent_pos[0])

sketch.addConstraint(Sketcher.Constraint('DistanceY',-1,1,0,3,23.831428))
# sketch.setDatum(3,App.Units.Quantity('33.000000 mm'))
sketch.setDatum(3, parent_pos[1])

sketch.addConstraint(Sketcher.Constraint('DistanceY',-1,1,1,1,18.190452))
sketch.setDatum(4, parent_pos[1])

sketch.addConstraint(Sketcher.Constraint('DistanceX',-1,1,0,1,21.193090))
sketch.setDatum(5, parent_pos[0])

sketch.addConstraint(Sketcher.Constraint('DistanceX',1,1,0,1,44.905686))
sketch.setDatum(6, parent_focal_length)

sketch.addConstraint(Sketcher.Constraint('DistanceX',0,2,0,1,17.816621))
sketch.setDatum(7, thickness + parent_pos[1] + 20)

sketch.addGeometry(Part.LineSegment(Vector(-67.803955,-79.955521,0),Vector(-98.153954,13.950961,0)),False)
sketch.addGeometry(Part.LineSegment(Vector(-98.153954,13.950961,0),Vector(-11.745703,18.949785,0)),False)
sketch.addConstraint(Sketcher.Constraint('Coincident',3,2,4,1)) 

sketch.addConstraint(Sketcher.Constraint('Coincident',4,2,0,1))

sketch.addConstraint(Sketcher.Constraint('Coincident',3,1,0,2))

sketch.addConstraint(Sketcher.Constraint('Horizontal',4))

sketch.addConstraint(Sketcher.Constraint('Vertical',3))

DOC.recompute()


### Begin command PartDesign_Revolution
revol = rotparab.newObject('PartDesign::Revolution','Revolution')
revol.Profile = (sketch, ['',])

revol.Angle = 360.000000
revol.ReferenceAxis = (sketch, ['Edge3'])
revol.Midplane = 0
revol.Reversed = 0
revol.Type = 0
revol.UpToFace = None
DOC.recompute()

sketch.Visibility = False

cyl = DOC.addObject("Part::Cylinder","Cylinder")
cyl.Label = "Cylinder"
# Object created at document root.
DOC.recompute()
# Gui.SendMsgToActiveView("ViewFit")
### End command Part_Cylinder
# Gui.Selection.addSelection('Unnamed','Cylinder')
cyl.Placement=Placement(Vector(-cylinder_shift,0,0), Rotation(0,90,0), Vector(0,0,0))

cyl.Radius = diameter / 2
cyl.Height = thickness + 10

# cyl.Radius = '1 mm'
# cyl.Radius = '12 mm'
# cyl.Height = '3 mm'
# cyl.Height = '30 mm'


bp = BOPFeatures.BOPFeatures(DOC)
offaxisparab = bp.make_cut(["Cylinder", "Body", ])
DOC.recompute()





