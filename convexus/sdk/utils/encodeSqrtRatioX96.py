import math
from convexus.icontoolkit.BigInt import BigInt

from convexus.icontoolkit.constants import BigintIsh

def encodeSqrtRatioX96(amount1: BigintIsh, amount0: BigintIsh) -> int:
  """
  * Returns the sqrt ratio as a Q64.96 corresponding to a given ratio of amount1 and amount0
  * @param amount1 The numerator amount i.e., the amount of token1
  * @param amount0 The denominator amount i.e., the amount of token0
  * @returns The sqrt ratio
  """
  amount0 = BigInt(amount0)
  amount1 = BigInt(amount1)

  numerator = amount1 << 192
  ratioX192 = numerator // amount0
  return int(math.sqrt(ratioX192))
