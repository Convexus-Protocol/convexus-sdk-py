from abc import ABCMeta

class LiquidityMath(metaclass=ABCMeta):

  @staticmethod
  def addDelta(x: int, y: int) -> int:
    if (y < 0):
      return x - (y * -1)
    else:
      return x + y
