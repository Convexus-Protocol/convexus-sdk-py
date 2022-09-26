import unittest
from icontoolkit.test.expect import expect

from sdkcore.entities.currency import Token
from sdkcore.entities.fractions.currencyAmount import CurrencyAmount
from sdkcore.entities.fractions.percent import Percent
from sdkcore.entities.fractions.price import Price
from sdkcore.entities.icx import Icx
from sdkcore.utils.computePriceImpact import computePriceImpact

ADDRESS_ZERO = 'hx0000000000000000000000000000000000000000'
ADDRESS_ONE = 'hx0000000000000000000000000000000000000001'

t0 = Token(ADDRESS_ZERO, 18)
t1 = Token(ADDRESS_ONE, 18)

class TestComputePriceImpact(unittest.TestCase):

  def test_isCorrectForZero(self):
    expect(
      computePriceImpact(
        Price(Icx(), t0, 10, 100),
        CurrencyAmount.fromRawAmount(Icx(), 10),
        CurrencyAmount.fromRawAmount(t0, 100)
      )
    ).toEqual(Percent(0, 10000))

  def test_isCorrectForHalfOutput(self):
    expect(
      computePriceImpact(
        Price(t0, t1, 10, 100),
        CurrencyAmount.fromRawAmount(t0, 10),
        CurrencyAmount.fromRawAmount(t1, 50)
      )
    ).toEqual(Percent(5000, 10000))

  def test_isNegativeForMoreOutput(self):
    expect(
      computePriceImpact(
        Price(t0, t1, 10, 100),
        CurrencyAmount.fromRawAmount(t0, 10),
        CurrencyAmount.fromRawAmount(t1, 200)
      )
    ).toEqual(Percent(-10000, 10000))
