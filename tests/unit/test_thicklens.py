# -*- coding: utf-8 -*-
"""
Tests für LaserCAD.basic_optics.lens.Thicklens (dicke Linse)

Die Linse wird durch die Brechung an zwei Kugelflächen berechnet (exaktes
Raytracing). Erwartungswerte kommen aus der Optik dicker Linsen: paraxiale
Strahlen müssen sich im Abstand f hinter der hinteren Hauptebene H2 schneiden.
self.pos ist der vordere Scheitelpunkt, h1/h2 messen die Hauptebenen vom
vorderen bzw. hinteren Scheitel (negativ = innerhalb der Linse).
"""
import unittest
import warnings

import numpy as np
from numpy.testing import assert_allclose

from LaserCAD import Ray, Thicklens

LENS_POS = np.array((100.0, 0.0, 80.0))

CONFIGS = [
  dict(f=100, biconvex=True),
  dict(f=100, biconvex=False),
  dict(f=-100, biconvex=True),
  dict(f=-100, biconvex=False),
  dict(f=50, n=1.8, biconvex=True, aperture=12.7),
  dict(f=100, biconvex=True, thickness=10),
]


def make_lens(**kwargs):
  lens = Thicklens(**kwargs)
  lens.pos = LENS_POS
  return lens


def trace(lens, h):
  r = Ray()
  r.pos = LENS_POS - (100, 0, 0) + (0, 0, h)
  return lens.next_ray(r)


def focus_x(out):
  """x-Koordinate, an der der Strahl die optische Achse (z=80) schneidet."""
  s = (LENS_POS[2] - out.pos[2]) / out.normal[2]
  return out.pos[0] + s * out.normal[0]


class TestGeometry(unittest.TestCase):

  def test_plano_convex_radii(self):
    lens = make_lens(f=100, n=1.5, biconvex=False)
    self.assertAlmostEqual(lens.radius1(), 50.0)
    self.assertEqual(lens.radius2(), 0)

  def test_biconvex_radii_are_symmetric(self):
    lens = make_lens(f=100, biconvex=True)
    self.assertAlmostEqual(lens.radius2(), -lens.radius1())
    self.assertGreater(lens.radius1(), 0)

  def test_negative_lens_has_opposite_curvature(self):
    lens = make_lens(f=-100, biconvex=True)
    self.assertLess(lens.radius1(), 0)
    self.assertGreater(lens.radius2(), 0)

  def test_lensmaker_equation_holds_for_all_configs(self):
    for kw in CONFIGS:
      lens = make_lens(**kw)
      n, d = lens.refractive_index, lens.thickness
      R1, R2 = lens.radius1(), lens.radius2()
      inv1 = 1 / R1
      inv2 = 1 / R2 if R2 != 0 else 0.0
      inv_f = (n - 1) * (inv1 - inv2 + (n - 1) * d * inv1 * inv2 / n)
      # Linsenschleiferformel einer dicken Linse (R2 mit Vorzeichenkonvention
      # R2<0 für bikonvex): 1/f = (n-1)[1/R1 - 1/R2 + (n-1)d/(n R1 R2)]
      assert_allclose(inv_f, 1 / lens.focal_length, rtol=1e-9, err_msg=str(kw))

  def test_thickness_keyword_is_used(self):
    self.assertEqual(make_lens(f=100, thickness=10).thickness, 10)

  def test_positive_lens_thickness_follows_edge_thickness(self):
    thin_edge = make_lens(f=100, edge_thickness=1).thickness
    thick_edge = make_lens(f=100, edge_thickness=5).thickness
    self.assertGreater(thick_edge, thin_edge)
    self.assertGreater(thin_edge, 1)

  def test_negative_lens_thickness_equals_edge_thickness(self):
    self.assertEqual(make_lens(f=-100, edge_thickness=4).thickness, 4)

  def test_principal_planes_plano_convex(self):
    lens = make_lens(f=100, biconvex=False)
    self.assertEqual(lens.h1, 0)
    self.assertLess(lens.h2, 0)                       # innerhalb der Linse
    # Plankonvex: H2 liegt um d/n hinter der gekrümmten Fläche, also im Glas
    self.assertAlmostEqual(lens.h2, -lens.thickness / lens.refractive_index,
                           places=9)

  def test_principal_planes_biconvex_are_symmetric(self):
    lens = make_lens(f=100, biconvex=True)
    self.assertAlmostEqual(lens.h1, lens.h2)
    self.assertLess(lens.h1, 0)


class TestRayTracing(unittest.TestCase):

  def test_axis_ray_goes_straight_through(self):
    for kw in CONFIGS:
      lens = make_lens(**kw)
      out = trace(lens, 0.0)
      assert_allclose(out.normal, (1, 0, 0), atol=1e-12, err_msg=str(kw))
      self.assertAlmostEqual(out.pos[0], LENS_POS[0] + lens.thickness,
                             places=9, msg=str(kw))

  def test_focus_is_f_behind_rear_principal_plane(self):
    for kw in CONFIGS:
      lens = make_lens(**kw)
      x_h2 = LENS_POS[0] + lens.thickness + lens.h2
      out = trace(lens, 0.05)
      self.assertAlmostEqual(focus_x(out) - x_h2, lens.focal_length,
                             delta=1e-3 * abs(lens.focal_length), msg=str(kw))

  def test_positive_lens_deflects_towards_axis_negative_away(self):
    up = trace(make_lens(f=100), 2.0).normal[2]
    down = trace(make_lens(f=-100), 2.0).normal[2]
    self.assertLess(up, 0)
    self.assertGreater(down, 0)

  def test_symmetry_for_mirrored_ray_height(self):
    lens = make_lens(f=100, biconvex=True)
    a, b = trace(lens, 3.0), trace(lens, -3.0)
    assert_allclose(a.normal[[0, 2]], b.normal[[0, 2]] * (1, -1), atol=1e-12)

  def test_ray_in_other_transverse_direction_behaves_the_same(self):
    lens = make_lens(f=100, biconvex=True)
    r = Ray()
    r.pos = LENS_POS - (100, 0, 0) + (0, 3, 0)
    out = lens.next_ray(r)
    ref = trace(lens, 3.0)
    assert_allclose(out.normal[[0, 1]], ref.normal[[0, 2]], atol=1e-12)

  def test_lens_position_is_not_changed_by_tracing(self):
    lens = make_lens(f=100, biconvex=True)
    trace(lens, 2.0)
    assert_allclose(lens.pos, LENS_POS)

  def test_input_ray_is_not_modified(self):
    lens = make_lens(f=100, biconvex=True)
    r = Ray()
    r.pos = LENS_POS - (100, 0, 0) + (0, 0, 2)
    lens.next_ray(r)
    assert_allclose(r.normal, (1, 0, 0))
    assert_allclose(r.pos, (0, 0, 82))

  def test_imaging_equation_with_principal_planes(self):
    # Hier ist g der Abstand Objekt -> vorderer Scheitel. H1 liegt bei
    # x_vorn - h1, der Abstand Objekt-H1 ist daher g - h1; der Abstand
    # H2-Bild b_H hängt mit dem Abstand b vom hinteren Scheitel über
    # b = b_H + h2 zusammen. (Der Docstring von calc_principal_planes meint mit
    # g und b dagegen die Abstände zu den Hauptebenen: Strecken g+h1 bzw. b+h2.)
    lens = make_lens(f=100, biconvex=True)
    g = 300.0
    r = Ray()
    r.pos = LENS_POS - (g, 0, 0)
    xs = []
    for ang in (0.001, 0.002):
      r.normal = (np.cos(ang), 0, np.sin(ang))
      out = lens.next_ray(r)
      xs.append(focus_x_from_height(out, h=0.0, z_axis=LENS_POS[2]))
    # beide Winkel müssen sich im selben Bildpunkt auf der Achse treffen
    self.assertAlmostEqual(xs[0], xs[1], delta=0.05)
    b = xs[0] - (LENS_POS[0] + lens.thickness)
    expected = 1 / (1 / lens.focal_length - 1 / (g - lens.h1)) + lens.h2
    self.assertAlmostEqual(b, expected, delta=0.05)


class TestMatrix(unittest.TestCase):
  """ABCD-Matrix von vorderem zu hinterem Scheitel (inkl. Glasweg)."""

  def test_determinant_is_one(self):
    for kw in CONFIGS:
      with self.subTest(kw=kw):
        self.assertAlmostEqual(np.linalg.det(make_lens(**kw).matrix()), 1, places=9)

  def test_power_is_minus_one_over_f(self):
    for kw in CONFIGS:
      with self.subTest(kw=kw):
        lens = make_lens(**kw)
        self.assertAlmostEqual(lens.matrix()[1, 0], -1 / lens.focal_length,
                               places=9)

  def test_principal_planes_in_matrix(self):
    # M = T(-h2) * L(f) * T(-h1)  ->  A = 1 + h2/f, D = 1 + h1/f
    for kw in CONFIGS:
      with self.subTest(kw=kw):
        lens = make_lens(**kw)
        M = lens.matrix()
        self.assertAlmostEqual(M[0, 0], 1 + lens.h2 / lens.focal_length, places=9)
        self.assertAlmostEqual(M[1, 1], 1 + lens.h1 / lens.focal_length, places=9)

  def test_thin_limit(self):
    lens = make_lens(f=100, biconvex=True, thickness=1e-9)
    assert_allclose(lens.matrix(), [[1, 0], [-0.01, 1]], atol=1e-9)

  def test_matrix_follows_changed_thickness(self):
    lens = make_lens(f=100, biconvex=True)
    d_old = lens.matrix()[0, 1]
    lens.thickness *= 2
    self.assertGreater(lens.matrix()[0, 1], d_old)

  def test_matrix_returns_a_copy(self):
    lens = make_lens(f=100)
    M = lens.matrix()
    M[0, 0] = 99
    self.assertNotEqual(lens.matrix()[0, 0], 99)

  def test_matrix_agrees_with_ray_tracing(self):
    # paraxialer Strahl: Höhe/Winkel am vorderen Scheitel -> hinterer Scheitel
    for kw in CONFIGS:
      with self.subTest(kw=kw):
        lens = make_lens(**kw)
        h, alpha = 1e-3, 1e-4
        r = Ray()
        r.pos = LENS_POS - (10, 0, 0) + (0, 0, h)
        r.normal = (np.cos(alpha), 0, np.sin(alpha))
        out = lens.next_ray(r)
        # Strahl auf die Ebene des vorderen Scheitels zurückrechnen
        s = (LENS_POS[0] - r.pos[0]) / r.normal[0]
        h_in = r.pos[2] + s * r.normal[2] - LENS_POS[2]
        # und vorwärts auf die Ebene des hinteren Scheitels
        x2 = LENS_POS[0] + lens.thickness
        s2 = (x2 - out.pos[0]) / out.normal[0]
        h_out = out.pos[2] + s2 * out.normal[2] - LENS_POS[2]
        alpha_out = np.arctan2(out.normal[2], out.normal[0])
        expected = lens.matrix() @ np.array([h_in, alpha])
        assert_allclose([h_out, alpha_out], expected, rtol=1e-3, atol=1e-9,
                        err_msg=str(kw))


class TestImagingMatrix(unittest.TestCase):
  """Die Composition-Matrix des Abbildungsrezepts muss abbilden (B = 0)."""

  def test_composition_matrix_images(self):
    from LaserCAD import Beam, Composition
    for kw in CONFIGS:
      with self.subTest(kw=kw):
        lens = make_lens(**kw)
        g = 300.0
        b = 1 / (1 / lens.focal_length - 1 / g)
        comp = Composition()
        comp.set_light_source(Beam(radius=1, angle=0))
        comp.propagate(g)
        comp.propagate(lens.h1)
        comp.add_on_axis(lens)
        comp.propagate(lens.h2)
        comp.propagate(b)
        M = comp.matrix()
        self.assertAlmostEqual(M[0, 1], 0, delta=1e-6)          # B = 0
        self.assertAlmostEqual(M[0, 0], -b / g, places=6)       # Vergrößerung


class TestImagingRecipe(unittest.TestCase):
  """Abbildung wie im Docstring von calc_principal_planes beschrieben:
  propagate(g), propagate(h1), add_on_axis(lens), propagate(h2), propagate(b)
  mit g, b als Abstand zu H1 bzw. von H2 (1/g + 1/b = 1/f)."""

  def test_image_position_matches_ray_tracing(self):
    from LaserCAD import Beam, Composition
    for kw in CONFIGS:
      lens = make_lens(**kw)
      g = 300.0
      b = 1 / (1 / lens.focal_length - 1 / g)
      comp = Composition()
      comp.set_light_source(Beam(radius=1, angle=0))
      comp.propagate(g)
      comp.propagate(lens.h1)
      comp.add_on_axis(lens)
      comp.propagate(lens.h2)
      comp.propagate(b)
      image_x = comp.last_geom()[0][0]
      xs = []
      for ang in (0.001, 0.002):
        r = Ray()
        r.normal = (np.cos(ang), 0, np.sin(ang))   # Objektpunkt im Ursprung
        out = lens.next_ray(r)
        xs.append(focus_x_from_height(out, h=0.0, z_axis=r.pos[2]))
      for x in xs:
        self.assertAlmostEqual(x, image_x, delta=0.1, msg=str(kw))


def focus_x_from_height(out, h, z_axis):
  """Schnittpunkt des Strahls mit der Achse z = z_axis + h."""
  s = (z_axis + h - out.pos[2]) / out.normal[2]
  return out.pos[0] + s * out.normal[0]


class TestRepr(unittest.TestCase):

  def test_repr_starts_with_class_name(self):
    self.assertTrue(repr(make_lens(f=100)).startswith("Thicklens(f=100"))

  def test_eval_of_repr_reproduces_the_lens(self):
    for kw in CONFIGS:
      lens = make_lens(**kw)
      with warnings.catch_warnings():
        warnings.simplefilter("ignore")     # pos/normal im repr werden ignoriert
        copy = eval(repr(lens))
      copy.pos = lens.pos
      self.assertIsInstance(copy, Thicklens)
      self.assertEqual(copy.focal_length, lens.focal_length)
      self.assertEqual(copy.biconvex, lens.biconvex)
      self.assertAlmostEqual(copy.thickness, lens.thickness)
      assert_allclose(trace(copy, 2.0).normal, trace(lens, 2.0).normal)


if __name__ == "__main__":
  unittest.main()
