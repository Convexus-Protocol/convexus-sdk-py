from dataclasses import dataclass
from typing import Any, Dict
from convexus.icontoolkit.BigInt import BigInt
from convexus.icontoolkit.constants import BigintIsh

@dataclass
class NextInitializedTickWithinOneWordResult:
  tickNext: int
  initialized: bool

  @staticmethod
  def fromCall (data: Dict[str, Any]) -> 'NextInitializedTickWithinOneWordResult':
    return NextInitializedTickWithinOneWordResult (
      int(data['tickNext'], 0),
      bool(int(data['initialized'], 0))
    )

  def __repr__(self) -> str:
    return str(self.__dict__)

  def __iter__(self):
    yield self.tickNext
    yield self.initialized


class QuoteResult:
  amountOut: int
  sqrtPriceX96After: int
  initializedTicksCrossed: int
  
  def __init__(self, amountOut: BigintIsh, sqrtPriceX96After: BigintIsh, initializedTicksCrossed: int) -> None:
    self.amountOut = BigInt(amountOut)
    self.sqrtPriceX96After = BigInt(sqrtPriceX96After)
    self.initializedTicksCrossed = initializedTicksCrossed

  @staticmethod
  def fromCall (data: Dict[str, Any]) -> 'QuoteResult':
    return QuoteResult (
      data['amountOut'],
      data['sqrtPriceX96After'],
      int(data['initializedTicksCrossed'], 0)
    )

  def __repr__(self) -> str:
    return str(self.__dict__)

  def __iter__(self):
    yield self.amountOut
    yield self.sqrtPriceX96After
    yield self.initializedTicksCrossed
  