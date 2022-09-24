def decodeSqrtRatioX96(sqrtRatiox96: int) -> float:
  """
  * Returns a floating point price from a sqrt ratio as a Q64.96
  * @param sqrtRatiox96 The sqrt ratio
  * @returns A floating point price
  """
  return sqrtRatiox96**2 / 2**192
