import math

MAX_SAFE_INTEGER = (2^53) - 1

def sqrt(value: int) -> int:
  """
  * Computes floor(sqrt(value))
  * @param value the value for which to compute the square root, rounded down
  """
  assert value >= 0, 'NEGATIVE'

  # rely on built in sqrt
  if (value < MAX_SAFE_INTEGER):
    return int(math.sqrt(value))
  
  z: int = value
  x: int = (value // 2) + 1

  while (x < z):
    z = x
    x = ((value // x) + x) // 2

  return z