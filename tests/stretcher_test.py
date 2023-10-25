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
# from LaserCAD.moduls import Make_Stretcher_old,Make_Stretcher
from LaserCAD.moduls import Make_Stretcher


def stretcher_test():  
  stretch1 = Make_Stretcher()
  stretch1.pos = (0, 0, 100)
  stretch1.draw()
  # stretch2 = Make_Stretcher_old()
  # stretch2.pos = (0, 500,100)
  # stretch2.draw()
  # return stretch1,stretch2
  return stretch1


if __name__ == "__main__":
  stretcher_test()