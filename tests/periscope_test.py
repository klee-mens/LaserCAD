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

from LaserCAD.moduls import Make_Periscope,Periscope2


def periscope_test():  
  peris = Make_Periscope()
  peris.pos = (0, 0,100)
  peris.draw()
  peris2 = Periscope2()
  peris2.pos = (0, 300,100)
  peris2.draw()
  return peris,peris2

if __name__ == "__main__":
  periscope_test()