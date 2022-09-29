from abc import ABCMeta, abstractmethod
from typing import Tuple

class TickDataProvider(metaclass=ABCMeta):
  """
  * Provides information about ticks
  """

  @abstractmethod
  def getTick(self, tick: int):
    """
    * Return information corresponding to a specific tick
    * @param tick the tick to load
    * @returns Must return an object with a `liquidityNet` field
    """
    pass

  @abstractmethod
  def nextInitializedTickWithinOneWord(self, tick: int, lte: bool, tickSpacing: int) -> Tuple[int, bool]:
    """
    * Return the next tick that is initialized within a single word
    * @param tick The current tick
    * @param lte Whether the next tick should be lte the current tick
    * @param tickSpacing The tick spacing of the pool
    """
    pass

class NoTickDataProvider(TickDataProvider):
  """
  * This tick data provider does not know how to fetch any tick data. 
  * It throws whenever it is required. Useful if you
  * do not need to load tick data for your use case.
  """

  ERROR_MESSAGE = 'No tick data provider was given'
  
  def getTick(self, _tick: int):
    raise Exception(NoTickDataProvider.ERROR_MESSAGE)

  def nextInitializedTickWithinOneWord(
    self,
    _tick: int,
    _lte: bool,
    _tickSpacing: int
  ):
    raise Exception(NoTickDataProvider.ERROR_MESSAGE)
