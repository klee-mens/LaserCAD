# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 01:06:20 2024

@author: mens
"""

# Explanations and Tutorial

Some nice stuff is drawn in Opening.py

That is code:

```python

firsttry = Composition(name="BeamLine1")
firsttry.set_light_source(Beam(radius=2, angle=0.02))
firsttry.propagate(200)
firsttry.add_on_axis(Lens(f=150))
firsttry.propagate(400)
firsttry.add_on_axis(Lens(f=120))
firsttry.propagate(110)
firsttry.add_on_axis(Mirror(phi=110))
firsttry.propagate(90)
firsttry.add_on_axis(Mirror(phi=70))
firsttry.propagate(150)
firsttry.add_on_axis(Lens(f=200))
firsttry.propagate(400)
firsttry.add_on_axis(Mirror(phi=-90))
firsttry.propagate(60)

firsttry.draw()

```