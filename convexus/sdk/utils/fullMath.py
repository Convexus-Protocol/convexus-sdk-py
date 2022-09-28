from abc import ABCMeta

class FullMath(metaclass=ABCMeta):

  @staticmethod
  def mulDivRoundingUp(a: int, b: int, denominator: int) -> int:
    product = a * b
    result = product // denominator

    if (product % denominator != 0):
      result = result + 1
    
    return result
