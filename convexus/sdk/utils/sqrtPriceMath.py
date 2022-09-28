from abc import ABCMeta

from convexus.sdkcore.constants import MaxUint256
from convexus.sdk.utils.fullMath import FullMath
from convexus.sdk.internalConstants import Q96

MaxUint160 = 2**160 - 1

def multiplyIn256(x: int, y: int) -> int:
  product = x * y
  return product & MaxUint256

def addIn256(x: int, y: int) -> int:
  sum = x + y
  return sum & MaxUint256


class SqrtPriceMath(metaclass=ABCMeta):

  @staticmethod
  def getAmount0Delta(sqrtRatioAX96: int, sqrtRatioBX96: int, liquidity: int, roundUp: bool) -> int:
    if sqrtRatioAX96 > sqrtRatioBX96:
      sqrtRatioAX96, sqrtRatioBX96 = sqrtRatioBX96, sqrtRatioAX96
    
    numerator1 = liquidity << 96
    numerator2 = sqrtRatioBX96 - sqrtRatioAX96

    a = FullMath.mulDivRoundingUp(FullMath.mulDivRoundingUp(numerator1, numerator2, sqrtRatioBX96), 1, sqrtRatioAX96)
    b = numerator1 * numerator2 // sqrtRatioBX96 // sqrtRatioAX96

    return a if roundUp else b

  @staticmethod
  def getAmount1Delta(sqrtRatioAX96: int, sqrtRatioBX96: int, liquidity: int, roundUp: bool) -> int:
    if sqrtRatioAX96 > sqrtRatioBX96:
      sqrtRatioAX96, sqrtRatioBX96 = sqrtRatioBX96, sqrtRatioAX96

    a = FullMath.mulDivRoundingUp(liquidity, (sqrtRatioBX96 - sqrtRatioAX96), Q96)
    b = liquidity * (sqrtRatioBX96 - sqrtRatioAX96) // Q96

    return a if roundUp else b

  @staticmethod
  def getNextSqrtPriceFromInput(sqrtPX96: int, liquidity: int, amountIn: int, zeroForOne: bool) -> int:
    assert sqrtPX96 > 0
    assert liquidity > 0

    a = SqrtPriceMath.getNextSqrtPriceFromAmount0RoundingUp(sqrtPX96, liquidity, amountIn, True)
    b = SqrtPriceMath.getNextSqrtPriceFromAmount1RoundingDown(sqrtPX96, liquidity, amountIn, True)

    return a if zeroForOne else b

  @staticmethod
  def getNextSqrtPriceFromOutput(
    sqrtPX96: int,
    liquidity: int,
    amountOut: int,
    zeroForOne: bool
  ) -> int:
    assert sqrtPX96 > 0
    assert liquidity > 0

    a = SqrtPriceMath.getNextSqrtPriceFromAmount1RoundingDown(sqrtPX96, liquidity, amountOut, False)
    b = SqrtPriceMath.getNextSqrtPriceFromAmount0RoundingUp(sqrtPX96, liquidity, amountOut, False)

    return a if zeroForOne else b

  @staticmethod
  def getNextSqrtPriceFromAmount0RoundingUp(
    sqrtPX96: int,
    liquidity: int,
    amount: int,
    add: bool
  ) -> int:
    if (amount == 0):
      return sqrtPX96

    numerator1 = liquidity << 96

    if (add):
      product = multiplyIn256(amount, sqrtPX96)
      if ((product // amount) == sqrtPX96):
        denominator = addIn256(numerator1, product)
        if (denominator >= numerator1):
          return FullMath.mulDivRoundingUp(numerator1, sqrtPX96, denominator)

      return FullMath.mulDivRoundingUp(numerator1, 1, (numerator1 // sqrtPX96) + amount)
    
    else:
      product = multiplyIn256(amount, sqrtPX96)
      assert (product // amount) == sqrtPX96
      assert numerator1 > product
      denominator = numerator1 - product
      return FullMath.mulDivRoundingUp(numerator1, sqrtPX96, denominator)
  
  @staticmethod
  def getNextSqrtPriceFromAmount1RoundingDown(
    sqrtPX96: int,
    liquidity: int,
    amount: int,
    add: bool
  ) -> int:
    if add:
      a = (amount << 96) // liquidity
      b = (amount * Q96) // liquidity
      quotient = a if (amount <= MaxUint160) else b
      return sqrtPX96 + quotient
    else:
      quotient = FullMath.mulDivRoundingUp(amount, Q96, liquidity)
      assert sqrtPX96 > quotient
      return sqrtPX96 - quotient