# -*- coding: utf-8 -*-
"""
Tests für Delay_Stage (moduls/delay_stage.py): U-Turn aus zwei 90°-Spiegeln.
"""
import contextlib
import io
import unittest
import warnings

import numpy as np

from LaserCAD import Ray
from LaserCAD.moduls.delay_stage import Delay_Stage


def make(**kw):
  with contextlib.redirect_stdout(io.StringIO()), warnings.catch_warnings():
    warnings.simplefilter("ignore")
    return Delay_Stage(**kw)


def trace(ds, start=(0, 0, 80)):
  r = Ray()
  r.pos = start
  path = [np.array(r.pos, float)]
  cur = r
  for e in ds._elements:
    cur = e.next_ray(cur)
    path.append(np.array(cur.pos, float))
  return cur, path


class TestDelayStage(unittest.TestCase):
  def test_two_mirrors_and_one_stage(self):
    ds = make()
    self.assertEqual(len(ds._elements), 2)
    self.assertEqual(len(ds.non_opticals), 1)

  def test_mirror_positions(self):
    ds = make(path_length=250, xstage_distance=38)
    p1, p2 = ds._elements[0].pos, ds._elements[1].pos
    self.assertAlmostEqual(p2[1] - p1[1], 38)
    self.assertAlmostEqual(p1[0], p2[0])
    self.assertAlmostEqual(p1[0], (250 - 38) / 2)

  def test_ray_is_turned_back(self):
    ds = make()
    ray, _ = trace(ds)
    np.testing.assert_allclose(ray.normal, [-1, 0, 0], atol=1e-9)

  def test_output_offset_equals_stage_distance(self):
    for dist in (20, 38, 60):
      with self.subTest(dist=dist):
        ds = make(xstage_distance=dist)
        ray, _ = trace(ds)
        self.assertAlmostEqual(abs(ray.pos[1]), dist)
        self.assertAlmostEqual(ray.pos[2], 80)

  def test_left_turn_mirrors_the_geometry(self):
    r_left, _ = trace(make(left_turn=True))
    r_right, _ = trace(make(left_turn=False))
    self.assertAlmostEqual(r_left.pos[1], -r_right.pos[1])
    np.testing.assert_allclose(r_left.normal, r_right.normal, atol=1e-9)

  def test_stage_geometry_follows_path_length(self):
    ds = make(path_length=300)
    self.assertAlmostEqual(ds._elements[0].pos[0], (300 - 38) / 2)

  def test_xstage_shift_moves_only_the_stage(self):
    a, b = make(xstage_shift=0), make(xstage_shift=5)
    np.testing.assert_allclose(a._elements[0].pos, b._elements[0].pos)
    self.assertAlmostEqual(b.non_opticals[0].pos[0] - a.non_opticals[0].pos[0], 5)


if __name__ == "__main__":
  unittest.main()
