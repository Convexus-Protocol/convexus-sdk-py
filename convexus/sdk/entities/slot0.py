from dataclasses import dataclass
from typing import Dict
from convexus.icontoolkit.BigInt import BigInt

@dataclass
class Slot0:
  feeProtocol: int
  observationCardinality: int
  observationCardinalityNext: int
  observationIndex: int
  sqrtPriceX96: int
  tick: int
  unlocked: bool

  @staticmethod
  def fromCall (data: Dict[str, str]) -> 'Slot0':
    return Slot0 (
      int(data['feeProtocol'], 0),
      int(data['observationCardinality'], 0),
      int(data['observationCardinalityNext'], 0),
      int(data['observationIndex'], 0),
      BigInt(data['sqrtPriceX96']),
      int(data['tick'], 0),
      bool(int(data['unlocked'], 0))
    )

  def __repr__(self) -> str:
    return str(self.__dict__)