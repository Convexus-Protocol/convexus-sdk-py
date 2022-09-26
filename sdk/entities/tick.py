
from typing import NamedTuple
from sdk.utils.tickMath import TickMath

class TickConstructorArgs(NamedTuple):
  index: int # type: ignore[assignment]
  liquidityGross: int
  liquidityNet: int

class Tick:
  def __init__(self, args: TickConstructorArgs) -> None:
    index, liquidityGross, liquidityNet = args
    assert index >= TickMath.MIN_TICK and index <= TickMath.MAX_TICK, 'TICK'
    self.index = index
    self.liquidityGross = liquidityGross
    self.liquidityNet = liquidityNet