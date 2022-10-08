from dataclasses import dataclass
from typing import Any, Dict, List
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
  

class QuoteMultiResult:
  amountOut: int
  sqrtPriceX96AfterList: List[int]
  initializedTicksCrossedList: List[int]
  
  def __init__(
    self, 
    amountOut: BigintIsh, 
    sqrtPriceX96AfterList: List[BigintIsh], 
    initializedTicksCrossedList: List[int]
  ) -> None:
    self.amountOut = BigInt(amountOut)
    self.sqrtPriceX96AfterList = list(map(BigInt, sqrtPriceX96AfterList))
    self.initializedTicksCrossedList = initializedTicksCrossedList

  @staticmethod
  def fromCall (data: Dict[str, Any]) -> 'QuoteMultiResult':
    return QuoteMultiResult (
      data['amountOut'],
      data['sqrtPriceX96AfterList'],
      list(map(lambda i: int(i, 0), data['initializedTicksCrossedList']))
    )

  def __repr__(self) -> str:
    return str(self.__dict__)

  def __iter__(self):
    yield self.amountOut
    yield self.sqrtPriceX96AfterList
    yield self.initializedTicksCrossedList
  