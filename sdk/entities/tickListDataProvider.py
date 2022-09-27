from typing import List
from icontoolkit.constants import BigintIsh
from sdk.utils.tickList import TickList
from sdk.entities.tick import Tick, TickConstructorArgs
from sdk.entities.tickDataProvider import TickDataProvider

class TickListDataProvider(TickDataProvider):
  """
  * A data provider for ticks that is backed by an in-memory array of ticks.
  """

  def __init__(self, ticks: List[Tick | TickConstructorArgs], tickSpacing: int) -> None:
    super().__init__()
    ticksMapped: List[Tick] = list(map(lambda t: (t if isinstance(t, Tick) else Tick(t)), ticks))
    TickList.validateList(ticksMapped, tickSpacing)
    self.ticks = ticksMapped

  def __repr__(self) -> str:
    return str(self.__dict__)

  def getTick(self, tick: int):
    return TickList.getTick(self.ticks, tick)

  def nextInitializedTickWithinOneWord(self, tick: int, lte: bool, tickSpacing: int):
    return TickList.nextInitializedTickWithinOneWord(self.ticks, tick, lte, tickSpacing)
