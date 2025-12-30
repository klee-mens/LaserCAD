# -*- coding: utf-8 -*-
"""
Created on Sat Dec 20 18:35:47 2025

@author: mens
"""

from ..basic_optics import Composition, Mirror, Post, Component, Composed_Mount
from ..freecad_models.utils import load_STL, thisfolder

X_STAGE_HEIGHT = 23.1
# X_STAGE_Y_OFFSET = 19


class Delay_Stage(Composition):
  def __init__(self, name="NewDelayStage", path_length=250, left_turn=True,
                   xstage_distance = 38, **kwargs):
    super().__init__(name=name, **kwargs)

    FIRST_PROP = (path_length - xstage_distance) / 2
    sign = 1.0  if left_turn else -1.0

    self.propagate(FIRST_PROP)

    mir1 = Mirror(phi=90*sign)
    mir1.set_mount(Composed_Mount(["KS1", "1inch_post"]))
    post = mir1.Mount.mount_list[1]

    post.set_lower_limit(X_STAGE_HEIGHT)

    self.add_on_axis(mir1)
    # self.propagate(50)

    xstage = Component()
    xstage.name = "X-Stage-XR25C"
    xstage.freecad_model = load_STL
    stl_file = thisfolder+"misc_meshes/XR25C.stl"
    xstage.draw_dict["stl_file"]=stl_file
    xstage.draw_dict["color"]=(0.1, 0.1, 0.1)

    xstage.pos = (FIRST_PROP, xstage_distance/2*sign, 0)

    self.add_fixed_elm(xstage)

    self.propagate(xstage_distance)

    mir2 = Mirror(phi=90*sign)
    mir2.set_mount(Composed_Mount(["KS1", "1inch_post"]))
    post2 = mir2.Mount.mount_list[1]
    post2.set_lower_limit(X_STAGE_HEIGHT)

    self.add_on_axis(mir2)

    self.propagate(FIRST_PROP)