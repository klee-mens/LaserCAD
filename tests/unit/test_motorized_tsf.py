# -*- coding: utf-8 -*-
"""
Tests für Motorized_TSF (moduls/motorized_TSF.py): zwei Prismen-/Keilflächen
auf der Strahlachse, <flip> spiegelt den Versatz der Elemente.
"""
import contextlib
import io
import unittest
import warnings

import numpy as np

from LaserCAD import Ray
from LaserCAD.moduls import Motorized_TSF


def make(**kw):
  with contextlib.redirect_stdout(io.StringIO()), warnings.catch_warnings():
    warnings.simplefilter("ignore")
    return Motorized_TSF(**kw)


class TestMotorizedTSF(unittest.TestCase):
  def test_two_elements_one_nonoptical(self):
    m = make()
    self.assertEqual(len(m._elements), 2)
    self.assertEqual(len(m.non_opticals), 1)

  def test_flip_mirrors_the_offset(self):
    a, b = make(flip=False), make(flip=True)
    self.assertAlmostEqual(a._elements[1].pos[1], -b._elements[1].pos[1])
    self.assertAlmostEqual(a._elements[0].pos[1], b._elements[0].pos[1])

  def test_flip_swaps_orientation(self):
    a, b = make(flip=False), make(flip=True)
    self.assertAlmostEqual(a._elements[0].phi, b._elements[1].phi)
    self.assertAlmostEqual(a._elements[1].phi, b._elements[0].phi)

  def test_beam_passes_straight(self):
    for flip in (False, True):
      with self.subTest(flip=flip):
        m = make(flip=flip)
        r = Ray()
        r.pos = (-20, 0, 80)
        cur = r
        for e in m._elements:
          cur = e.next_ray(cur)
        np.testing.assert_allclose(cur.normal, [1, 0, 0], atol=1e-9)
        self.assertAlmostEqual(cur.pos[2], 80)
        self.assertLess(abs(cur.pos[1]), 0.1)


if __name__ == "__main__":
  unittest.main()
