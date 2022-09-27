from typing import Union
from convexus.icontoolkit.constants import BigintIsh
from convexus.sdkcore.entities.fractions.fraction import Fraction
from convexus.sdkcore.entities.currency import Currency
from convexus.sdkcore.constants import MaxUint256, Rounding

class CurrencyAmount(Fraction):

  @staticmethod
  def fromRawAmount(currency: Currency, rawAmount: BigintIsh) -> 'CurrencyAmount':
    """
    * Returns a new currency amount instance from the unitless amount of token, i.e. the raw amount
    * @param currency the currency in the amount
    * @param rawAmount the raw token or ICX amount
    """
    return CurrencyAmount(currency, rawAmount)

  @staticmethod
  def fromFractionalAmount(
    currency: Currency,
    numerator: BigintIsh,
    denominator: BigintIsh
  ) -> 'CurrencyAmount':
    return CurrencyAmount(currency, numerator, denominator)

  def __repr__(self) -> str:
    return str(self.__dict__)

  def __eq__(self, __o) -> bool:
    return super().__eq__(__o) and self.currency.equals(__o.currency) and self.decimalScale == __o.decimalScale

  def __init__(self, currency: Currency, numerator: BigintIsh, denominator: BigintIsh = 1):
    super().__init__(numerator, denominator)
    assert self.quotient <= MaxUint256, 'AMOUNT'
    self.currency: Currency = currency
    self.decimalScale: int = 10**currency.decimals

  def add(self, other: 'CurrencyAmount') -> 'CurrencyAmount': # type: ignore[override]
    assert self.currency.equals(other.currency), 'CURRENCY'
    added = super().add(other)
    return CurrencyAmount.fromFractionalAmount(self.currency, added.numerator, added.denominator)

  def subtract(self, other: 'CurrencyAmount') -> 'CurrencyAmount': # type: ignore[override]
    assert self.currency.equals(other.currency), 'CURRENCY'
    subtracted = super().subtract(other)
    return CurrencyAmount.fromFractionalAmount(self.currency, subtracted.numerator, subtracted.denominator)

  def multiply(self, other: Union[Fraction, BigintIsh]) -> 'CurrencyAmount':
    multiplied = super().multiply(other)
    return CurrencyAmount.fromFractionalAmount(self.currency, multiplied.numerator, multiplied.denominator)

  def divide(self, other: Union[Fraction, BigintIsh]) -> 'CurrencyAmount':
    divided = super().divide(other)
    return CurrencyAmount.fromFractionalAmount(self.currency, divided.numerator, divided.denominator)

  def toFixed(self, decimalPlaces: int = None, rounding: Rounding = Rounding.ROUND_HALF_UP) -> str:
    if decimalPlaces is None:
      decimalPlaces = self.currency.decimals

    assert decimalPlaces <= self.currency.decimals, 'DECIMALS'
    return super().divide(self.decimalScale).toFixed(decimalPlaces, rounding)

  def toExact(self) -> str:
    return self.toFixed(self.currency.decimals)

  @property
  def wrapped(self) -> 'CurrencyAmount':
    if (self.currency.isToken):
        return self

    return CurrencyAmount.fromFractionalAmount(self.currency.wrapped, self.numerator, self.denominator)

