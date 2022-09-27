import unittest
from convexus.sdk.utils.encodeSqrtRatioX96 import encodeSqrtRatioX96

class TestEncodeSqrtRatioX96(unittest.TestCase):

  def test_100_1(self):
    self.assertEqual(encodeSqrtRatioX96(100, 1), 792281625142643375935439503360)

  def test_1_1(self):
    self.assertEqual(encodeSqrtRatioX96(1, 100), 7922816251426434199159046144)

  def test_111_3(self):
    self.assertEqual(encodeSqrtRatioX96(111, 333), 45742400955009929883957592064)

  def test_333_1(self):
    self.assertEqual(encodeSqrtRatioX96(333, 111), 137227202865029789651872776192)

if __name__ == '__main__':
    unittest.main()