import unittest

from convexus.sdkcore.entities.fractions.percent import Percent

class TestPercent(unittest.TestCase):

    def test(self):
      self.assertEqual(Percent(1), Percent(1, 1))
      self.assertEqual(Percent(1, 100).add(Percent(2, 100)), Percent(3, 100))
      self.assertEqual(Percent(1, 25).add(Percent(2, 100)), Percent(150, 2500))
      self.assertEqual(Percent(1, 100).subtract(Percent(2, 100)), Percent(-1, 100))
      self.assertEqual(Percent(1, 25).subtract(Percent(2, 100)), Percent(50, 2500))
      self.assertEqual(Percent(1, 100).multiply(Percent(2, 100)), Percent(2, 10000))
      self.assertEqual(Percent(1, 25).multiply(Percent(2, 100)), Percent(2, 2500))
      self.assertEqual(Percent(1, 100).divide(Percent(2, 100)), Percent(100, 200))
      self.assertEqual(Percent(1, 25).divide(Percent(2, 100)), Percent(100, 50))
      self.assertEqual(Percent(154, 10_000).toFixed(2), '1.54')

if __name__ == '__main__':
    unittest.main()