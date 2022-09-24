import unittest
from sdk.utils.decodeSqrtRatiox96 import decodeSqrtRatiox96

class TestDecodeSqrtRatioX96(unittest.TestCase):

  def test_100_1(self):
    self.assertEqual(decodeSqrtRatiox96(792281625142643375935439503360), 100.0)

  def test_100_1(self):
    self.assertEqual(decodeSqrtRatiox96(7922816251426434199159046144), 0.010000000000000002)

  def test_100_1(self):
    self.assertEqual(decodeSqrtRatiox96(45742400955009929883957592064), 1/3)

  def test_100_1(self):
    self.assertEqual(decodeSqrtRatiox96(137227202865029789651872776192), 2.9999999999999996)

if __name__ == '__main__':
    unittest.main()