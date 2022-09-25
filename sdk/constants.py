from enum import Enum

ADDRESS_ZERO = 'hx0000000000000000000000000000000000000000'

"""
 * The default factory enabled fee amounts, denominated in hundredths of bips.
"""
class FeeAmount(Enum):
  LOWEST = 100,
  LOW = 500,
  MEDIUM = 3000,
  HIGH = 10000

"""
 * The default factory tick spacings by fee amount.
"""
TICK_SPACINGS = {
  FeeAmount.LOWEST: 1,
  FeeAmount.LOW: 10,
  FeeAmount.MEDIUM: 60,
  FeeAmount.HIGH: 200
}
