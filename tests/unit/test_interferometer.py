# -*- coding: utf-8 -*-
"""
Tests für Michelson- und Mach-Zehnder-Interferometer: beide Arme müssen am
selben Punkt und in derselben Richtung enden, sonst gäbe es keine Interferenz.
"""
import contextlib
import io
import unittest
import warnings

import numpy as np

import LaserCAD.moduls.interferometer as I


def make(func):
  with contextlib.redirect_stdout(io.StringIO()), warnings.catch_warnings():
    warnings.simplefilter("ignore")
    return func()


class TestInterferometers(unittest.TestCase):
  FUNCS = [I.Make_Michelson_Interferometer, I.Make_Machzehnder_Interferometer]

  def test_two_arms(self):
    for f in self.FUNCS:
      with self.subTest(f=f.__name__):
        self.assertEqual(len(make(f)._subcomps), 2)

  def test_arms_end_at_same_point_and_direction(self):
    for f in self.FUNCS:
      with self.subTest(f=f.__name__):
        a, b = [s.last_geom() for s in make(f)._subcomps]
        np.testing.assert_allclose(a[0], b[0], atol=1e-6)
        np.testing.assert_allclose(a[1], b[1], atol=1e-6)

  def test_arms_have_different_lengths(self):
    for f in self.FUNCS:
      with self.subTest(f=f.__name__):
        a, b = make(f)._subcomps
        self.assertNotEqual(len(a._elements), len(b._elements))


if __name__ == "__main__":
  unittest.main()
