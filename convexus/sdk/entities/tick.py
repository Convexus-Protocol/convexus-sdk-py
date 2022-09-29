from dataclasses import dataclass
from typing import Dict
from convexus.icontoolkit.BigInt import BigInt
from convexus.icontoolkit.constants import BigintIsh
from convexus.sdk.utils.tickMath import TickMath

class FeeGrowthOutside:
  def __init__(self, feeGrowthOutside0X128: BigintIsh, feeGrowthOutside1X128: BigintIsh) -> None:
    self.feeGrowthOutside0X128 = BigInt(feeGrowthOutside0X128)
    self.feeGrowthOutside1X128 = BigInt(feeGrowthOutside1X128)

  def __repr__(self) -> str:
    return str(self.__dict__)

@dataclass
class TickConstructorArgs:
  index: int
  liquidityGross: BigintIsh
  liquidityNet: BigintIsh
  feeGrowthOutside: FeeGrowthOutside | None = None
  secondsOutside: BigintIsh | None = None
  secondsPerLiquidityOutsideX128: BigintIsh | None = None
  tickCumulativeOutside: BigintIsh | None = None
  initialized: bool | None = None

class Tick:
  def __init__(self, args: TickConstructorArgs) -> None:
    index = args.index
    assert index >= TickMath.MIN_TICK and index <= TickMath.MAX_TICK, 'TICK'

    self.index = index
    self.liquidityGross = BigInt(args.liquidityGross)
    self.liquidityNet = BigInt(args.liquidityNet)
    self.feeGrowthOutside = args.feeGrowthOutside
    self.secondsOutside = BigInt(args.secondsOutside) if args.secondsOutside else None
    self.secondsPerLiquidityOutsideX128 = BigInt(args.secondsPerLiquidityOutsideX128) if args.secondsPerLiquidityOutsideX128 else None
    self.tickCumulativeOutside = BigInt(args.tickCumulativeOutside) if args.tickCumulativeOutside else None
    self.initialized = args.initialized

  @staticmethod
  def fromCall (data: Dict[str, str]) -> 'Tick':
    return Tick (TickConstructorArgs(
      int(data['index'], 0),
      data['liquidityGross'],
      data['liquidityNet'],
      FeeGrowthOutside (
        data['feeGrowthOutside0X128'],
        data['feeGrowthOutside1X128']
      ),
      data['secondsOutside'],
      data['secondsPerLiquidityOutsideX128'],
      data['tickCumulativeOutside'],
      bool(int(data['initialized'], 0)),
    ))

  def __repr__(self) -> str:
    return str(self.__dict__)