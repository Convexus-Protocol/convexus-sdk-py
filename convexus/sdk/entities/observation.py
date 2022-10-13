from dataclasses import dataclass
from typing import Dict
from convexus.icontoolkit.BigInt import BigInt

@dataclass
class OracleObservation:
  # the block timestamp of the observation
  blockTimestamp: int
  # the tick accumulator, i.e. tick * time elapsed since the pool was first initialized
  tickCumulative: int
  # the seconds per liquidity, i.e. seconds elapsed / max(1, liquidity) since the pool was first initialized
  secondsPerLiquidityCumulativeX128: int
  # whether or not the observation is initialized
  initialized: bool

  @staticmethod
  def fromCall (data: Dict[str, str]) -> 'OracleObservation':
    return OracleObservation (
      BigInt(data['blockTimestamp']),
      BigInt(data['tickCumulative']),
      BigInt(data['secondsPerLiquidityCumulativeX128']),
      bool(int(data['initialized'], 0))
    )

  def __repr__(self) -> str:
    return str(self.__dict__)