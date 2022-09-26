from typing import List, NamedTuple, Tuple, cast
from recordclass import RecordClass
from icontoolkit.BigInt import BigInt
from icontoolkit.constants import BigintIsh
from sdkcore.entities.fractions.price import Price
from sdkcore.entities.fractions.currencyAmount import CurrencyAmount
from sdkcore.entities.currency import Token
from sdk.constants import FeeAmount, TICK_SPACINGS
from sdk.entities.tickDataProvider import NoTickDataProvider, TickDataProvider
from sdk.entities.factoryProvider import NoPoolFactoryProvider, PoolFactoryProvider
from sdk.entities.tick import Tick, TickConstructorArgs
from sdk.entities.tickListDataProvider import TickListDataProvider
from sdk.utils.tickMath import TickMath
from sdk.internalConstants import Q192
from sdk.utils.swapMath import SwapMath
from sdk.utils.liquidityMath import LiquidityMath
from collections.abc import Sequence

class StepComputations(RecordClass):
  sqrtPriceStartX96: int
  tickNext: int
  initialized: bool
  sqrtPriceNextX96: int
  amountIn: int
  amountOut: int
  feeAmount: int

class SwapResult (NamedTuple):
  amountCalculated: int
  sqrtRatioX96: int
  liquidity: int
  tickCurrent: int

"""
* By default, pools will not allow operations that require ticks.
"""
NO_TICK_DATA_PROVIDER_DEFAULT = NoTickDataProvider()
NO_POOL_FACTORY_PROVIDER_DEFAULT = NoPoolFactoryProvider()

class Pool:
  """
  * Represents a Convexus pool
  """
  def __init__(
    self,
    tokenA: Token,
    tokenB: Token,
    fee: FeeAmount,
    sqrtRatioX96: BigintIsh,
    liquidity: BigintIsh,
    tickCurrent: int,
    ticks: TickDataProvider | List[Tick | TickConstructorArgs] = NO_TICK_DATA_PROVIDER_DEFAULT,
    poolFactoryProvider: PoolFactoryProvider = NO_POOL_FACTORY_PROVIDER_DEFAULT
  ):
    """
    * Construct a pool
    * @param tokenA One of the tokens in the pool
    * @param tokenB The other token in the pool
    * @param fee The fee in hundredths of a bips of the input amount of every swap that is collected by the pool
    * @param sqrtRatioX96 The sqrt of the current ratio of amounts of token1 to token0
    * @param liquidity The current value of in range liquidity
    * @param tickCurrent The current tick of the pool
    * @param ticks The current state of the pool ticks or a data provider that can return tick data
    """
    assert isinstance(fee, int) and fee < 1_000_000, 'FEE'

    # Convert params
    sqrtRatioX96 = BigInt(sqrtRatioX96)
    liquidity = BigInt(sqrtRatioX96)

    tickCurrentSqrtRatioX96 = TickMath.getSqrtRatioAtTick(tickCurrent)
    nextTickSqrtRatioX96 = TickMath.getSqrtRatioAtTick(tickCurrent + 1)

    assert (sqrtRatioX96 >= tickCurrentSqrtRatioX96) and (sqrtRatioX96 <= nextTickSqrtRatioX96), 'PRICE_BOUNDS'

    # always create a copy of the list since we want the pool's tick list to be immutable
    self.token0, self.token1 = [tokenA, tokenB] if tokenA.sortsBefore(tokenB) else [tokenB, tokenA]
    self.fee = fee
    self.sqrtRatioX96 = (sqrtRatioX96)
    self.liquidity = (liquidity)
    self.tickCurrent = tickCurrent
    self.tickDataProvider = TickListDataProvider(ticks, TICK_SPACINGS[fee]) if isinstance(ticks, Sequence) else ticks
    self.poolFactoryProvider = poolFactoryProvider
    self._token0Price: Price | None = None
    self._token1Price: Price | None = None

  def __eq__(self, __o) -> bool:
    return self.token0 == __o.token0 and self.token1 == __o.token1 and self.fee == __o.fee

  @staticmethod
  def getAddress(poolFactoryProvider: PoolFactoryProvider, tokenA: Token, tokenB: Token, fee: FeeAmount) -> str:
    return poolFactoryProvider.getPool(tokenA, tokenB, fee)

  def involvesToken(self, token: Token) -> bool:
    """
    * Returns true if the token is either token0 or token1
    * @param token The token to check
    * @returns True if token is either token0 or token
    """
    return token.equals(self.token0) or token.equals(self.token1)

  @property
  def token0Price(self) -> Price:
    """
    * Returns the current mid price of the pool in terms of token0, i.e. the ratio of token1 over token0
    """
    if not self._token0Price:
      self._token0Price = Price (
        self.token0,
        self.token1,
        Q192,
        self.sqrtRatioX96 * self.sqrtRatioX96
      )

    return self._token0Price

  @property
  def token1Price(self) -> Price:
    """
    * Returns the current mid price of the pool in terms of token1, i.e. the ratio of token0 over token1
    """
    if not self._token1Price:
      self._token1Price = Price (
        self.token1,
        self.token0,
        self.sqrtRatioX96 * self.sqrtRatioX96,
        Q192
      )

    return self._token1Price

  def priceOf(self, token: Token) -> Price:
    """
    * Return the price of the given token in terms of the other token in the pool.
    * @param token The token to return price of
    * @returns The price of the given token, in terms of the other.
    """
    assert self.involvesToken(token), 'TOKEN'
    return self.token0Price if token.equals(self.token0) else self.token1Price

  def getOutputAmount(
    self,
    inputAmount: CurrencyAmount,
    sqrtPriceLimitX96: int = None
  ) -> Tuple[CurrencyAmount, 'Pool']:
    """
    * Given an input amount of a token, return the computed output amount, and a pool with state updated after the trade
    * @param inputAmount The input amount for which to quote the output amount
    * @param sqrtPriceLimitX96 The Q64.96 sqrt price limit
    * @returns The output amount and the pool with updated state
    """
    assert self.involvesToken(cast(Token, inputAmount.currency)), 'TOKEN'

    zeroForOne = inputAmount.currency.equals(self.token0)

    outputAmount, sqrtRatioX96, liquidity, tickCurrent = self.swap (
      zeroForOne,
      inputAmount.quotient,
      sqrtPriceLimitX96
    )

    outputToken = self.token1 if zeroForOne else self.token0
    return (
      CurrencyAmount.fromRawAmount(outputToken, outputAmount * -1),
      Pool(self.token0, self.token1, self.fee, sqrtRatioX96, liquidity, tickCurrent, self.tickDataProvider)
    )

  def getInputAmount (
    self,
    outputAmount: CurrencyAmount,
    sqrtPriceLimitX96: int = None
  ) -> Tuple[CurrencyAmount, 'Pool']:
    """
    * Given a desired output amount of a token, return the computed input amount and a pool with state updated after the trade
    * @param outputAmount the output amount for which to quote the input amount
    * @param sqrtPriceLimitX96 The Q64.96 sqrt price limit. If zero for one, the price cannot be less than this value after the swap. If one for zero, the price cannot be greater than this value after the swap
    * @returns The input amount and the pool with updated state
    """
    assert outputAmount.currency.isToken and self.involvesToken(cast(Token, outputAmount.currency)), 'TOKEN'

    zeroForOne = outputAmount.currency.equals(self.token1)

    inputAmount, sqrtRatioX96, liquidity, tickCurrent = self.swap (
      zeroForOne,
      outputAmount.quotient * -1,
      sqrtPriceLimitX96
    )

    inputToken = self.token0 if zeroForOne else self.token1

    return (
      CurrencyAmount.fromRawAmount(inputToken, inputAmount),
      Pool(self.token0, self.token1, self.fee, sqrtRatioX96, liquidity, tickCurrent, self.tickDataProvider)
    )

  def swap (
    self,
    zeroForOne: bool,
    amountSpecified: int,
    sqrtPriceLimitX96: int = None
  ) -> SwapResult:
    """
    * Executes a swap
    * @param zeroForOne Whether the amount in is token0 or token1
    * @param amountSpecified The amount of the swap, which implicitly configures the swap as exact input (positive), or exact output (negative)
    * @param sqrtPriceLimitX96 The Q64.96 sqrt price limit. 
    * If zero for one, the price cannot be less than this value after the swap. If one for zero, the price cannot be greater than this value after the swap
    * @returns amountCalculated
    * @returns sqrtRatioX96
    * @returns liquidity
    * @returns tickCurrent
    """
    if not sqrtPriceLimitX96:
      a = TickMath.MIN_SQRT_RATIO + 1
      b = TickMath.MAX_SQRT_RATIO - 1
      sqrtPriceLimitX96 = a if zeroForOne else b

    if (zeroForOne):
      assert (sqrtPriceLimitX96 > TickMath.MIN_SQRT_RATIO), 'RATIO_MIN'
      assert (sqrtPriceLimitX96 < self.sqrtRatioX96), 'RATIO_CURRENT'
    else:
      assert (sqrtPriceLimitX96 < TickMath.MAX_SQRT_RATIO), 'RATIO_MAX'
      assert (sqrtPriceLimitX96 > self.sqrtRatioX96), 'RATIO_CURRENT'
  
    exactInput = amountSpecified >= 0

    # keep track of swap state
    class SwapState(RecordClass):
      amountSpecifiedRemaining: int
      amountCalculated: int
      sqrtPriceX96: int
      tick: int
      liquidity: int

    state = SwapState (
      amountSpecified,
      0,
      self.sqrtRatioX96,
      self.tickCurrent,
      self.liquidity
    )

    # start swap while loop
    while ((state.amountSpecifiedRemaining != 0) and state.sqrtPriceX96 != sqrtPriceLimitX96):
      step = StepComputations(0, 0, False, 0, 0, 0, 0)
      step.sqrtPriceStartX96 = state.sqrtPriceX96

      # because each iteration of the while loop rounds, we can't optimize this code (relative to the smart contract)
      # by simply traversing to the next available tick, we instead need to exactly replicate
      # tickBitmap.nextInitializedTickWithinOneWord
      step.tickNext, step.initialized = self.tickDataProvider.nextInitializedTickWithinOneWord(
        state.tick,
        zeroForOne,
        self.tickSpacing
      )

      if (step.tickNext < TickMath.MIN_TICK):
        step.tickNext = TickMath.MIN_TICK
      elif (step.tickNext > TickMath.MAX_TICK):
        step.tickNext = TickMath.MAX_TICK
    
      direction = (step.sqrtPriceNextX96 < sqrtPriceLimitX96) if zeroForOne else (step.sqrtPriceNextX96 > sqrtPriceLimitX96)

      step.sqrtPriceNextX96 = TickMath.getSqrtRatioAtTick(step.tickNext)
      state.sqrtPriceX96, step.amountIn, step.amountOut, step.feeAmount = SwapMath.computeSwapStep (
        state.sqrtPriceX96, sqrtPriceLimitX96 if direction else step.sqrtPriceNextX96,
        state.liquidity,
        state.amountSpecifiedRemaining,
        self.fee
      )

      if exactInput:
        state.amountSpecifiedRemaining = state.amountSpecifiedRemaining - (step.amountIn + step.feeAmount)
        state.amountCalculated = state.amountCalculated - step.amountOut
      else:
        state.amountSpecifiedRemaining = state.amountSpecifiedRemaining + step.amountOut
        state.amountCalculated = state.amountCalculated + step.amountIn + step.feeAmount

      if state.sqrtPriceX96 == step.sqrtPriceNextX96:
        # if the tick is initialized, run the tick transition
        if step.initialized:
          liquidityNet = self.tickDataProvider.getTick(step.tickNext).liquidityNet
          # if we're moving leftward, we interpret liquidityNet as the opposite sign
          # safe because liquidityNet cannot be type(int128).min
          if (zeroForOne):
            liquidityNet = liquidityNet * -1
          state.liquidity = LiquidityMath.addDelta(state.liquidity, liquidityNet)

        state.tick = step.tickNext - 1 if zeroForOne else step.tickNext

      elif (state.sqrtPriceX96 != step.sqrtPriceStartX96):
        # recompute unless we're on a lower tick boundary (i.e. already transitioned ticks), and haven't moved
        state.tick = TickMath.getTickAtSqrtRatio(state.sqrtPriceX96)

    return SwapResult (
      state.amountCalculated,
      state.sqrtPriceX96,
      state.liquidity,
      state.tick
    )

  @property
  def tickSpacing(self) -> int:
    return TICK_SPACINGS[self.fee]