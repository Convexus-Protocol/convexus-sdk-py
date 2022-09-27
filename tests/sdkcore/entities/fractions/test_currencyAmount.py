import unittest

from convexus.sdkcore.entities.fractions.currencyAmount import CurrencyAmount
from convexus.sdkcore.entities.currency import Token
from convexus.sdkcore.entities.icx import Icx
from convexus.sdkcore.entities.fractions.percent import Percent
from convexus.sdkcore.constants import MaxUint256

ADDRESS_ONE = 'hx0000000000000000000000000000000000000001'

class TestCurrencyAmount(unittest.TestCase):
  
  def test_constructor(self):
    token = Token(ADDRESS_ONE, 18)
    amount = CurrencyAmount.fromRawAmount(token, 100)
    self.assertEqual(amount.quotient, 100)

  def test_quotient(self):
    token = Token(ADDRESS_ONE, 18)
    amount = CurrencyAmount.fromRawAmount(token, 100).multiply(Percent(15, 100))
    self.assertEqual(amount.quotient, 15)

  def test_icx(self):
    amount = CurrencyAmount.fromRawAmount(Icx(), 100)
    self.assertEqual(amount.quotient, 100)
    self.assertEqual(amount.currency, Icx())

  def test_canBeMaxUint256(self):
    amount = CurrencyAmount.fromRawAmount(Token(ADDRESS_ONE, 18), MaxUint256)
    self.assertEqual(amount.quotient, MaxUint256)

  def test_cannotExceedMaxUint256(self):
    with self.assertRaises(AssertionError) as cm:
      CurrencyAmount.fromRawAmount(Token(ADDRESS_ONE, 18), MaxUint256 + 1)
    self.assertEqual(str(cm.exception), "AMOUNT")

  def test_tokenAmountQuotientCannotExceedMaxUint256(self):
    with self.assertRaises(AssertionError) as cm:
      CurrencyAmount.fromFractionalAmount(
        Token(ADDRESS_ONE, 18),
        (MaxUint256 * 2) + 2,
        2
      )
    self.assertEqual(str(cm.exception), "AMOUNT")

  def test_tokenAmountNumeratorCanBeGtUint256IfDenominatorIsGt1(self):
    amount = CurrencyAmount.fromFractionalAmount(
      Token(ADDRESS_ONE, 18),
      MaxUint256 + 2,
      2
    )
    self.assertEqual(amount.numerator, 2 + MaxUint256)

  def test_throwsForDecimalsGtcurrencyDecimals(self):
    token = Token(ADDRESS_ONE, 0)
    amount = CurrencyAmount.fromRawAmount(token, 1000)
    with self.assertRaises(AssertionError) as cm:
      amount.toFixed(3)
    self.assertEqual(str(cm.exception), "DECIMALS")

  def test_isCorrectFor0Decimals_1(self):
    token = Token(ADDRESS_ONE, 0)
    amount = CurrencyAmount.fromRawAmount(token, 123456)
    self.assertEqual(amount.toFixed(0), '123456')

  def test_isCorrectFor18Decimals_1(self):
    token = Token(ADDRESS_ONE, 18)
    amount = CurrencyAmount.fromRawAmount(token, int(1e15))
    self.assertEqual(amount.toFixed(9), '0.001')

  def test_doesNotThrowForSigFigsGtCurrencyDecimals_0(self):
    token = Token(ADDRESS_ONE, 0)
    amount = CurrencyAmount.fromRawAmount(token, 1000)
    self.assertEqual(amount.toExact(), '1000')

  def test_isCorrectFor0Decimals_0(self):
    token = Token(ADDRESS_ONE, 0)
    amount = CurrencyAmount.fromRawAmount(token, 123456)
    self.assertEqual(amount.toExact(), '123456')

  def test_isCorrectFor18Decimals_0(self):
    token = Token(ADDRESS_ONE, 18)
    amount = CurrencyAmount.fromRawAmount(token, int(123e13))
    self.assertEqual(amount.toExact(), '0.00123')


if __name__ == '__main__':
    unittest.main()