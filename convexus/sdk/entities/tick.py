from dataclasses import dataclass
from typing import Dict
from convexus.sdk.utils.tickMath import TickMath

@dataclass
class FeeGrowthOutside:
  feeGrowthOutside0X128: int
  feeGrowthOutside1X128: int

@dataclass
class TickConstructorArgs:
  index: int # type: ignore[assignment]
  liquidityGross: int
  liquidityNet: int
  feeGrowthOutside: FeeGrowthOutside | None = None
  secondsOutside: int | None = None
  secondsPerLiquidityOutsideX128: int | None = None
  tickCumulativeOutside: int | None = None
  initialized: bool | None = None

class Tick:
  def __init__(self, args: TickConstructorArgs) -> None:
    index = args.index
    assert index >= TickMath.MIN_TICK and index <= TickMath.MAX_TICK, 'TICK'
    
    self.index = index
    self.liquidityGross = args.liquidityGross
    self.liquidityNet = args.liquidityNet
    self.feeGrowthOutside = args.feeGrowthOutside
    self.secondsOutside = args.secondsOutside
    self.secondsPerLiquidityOutsideX128 = args.secondsPerLiquidityOutsideX128
    self.tickCumulativeOutside = args.tickCumulativeOutside
    self.initialized = args.initialized
  
  @staticmethod
  def fromCall (data: Dict[str, str]) -> 'Tick':
    return Tick (TickConstructorArgs(
      int(data['index'], 0),
      int(data['liquidityGross'], 0),
      int(data['liquidityNet'], 0),
      int(data['feeGrowthOutside'], 0),
      int(data['secondsOutside'], 0),
      int(data['secondsPerLiquidityOutsideX128'], 0),
      int(data['tickCumulativeOutside'], 0),
      bool(int(data['initialized'], 0)),
    ))

  def __repr__(self) -> str:
    return str(self.__dict__)