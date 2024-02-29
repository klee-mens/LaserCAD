
import numpy as np
import sys

pfad = __file__
pfad = pfad.replace("\\","/") #folder conventions windows linux stuff
ind = pfad.rfind("/")
pfad = pfad[0:ind-1]
ind = pfad.rfind("/")
pfad = pfad[0:ind]
if not pfad in sys.path:
  sys.path.append(pfad)


from LaserCAD.freecad_models import clear_doc, setview, freecad_da
from LaserCAD.basic_optics import Mirror, Beam, Composition, inch, Curved_Mirror, Ray, Geom_Object
from LaserCAD.basic_optics import Grating, Opt_Element
import matplotlib.pyplot as plt
from LaserCAD.freecad_models.utils import thisfolder, load_STL

if freecad_da:
  clear_doc()
  

# First try with static positions
# P1 = Mirror(pos=[-50,0,100], phi=45)
# P2 = Mirror(pos=[50,0,100], phi=45+180)
# PM1 = Mirror(pos=[250,0,100])
# PM2 = Mirror(pos=[250,-250,100])
# M1 = Mirror(pos=[50,150,100])
# M2 = Mirror(pos=[-1650,150,100])
# M3 = Mirror(pos=[-1650,60,100])
# M4 = Mirror(pos=[-50,-150,100])
# R1 = Curved_Mirror(pos=[200,125,100],radius=2000)
# R2 = Curved_Mirror(pos=[-2050,125,100], radius=2500)
# TFP1 = Mirror(pos=[-1580,60,100])
# TFP2 = Mirror(pos=[-1350,-150,100])

beam = Beam(radius=5, angle=0)
beam.pos=[0,0,0]

tele_angle1 = 8
tele_angle2 = 3
TFP_angle = 66
TFP_ydist = 200
TFP_xdist = TFP_ydist*np.tan((2*TFP_angle-90)*np.pi/180)
TFP_dist = np.sqrt(TFP_ydist**2 + TFP_xdist**2)

P1 = Mirror(phi=-90)
P2 = Mirror(phi=90)
PM1 = Mirror()  # pump mirror
PM2 = Mirror()  # pump mirror 2
M1 = Mirror(phi=-90-tele_angle1)
M2 = Mirror(phi=-90-tele_angle2)
M3 = Mirror(phi=90)
M4 = Mirror(phi=90)
R1 = Curved_Mirror(phi=-180+tele_angle1, radius=2000)
R2 = Curved_Mirror(phi=-180+tele_angle2, radius=2500)
TFP1 = Mirror(phi=-180+2*66)
TFP2 = Mirror(phi=180-2*66)

Setup = Composition()
Setup.set_light_source(beam)

Setup.propagate(150)
Setup.add_on_axis(P1)
Setup.propagate(100)
Setup.add_on_axis(P2)
Setup.propagate(150)
Setup.add_on_axis(M1)
Setup.propagate(150/np.cos(np.pi/180*tele_angle1))
Setup.add_on_axis(R1)
Setup.propagate(2250)
Setup.add_on_axis(R2)
Setup.propagate(400/np.cos(np.pi/180*tele_angle2))
Setup.add_on_axis(M2)
Setup.propagate(100)
Setup.add_on_axis(M3)
Setup.propagate(50)
Setup.add_on_axis(TFP1)
Setup.propagate(TFP_dist)
Setup.add_on_axis(TFP2)
Setup.propagate(1370)
Setup.add_on_axis(M4)
Setup.propagate(40)
Setup.draw()

if freecad_da:
  setview()