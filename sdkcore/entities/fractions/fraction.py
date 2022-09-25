from typing import Union
from icontoolkit.BigInt import BigInt
from icontoolkit.constants import BigintIsh
from sdkcore.constants import Rounding
from decimal import Decimal, getcontext, ROUND_DOWN, ROUND_HALF_UP, ROUND_UP

toSignificantRounding = {
  Rounding.ROUND_DOWN: ROUND_DOWN,
  Rounding.ROUND_HALF_UP: ROUND_HALF_UP,
  Rounding.ROUND_UP: ROUND_UP
}

toFixedRounding = {
  Rounding.ROUND_DOWN: ROUND_DOWN,
  Rounding.ROUND_HALF_UP: ROUND_HALF_UP,
  Rounding.ROUND_UP: ROUND_UP
}

class Fraction:

  def __init__(self, numerator: int, denominator: int = 1):
    self.numerator = numerator
    self.denominator = denominator

  def __eq__(self, __o) -> bool:
    return self.numerator == __o.numerator and self.denominator == __o.denominator

  @staticmethod
  def tryParseFraction (fractionish: Union[BigintIsh, 'Fraction']) -> 'Fraction':
    if isinstance(fractionish, Fraction):
      return fractionish
    return Fraction(BigInt(fractionish))

  @property
  def quotient (self) -> int:
    """ performs floor division """
    return self.numerator // self.denominator
  
  @property
  def remainder (self) -> 'Fraction':
    """ remainder after floor division """
    return Fraction((self.numerator % self.denominator), self.denominator)
  
  def invert(self) -> 'Fraction':
    return Fraction(self.denominator, self.numerator)

  def add (self, other: Union[BigintIsh, 'Fraction']) -> 'Fraction':
    otherParsed = Fraction.tryParseFraction(other)

    if self.denominator == otherParsed.denominator:
      return Fraction(self.numerator + otherParsed.numerator, self.denominator)
    
    return Fraction (
        (self.numerator * otherParsed.denominator)
      + (otherParsed.numerator * self.denominator),
        self.denominator * otherParsed.denominator
    )

  def subtract(self, other: Union[BigintIsh, 'Fraction']) -> 'Fraction':
    otherParsed = Fraction.tryParseFraction(other)

    if (self.denominator == otherParsed.denominator):
      return Fraction (self.numerator - otherParsed.numerator, self.denominator)

    return Fraction (
          (self.numerator * otherParsed.denominator)
        - (otherParsed.numerator * self.denominator)
      ,
      (self.denominator * otherParsed.denominator)
    )

  def lessThan(self, other: Union[BigintIsh, 'Fraction']) -> bool:
    otherParsed = Fraction.tryParseFraction(other)
    return (self.numerator * otherParsed.denominator) < (otherParsed.numerator * self.denominator)

  def equalTo(self, other: Union[BigintIsh, 'Fraction']) -> bool:
    otherParsed = Fraction.tryParseFraction(other)
    return (self.numerator * otherParsed.denominator) == (otherParsed.numerator * self.denominator)

  def greaterThan(self, other: Union[BigintIsh, 'Fraction']) -> bool:
    otherParsed = Fraction.tryParseFraction(other)
    return (self.numerator * otherParsed.denominator) > (otherParsed.numerator * self.denominator)

  def multiply(self, other: Union[BigintIsh, 'Fraction']) -> 'Fraction':
    otherParsed = Fraction.tryParseFraction(other)
    return Fraction (self.numerator * otherParsed.numerator, self.denominator * otherParsed.denominator)

  def divide(self, other: Union[BigintIsh, 'Fraction']) -> 'Fraction':
    otherParsed = Fraction.tryParseFraction(other)
    return Fraction (self.numerator * otherParsed.denominator, self.denominator * otherParsed.numerator)

  def toFixed(self, decimalPlaces: int, rounding: Rounding = Rounding.ROUND_HALF_UP) -> str:
    assert decimalPlaces >= 0, f"{decimalPlaces} is negative."
    getcontext().prec = decimalPlaces + 1
    getcontext().rounding = toFixedRounding[rounding]
    return str(Decimal(self.numerator) / Decimal(self.denominator))

  @property
  def asFraction(self) -> 'Fraction':
    """
    * Helper method for converting any super class back to a fraction
    """
    return Fraction(self.numerator, self.denominator)