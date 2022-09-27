
from convexus.sdkcore.constants import Rounding
from convexus.sdkcore.entities.fractions.fraction import Fraction
from convexus.icontoolkit.constants import BigintIsh

ONE_HUNDRED = Fraction(100)

def toPercent(fraction: Fraction) -> 'Percent':
  """
  * Converts a fraction to a percent
  * @param fraction the fraction to convert
  """
  return Percent(fraction.numerator, fraction.denominator)


class Percent(Fraction):

  def __init__(self, numerator: int, denominator: int = 1):
    super().__init__(numerator, denominator)
    """ This boolean prevents a fraction from being interpreted as a Percent"""
    self.isPercent = True
  
  def __repr__(self) -> str:
    return str(self.__dict__)

  def add(self, other: Fraction | BigintIsh) -> 'Percent':
    return toPercent(super().add(other))

  def subtract(self, other: Fraction | BigintIsh) -> 'Percent':
    return toPercent(super().subtract(other))

  def multiply(self, other: Fraction | BigintIsh) -> 'Percent':
    return toPercent(super().multiply(other))

  def divide(self, other: Fraction | BigintIsh) -> 'Percent':
    return toPercent(super().divide(other))

  def toFixed(self, decimalPlaces: int = 2, rounding: Rounding = Rounding.ROUND_HALF_UP) -> str:
    return super().multiply(ONE_HUNDRED).toFixed(decimalPlaces, rounding)