import unittest

from sdkcore.entities.currency import Token

ADDRESS_ONE = 'hx0000000000000000000000000000000000000001'
ADDRESS_TWO = 'hx0000000000000000000000000000000000000002'

class TestToken(unittest.TestCase):

  def test_failsWithInvalidAddress(self):
    with self.assertRaises(Exception) as cm:
      Token('hxhello00000000000000000000000000000000002', 18).address

    self.assertEqual(str(cm.exception), 'hxhello00000000000000000000000000000000002 is not a valid address')

  def test_failsWithNegativeDecimals(self):
    with self.assertRaises(AssertionError) as cm:
      Token(ADDRESS_ONE, -1)
    self.assertEqual(str(cm.exception), 'DECIMALS')

  def test_failsWith256Decimals(self):
    with self.assertRaises(AssertionError) as cm:
      Token(ADDRESS_ONE, 256)
    self.assertEqual(str(cm.exception), 'DECIMALS')

  def test_failsWithNonIntegerDecimals(self):
    with self.assertRaises(AssertionError) as cm:
      Token(ADDRESS_ONE, 1.5)
    self.assertEqual(str(cm.exception), 'DECIMALS')

  def test_failsIfAddressDiffers(self):
    self.assertFalse(
              Token(ADDRESS_ONE, 18)
      .equals(Token(ADDRESS_TWO, 18))
    )

  def test_trueIfOnlyDecimalsDiffers(self):
    self.assertTrue(
              Token(ADDRESS_ONE, 9)
      .equals(Token(ADDRESS_ONE, 18)))

  def test_trueIfAddressIsTheSame(self):
    self.assertTrue(
              Token(ADDRESS_ONE, 18)
      .equals(Token(ADDRESS_ONE, 18)))

  def test_trueOnReferenceEquality(self):
    token = Token(ADDRESS_ONE, 18)
    self.assertTrue(token.equals(token))

  def test_trueEvenIfNameSymbolDecimalsDiffer(self):
    tokenA = Token(ADDRESS_ONE, 9, 'abc', 'def')
    tokenB = Token(ADDRESS_ONE, 18, 'ghi', 'jkl')
    self.assertTrue(tokenA.equals(tokenB))
