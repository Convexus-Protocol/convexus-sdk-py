from convexus.sdk.utils.tickMath import TickMath
import math

def nearestUsableTick (tick: int, tickSpacing: int):
  """
  * Returns the closest tick that is nearest a given tick and usable for the given tick spacing
  * @param tick the target tick
  * @param tickSpacing the spacing of the pool
  """
  assert isinstance(tick, int) and isinstance(tickSpacing, int), 'INTEGERS'
  assert tickSpacing > 0, 'TICK_SPACING'
  assert tick >= TickMath.MIN_TICK and tick <= TickMath.MAX_TICK, 'TICK_BOUND'

  def _round(n):
    if n - math.floor(n) < 0.5:
      return math.floor(n)
    return math.ceil(n)

  rounded = _round(tick / tickSpacing) * tickSpacing

  if rounded < TickMath.MIN_TICK:
    return rounded + tickSpacing
  elif rounded > TickMath.MAX_TICK:
    return rounded - tickSpacing
  else:
    return rounded
