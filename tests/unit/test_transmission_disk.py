# -*- coding: utf-8 -*-
"""
Tests für Transmission_Disk: Planplatte unter Winkel AOI.
Parallelversatz  s = t*sin(a-b)/cos(b),  mit sin(a) = n*sin(b).
"""
import contextlib
import io
import unittest
import warnings

import numpy as np

from LaserCAD import Ray
from LaserCAD.moduls.transmission_disk import Transmission_Disk


def make(**kw):
  with contextlib.redirect_stdout(io.StringIO()), warnings.catch_warnings():
    warnings.simplefilter("ignore")
    return Transmission_Disk(**kw)


class TestTransmissionDisk(unittest.TestCase):
  def test_lateral_formula(self):
    for n, aoi, t in [(1.5, 56, 5), (1.45, 45, 10), (1.7, 30, 3)]:
      with self.subTest(n=n, aoi=aoi, t=t):
        d = make(refractive_index=n, AOI=aoi, thickness=t)
        a = np.deg2rad(aoi)
        b = np.arcsin(np.sin(a) / n)
        self.assertAlmostEqual(d.lateral, t * (np.tan(a) - np.tan(b)))

  def test_two_surfaces(self):
    self.assertEqual(len(make()._elements), 2)

  def test_exit_ray_parallel_to_input(self):
    d = make()
    r = Ray()
    r.pos = (-20, 0, 80)
    cur = r
    for e in d._elements:
      cur = e.next_ray(cur)
    np.testing.assert_allclose(cur.normal, r.normal, atol=1e-9)

  def test_perpendicular_shift(self):
    n, aoi, t = 1.5, 56, 5
    d = make(refractive_index=n, AOI=aoi, thickness=t)
    r = Ray()
    r.pos = (-20, 0, 80)
    cur = r
    for e in d._elements:
      cur = e.next_ray(cur)
    # Abstand des Austrittsstrahls zur Verlängerung des Eintrittsstrahls
    delta = np.array(cur.pos) - np.array(d._elements[0].next_ray(r).pos)
    a = np.deg2rad(aoi)
    b = np.arcsin(np.sin(a) / n)
    s = t * np.sin(a - b) / np.cos(b)
    d0 = np.array(d._elements[0].next_ray(r).pos)
    ex = np.array(cur.pos)
    line_dir = np.array(r.normal)
    perp = (ex - d0) - np.dot(ex - d0, line_dir) * line_dir
    self.assertAlmostEqual(np.linalg.norm(perp), s, places=6)


if __name__ == "__main__":
  unittest.main()
