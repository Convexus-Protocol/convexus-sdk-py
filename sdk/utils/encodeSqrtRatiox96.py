import math

def encodeSqrtRatiox96(amount1: int, amount0: int) -> int:
  """
  * Returns the sqrt ratio as a Q64.96 corresponding to a given ratio of amount1 and amount0
  * @param amount1 The numerator amount i.e., the amount of token1
  * @param amount0 The denominator amount i.e., the amount of token0
  * @returns The sqrt ratio
  """
  numerator = amount1 << 192
  ratioX192 = numerator // amount0
  return int(math.sqrt(ratioX192))
