import unittest
from sdk.utils.tickMath import TickMath 

class TestGetSqrtRatioAtTick(unittest.TestCase):

  def test_throwsForNonInteger(self):
    with self.assertRaises(AssertionError):
      TickMath.getSqrtRatioAtTick(1.5)

  def test_throwsForTickTooSmall(self):
    with self.assertRaises(AssertionError):
      TickMath.getSqrtRatioAtTick(TickMath.MIN_TICK - 1)

  def test_throwsForTickTooLarge(self):
    with self.assertRaises(AssertionError):
      TickMath.getSqrtRatioAtTick(TickMath.MAX_TICK + 1)

  def test_returnsTheCorrectValueForMinTick(self):
      self.assertEqual(TickMath.getSqrtRatioAtTick(TickMath.MIN_TICK), TickMath.MIN_SQRT_RATIO)

  def test_returnsTheCorrectValueForTick0(self):
      self.assertEqual(TickMath.getSqrtRatioAtTick(0), 1 << 96)

  def test_returnsTheCorrectValueForMaxTick(self):
      self.assertEqual(TickMath.getSqrtRatioAtTick(TickMath.MAX_TICK), TickMath.MAX_SQRT_RATIO)


class TestGetTickAtSqrtRatio(unittest.TestCase):

  def test_returnsTheCorrectValueForSqrtRatioAtMinTick(self):
      self.assertEqual(TickMath.getTickAtSqrtRatio(TickMath.MIN_SQRT_RATIO), TickMath.MIN_TICK)

  def test_returnsTheCorrectValueForSqrtRatioAtMaxTick(self):
      self.assertEqual(TickMath.getTickAtSqrtRatio(TickMath.MAX_SQRT_RATIO - 1), TickMath.MAX_TICK - 1)


if __name__ == '__main__':
    unittest.main()