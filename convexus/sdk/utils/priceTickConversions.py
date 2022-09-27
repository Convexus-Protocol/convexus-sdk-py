from convexus.sdkcore.entities.currency import Token
from convexus.sdkcore.entities.fractions.price import Price
from convexus.sdk.utils.encodeSqrtRatioX96 import encodeSqrtRatioX96
from convexus.sdk.utils.tickMath import TickMath
from convexus.sdk.internalConstants import Q192
from typing import cast


def tickToPrice(baseToken: Token, quoteToken: Token, tick: int) -> Price:
  """
  * Returns a price object corresponding to the input tick and the base/quote token
  * Inputs must be tokens because the address order is used to interpret the price represented by the tick
  * @param baseToken the base token of the price
  * @param quoteToken the quote token of the price
  * @param tick the tick for which to return the price
  """
  sqrtRatioX96 = TickMath.getSqrtRatioAtTick(tick)
  ratioX192 = sqrtRatioX96**2

  return Price(baseToken, quoteToken, Q192, ratioX192) if baseToken.sortsBefore(quoteToken) else Price(baseToken, quoteToken, ratioX192, Q192)


def priceToClosestTick(price: Price) -> int:
  """
  * Returns the first tick for which the given price is greater than or equal to the tick price
  * @param price for which to return the closest tick that represents a price less than or equal to the input price,
  * i.e. the price of the returned tick is less than or equal to the input price
  """
  baseToken = cast(Token, price.baseCurrency)
  quoteToken = cast(Token, price.quoteCurrency)

  sorted = baseToken.sortsBefore(quoteToken)
  sqrtRatioX96 = encodeSqrtRatioX96(price.numerator, price.denominator) if sorted else encodeSqrtRatioX96(price.denominator, price.numerator)

  tick = TickMath.getTickAtSqrtRatio(sqrtRatioX96)
  nextTickPrice = tickToPrice(baseToken, quoteToken, tick + 1)
  if (sorted):
    if (not price.lessThan(nextTickPrice)):
      tick += 1
  else:
    if (not price.greaterThan(nextTickPrice)):
      tick += 1
  
  return tick

