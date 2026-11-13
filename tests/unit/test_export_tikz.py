# -*- coding: utf-8 -*-
"""
Tests für export_to_TikZ (LaserCAD.basic_optics.composition)

Der Export schreibt in die angegebene Datei im Anhänge-Modus. Die Tests
benutzen deshalb ein temporäres Verzeichnis, das am Ende gelöscht wird; im
Projektordner bleibt nichts liegen.
"""
import contextlib
import io
import os
import re
import tempfile
import unittest

from LaserCAD.basic_optics import export_to_TikZ
from LaserCAD.basic_optics.composition import make_unique_names
from LaserCAD.moduls import Make_Telescope


def export(setup, **kwargs):
  """Exportiert <setup> in eine temporäre Datei und gibt (Dateitext, stdout) zurück."""
  with tempfile.TemporaryDirectory() as folder:
    path = os.path.join(folder, "setup.tex")
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
      export_to_TikZ(setup, filename=path, **kwargs)
    with open(path) as f:
      return f.read(), out.getvalue()


class TestExportTelescope(unittest.TestCase):

  def test_file_has_header_with_setup_name(self):
    tex, _ = export(Make_Telescope())
    self.assertTrue(tex.startswith("%%%%% Teleskop %%%%%"))

  def test_file_content_equals_console_output(self):
    tex, out = export(Make_Telescope())
    nonblank = lambda t: [l for l in t.splitlines() if l.strip()]
    self.assertEqual(nonblank(tex), nonblank(out))

  def test_start_coordinate_and_both_lens_positions_are_written(self):
    tex, _ = export(Make_Telescope())
    self.assertIn("\\coordinate (Start_Teleskop) at (0.00, 0.00);", tex)
    self.assertIn("at (1.00, 0.00);", tex)
    self.assertIn("at (3.00, 0.00);", tex)

  def test_two_convex_lenses_are_drawn(self):
    tex, _ = export(Make_Telescope())
    self.assertEqual(len(re.findall(r"\\convexlens\[angle=0", tex)), 2)
    self.assertEqual(len(re.findall(r"\\concavelens", tex)), 0)

  def test_negative_lens_is_drawn_concave(self):
    tex, _ = export(Make_Telescope(f1=-50, f2=100))     # Galilei-Teleskop
    self.assertEqual(len(re.findall(r"\\concavelens", tex)), 1)
    self.assertEqual(len(re.findall(r"\\convexlens", tex)), 1)

  def test_export_appends_to_existing_file(self):
    with tempfile.TemporaryDirectory() as folder:
      path = os.path.join(folder, "setup.tex")
      with contextlib.redirect_stdout(io.StringIO()):
        export_to_TikZ(Make_Telescope(), filename=path)
        export_to_TikZ(Make_Telescope(), filename=path)
      with open(path) as f:
        tex = f.read()
    self.assertEqual(tex.count("%%%%% Teleskop %%%%%"), 2)

  def test_without_filename_nothing_is_written(self):
    with tempfile.TemporaryDirectory() as folder:
      cwd = os.getcwd()
      os.chdir(folder)
      try:
        with contextlib.redirect_stdout(io.StringIO()):
          export_to_TikZ(Make_Telescope())
        self.assertEqual(os.listdir(folder), [])
      finally:
        os.chdir(cwd)

  def test_node_names_are_unique(self):
    # Beide Linsen des Teleskops heißen "NewLens". Ohne eindeutige Namen würde
    # TikZ nur die zweite Koordinate benutzen und beide Linsen bei x=3.0 zeichnen.
    tex, _ = export(Make_Telescope())
    names = re.findall(r"\\coordinate \((\S+)\)", tex)
    self.assertEqual(len(names), len(set(names)))

  def test_each_lens_is_placed_at_its_own_node(self):
    tex, _ = export(Make_Telescope())
    self.assertIn("\\coordinate (Teleskop_NewLens_1) at (1.00, 0.00);", tex)
    self.assertIn("\\coordinate (Teleskop_NewLens_2) at (3.00, 0.00);", tex)
    self.assertRegex(tex, r"\\convexlens\[angle=0, width=0.66\] at \(Teleskop_NewLens_1\)")
    self.assertRegex(tex, r"\\convexlens\[angle=0, width=0.67\] at \(Teleskop_NewLens_2\)")


class TestMakeUniqueNames(unittest.TestCase):

  def test_unique_names_are_unchanged(self):
    self.assertEqual(make_unique_names(["a", "b"]), ["a", "b"])

  def test_duplicates_get_numbered_suffixes(self):
    self.assertEqual(make_unique_names(["a", "b", "a", "a"]),
                     ["a_1", "b", "a_2", "a_3"])

  def test_suffix_does_not_collide_with_existing_name(self):
    result = make_unique_names(["a", "a", "a_1"])
    self.assertEqual(len(result), len(set(result)))
    self.assertEqual(result[2], "a_1")

  def test_reserved_names_are_avoided(self):
    result = make_unique_names(["Start", "x"], reserved=["Start"])
    self.assertNotIn("Start", result)
    self.assertEqual(result[1], "x")


if __name__ == "__main__":
  unittest.main()
