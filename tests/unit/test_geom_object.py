# -*- coding: utf-8 -*-
"""
Tests für LaserCAD.basic_optics.geom_object

Geom_Object ist die Basisklasse für alles mit Position (pos) und Ausrichtung
(normal / _axes). Fehler hier wirken sich auf jedes andere Objekt aus.

Tests, die mit @unittest.expectedFailure markiert sind, beschreiben ein
Verhalten, das nach Ansicht der Doku bzw. der Physik gelten sollte, vom Code
aber aktuell nicht erfüllt wird. Sie halten die Auffälligkeit fest, ohne die
Test-Suite rot zu färben. Sobald der Code korrigiert ist, schlägt der Test
mit "unexpected success" an, und man entfernt einfach den Dekorator.
"""
import io
import unittest
from contextlib import redirect_stdout

import numpy as np
from numpy.testing import assert_allclose

from LaserCAD import Geom_Object, freecad_da
from LaserCAD.basic_optics.geom_object import (rotation_matrix,
                                               rotation_matrix_from_vectors)
from helpers import is_orthonormal_right_handed


class TestRotationMatrix(unittest.TestCase):

  def test_rotation_about_z_by_90_degrees_maps_x_to_y(self):
    R = rotation_matrix((0, 0, 1), np.pi / 2)
    assert_allclose(R @ (1, 0, 0), (0, 1, 0), atol=1e-12)
    assert_allclose(R @ (0, 1, 0), (-1, 0, 0), atol=1e-12)
    assert_allclose(R @ (0, 0, 1), (0, 0, 1), atol=1e-12)

  def test_zero_angle_is_identity(self):
    assert_allclose(rotation_matrix((1, 2, 3), 0), np.eye(3), atol=1e-12)

  def test_full_turn_is_identity(self):
    assert_allclose(rotation_matrix((1, 2, 3), 2 * np.pi), np.eye(3),
                    atol=1e-12)

  def test_result_is_proper_rotation_for_random_inputs(self):
    rng = np.random.default_rng(0)
    for _ in range(20):
      vec = rng.normal(size=3)
      phi = rng.uniform(-2 * np.pi, 2 * np.pi)
      with self.subTest(vec=vec, phi=phi):
        self.assertTrue(is_orthonormal_right_handed(rotation_matrix(vec, phi)))

  def test_rotation_axis_stays_fixed(self):
    vec = np.array((1.0, 2.0, 3.0))
    R = rotation_matrix(vec, 0.8)
    assert_allclose(R @ vec, vec, atol=1e-12)

  def test_input_vector_is_not_modified(self):
    vec = np.array((0.0, 0.0, 5.0))
    rotation_matrix(vec, 1.0)
    assert_allclose(vec, (0, 0, 5))

  def test_negative_angle_is_inverse(self):
    R = rotation_matrix((1, 1, 0), 0.6)
    Rinv = rotation_matrix((1, 1, 0), -0.6)
    assert_allclose(R @ Rinv, np.eye(3), atol=1e-12)


class TestRotationMatrixFromVectors(unittest.TestCase):

  def test_maps_first_vector_onto_second(self):
    rng = np.random.default_rng(1)
    for _ in range(20):
      v1 = rng.normal(size=3)
      v2 = rng.normal(size=3)
      with self.subTest(v1=v1, v2=v2):
        R = rotation_matrix_from_vectors(v1, v2)
        assert_allclose(R @ (v1 / np.linalg.norm(v1)),
                        v2 / np.linalg.norm(v2), atol=1e-12)
        self.assertTrue(is_orthonormal_right_handed(R))

  def test_identical_directions_give_identity(self):
    assert_allclose(rotation_matrix_from_vectors((1, 0, 0), (5, 0, 0)),
                    np.eye(3), atol=1e-12)

  @unittest.expectedFailure
  def test_antiparallel_vectors_are_mapped_correctly(self):
    # BEKANNTE LÜCKE: Für antiparallele Vektoren ist das Kreuzprodukt Null,
    # die Funktion nimmt aber an, das passiere nur bei identischen
    # Richtungen, und gibt die Einheitsmatrix zurück. Dann wird v1 nicht auf
    # v2 = -v1 abgebildet. (Geom_Object.normal behandelt den Fall separat,
    # daher fällt es dort nicht auf.)
    R = rotation_matrix_from_vectors((1, 0, 0), (-1, 0, 0))
    assert_allclose(R @ (1, 0, 0), (-1, 0, 0), atol=1e-12)


class TestGeomObjectDefaults(unittest.TestCase):

  def test_default_position_and_orientation(self):
    g = Geom_Object()
    assert_allclose(g.pos, (0, 0, 80))       # Strahlhöhe 80 mm
    assert_allclose(g.normal, (1, 0, 0))     # Strahl startet in x-Richtung
    assert_allclose(g.get_axes(), np.eye(3))

  def test_name_is_stored(self):
    self.assertEqual(Geom_Object(name="abc").name, "abc")

  def test_repr_contains_class_and_name(self):
    txt = repr(Geom_Object(name="abc"))
    self.assertIn("Geom_Object", txt)
    self.assertIn("abc", txt)


class TestGeomObjectPosition(unittest.TestCase):

  def test_pos_setter_accepts_tuple_and_list(self):
    g = Geom_Object()
    g.pos = (1, 2, 3)
    assert_allclose(g.pos, (1, 2, 3))
    g.pos = [4, 5, 6]
    assert_allclose(g.pos, (4, 5, 6))

  def test_pos_is_float_array_even_for_int_input(self):
    g = Geom_Object()
    g.pos = (1, 2, 3)
    self.assertEqual(g.pos.dtype, float)

  def test_pos_getter_returns_a_copy(self):
    g = Geom_Object()
    p = g.pos
    p[0] = 999
    self.assertEqual(g.pos[0], 0)

  def test_pos_setter_copies_its_input(self):
    g = Geom_Object()
    arr = np.array([1.0, 2.0, 3.0])
    g.pos = arr
    arr[0] = 999
    self.assertEqual(g.pos[0], 1.0)

  def test_pos_changed_hook_is_called_with_old_and_new_position(self):
    calls = []

    class Spy(Geom_Object):
      def _pos_changed(self, old_pos, new_pos):
        calls.append((np.array(old_pos), np.array(new_pos)))

    s = Spy()
    s.pos = (1, 2, 3)
    self.assertEqual(len(calls), 1)
    assert_allclose(calls[0][0], (0, 0, 80))
    assert_allclose(calls[0][1], (1, 2, 3))


class TestGeomObjectOrientation(unittest.TestCase):

  def test_normal_setter_normalizes(self):
    g = Geom_Object()
    g.normal = (0, 5, 0)
    assert_allclose(g.normal, (0, 1, 0), atol=1e-12)

  def test_normal_setter_accepts_tuple(self):
    g = Geom_Object()
    g.normal = (1, 1, 0)
    assert_allclose(g.normal, np.array((1, 1, 0)) / np.sqrt(2), atol=1e-12)

  def test_normal_getter_returns_a_copy(self):
    g = Geom_Object()
    n = g.normal
    n[0] = 5
    assert_allclose(g.normal, (1, 0, 0))

  def test_get_axes_returns_a_copy(self):
    g = Geom_Object()
    ax = g.get_axes()
    ax[0, 0] = 5
    assert_allclose(g.get_axes(), np.eye(3))

  def test_axes_stay_a_proper_rotation_for_random_normals(self):
    rng = np.random.default_rng(2)
    g = Geom_Object()
    for _ in range(50):
      n = rng.normal(size=3)
      with self.subTest(n=n):
        g.normal = n
        assert_allclose(g.normal, n / np.linalg.norm(n), atol=1e-12)
        self.assertTrue(is_orthonormal_right_handed(g.get_axes()))

  def test_setting_the_antiparallel_normal_keeps_a_proper_rotation(self):
    g = Geom_Object()
    g.normal = (-1, 0, 0)
    assert_allclose(g.normal, (-1, 0, 0), atol=1e-12)
    self.assertTrue(is_orthonormal_right_handed(g.get_axes()))

    g = Geom_Object()
    g.rotate((1, 2, 3), 0.7)
    g.normal = -g.normal
    self.assertTrue(is_orthonormal_right_handed(g.get_axes()))

  def test_setting_the_same_normal_changes_nothing(self):
    g = Geom_Object()
    g.rotate((1, 2, 3), 0.7)
    before = g.get_axes()
    g.normal = g.normal
    assert_allclose(g.get_axes(), before, atol=1e-12)

  def test_coordinate_system_matches_axes_columns(self):
    g = Geom_Object()
    g.rotate((1, 2, 3), 0.7)
    x, y, z = g.get_coordinate_system()
    ax = g.get_axes()
    assert_allclose(x, ax[:, 0])
    assert_allclose(y, ax[:, 1])
    assert_allclose(z, ax[:, 2])

  def test_axes_changed_hook_is_called(self):
    calls = []

    class Spy(Geom_Object):
      def _axes_changed(self, old_axes, new_axes):
        calls.append((np.array(old_axes), np.array(new_axes)))

    s = Spy()
    s.rotate((0, 0, 1), np.pi / 2)
    self.assertEqual(len(calls), 1)
    assert_allclose(calls[0][0], np.eye(3))
    assert_allclose(calls[0][1], rotation_matrix((0, 0, 1), np.pi / 2),
                    atol=1e-12)


class TestGeomObjectRotate(unittest.TestCase):

  def test_rotate_about_z_by_90_degrees(self):
    g = Geom_Object()
    g.rotate((0, 0, 1), np.pi / 2)
    assert_allclose(g.normal, (0, 1, 0), atol=1e-12)

  def test_rotate_does_not_change_position(self):
    g = Geom_Object()
    g.pos = (1, 2, 3)
    g.rotate((0, 0, 1), 1.0)
    assert_allclose(g.pos, (1, 2, 3))

  def test_rotation_axis_needs_no_normalisation(self):
    a = Geom_Object()
    b = Geom_Object()
    a.rotate((0, 0, 1), 0.5)
    b.rotate((0, 0, 7), 0.5)
    assert_allclose(a.get_axes(), b.get_axes(), atol=1e-12)

  def test_two_half_turns_give_the_initial_orientation(self):
    g = Geom_Object()
    g.rotate((1, 2, 3), np.pi)
    g.rotate((1, 2, 3), np.pi)
    assert_allclose(g.get_axes(), np.eye(3), atol=1e-12)

  def test_rotations_keep_a_proper_rotation(self):
    rng = np.random.default_rng(3)
    g = Geom_Object()
    for _ in range(30):
      g.rotate(rng.normal(size=3), rng.uniform(-np.pi, np.pi))
    self.assertTrue(is_orthonormal_right_handed(g.get_axes(), atol=1e-10))


class TestGeomObjectGeom(unittest.TestCase):

  def test_get_geom_returns_pos_and_axes(self):
    g = Geom_Object()
    g.pos = (1, 2, 3)
    g.rotate((0, 0, 1), 0.4)
    pos, axes = g.get_geom()
    assert_allclose(pos, g.pos)
    assert_allclose(axes, g.get_axes())

  def test_set_geom_transfers_the_pose(self):
    a = Geom_Object()
    a.pos = (1, 2, 3)
    a.rotate((1, 1, 0), 0.9)
    b = Geom_Object()
    b.set_geom(a.get_geom())
    assert_allclose(b.pos, a.pos)
    assert_allclose(b.get_axes(), a.get_axes())

  def test_get_geom_is_decoupled_from_the_object(self):
    g = Geom_Object()
    pos, axes = g.get_geom()
    pos[0] = 999
    axes[0, 0] = 999
    assert_allclose(g.pos, (0, 0, 80))
    assert_allclose(g.get_axes(), np.eye(3))


class TestAngleTo(unittest.TestCase):

  def _angle_after_rotation(self, axis, phi):
    a = Geom_Object()
    b = Geom_Object()
    b.rotate(axis, phi)
    return a.angle_to(b)

  def test_zero_for_identical_orientation(self):
    self.assertAlmostEqual(self._angle_after_rotation((0, 1, 0), 0.0), 0.0)

  def test_rotation_about_y_has_correct_value_and_sign(self):
    for phi in (0.3, -0.3, 1.0, -1.0):
      with self.subTest(phi=phi):
        self.assertAlmostEqual(self._angle_after_rotation((0, 1, 0), phi), phi)

  def test_magnitude_for_rotation_about_z(self):
    for phi in (0.3, -0.3):
      with self.subTest(phi=phi):
        self.assertAlmostEqual(abs(self._angle_after_rotation((0, 0, 1), phi)),
                               abs(phi))

  @unittest.expectedFailure
  def test_sign_for_rotation_about_z(self):
    # ZU KLÄREN: Das Vorzeichen wird gegen die y-Achse des Objekts bestimmt.
    # Bei Drehungen um z (also in der Tischebene xy) steht das Kreuzprodukt
    # aber senkrecht auf y, daher kommt immer "+" heraus. Die Docstring sagt
    # "with correct sign". Ist das so gewollt (Konvention nur für Drehungen
    # um y) oder ein Fehler? Aufrufer: moduls/compressor.py, moduls/stretcher.py
    self.assertAlmostEqual(self._angle_after_rotation((0, 0, 1), -0.3), -0.3)

  @unittest.expectedFailure
  def test_angles_larger_than_90_degrees(self):
    # angle_to benutzt arcsin(|a x b|); damit ist der Wertebereich auf
    # [-90°, 90°] beschränkt, ein Winkel von 2 rad wird als pi-2 geliefert.
    self.assertAlmostEqual(self._angle_after_rotation((0, 1, 0), 2.0), 2.0)


class TestDraw(unittest.TestCase):

  @unittest.skipIf(freecad_da, "Textausgabe nur ohne FreeCAD-Backend")
  def test_draw_without_freecad_returns_a_text_with_the_name(self):
    g = Geom_Object(name="MeinObjekt")
    buf = io.StringIO()
    with redirect_stdout(buf):
      txt = g.draw()
    self.assertIn("MeinObjekt", txt)
    self.assertEqual(buf.getvalue().strip(), txt.strip())

  def test_invisible_object_is_not_drawn(self):
    g = Geom_Object()
    g.invisible = True
    buf = io.StringIO()
    with redirect_stdout(buf):
      result = g.draw()
    self.assertIsNone(result)
    self.assertEqual(buf.getvalue(), "")


if __name__ == "__main__":
  unittest.main()
