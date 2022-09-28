from math import floor
from typing import List, Tuple
from convexus.sdk.entities.tick import Tick
from functools import reduce

from convexus.sdk.utils.isSorted import isSorted

def tickComparator(a: Tick, b: Tick):
  return a.index - b.index


class TickList:
  """
  * Utility methods for interacting with sorted lists of ticks
  """

  @staticmethod
  def validateList(ticks: List[Tick], tickSpacing: int):
    assert tickSpacing > 0, 'TICK_SPACING_NONZERO'
    # ensure ticks are spaced appropriately
    assert all(map(lambda t: t.index % tickSpacing == 0, ticks)), "TICK_SPACING"

    # ensure tick liquidity deltas sum to 0
    assert reduce(lambda accumulator, tick: accumulator + tick.liquidityNet, ticks, 0) == 0, 'ZERO_NET'

    assert isSorted(ticks, tickComparator), 'SORTED'

  @staticmethod
  def isBelowSmallest (ticks: List[Tick], tick: int) -> bool:
    assert len(ticks) > 0, 'LENGTH'
    return tick < ticks[0].index

  @staticmethod
  def isAtOrAboveLargest(ticks: List[Tick], tick: int) -> bool:
    assert len(ticks) > 0, 'LENGTH'
    return tick >= ticks[len(ticks) - 1].index

  @staticmethod
  def getTick(ticks: List[Tick], index: int) -> Tick:
    tick = ticks[TickList.binarySearch(ticks, index)]
    assert tick.index == index, 'NOT_CONTAINED'
    return tick

  @staticmethod
  def binarySearch (ticks: List[Tick], tick: int) -> int:
    """
    * Finds the largest tick in the list of ticks that is less than or equal to tick
    * @param ticks list of ticks
    * @param tick tick to find the largest tick that is less than or equal to tick
    * @private
    """
    assert not TickList.isBelowSmallest(ticks, tick), 'BELOW_SMALLEST'

    l = 0
    r = len(ticks) - 1
    while (True):
      i = floor((l + r) / 2)

      if (ticks[i].index <= tick and (i == len(ticks) - 1 or ticks[i + 1].index > tick)):
        return i

      if (ticks[i].index < tick):
        l = i + 1
      else:
        r = i - 1

  @staticmethod
  def nextInitializedTick (ticks: List[Tick], tick: int, lte: bool) -> Tick:
    if (lte):
      assert not TickList.isBelowSmallest(ticks, tick), 'BELOW_SMALLEST'
      if (TickList.isAtOrAboveLargest(ticks, tick)):
        return ticks[len(ticks) - 1]

      index = TickList.binarySearch(ticks, tick)
      return ticks[index]
    else:
      assert not TickList.isAtOrAboveLargest(ticks, tick), 'AT_OR_ABOVE_LARGEST'
      if (TickList.isBelowSmallest(ticks, tick)):
        return ticks[0]
      
      index = TickList.binarySearch(ticks, tick)
      return ticks[index + 1]

  @staticmethod
  def nextInitializedTickWithinOneWord (
    ticks: List[Tick],
    tick: int,
    lte: bool,
    tickSpacing: int
  ) -> Tuple[int, bool]:
    compressed = floor(tick / tickSpacing) # matches rounding in the code

    if (lte):
      wordPos = compressed >> 8
      minimum = (wordPos << 8) * tickSpacing

      if (TickList.isBelowSmallest(ticks, tick)):
        return (minimum, False)

      index = TickList.nextInitializedTick(ticks, tick, lte).index
      nextInitializedTick = max(minimum, index)
      return (nextInitializedTick, nextInitializedTick == index)
    else:
      wordPos = (compressed + 1) >> 8
      maximum = (((wordPos + 1) << 8) - 1) * tickSpacing

      if (TickList.isAtOrAboveLargest(ticks, tick)):
        return (maximum, False)

      index = TickList.nextInitializedTick(ticks, tick, lte).index
      nextInitializedTick = min(maximum, index)
      return (nextInitializedTick, nextInitializedTick == index)
