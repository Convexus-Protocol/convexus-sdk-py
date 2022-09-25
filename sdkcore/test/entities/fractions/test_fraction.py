import unittest

from sdkcore.entities.fractions.fraction import Fraction

class TestFractionQuotient(unittest.TestCase):
    
    def test_floor_division(self):
        self.assertEqual(Fraction(8, 3).quotient, 2) # one below
        self.assertEqual(Fraction(12, 4).quotient, 3) # exact
        self.assertEqual(Fraction(16, 5).quotient, 3) # one above

class TestFractionRemainder(unittest.TestCase):
    
    def test_returnsFractionAfterDivison(self):
      self.assertEqual(Fraction(8, 3).remainder, Fraction(2, 3))
      self.assertEqual(Fraction(12, 4).remainder, Fraction(0, 4))
      self.assertEqual(Fraction(16, 5).remainder, Fraction(1, 5))

class TestFractionInvert(unittest.TestCase):
    
    def test_flipsNumAndDenom(self):
      self.assertEqual(Fraction(5, 10).invert().numerator, 10)
      self.assertEqual(Fraction(5, 10).invert().denominator, 5)

    def test_add_multiplesDenomsAndAddsNums(self):
      self.assertEqual(Fraction(1, 10).add(Fraction(4, 12)), Fraction(52, 120))

    def test_0(self):
      self.assertEqual(Fraction(1, 5).add(Fraction(2, 5)), Fraction(3, 5))

    def test_substract_multiplesDenomsAndSubtractsNums(self):
      self.assertEqual(Fraction(1, 10).subtract(Fraction(4, 12)), Fraction(-28, 120))

    def test_subtract_sameDenom(self):
      self.assertEqual(Fraction(3, 5).subtract(Fraction(2, 5)), Fraction(1, 5))

    def test_lessThan(self):
      self.assertTrue(Fraction(1, 10).lessThan(Fraction(4, 12)))
      self.assertFalse(Fraction(1, 3).lessThan(Fraction(4, 12)))
      self.assertFalse(Fraction(5, 12).lessThan(Fraction(4, 12)))

    def test_equalTo(self):
      self.assertFalse(Fraction(1, 10).equalTo(Fraction(4, 12)))
      self.assertTrue(Fraction(1, 3).equalTo(Fraction(4, 12)))
      self.assertFalse(Fraction(5, 12).equalTo(Fraction(4, 12)))

    def test_greaterThan(self):
      self.assertFalse(Fraction(1, 10).greaterThan(Fraction(4, 12)))
      self.assertFalse(Fraction(1, 3).greaterThan(Fraction(4, 12)))
      self.assertTrue(Fraction(5, 12).greaterThan(Fraction(4, 12)))

    def test_multiply(self):
      self.assertEqual(Fraction(1, 10).multiply(Fraction(4, 12)), Fraction(4, 120))
      self.assertEqual(Fraction(1, 3).multiply(Fraction(4, 12)), Fraction(4, 36))
      self.assertEqual(Fraction(5, 12).multiply(Fraction(4, 12)), Fraction(20, 144))

    def test_divide(self):
      self.assertEqual(Fraction(1, 10).divide(Fraction(4, 12)), Fraction(12, 40))
      self.assertEqual(Fraction(1, 3).divide(Fraction(4, 12)), Fraction(12, 12))
      self.assertEqual(Fraction(5, 12).divide(Fraction(4, 12)), Fraction(60, 48))

    def test_asFraction(self):
      f = Fraction(1, 2)
      self.assertEqual(f.asFraction, (f))

if __name__ == '__main__':
    unittest.main()