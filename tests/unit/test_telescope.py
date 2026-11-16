# -*- coding: utf-8 -*-
"""
Tests für Make_Telescope (moduls/telescope.py).

Ein Teleskop aus zwei dünnen Linsen im Abstand f1+f2 hat die Matrix
  [[-f2/f1, 0], [0, -f1/f2]]   (B = 0, afokal, det = 1).
"""
import contextlib
import io
import unittest
import warnings

import numpy as np

from LaserCAD.moduls import Make_Telescope


def make(*args, **kwargs):
  with contextlib.redirect_stdout(io.StringIO()), warnings.catch_warnings():
    warnings.simplefilter("ignore")
    return Make_Telescope(*args, **kwargs)


class TestTelescope(unittest.TestCase):
  CASES = [(100, 100, 0), (100, 50, 20), (200, 40, 100), (50, 150, 10)]

  def test_matrix_is_afocal(self):
    for f1, f2, d0 in self.CASES:
      with self.subTest(f1=f1, f2=f2, d0=d0):
        M = make(f1=f1, f2=f2, d0=d0).matrix()
        np.testing.assert_allclose(M, [[-f2 / f1, 0], [0, -f1 / f2]],
                                   atol=1e-9)

  def test_determinant_is_one(self):
    for f1, f2, d0 in self.CASES:
      with self.subTest(f1=f1, f2=f2, d0=d0):
        self.assertAlmostEqual(np.linalg.det(make(f1=f1, f2=f2, d0=d0).matrix()), 1)

  def test_amplification_attribute(self):
    for f1, f2, d0 in self.CASES:
      with self.subTest(f1=f1, f2=f2, d0=d0):
        t = make(f1=f1, f2=f2, d0=d0)
        self.assertAlmostEqual(t.amplification, f2 / f1)

  def test_two_lenses_in_sequence(self):
    t = make(f1=100, f2=50, d0=20)
    self.assertEqual(len(t.get_sequence()), 2)

  def test_lens_apertures(self):
    t = make(f1=100, f2=50, d0=20, lens1_aperture=30, lens2_aperture=40)
    ap = sorted(e.aperture for e in t._elements)
    self.assertEqual(ap, [30, 40])


if __name__ == "__main__":
  unittest.main()
