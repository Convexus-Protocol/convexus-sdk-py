from convexus.icontoolkit.constants import BigintIsh
from convexus.sdkcore.constants import Rounding
from convexus.sdkcore.entities.currency import Currency
from convexus.sdkcore.entities.fractions.fraction import Fraction
from convexus.sdkcore.entities.fractions.currencyAmount import CurrencyAmount

class Price(Fraction):
  def __init__(self, baseCurrency: Currency, quoteCurrency: Currency, denominator: BigintIsh, numerator: BigintIsh):
    super().__init__(numerator, denominator)
    # input i.e. denominator
    self.baseCurrency = baseCurrency
    # output i.e. numerator
    self.quoteCurrency = quoteCurrency
    # used to adjust the raw fraction w/r/t the decimals of the {base,quote}Token
    self.scalar = Fraction(10 ** baseCurrency.decimals, 10 ** quoteCurrency.decimals)

  @classmethod
  def fromSqrtPrice(cls, baseCurrency: Currency, quoteCurrency: Currency, sqrtPrice: BigintIsh) -> 'Price':
    return Price(baseCurrency, quoteCurrency, 2**192, sqrtPrice**2)

  @classmethod
  def fromAmounts(cls, baseAmount: CurrencyAmount, quoteAmount: CurrencyAmount) -> 'Price':
    result = quoteAmount.divide(baseAmount)
    return cls(baseAmount.currency, quoteAmount.currency, result.denominator, result.numerator)

  def invert(self) -> 'Price':
    """
    * Flip the price, switching the base and quote currency
    """
    return Price(self.quoteCurrency, self.baseCurrency, self.numerator, self.denominator)

  def multiply(self, other: 'Price') -> 'Price': # type: ignore[override]
    """
    * Multiply the price by another price, returning a price. The other price must have the same base currency as this price's quote currency
    * @param other the other price
    """
    assert self.quoteCurrency.equals(other.baseCurrency), 'TOKEN'
    fraction = super().multiply(other)
    return Price(self.baseCurrency, other.quoteCurrency, fraction.denominator, fraction.numerator)

  def quote(self, currencyAmount: CurrencyAmount) -> CurrencyAmount:
    """
    * Return the amount of quote currency corresponding to a given amount of the base currency
    * @param currencyAmount the amount of base currency to quote against the price
    """
    assert currencyAmount.currency.equals(self.baseCurrency), 'TOKEN'
    result = super().multiply(currencyAmount)
    return CurrencyAmount.fromFractionalAmount(self.quoteCurrency, result.numerator, result.denominator)

  @property
  def adjustedForDecimals(self) -> Fraction:
    """
    * Get the value scaled by decimals for formatting
    * @private
    """
    return super().multiply(self.scalar)

  def toSignificant(self, decimalPlaces: int = 4, rounding: Rounding = Rounding.ROUND_HALF_UP) -> str:
    return self.toFixed(decimalPlaces, rounding)

  def toFixed(self, decimalPlaces: int = 4, rounding: Rounding = Rounding.ROUND_HALF_UP) -> str:
    return self.adjustedForDecimals.toFixed(decimalPlaces, rounding)
