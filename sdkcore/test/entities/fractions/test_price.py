import unittest
from sdkcore.entities.currency import Token
from sdkcore.entities.fractions.currencyAmount import CurrencyAmount
from sdkcore.entities.fractions.price import Price

class TestPrice(unittest.TestCase):

  t0_18 = Token('cx0000000000000000000000000000000000000000', 18)
  t1_6 = Token('cx0000000000000000000000000000000000000001', 6)
  t2_18 = Token('cx0000000000000000000000000000000000000002', 18)

  def test_constructor_4(self):
    price = Price(TestPrice.t0_18, TestPrice.t2_18, 1, 54321)
    self.assertEqual(price.toFixed(5), '54321')
    self.assertTrue(price.baseCurrency.equals(TestPrice.t0_18))
    self.assertTrue(price.quoteCurrency.equals(TestPrice.t2_18))

  def test_constructor_2(self):
    price = Price.fromAmounts(
      CurrencyAmount.fromRawAmount(TestPrice.t0_18, 1),
      CurrencyAmount.fromRawAmount(TestPrice.t2_18, 54321)
    )
    self.assertEqual(price.toFixed(5), '54321')
    self.assertTrue(price.baseCurrency.equals(TestPrice.t0_18))
    self.assertTrue(price.quoteCurrency.equals(TestPrice.t2_18))

  def test_returnsCorrectValue(self):
    price = Price(TestPrice.t0_18, TestPrice.t2_18, 1, 5)
    self.assertEqual(
      price.quote(CurrencyAmount.fromRawAmount(TestPrice.t0_18, 10)),
      CurrencyAmount.fromRawAmount(TestPrice.t2_18, 50)
    )
    
  def test_noDecimals(self):
      p = Price(TestPrice.t0_18, TestPrice.t2_18, 123, 456)
      self.assertEqual(p.toFixed(3), '3.707')
    
  def test_noDecimalsFlipRatio(self):
      p = Price(TestPrice.t0_18, TestPrice.t2_18, 456, 123)
      self.assertEqual(p.toFixed(4), '0.2697')
    
  def test_withDecimalDifference(self):
      p = Price(TestPrice.t1_6, TestPrice.t2_18, 123, 456)
      self.assertEqual(p.toFixed(15), '0.000000000003707')
    
  def test_withDecimalDifferenceAgain(self):
      p = Price(
        TestPrice.t1_6,
        TestPrice.t2_18,
        10 ** 6, 
        10 ** 18
      )
      self.assertEqual(p.toFixed(4), '1')
    
  def test_withDecimalDifferenceFlipped(self):
      p = Price(TestPrice.t1_6, TestPrice.t2_18, 456, 123)
      self.assertEqual(p.toFixed(16), '0.0000000000002697')
    
  def test_withDecimalDifferenceFlippedBaseQuoteFlipped(self):
      p = Price(TestPrice.t2_18, TestPrice.t1_6, 456, 123)
      self.assertEqual(p.toFixed(5), '269736842105.26316')
    

if __name__ == '__main__':
    unittest.main()