from convexus.sdkcore.constants import MaxUint256

POWERS_OF_2 = list(map(lambda pow: [pow, 2**pow], [128, 64, 32, 16, 8, 4, 2, 1]))

def mostSignificantBit(x: int) -> int:
  assert x > 0, 'ZERO'
  assert x <= MaxUint256, 'MAX'

  msb: int = 0
  for power, min in POWERS_OF_2:
    if (x >= min):
      x = x >> power
      msb += power

  return msb