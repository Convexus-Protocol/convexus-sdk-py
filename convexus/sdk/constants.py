from enum import IntEnum
from typing import Dict
from convexus.icontoolkit.BigInt import BigInt

from convexus.icontoolkit.constants import BigintIsh

ADDRESS_ZERO = 'hx0000000000000000000000000000000000000000'

class FeeAmount(IntEnum):
  """
  * The default factory enabled fee amounts, denominated in hundredths of bips.
  """
  LOWEST = 100,
  LOW = 500,
  MEDIUM = 3000,
  HIGH = 10000

def parseFeeAmount (s: BigintIsh) -> FeeAmount:
  return FeeAmount(BigInt(s))

"""
* The default factory tick spacings by fee amount.
"""
TICK_SPACINGS: Dict[FeeAmount, int] = {
  FeeAmount.LOWEST: 1,
  FeeAmount.LOW: 10,
  FeeAmount.MEDIUM: 60,
  FeeAmount.HIGH: 200
}
