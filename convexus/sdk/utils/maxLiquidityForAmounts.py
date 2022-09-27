from convexus.sdk.internalConstants import Q96


def maxLiquidityForAmount0Imprecise(sqrtRatioAX96: int, sqrtRatioBX96: int, amount0: int) -> int:
  """
  * Returns an imprecise maximum amount of liquidity received for a given amount of token 0.
  * This function is available to accommodate LiquidityAmounts#getLiquidityForAmount0 in the Convexus periphery,
  * which could be more precise by at least 32 bits by dividing by Q64 instead of Q96 in the intermediate step,
  * and shifting the subtracted ratio left by 32 bits. This imprecise calculation will likely be replaced in a future
  * router contract.
  * @param sqrtRatioAX96 The price at the lower boundary
  * @param sqrtRatioBX96 The price at the upper boundary
  * @param amount0 The token0 amount
  * @returns liquidity for amount0, imprecise
  """
  if sqrtRatioAX96 > sqrtRatioBX96:
    sqrtRatioAX96, sqrtRatioBX96 = sqrtRatioBX96, sqrtRatioAX96

  intermediate = sqrtRatioAX96 * sqrtRatioBX96 // Q96
  return (amount0 * intermediate) // (sqrtRatioBX96 - sqrtRatioAX96)

def maxLiquidityForAmount0Precise (sqrtRatioAX96: int, sqrtRatioBX96: int, amount0: int) -> int:
  """
  * Returns a precise maximum amount of liquidity received for a given amount of token 0 by dividing by Q64 instead of Q96 in the intermediate step,
  * and shifting the subtracted ratio left by 32 bits.
  * @param sqrtRatioAX96 The price at the lower boundary
  * @param sqrtRatioBX96 The price at the upper boundary
  * @param amount0 The token0 amount
  * @returns liquidity for amount0, precise
  """
  if sqrtRatioAX96 > sqrtRatioBX96:
    sqrtRatioAX96, sqrtRatioBX96 = sqrtRatioBX96, sqrtRatioAX96

  numerator = amount0 * sqrtRatioAX96 * sqrtRatioBX96
  denominator = Q96 * (sqrtRatioBX96 - sqrtRatioAX96)

  return numerator // denominator

def maxLiquidityForAmount1 (sqrtRatioAX96: int, sqrtRatioBX96: int, amount1: int) -> int:
  """
  * Computes the maximum amount of liquidity received for a given amount of token1
  * @param sqrtRatioAX96 The price at the lower tick boundary
  * @param sqrtRatioBX96 The price at the upper tick boundary
  * @param amount1 The token1 amount
  * @returns liquidity for amount1
  """
  if sqrtRatioAX96 > sqrtRatioBX96:
    sqrtRatioAX96, sqrtRatioBX96 = sqrtRatioBX96, sqrtRatioAX96

  return (amount1 * Q96) // (sqrtRatioBX96 - sqrtRatioAX96)

def maxLiquidityForAmounts (
  sqrtRatioCurrentX96: int,
  sqrtRatioAX96: int,
  sqrtRatioBX96: int,
  amount0: int,
  amount1: int,
  useFullPrecision: bool
) -> int:
  """
  * Computes the maximum amount of liquidity received for a given amount of token0, token1,
  * and the prices at the tick boundaries.
  * @param sqrtRatioCurrentX96 the current price
  * @param sqrtRatioAX96 price at lower boundary
  * @param sqrtRatioBX96 price at upper boundary
  * @param amount0 token0 amount
  * @param amount1 token1 amount
  * @param useFullPrecision if false, liquidity will be maximized according to what the router can calculate,
  * not what core can theoretically support
  """
  if sqrtRatioAX96 > sqrtRatioBX96:
    sqrtRatioAX96, sqrtRatioBX96 = sqrtRatioBX96, sqrtRatioAX96

  maxLiquidityForAmount0 = maxLiquidityForAmount0Precise if useFullPrecision else maxLiquidityForAmount0Imprecise

  if sqrtRatioCurrentX96 <= sqrtRatioAX96:
    return maxLiquidityForAmount0(sqrtRatioAX96, sqrtRatioBX96, amount0)
  elif sqrtRatioCurrentX96 < sqrtRatioBX96:
    liquidity0 = maxLiquidityForAmount0(sqrtRatioCurrentX96, sqrtRatioBX96, amount0)
    liquidity1 = maxLiquidityForAmount1(sqrtRatioAX96, sqrtRatioCurrentX96, amount1)
    return liquidity0 if liquidity0 < liquidity1 else liquidity1
  else:
    return maxLiquidityForAmount1(sqrtRatioAX96, sqrtRatioBX96, amount1)
