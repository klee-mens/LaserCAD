#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 26 01:19:17 2025

@author: mens
"""

import os
from pathlib import Path
this_dir = Path(__file__).parent


files = [x for x in os.listdir() if x[-3::] == ".py"]
files.remove("run_all_tests.py")

print(files)

for file in files:
  namespace = {'__name__': '__main__'}
  filename = this_dir/file
  exec(filename.read_text(), namespace)