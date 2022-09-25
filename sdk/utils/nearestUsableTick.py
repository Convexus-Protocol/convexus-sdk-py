from sdk.utils.tickMath import TickMath

def nearestUsableTick (tick: int, tickSpacing: int):
  """
  * Returns the closest tick that is nearest a given tick and usable for the given tick spacing
  * @param tick the target tick
  * @param tickSpacing the spacing of the pool
  """
  assert isinstance(tick, int) and isinstance(tickSpacing, int), 'INTEGERS'
  assert tickSpacing > 0, 'TICK_SPACING'
  assert tick >= TickMath.MIN_TICK and tick <= TickMath.MAX_TICK, 'TICK_BOUND'

  rounded = round(tick / tickSpacing) * tickSpacing

  if rounded < TickMath.MIN_TICK:
    return rounded + tickSpacing
  elif rounded > TickMath.MAX_TICK:
    return rounded - tickSpacing
  else:
    return rounded
