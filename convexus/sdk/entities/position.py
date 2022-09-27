from dataclasses import dataclass
from typing import cast
from convexus.icontoolkit.BigInt import BigInt

from convexus.icontoolkit.constants import BigintIsh

from convexus.sdkcore.entities.fractions.price import Price
from convexus.sdkcore.entities.fractions.currencyAmount import CurrencyAmount
from convexus.sdkcore.entities.fractions.percent import Percent
from convexus.sdkcore.constants import MaxUint256

from convexus.sdk.entities.pool import Pool
from convexus.sdk.utils.tickMath import TickMath
from convexus.sdk.utils.priceTickConversions import tickToPrice
from convexus.sdk.utils.sqrtPriceMath import SqrtPriceMath
from convexus.sdk.utils.encodeSqrtRatioX96 import encodeSqrtRatioX96
from convexus.sdk.utils.maxLiquidityForAmounts import maxLiquidityForAmounts

@dataclass
class PositionConstructorArgs:
  pool: Pool
  tickLower: int
  tickUpper: int
  liquidity: BigintIsh

@dataclass
class FromAmountsArgs:
  pool: Pool
  tickLower: int
  tickUpper: int
  amount0: BigintIsh
  amount1: BigintIsh
  useFullPrecision: bool

@dataclass
class FromAmount0Args:
  pool: Pool
  tickLower: int
  tickUpper: int
  amount0: BigintIsh
  useFullPrecision: bool

@dataclass
class FromAmount1Args:
  pool: Pool
  tickLower: int
  tickUpper: int
  amount1: BigintIsh

@dataclass
class Amounts:
  amount0: int
  amount1: int


class Position:
  """
  * Represents a position on a Convexus Pool
  """

  def __init__(self, args: PositionConstructorArgs):
    """
    * Constructs a position for a given pool with the given liquidity
    * @param pool For which pool the liquidity is assigned
    * @param liquidity The amount of liquidity that is in the position
    * @param tickLower The lower tick of the position
    * @param tickUpper The upper tick of the position
    """
    
    pool: Pool = args.pool
    tickLower: int = args.tickLower
    tickUpper: int = args.tickUpper
    liquidity: int = BigInt(args.liquidity)

    assert tickLower < tickUpper, 'TICK_ORDER'
    assert tickLower >= TickMath.MIN_TICK and tickLower % pool.tickSpacing == 0, 'TICK_LOWER'
    assert tickUpper <= TickMath.MAX_TICK and tickUpper % pool.tickSpacing == 0, 'TICK_UPPER'

    self.pool: Pool = pool
    self.tickLower: int = tickLower
    self.tickUpper: int = tickUpper
    self.liquidity: int = liquidity
    self.__token0Amount: CurrencyAmount | None = None
    self.__token1Amount: CurrencyAmount | None = None
    self.__mintAmounts: Amounts | None = None

  @property
  def token0PriceLower(self) -> Price:
    """
    * Returns the price of token0 at the lower tick
    """
    return tickToPrice(self.pool.token0, self.pool.token1, self.tickLower)

  @property
  def token0PriceUpper(self) -> Price:
    """
    * Returns the price of token0 at the upper tick
    """
    return tickToPrice(self.pool.token0, self.pool.token1, self.tickUpper)

  @property
  def amount0(self) -> CurrencyAmount:
    """
    * Returns the amount of token0 that this position's liquidity could be burned for at the current pool price
    """
    if self.__token0Amount == None:
      if (self.pool.tickCurrent < self.tickLower):
        self.__token0Amount = CurrencyAmount.fromRawAmount(
          self.pool.token0,
          SqrtPriceMath.getAmount0Delta(
            TickMath.getSqrtRatioAtTick(self.tickLower),
            TickMath.getSqrtRatioAtTick(self.tickUpper),
            self.liquidity,
            True
          )
        )
      elif (self.pool.tickCurrent < self.tickUpper):
        self.__token0Amount = CurrencyAmount.fromRawAmount(
          self.pool.token0,
          SqrtPriceMath.getAmount0Delta(
            self.pool.sqrtRatioX96,
            TickMath.getSqrtRatioAtTick(self.tickUpper),
            self.liquidity,
            True
          )
        )
      else:
        self.__token0Amount = CurrencyAmount.fromRawAmount(self.pool.token0, 0)
    
    return cast(CurrencyAmount, self.__token0Amount)

  @property
  def amount1(self) -> CurrencyAmount:
    """
    * Returns the amount of token1 that this position's liquidity could be burned for at the current pool price
    """
    if (self.__token1Amount == None):
      if (self.pool.tickCurrent < self.tickLower):
        self.__token1Amount = CurrencyAmount.fromRawAmount(self.pool.token1, 0)
      elif (self.pool.tickCurrent < self.tickUpper):
        self.__token1Amount = CurrencyAmount.fromRawAmount(
          self.pool.token1,
          SqrtPriceMath.getAmount1Delta(
            TickMath.getSqrtRatioAtTick(self.tickLower),
            self.pool.sqrtRatioX96,
            self.liquidity,
            True
          )
        )
      else:
        self.__token1Amount = CurrencyAmount.fromRawAmount(
          self.pool.token1,
          SqrtPriceMath.getAmount1Delta(
            TickMath.getSqrtRatioAtTick(self.tickLower),
            TickMath.getSqrtRatioAtTick(self.tickUpper),
            self.liquidity,
            True
          )
        )
    return cast(CurrencyAmount, self.__token1Amount)

  @dataclass
  class RatiosAfterSlippageResult:
    """
    * Returns the lower and upper sqrt ratios if the price 'slips' up to slippage tolerance percentage
    * @param slippageTolerance The amount by which the price can 'slip' before the transaction will revert
    * @returns The sqrt ratios after slippage
    """
    sqrtRatioX96Lower: int
    sqrtRatioX96Upper: int

  def ratiosAfterSlippage(self, slippageTolerance: Percent) -> RatiosAfterSlippageResult:
    priceLower = self.pool.token0Price.asFraction.multiply(Percent(1).subtract(slippageTolerance))
    priceUpper = self.pool.token0Price.asFraction.multiply(slippageTolerance.add(1))
    sqrtRatioX96Lower = encodeSqrtRatioX96(priceLower.numerator, priceLower.denominator)
    
    if (sqrtRatioX96Lower <= TickMath.MIN_SQRT_RATIO):
      sqrtRatioX96Lower = TickMath.MIN_SQRT_RATIO + 1
    sqrtRatioX96Upper = encodeSqrtRatioX96(priceUpper.numerator, priceUpper.denominator)
    
    if sqrtRatioX96Upper >= TickMath.MAX_SQRT_RATIO:
      sqrtRatioX96Upper = TickMath.MAX_SQRT_RATIO - 1
    
    return self.RatiosAfterSlippageResult (
      sqrtRatioX96Lower,
      sqrtRatioX96Upper
    )

  def mintAmountsWithSlippage(self, slippageTolerance: Percent) -> Amounts:
    """
    * Returns the minimum amounts that must be sent in order to safely mint the amount of liquidity held by the position
    * with the given slippage tolerance
    * @param slippageTolerance Tolerance of unfavorable slippage from the current price
    * @returns The amounts, with slippage
    """
    # get lower/upper prices
    sqrtRatio = self.ratiosAfterSlippage(slippageTolerance)
    sqrtRatioX96Lower = sqrtRatio.sqrtRatioX96Lower
    sqrtRatioX96Upper = sqrtRatio.sqrtRatioX96Upper

    # construct counterfactual pools
    poolLower = Pool (
      self.pool.token0,
      self.pool.token1,
      self.pool.fee,
      sqrtRatioX96Lower,
      0, # liquidity doesn't matter
      TickMath.getTickAtSqrtRatio(sqrtRatioX96Lower)
    )

    poolUpper = Pool (
      self.pool.token0,
      self.pool.token1,
      self.pool.fee,
      sqrtRatioX96Upper,
      0, # liquidity doesn't matter
      TickMath.getTickAtSqrtRatio(sqrtRatioX96Upper)
    )

    # because the router is imprecise, we need to calculate the position that will be created (assuming no slippage)
    amounts = self.mintAmounts
    positionThatWillBeCreated = Position.fromAmounts(
      FromAmountsArgs (
        pool=self.pool,
        tickLower=self.tickLower,
        tickUpper=self.tickUpper,
        amount0=amounts.amount0, # the mint amounts are what will be passed as calldata
        amount1=amounts.amount1,
        useFullPrecision=False
      )
    )

    # we want the smaller amounts...
    # ...which occurs at the upper price for amount0...
    amount0 = Position (
      PositionConstructorArgs (
        pool=poolUpper,
        liquidity=positionThatWillBeCreated.liquidity,
        tickLower=self.tickLower,
        tickUpper=self.tickUpper
      )
    ).mintAmounts.amount0

    # ...and the lower for amount1
    amount1 = Position (
      PositionConstructorArgs (
        pool = poolLower,
        liquidity = positionThatWillBeCreated.liquidity,
        tickLower = self.tickLower,
        tickUpper = self.tickUpper
      )
    ).mintAmounts.amount1

    return Amounts(amount0, amount1)

  def burnAmountsWithSlippage(self, slippageTolerance: Percent) -> Amounts:
    """
    * Returns the minimum amounts that should be requested in order to safely burn the amount of liquidity held by the
    * position with the given slippage tolerance
    * @param slippageTolerance tolerance of unfavorable slippage from the current price
    * @returns The amounts, with slippage
    """
    # get lower/upper prices
    sqrtRatio = self.ratiosAfterSlippage(slippageTolerance)

    sqrtRatioX96Upper = sqrtRatio.sqrtRatioX96Upper
    sqrtRatioX96Lower = sqrtRatio.sqrtRatioX96Lower

    # construct counterfactual pools
    poolLower = Pool (
      self.pool.token0,
      self.pool.token1,
      self.pool.fee,
      sqrtRatioX96Lower,
      0, # liquidity doesn't matter
      TickMath.getTickAtSqrtRatio(sqrtRatioX96Lower)
    )

    poolUpper = Pool(
      self.pool.token0,
      self.pool.token1,
      self.pool.fee,
      sqrtRatioX96Upper,
      0, # liquidity doesn't matter
      TickMath.getTickAtSqrtRatio(sqrtRatioX96Upper)
    )

    # we want the smaller amounts...
    # ...which occurs at the upper price for amount0...
    amount0 = Position (
      PositionConstructorArgs (
        pool=poolUpper,
        liquidity=self.liquidity,
        tickLower=self.tickLower,
        tickUpper=self.tickUpper
      )
    ).amount0
    # ...and the lower for amount1
    amount1 = Position (
      PositionConstructorArgs (
        pool=poolLower,
        liquidity=self.liquidity,
        tickLower=self.tickLower,
        tickUpper=self.tickUpper
      )
    ).amount1

    return Amounts (
      amount0=amount0.quotient, 
      amount1=amount1.quotient
    )

  @property
  def mintAmounts(self) -> Amounts:
    """
    * Returns the minimum amounts that must be sent in order to mint the amount of liquidity held by the position at
    * the current price for the pool
    """
    if (self.__mintAmounts == None):
      if (self.pool.tickCurrent < self.tickLower):
        return Amounts(
          amount0=SqrtPriceMath.getAmount0Delta(
            TickMath.getSqrtRatioAtTick(self.tickLower),
            TickMath.getSqrtRatioAtTick(self.tickUpper),
            self.liquidity,
            True
          ),
          amount1=0
        )
      elif (self.pool.tickCurrent < self.tickUpper):
        return Amounts(
          amount0=SqrtPriceMath.getAmount0Delta(
            self.pool.sqrtRatioX96,
            TickMath.getSqrtRatioAtTick(self.tickUpper),
            self.liquidity,
            True
          ),
          amount1=SqrtPriceMath.getAmount1Delta(
            TickMath.getSqrtRatioAtTick(self.tickLower),
            self.pool.sqrtRatioX96,
            self.liquidity,
            True
          )
        )
      else:
        return Amounts(
          amount0=0,
          amount1=SqrtPriceMath.getAmount1Delta(
            TickMath.getSqrtRatioAtTick(self.tickLower),
            TickMath.getSqrtRatioAtTick(self.tickUpper),
            self.liquidity,
            True
          )
        )

    return cast(Amounts, self.__mintAmounts)

  @staticmethod
  def fromAmounts (
    args: FromAmountsArgs
  ):
    """
    * Computes the maximum amount of liquidity received for a given amount of token0, token1,
    * and the prices at the tick boundaries.
    * @param pool The pool for which the position should be created
    * @param tickLower The lower tick of the position
    * @param tickUpper The upper tick of the position
    * @param amount0 token0 amount
    * @param amount1 token1 amount
    * @param useFullPrecision If False, liquidity will be maximized according to what the router can calculate,
    * not what core can theoretically support
    * @returns The amount of liquidity for the position
    """
    pool: Pool = args.pool
    tickLower: int = args.tickLower
    tickUpper: int = args.tickUpper
    amount0: int = BigInt(args.amount0)
    amount1: int = BigInt(args.amount1)
    useFullPrecision: bool = args.useFullPrecision

    sqrtRatioAX96 = TickMath.getSqrtRatioAtTick(tickLower)
    sqrtRatioBX96 = TickMath.getSqrtRatioAtTick(tickUpper)

    return Position (
      PositionConstructorArgs (
        pool,
        tickLower,
        tickUpper,
        maxLiquidityForAmounts (
          pool.sqrtRatioX96,
          sqrtRatioAX96,
          sqrtRatioBX96,
          amount0,
          amount1,
          useFullPrecision
        )
      )
    )

  @staticmethod
  def fromAmount0(
    args: FromAmount0Args
  ):
    """
    * Computes a position with the maximum amount of liquidity received for a given amount of token0, assuming an unlimited amount of token1
    * @param pool The pool for which the position is created
    * @param tickLower The lower tick
    * @param tickUpper The upper tick
    * @param amount0 The desired amount of token0
    * @param useFullPrecision If True, liquidity will be maximized according to what the router can calculate,
    * not what core can theoretically support
    * @returns The position
    """
    
    pool: Pool = args.pool
    tickLower: int = args.tickLower
    tickUpper: int = args.tickUpper
    amount0: int = BigInt(args.amount0)
    useFullPrecision: bool = args.useFullPrecision

    return Position.fromAmounts (
      FromAmountsArgs (
        pool, 
        tickLower, 
        tickUpper, 
        amount0, 
        MaxUint256, 
        useFullPrecision
      )
    )

  @staticmethod
  def fromAmount1(
    args: FromAmount1Args
  ):
    """
    * Computes a position with the maximum amount of liquidity received for a given amount of token1, assuming an unlimited amount of token0
    * @param pool The pool for which the position is created
    * @param tickLower The lower tick
    * @param tickUpper The upper tick
    * @param amount1 The desired amount of token1
    * @returns The position
    """
    pool: Pool = args.pool
    tickLower: int = args.tickLower
    tickUpper: int = args.tickUpper
    amount1: int = BigInt(args.amount1)

    # this function always uses full precision,
    return Position.fromAmounts (
      FromAmountsArgs (
        pool,
        tickLower,
        tickUpper,
        MaxUint256,
        amount1,
        True
      )
    )
