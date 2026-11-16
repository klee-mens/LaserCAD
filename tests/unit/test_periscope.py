# -*- coding: utf-8 -*-
"""
Tests für Make_Periscope und Make_RoofTop_Mirror. Geprüft wird per echtem
Strahldurchlauf durch die Elemente (nicht über last_geom()).
"""
import contextlib
import io
import unittest
import warnings

import numpy as np

from LaserCAD import Ray
from LaserCAD.moduls import Make_Periscope, Make_RoofTop_Mirror


def make(func, **kw):
  with contextlib.redirect_stdout(io.StringIO()), warnings.catch_warnings():
    warnings.simplefilter("ignore")
    return func(**kw)


def through(comp, start=(0, 0, 80)):
  r = Ray()
  r.pos = start
  cur = r
  for e in comp._elements:
    cur = e.next_ray(cur)
  return cur


class TestPeriscope(unittest.TestCase):
  def test_height_up_and_down(self):
    for h, up in [(150, True), (150, False), (60, True)]:
      with self.subTest(h=h, up=up):
        ray = through(make(Make_Periscope, height=h, up=up))
        self.assertAlmostEqual(ray.pos[2], 80 + (h if up else -h), places=6)
        np.testing.assert_allclose(ray.normal, [1, 0, 0], atol=1e-9)
        self.assertAlmostEqual(ray.pos[1], 0, places=6)

  def test_backwards_reverses_direction(self):
    ray = through(make(Make_Periscope, backwards=True))
    np.testing.assert_allclose(ray.normal, [-1, 0, 0], atol=1e-9)
    self.assertAlmostEqual(ray.pos[2], 230, places=6)

  def test_last_geom_matches_ray_tracing(self):
    # Auffälligkeit: m2.normal wird erst nach add_on_axis gesetzt, die optische
    # Achse ist deshalb veraltet, bis recompute_optical_axis() läuft.
    p = make(Make_Periscope, height=150, up=True)
    ray = through(p)
    self.assertAlmostEqual(p.last_geom()[0][2], ray.pos[2], places=6)


class TestRoofTop(unittest.TestCase):
  def test_beam_is_sent_back_with_height_offset(self):
    ray = through(make(Make_RoofTop_Mirror, height=20, up=True))
    np.testing.assert_allclose(ray.normal, [-1, 0, 0], atol=1e-9)
    self.assertAlmostEqual(ray.pos[2], 100, places=6)

  def test_down_shifts_the_other_way(self):
    ray = through(make(Make_RoofTop_Mirror, height=20, up=False))
    self.assertAlmostEqual(ray.pos[2], 60, places=6)


if __name__ == "__main__":
  unittest.main()
