from abc import ABCMeta
from convexus.sdk.utils.tickLibrary import subIn256

Q128 = 2**128

class PositionLibrary(metaclass=ABCMeta):
  
  @staticmethod
  def getTokensOwed (
    feeGrowthInside0LastX128: int,
    feeGrowthInside1LastX128: int,
    liquidity: int,
    feeGrowthInside0X128: int,
    feeGrowthInside1X128: int
  ):
    """ Replicates the portions of Position#update required to compute unaccounted fees """
    tokensOwed0 = subIn256(feeGrowthInside0X128, feeGrowthInside0LastX128) * liquidity // Q128
    tokensOwed1 = subIn256(feeGrowthInside1X128, feeGrowthInside1LastX128) * liquidity // Q128
    return [tokensOwed0, tokensOwed1]
