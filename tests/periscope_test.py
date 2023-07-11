# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 10:53:52 2023

@author: 12816
"""

from moduls import Make_Periscope,Periscope2


def periscope_test():  
  peris = Make_Periscope()
  peris.pos = (0, 0,100)
  peris.draw()
  peris2 = Periscope2()
  peris2.pos = (0, 300,100)
  peris2.draw()
  return peris,peris2