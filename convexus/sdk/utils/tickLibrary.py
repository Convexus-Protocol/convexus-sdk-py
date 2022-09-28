from abc import ABCMeta
from dataclasses import dataclass

from convexus.sdk.entities.tick import FeeGrowthOutside

Q256 = 2**256

def subIn256(x: int, y: int) -> int:
  difference = x - y
  if (difference < 0):
    return Q256 + difference
  else:
    return difference

class TickLibrary(metaclass=ABCMeta):

  @staticmethod
  def getFeeGrowthInside(
    feeGrowthOutsideLower: FeeGrowthOutside,
    feeGrowthOutsideUpper: FeeGrowthOutside,
    tickLower: int,
    tickUpper: int,
    tickCurrent: int,
    feeGrowthGlobal0X128: int,
    feeGrowthGlobal1X128: int
  ):
    feeGrowthBelow0X128: int
    feeGrowthBelow1X128: int
    if (tickCurrent >= tickLower):
      feeGrowthBelow0X128 = feeGrowthOutsideLower.feeGrowthOutside0X128
      feeGrowthBelow1X128 = feeGrowthOutsideLower.feeGrowthOutside1X128
    else:
      feeGrowthBelow0X128 = subIn256(feeGrowthGlobal0X128, feeGrowthOutsideLower.feeGrowthOutside0X128)
      feeGrowthBelow1X128 = subIn256(feeGrowthGlobal1X128, feeGrowthOutsideLower.feeGrowthOutside1X128)
    
    feeGrowthAbove0X128: int
    feeGrowthAbove1X128: int
    if (tickCurrent < tickUpper):
      feeGrowthAbove0X128 = feeGrowthOutsideUpper.feeGrowthOutside0X128
      feeGrowthAbove1X128 = feeGrowthOutsideUpper.feeGrowthOutside1X128
    else:
      feeGrowthAbove0X128 = subIn256(feeGrowthGlobal0X128, feeGrowthOutsideUpper.feeGrowthOutside0X128)
      feeGrowthAbove1X128 = subIn256(feeGrowthGlobal1X128, feeGrowthOutsideUpper.feeGrowthOutside1X128)
    

    return [
      subIn256(subIn256(feeGrowthGlobal0X128, feeGrowthBelow0X128), feeGrowthAbove0X128),
      subIn256(subIn256(feeGrowthGlobal1X128, feeGrowthBelow1X128), feeGrowthAbove1X128)
    ]
  
