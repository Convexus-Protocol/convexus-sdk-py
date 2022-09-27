from typing import Union
from convexus.icontoolkit.BigInt import BigInt
from convexus.icontoolkit.constants import BigintIsh
from convexus.sdkcore.constants import Rounding
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

  def __init__(self, numerator: BigintIsh, denominator: BigintIsh = 1):
    self.numerator = BigInt(numerator)
    self.denominator = BigInt(denominator)

  def __eq__(self, __o) -> bool:
    return __o is not None and self.equalTo(__o)

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
    getcontext().prec = 256
    getcontext().rounding = toFixedRounding[rounding]
    d = Decimal(self.numerator) / Decimal(self.denominator)
    formatted = ("{:." + str(decimalPlaces) + "f}").format(d)

    # Remove trailing zeroes
    numbers = formatted.split('.')
    if len(numbers) == 1:
      return formatted

    rnumbers = numbers[1].rstrip("0")
    if len(rnumbers) == 0:
      return numbers[0]

    return numbers[0] + '.' + rnumbers

  @property
  def asFraction(self) -> 'Fraction':
    """
    * Helper method for converting any super class back to a fraction
    """
    return Fraction(self.numerator, self.denominator)