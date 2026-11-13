# -*- coding: utf-8 -*-
"""
Tests für LaserCAD.moduls.polarization_rotator

Der Polarisationsdreher besteht aus drei Spiegeln, die einen Strahl entlang +x
so durch den Raum führen, dass er wieder in +x-Richtung austritt (und dabei
seine Polarisation um 90 Grad dreht, was hier nicht geprüft wird). Das
Argument <flip> spiegelt den Aufbau an der xz-Ebene (y -> -y).
"""
import contextlib
import io
import unittest
import warnings

import numpy as np
from numpy.testing import assert_allclose

from LaserCAD import Mirror, Ray
from LaserCAD.moduls.polarization_rotator import Polarization_Rotator


def build(flip):
  with contextlib.redirect_stdout(io.StringIO()):
    return Polarization_Rotator(flip=flip)


def mirrors_of(rotator):
  found = {}
  for el in rotator._elements:
    if isinstance(el, Mirror):
      for key in ("M1", "M2", "M3"):
        if el.name.endswith(key):
          found[key] = el
  return found["M1"], found["M2"], found["M3"]


class TestPolarizationRotator(unittest.TestCase):

  def test_building_gives_no_runtime_warning(self):
    for flip in (False, True):
      with self.subTest(flip=flip):
        with warnings.catch_warnings():
          warnings.simplefilter("error")
          build(flip)

  def test_beam_enters_and_leaves_along_plus_x(self):
    for flip in (False, True):
      with self.subTest(flip=flip):
        m1, m2, m3 = mirrors_of(build(flip))
        r = Ray()
        r.pos = m1.pos - (14.496, 0, 0)     # auf der Achse vor dem ersten Spiegel
        r1 = m1.next_ray(r)
        r2 = m2.next_ray(r1)
        r3 = m3.next_ray(r2)
        # der Strahl trifft jeden Spiegel in dessen Mittelpunkt ...
        assert_allclose(r1.pos, m1.pos, atol=1e-9)
        assert_allclose(r2.pos, m2.pos, atol=1e-9)
        assert_allclose(r3.pos, m3.pos, atol=1e-9)
        # ... und verlässt den Aufbau wieder in +x-Richtung
        assert_allclose(r3.normal, (1, 0, 0), atol=1e-9)

  def test_flip_mirrors_the_middle_mirror_in_y(self):
    _, m2, _ = mirrors_of(build(False))
    _, m2f, _ = mirrors_of(build(True))
    self.assertAlmostEqual(m2.pos[1], -m2f.pos[1])
    self.assertAlmostEqual(m2.pos[2], m2f.pos[2])

  def test_mirror_angles_are_finite_and_consistent_with_the_normals(self):
    # Regression: Der mittlere Spiegel hatte phi = theta = 0 (siehe
    # Mirror.set_normal_with_2_points), ein erneutes Setzen von phi hätte
    # seine Normale auf (0, 1, 0) zurückgesetzt.
    for flip in (False, True):
      for m in mirrors_of(build(flip)):
        with self.subTest(flip=flip, mirror=m.name):
          self.assertTrue(np.isfinite(m.phi) and np.isfinite(m.theta))
          n = m.normal
          m.phi = m.phi
          assert_allclose(m.normal, n, atol=1e-9)

  def test_path_length_bookkeeping(self):
    pr = build(False)
    self.assertAlmostEqual(pr.length_diff, pr.path_length - pr.geometric_length)


if __name__ == "__main__":
  unittest.main()
