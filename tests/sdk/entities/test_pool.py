import unittest

from convexus.icontoolkit.expect import expect
from convexus.sdk.constants import TICK_SPACINGS, FeeAmount
from convexus.sdkcore.entities.currency import Token

from convexus.sdk.utils.encodeSqrtRatioX96 import encodeSqrtRatioX96
from convexus.sdk.entities.pool import Pool
from convexus.sdk.utils.tickMath import TickMath

from convexus.sdk.entities.tick import TickConstructorArgs
from convexus.sdk.utils.nearestUsableTick import nearestUsableTick
from convexus.sdkcore.entities.fractions.currencyAmount import CurrencyAmount

from TestPoolFactoryProvider import TestPoolFactoryProvider

ONE_ICX = 10**18
USDC = Token('cxa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48', 6, 'USDC', 'USD Coin')
DAI = Token('cx6b175474e89094c44da98b954eedeac495271d0f', 18, 'DAI', 'DAI Stablecoin')
BNUSD = Token('cx6b175474e89094c44da98b954eedeac495271d0e', 18, 'bnUSD', 'Balanced USD')
pool = Pool(USDC, DAI, FeeAmount.LOW, encodeSqrtRatioX96(1, 1), 0, 0, [])

class TestPool(unittest.TestCase):

  def test_feeMustBeInteger(self):
    expect(lambda: 
      Pool(USDC, DAI, FeeAmount.MEDIUM + 0.5, encodeSqrtRatioX96(1, 1), 0, 0, [])).toThrow(AssertionError, 'FEE')
  
  def test_feeCannotBeMoreThan1e6(self):
    expect(lambda:
      Pool(USDC, DAI, 1e6, encodeSqrtRatioX96(1, 1), 0, 0, [])
    ).toThrow(AssertionError, 'FEE')
  
  def test_DifferentDecimalsPoolPrice(self):
    t0_18 = Token('cx0000000000000000000000000000000000000000', 18)
    t1_6 = Token('cx0000000000000000000000000000000000000001', 6)
    
    poolPrice = encodeSqrtRatioX96(
      10**6,
      10**18
    )

    pool = Pool(
      t0_18, 
      t1_6, 
      FeeAmount.MEDIUM,
      poolPrice, 
      0, 
      TickMath.getTickAtSqrtRatio(poolPrice)
    )

    expect(pool.token0Price.toFixed(4)).toEqual('1')
  
  def test_05PoolPrice(self):
    decimals0 = 18
    decimals1 = 6

    t0_18 = Token('cx0000000000000000000000000000000000000000', decimals0)
    t1_6 = Token('cx0000000000000000000000000000000000000001', decimals1)

    # We want to encode price 0.5
    price = 0.5
    precision = 18 # limit the precision at 18 decimals precision
    precision_exp = 10**precision
    price_exp = price * precision_exp
    amount0 = int(precision_exp)
    amount1 = int(price_exp)

    decimals0_exp = 10**decimals0
    decimals1_exp = 10**decimals1

    poolPrice = encodeSqrtRatioX96(
      amount1 * decimals1_exp, 
      amount0 * decimals0_exp, 
    )

    pool = Pool(
      t0_18, 
      t1_6, 
      FeeAmount.MEDIUM,
      poolPrice, 
      0, 
      TickMath.getTickAtSqrtRatio(poolPrice)
    )

    expect(pool.token0Price.toFixed(4)).toEqual('0.5')
  
  def test_cannotBeGivenTwoOfTheSameToken(self):
    expect(lambda:
      Pool(USDC, USDC, FeeAmount.MEDIUM, encodeSqrtRatioX96(1, 1), 0, 0, [])
    ).toThrow(AssertionError, 'ADDRESSES')
  
  def test_priceMustBeWithinTickPriceBounds(self):
    expect(lambda:
      Pool(USDC, DAI, FeeAmount.MEDIUM, encodeSqrtRatioX96(1, 1), 0, 1, [])
    ).toThrow(AssertionError, 'PRICE_BOUNDS')
    expect(lambda:
      Pool(USDC, DAI, FeeAmount.MEDIUM, (encodeSqrtRatioX96(1, 1) + 1), 0, -1, [])
    ).toThrow(AssertionError, 'PRICE_BOUNDS')
  
  def test_worksWithValidArgumentsForEmptyPoolMediumFee(self):
    Pool(USDC, DAI, FeeAmount.MEDIUM, encodeSqrtRatioX96(1, 1), 0, 0, [])
  
  def test_worksWithValidArgumentsForEmptyPoolLowFee(self):
    Pool(USDC, DAI, FeeAmount.LOW, encodeSqrtRatioX96(1, 1), 0, 0, [])
  
  def test_worksWithValidArgumentsForEmptyPoolLowestFee(self):
    Pool(USDC, DAI, FeeAmount.LOWEST, encodeSqrtRatioX96(1, 1), 0, 0, [])
  
  def test_worksWithValidArgumentsForEmptyPoolHighFee(self):
    Pool(USDC, DAI, FeeAmount.HIGH, encodeSqrtRatioX96(1, 1), 0, 0, [])
    
  def test_matchesAnExample(self):
    factory = TestPoolFactoryProvider()
    result = Pool.getAddress(factory, USDC, DAI, FeeAmount.LOW)
    expect(result).toEqual('cx41cb9a6b41cba89e41cb9c2241cba0f241cba129')
        
  def test_alwaysIsTheTokenThatSortsBefore(self):
    pool = Pool(USDC, DAI, FeeAmount.LOW, encodeSqrtRatioX96(1, 1), 0, 0, [])
    expect(pool.token0).toEqual(DAI)
    pool = Pool(DAI, USDC, FeeAmount.LOW, encodeSqrtRatioX96(1, 1), 0, 0, [])
    expect(pool.token0).toEqual(DAI)
  
  def test_alwaysIsTheTokenThatSortsAfter(self):
    pool = Pool(USDC, DAI, FeeAmount.LOW, encodeSqrtRatioX96(1, 1), 0, 0, [])
    expect(pool.token1).toEqual(USDC)
    pool = Pool(DAI, USDC, FeeAmount.LOW, encodeSqrtRatioX96(1, 1), 0, 0, [])
    expect(pool.token1).toEqual(USDC)
    
  def test_returnsPriceOfToken0InTermsOfToken1(self):
    expect(
      Pool(
        USDC,
        DAI,
        FeeAmount.LOW,
        encodeSqrtRatioX96(int(101e6), int(100e18)),
        0,
        TickMath.getTickAtSqrtRatio(encodeSqrtRatioX96(int(101e6), int(100e18))),
        []
      ).token0Price.toFixed(5)
    ).toEqual('1.01')
    expect(
      Pool(
        DAI,
        USDC,
        FeeAmount.LOW,
        encodeSqrtRatioX96(int(101e6), int(100e18)),
        0,
        TickMath.getTickAtSqrtRatio(encodeSqrtRatioX96(int(101e6), int(100e18))),
        []
      ).token0Price.toFixed(5)
    ).toEqual('1.01')
    
  def test_returnsPriceOfToken1InTermsOfToken0(self):
    expect(
      Pool(
        USDC,
        DAI,
        FeeAmount.LOW,
        encodeSqrtRatioX96(int(101e6), int(100e18)),
        0,
        TickMath.getTickAtSqrtRatio(encodeSqrtRatioX96(int(101e6), int(100e18))),
        []
      ).token1Price.toFixed(5)
    ).toEqual('0.9901')
    expect(
      Pool(
        DAI,
        USDC,
        FeeAmount.LOW,
        encodeSqrtRatioX96(int(101e6), int(100e18)),
        0,
        TickMath.getTickAtSqrtRatio(encodeSqrtRatioX96(int(101e6), int(100e18))),
        []
      ).token1Price.toFixed(5)
    ).toEqual('0.9901')
    
  def test_returnsPriceOfTokenInTermsOfOtherToken(self):
    expect(pool.priceOf(DAI)).toEqual(pool.token0Price)
    expect(pool.priceOf(USDC)).toEqual(pool.token1Price)
  
  def test_throwsIfInvalidToken(self):
    expect(lambda:
      pool.priceOf(BNUSD)).toThrow(AssertionError, 'TOKEN')
    
  def test_equals(self):
    pool = Pool(USDC, DAI, FeeAmount.LOW, encodeSqrtRatioX96(1, 1), 0, 0, [])
    expect(pool.involvesToken(USDC)).toEqual(True)
    expect(pool.involvesToken(DAI)).toEqual(True)
    
  pool: Pool


class TestPoolSwap(unittest.TestCase):

  def setUp(self):
    super().setUp()
    self.pool = Pool(USDC, DAI, FeeAmount.LOW, encodeSqrtRatioX96(1, 1), ONE_ICX, 0, [
      TickConstructorArgs(
        index= nearestUsableTick(TickMath.MIN_TICK, TICK_SPACINGS[FeeAmount.LOW]),
        liquidityNet= ONE_ICX,
        liquidityGross= ONE_ICX
      ),
      TickConstructorArgs (
        index=nearestUsableTick(TickMath.MAX_TICK, TICK_SPACINGS[FeeAmount.LOW]),
        liquidityNet=ONE_ICX * -1,
        liquidityGross=ONE_ICX
      )
    ])

  def test_USDCToDAI_0(self):
    inputAmount = CurrencyAmount.fromRawAmount(USDC, 100)
    outputAmount, _ = self.pool.getOutputAmount(inputAmount)
    expect(outputAmount.currency.equals(DAI)).toBe(True)
    expect(outputAmount.quotient).toEqual(98)

  def test_DAIToUSDC_0(self):
    inputAmount = CurrencyAmount.fromRawAmount(DAI, 100)
    outputAmount, _ = self.pool.getOutputAmount(inputAmount)
    expect(outputAmount.currency.equals(USDC)).toBe(True)
    expect(outputAmount.quotient).toEqual(98)

  def test_USDCToDAI_1(self):
    outputAmount = CurrencyAmount.fromRawAmount(DAI, 98)
    inputAmount, _ = self.pool.getInputAmount(outputAmount)
    expect(inputAmount.currency.equals(USDC)).toBe(True)
    expect(inputAmount.quotient).toEqual(100)
  
  def test_DAIToUSDC_1(self):
    outputAmount = CurrencyAmount.fromRawAmount(USDC, 98)
    inputAmount, _ = self.pool.getInputAmount(outputAmount)
    expect(inputAmount.currency.equals(DAI)).toBe(True)
    expect(inputAmount.quotient).toEqual(100)
  