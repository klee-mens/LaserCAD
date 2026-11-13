# -*- coding: utf-8 -*-
"""
Tests für Cylindrical_Mirror, Stripe_mirror und Rectangular_Mirror

Zylinderspiegel: die Zylinderachse zeigt in z-Richtung. Er fokussiert nur in
der Horizontalen (xy-Ebene) mit f = R/2, in z-Richtung wirkt er wie ein
Planspiegel. Stripe_mirror ist ein sphärischer Streifenspiegel (verhält sich
wie Curved_Mirror), Rectangular_Mirror ein Planspiegel mit Rechteckmaß.
"""
import io
import unittest
import warnings
from contextlib import redirect_stdout

import numpy as np
from numpy.testing import assert_allclose

from LaserCAD import Ray, Mirror, Curved_Mirror
from LaserCAD.basic_optics import (Cylindrical_Mirror, Stripe_mirror,
                                   Rectangular_Mirror)

POS = np.array((100.0, 0.0, 80.0))


def placed(obj):
  obj.pos = POS
  return obj


def parallel_ray(offset):
  r = Ray()
  r.pos = POS - (100, 0, 0) + offset
  return r


class TestCylindricalMirror(unittest.TestCase):

  def test_horizontal_offset_is_focused_with_f_equal_R_over_2(self):
    mirror = placed(Cylindrical_Mirror(radius=200))
    h = 2.0
    out = mirror.next_ray(parallel_ray((0, h, 0)))
    # Neigung -h/f mit f = R/2 = 100 (kleine Winkel)
    self.assertAlmostEqual(out.normal[1] / abs(out.normal[0]), -h / 100, places=3)

  def test_focus_lies_f_in_front_of_the_mirror(self):
    mirror = placed(Cylindrical_Mirror(radius=200))
    out = mirror.next_ray(parallel_ray((0, 1.0, 0)))
    s = -out.pos[1] / out.normal[1]
    focus_x = out.pos[0] + s * out.normal[0]
    self.assertAlmostEqual(focus_x, POS[0] - 100, delta=0.02)

  def test_vertical_offset_is_not_deflected(self):
    mirror = placed(Cylindrical_Mirror(radius=200))
    out = mirror.next_ray(parallel_ray((0, 0, 3)))
    assert_allclose(out.normal, (-1, 0, 0), atol=1e-12)
    self.assertAlmostEqual(out.pos[2], 83.0)

  def test_negative_radius_diverges(self):
    out = placed(Cylindrical_Mirror(radius=-200)).next_ray(parallel_ray((0, 2, 0)))
    self.assertGreater(out.normal[1], 0)

  def test_axis_ray_is_reflected_back(self):
    out = placed(Cylindrical_Mirror(radius=200)).next_ray(parallel_ray((0, 0, 0)))
    assert_allclose(out.normal, (-1, 0, 0), atol=1e-12)
    assert_allclose(out.pos, POS, atol=1e-9)

  def test_reflected_ray_is_normalized(self):
    out = placed(Cylindrical_Mirror(radius=200)).next_ray(parallel_ray((0, 5, 4)))
    self.assertAlmostEqual(np.linalg.norm(out.normal), 1.0, places=12)

  def test_matrix_is_a_horizontal_thin_lens(self):
    M = Cylindrical_Mirror(radius=200).matrix()
    assert_allclose(M, [[1, 0], [-1 / 100, 1]], atol=1e-15)

  def test_radius_zero_gives_identity_matrix(self):
    assert_allclose(Cylindrical_Mirror(radius=0).matrix(), np.eye(2))

  def test_radius_can_be_changed_afterwards(self):
    mirror = Cylindrical_Mirror(radius=200)
    mirror.radius = 400
    assert_allclose(mirror.matrix(), [[1, 0], [-1 / 200, 1]], atol=1e-15)
    self.assertEqual(mirror.radius, 400)

  def test_ray_that_misses_gives_a_warning_and_a_nan_ray(self):
    mirror = placed(Cylindrical_Mirror(radius=200))
    with warnings.catch_warnings(record=True) as caught:
      warnings.simplefilter("always")
      out = mirror.next_ray(parallel_ray((0, 500, 0)))
    texts = [str(w.message) for w in caught]
    self.assertEqual(len(texts), 1)
    self.assertIn("misses", texts[0])
    self.assertIn("Cylindrical_Mirror", texts[0])
    self.assertTrue(np.all(np.isnan(out.pos)))
    self.assertTrue(np.all(np.isnan(out.normal)))

  def test_miss_prints_nothing_and_does_not_draw(self):
    mirror = placed(Cylindrical_Mirror(radius=200))
    buf = io.StringIO()
    with redirect_stdout(buf), warnings.catch_warnings():
      warnings.simplefilter("ignore")
      mirror.next_ray(parallel_ray((0, 500, 0)))
    self.assertEqual(buf.getvalue(), "")


class TestCurvedMirrorMiss(unittest.TestCase):

  def test_miss_gives_a_warning_and_nan(self):
    mirror = placed(Curved_Mirror(radius=200))
    with warnings.catch_warnings(record=True) as caught:
      warnings.simplefilter("always")
      out = mirror.next_ray(parallel_ray((0, 500, 0)))
    texts = [str(w.message) for w in caught]
    self.assertEqual(len(texts), 1)
    self.assertIn("misses", texts[0])
    self.assertTrue(np.all(np.isnan(out.pos)))

  def test_normal_hit_gives_no_warning(self):
    mirror = placed(Curved_Mirror(radius=200))
    with warnings.catch_warnings():
      warnings.simplefilter("error")
      mirror.next_ray(parallel_ray((0, 3, 2)))


class TestStripeMirror(unittest.TestCase):

  def test_behaves_like_curved_mirror(self):
    stripe = placed(Stripe_mirror(radius=200))
    curved = placed(Curved_Mirror(radius=200))
    for off in ((0, 2, 0), (0, 0, 3), (0, 1, -2)):
      a = stripe.next_ray(parallel_ray(off))
      b = curved.next_ray(parallel_ray(off))
      assert_allclose(a.normal, b.normal, atol=1e-12)
      assert_allclose(a.pos, b.pos, atol=1e-12)

  def test_default_dimensions(self):
    stripe = Stripe_mirror()
    self.assertEqual(stripe.height, 10)
    self.assertEqual(stripe.thickness, 25)
    self.assertAlmostEqual(stripe.aperture, 3 * 25.4)


class TestRectangularMirror(unittest.TestCase):

  def test_size_is_stored(self):
    mirror = Rectangular_Mirror(height=20, width=30)
    self.assertEqual((mirror.height, mirror.width), (20, 30))

  def test_acts_like_a_flat_mirror(self):
    rect = placed(Rectangular_Mirror(phi=90))
    flat = placed(Mirror(phi=90))
    r = parallel_ray((0, 1, 2))
    assert_allclose(rect.next_ray(r).normal, flat.next_ray(r).normal, atol=1e-12)
    assert_allclose(rect.matrix(), np.eye(2))

  def test_phi_is_used(self):
    out = placed(Rectangular_Mirror(phi=90)).next_ray(parallel_ray((0, 0, 0)))
    assert_allclose(out.normal, (0, 1, 0), atol=1e-12)

  def test_unknown_keywords_give_a_warning(self):
    # Regression: Rectangular_Mirror hat **kwargs früher nicht weitergegeben
    with warnings.catch_warnings(record=True) as caught:
      warnings.simplefilter("always")
      Rectangular_Mirror(foo=1)
    self.assertTrue(any("unknown keyword" in str(w.message) for w in caught))


if __name__ == "__main__":
  unittest.main()
