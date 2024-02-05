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
from LaserCAD.moduls import Make_Stretcher_chromeo
from LaserCAD.freecad_models import freecad_da, clear_doc, setview


def stretcher_test():
  stretch1 = Make_Stretcher_chromeo()
  stretch1.pos = (0, 0, 100)
  stretch1.draw()
  return stretch1


if __name__ == "__main__":
  if freecad_da:
    clear_doc()
  stretcher_test()
  if freecad_da:
    setview()