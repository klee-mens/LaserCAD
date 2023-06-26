# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 10:53:52 2023

@author: 12816
"""

from moduls import Make_Stretcher_old,Make_Stretcher


def stretcher_test():  
  stretch1 = Make_Stretcher()
  stretch1.pos = (0, 0, 100)
  stretch1.draw()
  stretch2 = Make_Stretcher_old()
  stretch2.pos = (0, 500,100)
  stretch2.draw()
  return stretch1,stretch2