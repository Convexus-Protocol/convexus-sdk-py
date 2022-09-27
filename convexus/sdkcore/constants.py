from enum import Enum

class TradeType(Enum):
  EXACT_INPUT = 0
  EXACT_OUTPUT = 1

class Rounding(Enum):
  ROUND_DOWN = 0
  ROUND_HALF_UP = 1
  ROUND_UP = 2

MaxUint256 = (2**256)-1
