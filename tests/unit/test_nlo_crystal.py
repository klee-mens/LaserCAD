# -*- coding: utf-8 -*-
"""Tests für NLO_Crystal: Wellenlänge * Multiplikator, Farbe, Strahl bleibt gerade."""
import unittest

import numpy as np

from LaserCAD import NLO_Crystal, Ray, Beam


class TestNLOCrystal(unittest.TestCase):
  def test_ray_wavelength_is_multiplied(self):
    for mult in (0.5, 1 / 3, 2.0):
      with self.subTest(mult=mult):
        c = NLO_Crystal(wavelength_multiplier=mult)
        r = Ray()
        r.wavelength = 800e-6
        self.assertAlmostEqual(c.next_ray(r).wavelength, 800e-6 * mult)

  def test_input_ray_not_modified(self):
    c = NLO_Crystal()
    r = Ray()
    r.wavelength = 800e-6
    c.next_ray(r)
    self.assertEqual(r.wavelength, 800e-6)

  def test_ray_passes_straight(self):
    c = NLO_Crystal()
    r = Ray()
    r.pos = (-10, 0, 80)
    r2 = c.next_ray(r)
    np.testing.assert_allclose(r2.normal, r.normal, atol=1e-12)

  def test_beam_wavelength_halved_and_color_set(self):
    c = NLO_Crystal(output_color=(0.2, 0.3, 0.4))
    b = Beam()
    wl = b.wavelength()
    b2 = c.next_beam(b)
    self.assertAlmostEqual(b2.wavelength(), wl * 0.5)
    self.assertEqual(b2.draw_dict["color"], (0.2, 0.3, 0.4))
    self.assertAlmostEqual(b.wavelength(), wl)


if __name__ == "__main__":
  unittest.main()
