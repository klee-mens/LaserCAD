# -*- coding: utf-8 -*-
"""
Tests für die generierte Referenz (manual/reference).

Die Seiten werden von manual/reference/build_reference.py aus Signaturen und
Docstrings erzeugt. Diese Tests stellen sicher, dass
  - jede öffentliche Klasse und jede Make_*-Funktion in der Referenz steht und
  - die eingecheckten Seiten zum aktuellen Code passen.
Schlägt der zweite Test fehl, einfach
    python manual/reference/build_reference.py
ausführen und die geänderten Seiten committen.
"""
import contextlib
import importlib.util
import inspect
import io
import unittest
import warnings
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
REF_DIR = REPO_ROOT / "manual" / "reference"


def load_builder():
  spec = importlib.util.spec_from_file_location(
    "build_reference", REF_DIR / "build_reference.py")
  mod = importlib.util.module_from_spec(spec)
  with contextlib.redirect_stdout(io.StringIO()), warnings.catch_warnings():
    warnings.simplefilter("ignore")
    spec.loader.exec_module(mod)
  return mod


class TestReference(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.builder = load_builder()
    with contextlib.redirect_stdout(io.StringIO()), warnings.catch_warnings():
      warnings.simplefilter("ignore")
      cls.files = cls.builder.build()
    cls.all_text = "\n".join(cls.files.values())

  def test_every_exported_class_is_documented(self):
    import LaserCAD
    for name in dir(LaserCAD):
      if inspect.isclass(getattr(LaserCAD, name)):
        with self.subTest(cls=name):
          self.assertIn(f"### {name}\n", self.all_text)

  def test_every_make_function_is_documented(self):
    import LaserCAD.moduls as moduls
    for name in dir(moduls):
      if name.startswith("Make_") and inspect.isfunction(getattr(moduls, name)):
        with self.subTest(func=name):
          self.assertIn(f"### {name}\n", self.all_text)

  def test_public_classes_have_a_docstring(self):
    import LaserCAD
    for name in dir(LaserCAD):
      obj = getattr(LaserCAD, name)
      if inspect.isclass(obj):
        with self.subTest(cls=name):
          self.assertTrue(obj.__dict__.get("__doc__"),
                          f"{name} hat keinen eigenen Docstring")

  def test_committed_pages_are_up_to_date(self):
    for name, text in self.files.items():
      with self.subTest(page=name):
        path = REF_DIR / name
        self.assertTrue(path.exists(), f"{name} fehlt, build_reference.py ausführen")
        committed = path.read_text(encoding="utf-8").replace("\r\n", "\n")
        self.assertEqual(
          committed, text,
          f"{name} ist veraltet: python manual/reference/build_reference.py")


if __name__ == "__main__":
  unittest.main()
