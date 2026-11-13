# -*- coding: utf-8 -*-
"""
Tests für die winkelabhängige ABCD-Matrix gekrümmter Spiegel
(Curved_Mirror.angle_dependent_matrix, Standard: False)

Bei schrägem Einfall (Winkel theta zur Spiegelnormalen) gilt für eine Kugel
  tangential (Einfallsebene):  f_t = R/2 * cos(theta)   -> P = 2 / (R cos theta)
  sagittal (senkrecht dazu):   f_s = R/(2 cos(theta))   -> P = 2 cos(theta) / R
Die 2x2-Matrix eines Aufbaus gilt für die horizontale Ebene. Bei horizontaler
Einfallsebene (Tisch) ist das die tangentiale, bei vertikaler (Periskop) die
sagittale Brechkraft. Der Zylinderspiegel krümmt nur senkrecht zu seiner
Achse. Die Erwartungswerte werden zusätzlich durch echtes Strahlverfolgen
(parallele, horizontal versetzte Strahlen) bestätigt.
"""
import unittest

import numpy as np
from numpy.testing import assert_allclose

from LaserCAD import Beam, Composition, Curved_Mirror, Ray
from LaserCAD.basic_optics import Cylindrical_Mirror, Stripe_mirror

POS = np.array((100.0, 0.0, 80.0))
R = 300.0
Z = np.array((0.0, 0.0, 1.0))
ANGLES = (0, 30, 50, 70)


def tilted(mirror, deg, plane="horizontal", axis_rotation=0.0):
  """Stellt <mirror> so, dass der Strahl +x unter <deg> einfällt."""
  c, s = np.cos(np.radians(deg)), np.sin(np.radians(deg))
  mirror.pos = POS
  mirror.normal = (c, s, 0) if plane == "horizontal" else (c, 0, s)
  if axis_rotation:
    mirror.rotate(vec=mirror.normal, phi=axis_rotation)
  return mirror


def C_of(mirror, direction=(1, 0, 0)):
  r = Ray()
  r.normal = direction
  return mirror.matrix(inray=r)[1, 0]


def traced_C(mirror, k=(1.0, 0.0, 0.0), d=1e-4):
  """C-Element aus echtem Strahlverfolgen (horizontal versetzte Strahlen)."""
  k = np.array(k)
  e_h = np.cross(Z, k)
  e_h = e_h / np.linalg.norm(e_h)
  outs = []
  for sign in (1, -1):
    r = Ray()
    r.normal = k
    r.pos = POS - 50 * k + sign * d * e_h
    outs.append(mirror.next_ray(r))
  e_out = np.cross(Z, outs[0].normal)
  e_out = e_out / np.linalg.norm(e_out)
  d_angle = np.dot(outs[0].normal - outs[1].normal, e_out)
  d_pos = np.dot(outs[0].pos - outs[1].pos, e_out)
  return d_angle / d_pos


class TestSwitch(unittest.TestCase):

  def test_default_is_off(self):
    self.assertFalse(Curved_Mirror.angle_dependent_matrix)
    self.assertFalse(Curved_Mirror(radius=R).angle_dependent_matrix)

  def test_off_keeps_the_old_angle_independent_matrix(self):
    for deg in ANGLES:
      m = tilted(Curved_Mirror(radius=R), deg)
      self.assertAlmostEqual(C_of(m), -2 / R, places=12)

  def test_switch_is_per_instance(self):
    a, b = Curved_Mirror(radius=R), Curved_Mirror(radius=R)
    a.angle_dependent_matrix = True
    self.assertTrue(a.angle_dependent_matrix)
    self.assertFalse(b.angle_dependent_matrix)
    self.assertFalse(Curved_Mirror.angle_dependent_matrix)

  def test_matrix_returns_a_copy(self):
    m = Curved_Mirror(radius=R)
    m.matrix()[1, 0] = 5
    self.assertAlmostEqual(m.matrix()[1, 0], -2 / R)

  def test_normal_incidence_is_identical_in_both_modes(self):
    for cls in (Curved_Mirror, Stripe_mirror, Cylindrical_Mirror):
      m = tilted(cls(radius=R), 0)
      off = C_of(m)
      m.angle_dependent_matrix = True
      self.assertAlmostEqual(C_of(m), off, places=12, msg=cls.__name__)


class TestSphere(unittest.TestCase):

  def make(self, deg, plane):
    m = tilted(Curved_Mirror(radius=R), deg, plane)
    m.angle_dependent_matrix = True
    return m

  def test_horizontal_plane_is_tangential(self):
    for deg in ANGLES:
      expected = -2 / (R * np.cos(np.radians(deg)))
      self.assertAlmostEqual(C_of(self.make(deg, "horizontal")), expected, places=12)

  def test_vertical_plane_is_sagittal(self):
    for deg in ANGLES:
      expected = -2 * np.cos(np.radians(deg)) / R
      self.assertAlmostEqual(C_of(self.make(deg, "vertical")), expected, places=12)

  def test_negative_radius_changes_the_sign(self):
    m = tilted(Curved_Mirror(radius=-R), 45)
    m.angle_dependent_matrix = True
    self.assertAlmostEqual(C_of(m), 2 / (R * np.cos(np.radians(45))), places=12)

  def test_flat_radius_zero_has_no_power(self):
    m = tilted(Curved_Mirror(radius=0), 45)
    m.angle_dependent_matrix = True
    self.assertEqual(C_of(m), 0)

  def test_other_matrix_elements_are_unchanged(self):
    m = self.make(50, "horizontal")
    M = m.matrix(inray=Ray())
    assert_allclose(M[0], (1, 0))
    self.assertEqual(M[1, 1], 1)

  def test_matches_ray_tracing(self):
    for deg in ANGLES:
      for plane in ("horizontal", "vertical"):
        m = self.make(deg, plane)
        self.assertAlmostEqual(C_of(m), traced_C(m), delta=2e-6,
                               msg=f"{deg} {plane}")

  def test_tilted_incidence_plane_lies_between_the_two_extremes(self):
    deg = 50
    m = tilted(Curved_Mirror(radius=R), 0)
    c, s = np.cos(np.radians(deg)), np.sin(np.radians(deg))
    m.normal = (c, s / np.sqrt(2), s / np.sqrt(2))      # 45° schräge Ebene
    m.angle_dependent_matrix = True
    p = -C_of(m)
    p_tang = 2 / (R * c)
    p_sag = 2 * c / R
    self.assertGreater(p, p_sag)
    self.assertLess(p, p_tang)

  def test_stripe_mirror_behaves_like_a_sphere(self):
    a = tilted(Stripe_mirror(radius=R), 50)
    b = tilted(Curved_Mirror(radius=R), 50)
    a.angle_dependent_matrix = b.angle_dependent_matrix = True
    self.assertAlmostEqual(C_of(a), C_of(b), places=12)


class TestCylinder(unittest.TestCase):

  def make(self, deg, plane, rotation=0.0):
    m = tilted(Cylindrical_Mirror(radius=R), deg, plane, rotation)
    m.angle_dependent_matrix = True
    return m

  def test_vertical_axis_in_horizontal_plane_is_tangential(self):
    for deg in ANGLES:
      expected = -2 / (R * np.cos(np.radians(deg)))
      self.assertAlmostEqual(C_of(self.make(deg, "horizontal")), expected, places=12)

  def test_horizontal_plane_matches_ray_tracing(self):
    for deg in ANGLES:
      m = self.make(deg, "horizontal")
      self.assertAlmostEqual(C_of(m), traced_C(m), delta=2e-6, msg=str(deg))

  def test_vertical_plane_with_axis_in_the_plane_is_sagittal(self):
    # Achse liegt in der Einfallsebene, die Krümmung steht senkrecht dazu
    for deg in ANGLES:
      expected = -2 * np.cos(np.radians(deg)) / R
      self.assertAlmostEqual(C_of(self.make(deg, "vertical")), expected, places=12)

  def test_vertical_plane_with_axis_in_the_plane_matches_ray_tracing(self):
    for deg in ANGLES:
      m = self.make(deg, "vertical")
      self.assertAlmostEqual(C_of(m), traced_C(m), delta=2e-6, msg=str(deg))

  def test_vertical_plane_with_horizontal_axis_has_no_horizontal_power(self):
    for deg in (30, 50):
      m = self.make(deg, "vertical", rotation=np.pi / 2)
      self.assertAlmostEqual(C_of(m), 0.0, places=12)
      self.assertAlmostEqual(traced_C(m), 0.0, delta=2e-6)


class TestInComposition(unittest.TestCase):

  def build(self, flag):
    comp = Composition()
    comp.set_light_source(Beam(radius=1.0, angle=0))
    comp.propagate(100)
    mirror = Curved_Mirror(radius=R, phi=90)           # 45 Grad Einfall
    mirror.angle_dependent_matrix = flag
    comp.add_on_axis(mirror)
    return comp

  def test_old_behaviour_by_default(self):
    self.assertAlmostEqual(self.build(False).matrix()[1, 0], -2 / R, places=12)

  def test_composition_uses_the_real_angle_of_incidence(self):
    expected = -2 / (R * np.cos(np.radians(45)))
    self.assertAlmostEqual(self.build(True).matrix()[1, 0], expected, places=10)


if __name__ == "__main__":
  unittest.main()
