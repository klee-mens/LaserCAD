# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 10:53:52 2023

@author: 12816
"""

import sys
pfad = __file__
pfad = pfad.replace("\\","/") #folder conventions windows linux stuff
pfad = pfad.lower()
ind = pfad.rfind("lasercad")
pfad = pfad[0:ind-1]
if not pfad in sys.path:
  sys.path.append(pfad)
from LaserCAD.moduls import Make_Amplifier_Typ_I_simple,Make_Amplifier_Typ_I_Mirror
from LaserCAD.moduls import Make_Amplifier_Typ_II_simple,Make_Amplifier_Typ_II_Mirror
from LaserCAD.moduls import Make_Amplifier_Typ_II_UpDown,Make_Amplifier_Typ_II_Juergen
from LaserCAD.moduls import Make_Amplifier_Typ_II_with_theta,Make_Amplifier_Typ_II_plane
from LaserCAD.freecad_models import freecad_da, clear_doc, setview

if freecad_da:
  clear_doc()

def Amplifter_Typ_I_test():  
  Ampli1 = Make_Amplifier_Typ_I_simple()
  Ampli1.pos = (0, 0,100)
  Ampli1.draw()
  Ampli2 = Make_Amplifier_Typ_I_Mirror()
  Ampli2.pos = (0, 300,100)
  Ampli2.draw()
  return Ampli1,Ampli2

def Amplifter_Typ_II_test():
  Ampli1 = Make_Amplifier_Typ_II_simple()
  Ampli1.pos = (0, 0,100)
  Ampli1.draw()
  Ampli2 = Make_Amplifier_Typ_II_Mirror()
  Ampli2.pos = (0, 500,100)
  Ampli2.draw()
  Ampli3 = Make_Amplifier_Typ_II_UpDown()
  Ampli3.pos = (0, -500,100)
  # Ampli3.draw()
  Ampli4 = Make_Amplifier_Typ_II_plane()
  Ampli4.pos = (0, -1000,100)
  # Ampli4.draw()
  Ampli5 = Make_Amplifier_Typ_II_with_theta()
  Ampli5.pos = (0, 1000,100)
  # Ampli5.draw()
  Ampli6 = Make_Amplifier_Typ_II_Juergen()
  Ampli6.pos = (0, 1500,100)
  # Ampli6.draw()
  return Ampli1,Ampli2,Ampli3,Ampli4,Ampli5,Ampli6

if __name__ == "__main__":
  # Amplifter_Typ_I_test()
  Amplifter_Typ_II_test()
  
  
if freecad_da:
  setview()