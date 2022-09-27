import unittest

from convexus.sdk.utils.mostSignificantBit import mostSignificantBit
from convexus.sdkcore.constants import MaxUint256

class TestMostSignificantBit(unittest.TestCase):

  def test_throwsForZero(self):
    with self.assertRaises(AssertionError):
       mostSignificantBit(0)

  def test_correctValueForEveryPowerOf2(self):
    for i in range(1, 256):
      self.assertEqual(mostSignificantBit(2**i), i)

  def test_correctValueForEveryPowerOf2Minus1(self):
    for i in range(2, 256):
      self.assertEqual(mostSignificantBit(2**i - 1), i - 1)

  def test_succeedsForMaxUint256(self):
    self.assertEqual(mostSignificantBit(MaxUint256), 255)

  def test_throwsForMaxUint256Plus1(self):
    with self.assertRaises(AssertionError):
      mostSignificantBit(MaxUint256 + 1)

if __name__ == '__main__':
    unittest.main()