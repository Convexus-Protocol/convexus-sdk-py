import unittest
from convexus.sdk.utils.decodeSqrtRatioX96 import decodeSqrtRatioX96

class TestDecodeSqrtRatioX96(unittest.TestCase):

  def test_0(self):
    self.assertEqual(decodeSqrtRatioX96(792281625142643375935439503360), 100.0)

  def test_1(self):
    self.assertEqual(decodeSqrtRatioX96(7922816251426434199159046144), 0.010000000000000002)

  def test_2(self):
    self.assertEqual(decodeSqrtRatioX96(45742400955009929883957592064), 1/3)

  def test_3(self):
    self.assertEqual(decodeSqrtRatioX96(137227202865029789651872776192), 2.9999999999999996)

if __name__ == '__main__':
    unittest.main()