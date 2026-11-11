# -*- coding: utf-8 -*-
"""
Tests für LaserCAD.basic_optics.mirror (Mirror, Curved_Mirror)

Konvention (siehe Docstring von Mirror): <phi> ist der Winkel, um den der
Spiegel einen Strahl in der xy-Ebene (mathematisch positiv) weiterdreht,
<theta> der Winkel, um den er ihn aus der xy-Ebene heraus (nach +z) dreht.
Die Normale des Spiegels wird aus Einfallsrichtung, phi und theta berechnet.
"""
import unittest

import numpy as np
from numpy.testing import assert_allclose

from LaserCAD import Mirror, Curved_Mirror, Ray
from LaserCAD.basic_optics.geom_object import rotation_matrix
from helpers import axis_crossing

MIRROR_POS = np.array((100.0, 0.0, 80.0))
S2 = np.sqrt(2) / 2


def reflect(mirror, ray=None):
  """Spiegel an MIRROR_POS, Strahl default: (0,0,80) in +x."""
  mirror.pos = MIRROR_POS
  if ray is None:
    ray = Ray()
  return mirror.next_ray(ray)


class TestMirrorAngles(unittest.TestCase):

  def test_phi_rotates_the_beam_in_the_xy_plane(self):
    cases = {
      90: (0, 1, 0),
      -90: (0, -1, 0),
      180: (-1, 0, 0),
      45: (S2, S2, 0),
      -45: (S2, -S2, 0),
      135: (-S2, S2, 0),
    }
    for phi, expected in cases.items():
      with self.subTest(phi=phi):
        out = reflect(Mirror(phi=phi))
        assert_allclose(out.normal, expected, atol=1e-12)

  def test_theta_tilts_the_beam_out_of_the_plane(self):
    for theta in (30, -30, 10, 60):
      with self.subTest(theta=theta):
        out = reflect(Mirror(phi=90, theta=theta))
        self.assertAlmostEqual(out.normal[2], np.sin(np.radians(theta)))
        self.assertAlmostEqual(out.normal[1], np.cos(np.radians(theta)))
        self.assertAlmostEqual(out.normal[0], 0)

  def test_phi_setter_updates_the_mirror_normal(self):
    m = Mirror(phi=90)
    n90 = m.normal
    m.phi = 180
    self.assertEqual(m.phi, 180)
    self.assertFalse(np.allclose(m.normal, n90))
    out = reflect(m)
    assert_allclose(out.normal, (-1, 0, 0), atol=1e-12)

  def test_theta_setter_updates_the_mirror_normal(self):
    m = Mirror(phi=90, theta=0)
    m.theta = 30
    self.assertEqual(m.theta, 30)
    out = reflect(m)
    self.assertAlmostEqual(out.normal[2], 0.5)

  def test_set_geom_makes_phi_relative_to_the_incoming_beam(self):
    # Strahl läuft in +y; phi=90 dreht ihn dann (mathematisch positiv) nach -x
    r = Ray()
    r.pos = (0, -100, 80)
    r.normal = (0, 1, 0)
    m = Mirror(phi=90)
    m.set_geom(r.get_geom())
    m.pos = (0, 0, 80)
    out = m.next_ray(r)
    assert_allclose(out.normal, (-1, 0, 0), atol=1e-12)


class TestMirrorReflection(unittest.TestCase):

  def test_reflected_ray_starts_at_the_intersection_with_the_mirror(self):
    out = reflect(Mirror(phi=90))
    assert_allclose(out.pos, MIRROR_POS, atol=1e-12)

  def test_offset_ray_is_reflected_at_the_offset_point(self):
    r = Ray()
    r.pos = (0, 0, 83)           # 3 mm über der Mittelachse
    out = reflect(Mirror(phi=90), r)
    assert_allclose(out.pos, (100, 0, 83), atol=1e-12)
    assert_allclose(out.normal, (0, 1, 0), atol=1e-12)

  def test_output_direction_is_a_unit_vector(self):
    out = reflect(Mirror(phi=37, theta=12))
    self.assertAlmostEqual(np.linalg.norm(out.normal), 1.0)

  def test_phi_90_is_a_rotation_of_the_beam_direction_about_z(self):
    for incident_angle in (0.0, 0.7, -1.2, 2.5):
      with self.subTest(incident_angle=incident_angle):
        r = Ray()
        r.rotate((0, 0, 1), incident_angle)
        m = Mirror(phi=60)
        m.set_geom(r.get_geom())
        m.pos = r.pos + 100 * r.normal
        out = m.next_ray(r)
        expected = rotation_matrix((0, 0, 1), np.radians(60)) @ r.normal
        assert_allclose(out.normal, expected, atol=1e-12)

  def test_law_of_reflection_for_arbitrary_orientation(self):
    # Normalkomponente kehrt sich um, Tangentialkomponente bleibt erhalten
    rng = np.random.default_rng(4)
    for _ in range(15):
      r = Ray()
      r.normal = rng.normal(size=3)
      r.pos = rng.uniform(-50, 50, size=3)
      m = Mirror(phi=rng.uniform(20, 160), theta=rng.uniform(-40, 40))
      m.set_geom(r.get_geom())
      m.pos = r.pos + rng.uniform(80, 150) * r.normal
      out = m.next_ray(r)
      n = m.normal
      k_in, k_out = r.normal, out.normal
      with self.subTest(k_in=k_in):
        self.assertAlmostEqual(np.dot(k_out, n), -np.dot(k_in, n))
        assert_allclose(k_out - np.dot(k_out, n) * n,
                        k_in - np.dot(k_in, n) * n, atol=1e-12)
        self.assertAlmostEqual(np.linalg.norm(k_out), 1.0)

  def test_reflection_is_reversible(self):
    # Läuft der reflektierte Strahl rückwärts, kommt er in der Ursprungs-
    # richtung wieder heraus (Umkehrbarkeit des Lichtwegs).
    m = Mirror(phi=60, theta=10)
    r = Ray()
    m.set_geom(r.get_geom())
    m.pos = (100, 0, 80)
    out = m.next_ray(r)
    back = Ray()
    back.set_geom(out.get_geom())
    back.normal = -out.normal
    back.pos = out.pos + 50 * out.normal
    again = m.next_ray(back)
    assert_allclose(again.normal, -r.normal, atol=1e-12)

  def test_input_ray_direction_is_not_changed(self):
    r = Ray()
    r.pos = (0, 0, 83)
    reflect(Mirror(phi=90), r)
    assert_allclose(r.pos, (0, 0, 83))
    assert_allclose(r.normal, (1, 0, 0))

  def test_reflection_method_and_next_ray_agree(self):
    m = Mirror(phi=75, theta=5)
    m.pos = MIRROR_POS
    a = m.reflection(Ray())
    b = m.next_ray(Ray())
    assert_allclose(a.pos, b.pos)
    assert_allclose(a.normal, b.normal)


class TestCurvedMirror(unittest.TestCase):

  def _focus_of_parallel_ray(self, radius, offset):
    cm = Curved_Mirror(radius=radius, phi=180)   # senkrechter Einfall
    cm.pos = MIRROR_POS
    r = Ray()
    r.pos = MIRROR_POS - (100, 0, 0) + offset
    out = cm.next_ray(r)
    # Fokus liegt vor dem Spiegel, also entgegen der Einfallsrichtung (+x)
    s, miss = axis_crossing(out, cm.pos, (-1, 0, 0))
    return s, miss

  def test_focal_length_is_half_the_radius(self):
    self.assertEqual(Curved_Mirror(radius=200).focal_length(), 100)
    self.assertEqual(Curved_Mirror(radius=-300).focal_length(), -150)

  def test_matrix_element_C_is_minus_two_over_radius(self):
    self.assertAlmostEqual(Curved_Mirror(radius=200).matrix()[1, 0], -2 / 200)

  def test_changing_the_radius_updates_the_matrix(self):
    cm = Curved_Mirror(radius=200)
    cm.radius = 400
    self.assertEqual(cm.radius, 400)
    self.assertAlmostEqual(cm.matrix()[1, 0], -2 / 400)

  def test_parallel_rays_focus_near_half_the_radius(self):
    for radius in (200, 500, 1000):
      with self.subTest(radius=radius):
        s, miss = self._focus_of_parallel_ray(radius, np.array((0, 0, 0.5)))
        self.assertAlmostEqual(miss, 0, places=6)
        self.assertAlmostEqual(s / (radius / 2), 1, places=4)

  def test_focus_matches_the_exact_sphere_geometry(self):
    # Die Spiegelfläche wird als echte Kugel berechnet, d.h. inklusive
    # sphärischer Aberration: Fokus bei R * (1 - 1/(2 cos(theta))) mit
    # sin(theta) = h / R.
    R = 200.0
    for h in (0.5, 5.0, 20.0):
      with self.subTest(h=h):
        theta = np.arcsin(h / R)
        expected = R * (1 - 1 / (2 * np.cos(theta)))
        s, miss = self._focus_of_parallel_ray(R, np.array((0, 0, h)))
        self.assertAlmostEqual(miss, 0, places=6)
        self.assertAlmostEqual(s, expected, places=6)

  def test_y_and_z_offsets_focus_alike_at_normal_incidence(self):
    sz, _ = self._focus_of_parallel_ray(200, np.array((0, 0, 3.0)))
    sy, _ = self._focus_of_parallel_ray(200, np.array((0, 3.0, 0)))
    self.assertAlmostEqual(sz, sy, places=9)

  def test_central_ray_behaves_like_a_plane_mirror(self):
    cm = Curved_Mirror(radius=200, phi=90)
    out = reflect(cm)
    assert_allclose(out.normal, (0, 1, 0), atol=1e-9)
    assert_allclose(out.pos, MIRROR_POS, atol=1e-9)


if __name__ == "__main__":
  unittest.main()
