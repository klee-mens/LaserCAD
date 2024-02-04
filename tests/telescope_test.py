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
from LaserCAD.moduls import Make_Telescope


def telescope_test():  
  teles = Make_Telescope()
  teles.pos = (0, 500,100)
  teles.draw()
  return teles

if __name__ == "__main__":
  telescope_test()git 