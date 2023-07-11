# -*- coding: utf-8 -*-
"""
Created on Thu Aug 18 12:29:04 2022

@author: mens
"""

if __name__ == "__main__":
  from utils import freecad_da, get_DOC
else:
  from .utils import freecad_da, get_DOC
  
  
if freecad_da:
  DOC = get_DOC()
else:
  DOC = -1
