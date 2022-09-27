
from dataclasses import dataclass
from convexus.sdk.utils.tickMath import TickMath

@dataclass
class TickConstructorArgs:
  index: int # type: ignore[assignment]
  liquidityGross: int
  liquidityNet: int

class Tick:
  def __init__(self, args: TickConstructorArgs) -> None:
    index = args.index
    liquidityGross = args.liquidityGross
    liquidityNet = args.liquidityNet
    
    assert index >= TickMath.MIN_TICK and index <= TickMath.MAX_TICK, 'TICK'
    self.index = index
    self.liquidityGross = liquidityGross
    self.liquidityNet = liquidityNet
  
  def __repr__(self) -> str:
    return str(self.__dict__)