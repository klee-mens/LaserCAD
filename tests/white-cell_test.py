# -*- coding: utf-8 -*-
"""
Created on Sun Feb  4 19:00:00 2024

@author: mens
"""

import sys
pfad = __file__
pfad = pfad.replace("\\","/") #folder conventions windows linux stuff
pfad = pfad.lower()
ind = pfad.rfind("lasercad")
pfad = pfad[0:ind-1]
if not pfad in sys.path:
  sys.path.append(pfad)
from LaserCAD.moduls import Make_White_Cell
from LaserCAD.freecad_models import freecad_da, setview, clear_doc

if freecad_da:
  clear_doc()

# def white_cell_test():
#   whitec = Make_White_Cell()
#   whitec.pos = (100,0,0)
#   whitec.draw()
#   return whitec

if __name__ == "__main__":

  wc = Make_White_Cell(roundtrips4=3, seperation=8)
  wc.draw()

if freecad_da:
  setview()