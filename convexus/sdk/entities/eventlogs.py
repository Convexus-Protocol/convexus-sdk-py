from convexus.icontoolkit.constants import BigintIsh
from convexus.icontoolkit.BigInt import BigInt

class IntrinsicsUpdate:
  def __init__(self,
    sqrtPriceX96: BigintIsh,
    tick: int,
    liquidity: BigintIsh
  ) -> None:
    self.sqrtPriceX96 = BigInt(sqrtPriceX96)
    self.tick = tick
    self.liquidity = BigInt(liquidity)

  @staticmethod
  def fromEventLog(eventlog: dict):
    return IntrinsicsUpdate(
      eventlog['data'][0],
      int(eventlog['data'][1], 16),
      eventlog['data'][2]
    )


class PoolCreated:
  def __init__(self,
    token0: str, 
    token1: str, 
    fee: int, 
    tickSpacing: int, 
    pool: str
  ):
    self.token0 = token0
    self.token1 = token1
    self.fee = fee
    self.tickSpacing = tickSpacing
    self.pool = pool

  @staticmethod
  def fromEventLog(eventlog: dict):
    return PoolCreated(
      eventlog['indexed'][1],
      eventlog['indexed'][2],
      int(eventlog['indexed'][3], 16),
      int(eventlog['data'][0], 16),
      eventlog['data'][1]
    )

class TickUpdate:
  def __init__(self, 
    index: int,
    liquidityGross: BigintIsh,
    liquidityNet: BigintIsh,
    feeGrowthOutside0X128: BigintIsh,
    feeGrowthOutside1X128: BigintIsh,
    tickCumulativeOutside: BigintIsh,
    secondsPerLiquidityOutsideX128: BigintIsh,
    secondsOutside: BigintIsh,
    initialized: bool
  ):
    self.index = index
    self.liquidityGross = BigInt(liquidityGross)
    self.liquidityNet = BigInt(liquidityNet)
    self.feeGrowthOutside0X128 = BigInt(feeGrowthOutside0X128)
    self.feeGrowthOutside1X128 = BigInt(feeGrowthOutside1X128)
    self.tickCumulativeOutside = BigInt(tickCumulativeOutside)
    self.secondsPerLiquidityOutsideX128 = BigInt(secondsPerLiquidityOutsideX128)
    self.secondsOutside = BigInt(secondsOutside)
    self.initialized = initialized

  @staticmethod
  def fromEventLog(eventlog: dict):
    return TickUpdate(
      int(eventlog['indexed'][1], 16),
      eventlog['data'][0],
      eventlog['data'][1],
      eventlog['data'][2],
      eventlog['data'][3],
      eventlog['data'][4],
      eventlog['data'][5],
      eventlog['data'][6],
      bool(int(eventlog['data'][7], 16)),
    )
