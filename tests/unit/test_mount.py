# -*- coding: utf-8 -*-
"""
Tests for the default mounts and posts (LaserCAD.basic_optics.mount).
"""
import unittest
import warnings
from unittest import mock

from LaserCAD.basic_optics import mount as mount_module
from LaserCAD.basic_optics.mount import (Composed_Mount, Post, Unit_Mount,
                                         get_mount_by_aperture_and_element)
from LaserCAD.basic_optics import Lens

INCH = 25.4


class TestLensMountByAperture(unittest.TestCase):

  def model_for(self, aperture):
    mount = get_mount_by_aperture_and_element(aperture, "Lens", 5)
    return mount.mount_list[0].model

  def test_lens_mount_models(self):
    expected = {0.5*INCH: "MLH05_M", 1*INCH: "LMR1_M", 1.5*INCH: "LMR15_M",
                2*INCH: "LMR2_M", 3*INCH: "LMR3_M", 4*INCH: "LMR4_M"}
    for aperture, model in expected.items():
      with self.subTest(aperture=aperture):
        self.assertEqual(self.model_for(aperture), model)

  def test_1_5_inch_lens_mount_is_in_the_database(self):
    # the model name used to be "LMR1.5_M", which is not in lensmounts.csv
    unit = Unit_Mount(model="LMR15_M")
    self.assertTrue(unit.set_by_table())
    self.assertIn("/lens/", unit.draw_dict["stl_file"].replace("\\", "/"))
    self.assertAlmostEqual(unit.aperture, 1.5*INCH)

  def test_lens_larger_than_4_inch_gets_invisible_mount_with_warning(self):
    with warnings.catch_warnings(record=True) as caught:
      warnings.simplefilter("always")
      mount = get_mount_by_aperture_and_element(6*INCH, "Lens", 5)
    self.assertIsInstance(mount, Unit_Mount)
    self.assertNotIsInstance(mount, Composed_Mount)
    self.assertEqual(mount.model, "dont_draw")
    self.assertTrue(any("No lens mount" in str(w.message) for w in caught))

  def test_large_lens_can_be_created(self):
    with warnings.catch_warnings():
      warnings.simplefilter("ignore")
      lens = Lens()
      lens.aperture = 6*INCH
    self.assertEqual(lens.aperture, 6*INCH)

  def test_mirror_larger_than_4_inch_still_gets_6_inch_mount(self):
    mount = get_mount_by_aperture_and_element(6*INCH, "Mirror", 10)
    self.assertEqual(mount.mount_list[0].model, "6inch_mirror_mount")


class TestUnitMountDrawText(unittest.TestCase):

  def test_draw_text_returns_text_with_model(self):
    unit = Unit_Mount(model="POLARIS-K1")
    txt = unit.draw_text()
    self.assertIsInstance(txt, str)
    self.assertIn("POLARIS-K1", txt)


class TestFind1InchPost(unittest.TestCase):

  def chosen(self, height, lower_limit=0):
    post = Post(lower_limit=lower_limit)
    post.pos = (0, 0, height)
    with mock.patch.object(mount_module, "draw_1inch_post",
                           side_effect=lambda **kw: kw):
      return post.find_1inch_post()

  def test_height_exactly_on_catalogue_value(self):
    for height, model in ((19, "RS075P4M"), (25, "RS1P4M"), (50, "RS2P4M"),
                          (100, "RS4P4M"), (155, "RS6P4M")):
      with self.subTest(height=height):
        result = self.chosen(height)
        self.assertEqual(result["name"], model)
        self.assertAlmostEqual(result["h_diff"], 0)

  def test_height_between_catalogue_values(self):
    result = self.chosen(30)
    self.assertEqual(result["name"], "RS1P4M")
    self.assertAlmostEqual(result["h_diff"], 5)

  def test_lowest_post(self):
    result = self.chosen(12.5)
    self.assertEqual(result["name"], "RS05P4M")
    self.assertAlmostEqual(result["h_diff"], 0)

  def test_lower_limit_is_subtracted(self):
    result = self.chosen(75, lower_limit=25)
    self.assertEqual(result["name"], "RS2P4M")
    self.assertAlmostEqual(result["h_diff"], 0)

  def test_too_low_returns_none(self):
    with mock.patch("builtins.print"):
      self.assertIsNone(self.chosen(10))


if __name__ == "__main__":
  unittest.main()
