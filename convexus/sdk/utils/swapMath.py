from abc import ABCMeta
from dataclasses import dataclass
from typing import Tuple

from convexus.sdk.constants import FeeAmount
from convexus.sdk.utils.sqrtPriceMath import SqrtPriceMath
from convexus.sdk.utils.fullMath import FullMath

MAX_FEE = 10**6

class SwapMath(metaclass=ABCMeta):

  @dataclass
  class ReturnValues:
    sqrtRatioNextX96: int
    amountIn: int
    amountOut: int
    feeAmount: int

  @classmethod
  def computeSwapStep(
    cls,
    sqrtRatioCurrentX96: int,
    sqrtRatioTargetX96: int,
    liquidity: int,
    amountRemaining: int,
    feePips: FeeAmount
  ) -> Tuple[int, int, int, int]:

    returnValues = cls.ReturnValues(0, 0, 0, 0)

    zeroForOne = sqrtRatioCurrentX96 >= sqrtRatioTargetX96
    exactIn = amountRemaining >= 0

    if exactIn:
      amountRemainingLessFee = (amountRemaining * (MAX_FEE - feePips)) // MAX_FEE
      a = SqrtPriceMath.getAmount0Delta(sqrtRatioTargetX96, sqrtRatioCurrentX96, liquidity, True)
      b = SqrtPriceMath.getAmount1Delta(sqrtRatioCurrentX96, sqrtRatioTargetX96, liquidity, True)
      returnValues.amountIn = a if zeroForOne else b

      if amountRemainingLessFee >= returnValues.amountIn:
        returnValues.sqrtRatioNextX96 = sqrtRatioTargetX96
      else:
        returnValues.sqrtRatioNextX96 = SqrtPriceMath.getNextSqrtPriceFromInput(
          sqrtRatioCurrentX96,
          liquidity,
          amountRemainingLessFee,
          zeroForOne
        )
    else:
      a = SqrtPriceMath.getAmount1Delta(sqrtRatioTargetX96, sqrtRatioCurrentX96, liquidity, False)
      b = SqrtPriceMath.getAmount0Delta(sqrtRatioCurrentX96, sqrtRatioTargetX96, liquidity, False)
      returnValues.amountOut = a if zeroForOne else b
      
      if (amountRemaining * -1) >= returnValues.amountOut:
        returnValues.sqrtRatioNextX96 = sqrtRatioTargetX96
      else:
        returnValues.sqrtRatioNextX96 = SqrtPriceMath.getNextSqrtPriceFromOutput(
          sqrtRatioCurrentX96,
          liquidity,
          amountRemaining * -1,
          zeroForOne
        )

    max = sqrtRatioTargetX96 == returnValues.sqrtRatioNextX96

    if zeroForOne:
      b = SqrtPriceMath.getAmount0Delta(returnValues.sqrtRatioNextX96, sqrtRatioCurrentX96, liquidity, True)
      returnValues.amountIn = returnValues.amountIn if (max and exactIn) else b
      b = SqrtPriceMath.getAmount1Delta(returnValues.sqrtRatioNextX96, sqrtRatioCurrentX96, liquidity, False)
      returnValues.amountOut = returnValues.amountOut if (max and not exactIn) else b
    else:
      b = SqrtPriceMath.getAmount1Delta(sqrtRatioCurrentX96, returnValues.sqrtRatioNextX96, liquidity, True)
      returnValues.amountIn = returnValues.amountIn if (max and exactIn) else b
      b = SqrtPriceMath.getAmount0Delta(sqrtRatioCurrentX96, returnValues.sqrtRatioNextX96, liquidity, False)
      returnValues.amountOut = returnValues.amountOut if (max and not exactIn) else b

    if (not exactIn and (returnValues.amountOut > (amountRemaining * -1))):
      returnValues.amountOut = (amountRemaining * -1)

    if (exactIn and (returnValues.sqrtRatioNextX96 != sqrtRatioTargetX96)):
      # we didn't reach the target, so take the remainder of the maximum input as fee
      returnValues.feeAmount = amountRemaining - returnValues.amountIn
    else:
      returnValues.feeAmount = FullMath.mulDivRoundingUp(returnValues.amountIn, feePips, (MAX_FEE - feePips))
    
    return (returnValues.sqrtRatioNextX96, returnValues.amountIn, returnValues.amountOut, returnValues.feeAmount)
