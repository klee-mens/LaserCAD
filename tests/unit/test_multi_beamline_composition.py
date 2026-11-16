# -*- coding: utf-8 -*-
"""Tests für Multi_Beamline_Composition."""
import contextlib
import io
import unittest
import warnings

import numpy as np

import LaserCAD.moduls.interferometer as I


def make():
  with contextlib.redirect_stdout(io.StringIO()), warnings.catch_warnings():
    warnings.simplefilter("ignore")
    return I.Make_Michelson_Interferometer()


class TestMultiBeamline(unittest.TestCase):
  def test_translation_moves_all_lines(self):
    m = make()
    before = [np.array(s.last_geom()[0]) for s in m._subcomps]
    m.pos = np.array(m.pos) + np.array([10.0, 5.0, 0.0])
    after = [np.array(s.last_geom()[0]) for s in m._subcomps]
    for b, a in zip(before, after):
      np.testing.assert_allclose(a - b, [10, 5, 0], atol=1e-9)

  def test_rotation_keeps_arms_together(self):
    # Bekannter Fehler: _axes_changed uebergibt [self._subcomps] (Liste in
    # der Liste) statt self._subcomps -> AttributeError.
    m = make()
    m.normal = np.array([0.0, 1.0, 0.0])
    a, b = [s.last_geom() for s in m._subcomps]
    np.testing.assert_allclose(a[0], b[0], atol=1e-6)


if __name__ == "__main__":
  unittest.main()
