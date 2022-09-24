
from sdk.utils.tickMath import TickMath

class Tick:
  def __init__(self, index: int, liquidityGross: int, liquidityNet: int) -> None:
    assert index >= TickMath.MIN_TICK and index <= TickMath.MAX_TICK, 'TICK'
    self.index = index
    self.liquidityGross = liquidityGross
    self.liquidityNet = liquidityNet