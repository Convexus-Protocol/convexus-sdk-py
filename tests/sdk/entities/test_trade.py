import unittest
from convexus.icontoolkit.expect import expect

from convexus.sdk.constants import TICK_SPACINGS, FeeAmount
from convexus.sdk.entities.factoryProvider import PoolFactoryProvider
from convexus.sdkcore.constants import TradeType
from convexus.sdkcore.entities.currency import Token

from convexus.sdk.utils.encodeSqrtRatioX96 import encodeSqrtRatioX96
from convexus.sdk.entities.pool import Pool
from convexus.sdk.utils.tickMath import TickMath

from convexus.sdk.utils.nearestUsableTick import nearestUsableTick
from convexus.sdkcore.entities.fractions.percent import Percent
from convexus.sdkcore.entities.fractions.price import Price
from convexus.sdkcore.entities.icx import Icx
from convexus.sdk.entities.route import Route

from convexus.sdk.entities.trade import BestTradeOptions, RouteInfo, Trade, RouteAmount, TradeConstructorArgs, UncheckedTradeConstructorArguments
from convexus.sdkcore.utils.sqrt import sqrt
from convexus.sdkcore.entities.fractions.currencyAmount import CurrencyAmount
from convexus.sdk.entities.tick import TickConstructorArgs, Tick
from TestPoolFactoryProvider import TestPoolFactoryProvider

ICX = Icx()
WICX = ICX.wrapped
token0 = Token('cx0000000000000000000000000000000000000001', 18, 't0', 'token0')
token1 = Token('cx0000000000000000000000000000000000000002', 18, 't1', 'token1')
token2 = Token('cx0000000000000000000000000000000000000003', 18, 't2', 'token2')
token3 = Token('cx0000000000000000000000000000000000000004', 18, 't3', 'token3')

poolFactoryProvider = TestPoolFactoryProvider()

def simplePool(
  reserve0: CurrencyAmount,
  reserve1: CurrencyAmount,
  feeAmount: FeeAmount = FeeAmount.MEDIUM
):
  sqrtRatioX96 = encodeSqrtRatioX96(reserve1.quotient, reserve0.quotient)
  liquidity = sqrt((reserve0.quotient * reserve1.quotient))
  return Pool(
    reserve0.currency,
    reserve1.currency,
    feeAmount,
    sqrtRatioX96,
    liquidity,
    TickMath.getTickAtSqrtRatio(sqrtRatioX96), [
      TickConstructorArgs(
        index=nearestUsableTick(TickMath.MIN_TICK, TICK_SPACINGS[feeAmount]),
        liquidityNet=liquidity,
        liquidityGross=liquidity
      ),
      TickConstructorArgs(
        index=nearestUsableTick(TickMath.MAX_TICK, TICK_SPACINGS[feeAmount]),
        liquidityNet=(liquidity * -1),
        liquidityGross=liquidity
      )
    ]
  )

pool_0_1 = simplePool(
  CurrencyAmount.fromRawAmount(token0, 100000),
  CurrencyAmount.fromRawAmount(token1, 100000)
)
pool_0_2 = simplePool(
  CurrencyAmount.fromRawAmount(token0, 100000),
  CurrencyAmount.fromRawAmount(token2, 110000)
)
pool_0_3 = simplePool(
  CurrencyAmount.fromRawAmount(token0, 100000),
  CurrencyAmount.fromRawAmount(token3, 90000)
)
pool_1_2 = simplePool(
  CurrencyAmount.fromRawAmount(token1, 120000),
  CurrencyAmount.fromRawAmount(token2, 100000)
)
pool_1_3 = simplePool(
  CurrencyAmount.fromRawAmount(token1, 120000),
  CurrencyAmount.fromRawAmount(token3, 130000)
)

pool_wicx_0 = simplePool(
  CurrencyAmount.fromRawAmount(WICX, (100000)),
  CurrencyAmount.fromRawAmount(token0, (100000))
)

pool_wicx_1 = simplePool(
  CurrencyAmount.fromRawAmount(WICX, (100000)),
  CurrencyAmount.fromRawAmount(token1, (100000))
)

pool_wicx_2 = simplePool(
  CurrencyAmount.fromRawAmount(WICX, (100000)),
  CurrencyAmount.fromRawAmount(token2, (100000))
)

class TestTrade(unittest.TestCase):

  def test_canBeConstructedWithICXAsInput(self):
    trade = Trade.fromRoute(
      poolFactoryProvider,
      Route([pool_wicx_0], ICX, token0),
      CurrencyAmount.fromRawAmount(ICX, (10000)),
      TradeType.EXACT_INPUT
    )
    expect(trade.inputAmount.currency).toEqual(ICX)
    expect(trade.outputAmount.currency).toEqual(token0)
  def test_canBeConstructedWithICXAsInputForExactOutput(self):
    trade = Trade.fromRoute(
      poolFactoryProvider,
      Route([pool_wicx_0], ICX, token0),
      CurrencyAmount.fromRawAmount(token0, (10000)),
      TradeType.EXACT_OUTPUT
    )
    expect(trade.inputAmount.currency).toEqual(ICX)
    expect(trade.outputAmount.currency).toEqual(token0)

  def test_canBeConstructedWithICXAsOutput(self):
    trade = Trade.fromRoute(
      poolFactoryProvider,
      Route([pool_wicx_0], token0, ICX),
      CurrencyAmount.fromRawAmount(ICX, (10000)),
      TradeType.EXACT_OUTPUT
    )
    expect(trade.inputAmount.currency).toEqual(token0)
    expect(trade.outputAmount.currency).toEqual(ICX)
  def test_canBeConstructedWithICXAsOutputForExactInput(self):
    trade = Trade.fromRoute(
      poolFactoryProvider,
      Route([pool_wicx_0], token0, ICX),
      CurrencyAmount.fromRawAmount(token0, (10000)),
      TradeType.EXACT_INPUT
    )
    expect(trade.inputAmount.currency).toEqual(token0)
    expect(trade.outputAmount.currency).toEqual(ICX)

  def test_canBeConstructedWithICXAsInputWithMultipleRoutes(self):
    trade = Trade.fromRoutes(
      poolFactoryProvider,
      [
        RouteAmount(
          amount=CurrencyAmount.fromRawAmount(ICX, (10000)),
          route=Route([pool_wicx_0], ICX, token0)
        )
      ],
      TradeType.EXACT_INPUT
    )
    expect(trade.inputAmount.currency).toEqual(ICX)
    expect(trade.outputAmount.currency).toEqual(token0)

  def test_canBeConstructedWithICXAsInputForExactOutputWithMultipleRoutes(self):
    trade = Trade.fromRoutes(
      poolFactoryProvider,
      [
        RouteAmount(
          amount=CurrencyAmount.fromRawAmount(token0, (3000)),
          route=Route([pool_wicx_0], ICX, token0)
        ),
        RouteAmount(
          amount=CurrencyAmount.fromRawAmount(token0, (7000)),
          route=Route([pool_wicx_1, pool_0_1], ICX, token0)
        )
      ],
      TradeType.EXACT_OUTPUT
    )
    expect(trade.inputAmount.currency).toEqual(ICX)
    expect(trade.outputAmount.currency).toEqual(token0)

  def test_canBeConstructedWithICXAsOutputWithMultipleRoutes(self):
    trade = Trade.fromRoutes(
      poolFactoryProvider,
      [
        RouteAmount(
          amount=CurrencyAmount.fromRawAmount(ICX, (4000)),
          route=Route([pool_wicx_0], token0, ICX)
        ),
        RouteAmount(
          amount=CurrencyAmount.fromRawAmount(ICX, (6000)),
          route=Route([pool_0_1, pool_wicx_1], token0, ICX)
        )
      ],
      TradeType.EXACT_OUTPUT
    )
    expect(trade.inputAmount.currency).toEqual(token0)
    expect(trade.outputAmount.currency).toEqual(ICX)
  def test_canBeConstructedWithICXAsOutputForExactInputWithMultipleRoutes(self):
    trade = Trade.fromRoutes(
      poolFactoryProvider,
      [
        RouteAmount(
          amount=CurrencyAmount.fromRawAmount(token0, (3000)),
          route=Route([pool_wicx_0], token0, ICX)
        ),
        RouteAmount(
          amount=CurrencyAmount.fromRawAmount(token0, (7000)),
          route=Route([pool_0_1, pool_wicx_1], token0, ICX)
        )
      ],
      TradeType.EXACT_INPUT
    )
    expect(trade.inputAmount.currency).toEqual(token0)
    expect(trade.outputAmount.currency).toEqual(ICX)

  def test_throwsIfPoolsAreReUsedBetweenRoutes(self):
    expect(
      lambda: Trade.fromRoutes(
        poolFactoryProvider,
        [
          RouteAmount(
            amount=CurrencyAmount.fromRawAmount(token0, (4500)),
            route=Route([pool_0_1, pool_wicx_1], token0, ICX)
          ),
          RouteAmount(
            amount=CurrencyAmount.fromRawAmount(token0, (5500)),
            route=Route([pool_0_1, pool_1_2, pool_wicx_2], token0, ICX)
          )
        ],
        TradeType.EXACT_INPUT
      )
    ).toThrow(AssertionError, 'POOLS_DUPLICATED')

  def test_throwsIfInputCurrencyDoesNotMatchRoute(self):
    expect(lambda: 
      Trade.createUncheckedTrade(
      poolFactoryProvider, UncheckedTradeConstructorArguments(
          route=Route([pool_0_1], token0, token1),
          inputAmount=CurrencyAmount.fromRawAmount(token2, 10000),
          outputAmount=CurrencyAmount.fromRawAmount(token1, 10000),
          tradeType=TradeType.EXACT_INPUT
        )
      )
    ).toThrow(AssertionError, 'INPUT_CURRENCY_MATCH')

  def test_throwsIfOutputCurrencyDoesNotMatchRoute(self):
    expect(lambda:
      Trade.createUncheckedTrade(
        poolFactoryProvider, UncheckedTradeConstructorArguments(
          route=Route([pool_0_1], token0, token1),
          inputAmount=CurrencyAmount.fromRawAmount(token0, 10000),
          outputAmount=CurrencyAmount.fromRawAmount(token2, 10000),
          tradeType=TradeType.EXACT_INPUT
        )
      )
    ).toThrow(AssertionError, 'OUTPUT_CURRENCY_MATCH')
  
  def test_canCreateAnExactInputTradeWithoutSimulating(self):
    Trade.createUncheckedTrade(
      poolFactoryProvider, UncheckedTradeConstructorArguments(
        route=Route([pool_0_1], token0, token1),
        inputAmount=CurrencyAmount.fromRawAmount(token0, 10000),
        outputAmount=CurrencyAmount.fromRawAmount(token1, 100000),
        tradeType=TradeType.EXACT_INPUT
      )
    )
  
  def test_canCreateAnExactOutputTradeWithoutSimulating(self):
    Trade.createUncheckedTrade(
      poolFactoryProvider, UncheckedTradeConstructorArguments(
        route=Route([pool_0_1], token0, token1),
        inputAmount=CurrencyAmount.fromRawAmount(token0, 10000),
        outputAmount=CurrencyAmount.fromRawAmount(token1, 100000),
        tradeType=TradeType.EXACT_OUTPUT
      )
    )
  
  def test_throwsIfInputCurrencyDoesNotMatchRouteWithMultipleRoutes(self):
    expect(lambda:
      Trade.createUncheckedTradeWithMultipleRoutes(poolFactoryProvider, TradeConstructorArgs(
        routes=[
          RouteInfo(
            route=Route([pool_1_2], token2, token1),
            inputAmount=CurrencyAmount.fromRawAmount(token2, 2000),
            outputAmount=CurrencyAmount.fromRawAmount(token1, 2000)
          ),
          RouteInfo(
            route=Route([pool_0_1], token0, token1),
            inputAmount=CurrencyAmount.fromRawAmount(token2, 8000),
            outputAmount=CurrencyAmount.fromRawAmount(token1, 8000)
          )
        ],
        tradeType=TradeType.EXACT_INPUT
      ))
    ).toThrow(AssertionError, 'INPUT_CURRENCY_MATCH')

  def test_throwsIfOutputCurrencyDoesNotMatchRouteWithMultipleRoutes(self):
    expect(lambda:
      Trade.createUncheckedTradeWithMultipleRoutes(poolFactoryProvider, TradeConstructorArgs(
        routes=[
          RouteInfo(
            route=Route([pool_0_2], token0, token2),
            inputAmount=CurrencyAmount.fromRawAmount(token0, 10000),
            outputAmount=CurrencyAmount.fromRawAmount(token2, 10000)
          ),
          RouteInfo(
            route=Route([pool_0_1], token0, token1),
            inputAmount=CurrencyAmount.fromRawAmount(token0, 10000),
            outputAmount=CurrencyAmount.fromRawAmount(token2, 10000)
          )
        ],
        tradeType=TradeType.EXACT_INPUT
      ))
    ).toThrow(AssertionError, 'OUTPUT_CURRENCY_MATCH')

  def test_canCreateAnExactInputTradeWithoutSimulatingWithMultipleRoutes(self):
    Trade.createUncheckedTradeWithMultipleRoutes(poolFactoryProvider, TradeConstructorArgs(
      routes=[
        RouteInfo(
          route=Route([pool_0_1], token0, token1),
          inputAmount=CurrencyAmount.fromRawAmount(token0, 5000),
          outputAmount=CurrencyAmount.fromRawAmount(token1, 50000)
        ),
        RouteInfo(
          route=Route([pool_0_2, pool_1_2], token0, token1),
          inputAmount=CurrencyAmount.fromRawAmount(token0, 5000),
          outputAmount=CurrencyAmount.fromRawAmount(token1, 50000)
        )
      ],
      tradeType=TradeType.EXACT_INPUT
    ))

  def test_canCreateAnExactOutputTradeWithoutSimulatingWithMultipleRoutes(self):
    Trade.createUncheckedTradeWithMultipleRoutes(poolFactoryProvider, TradeConstructorArgs(
      routes=[
        RouteInfo(
          route=Route([pool_0_1], token0, token1),
          inputAmount=CurrencyAmount.fromRawAmount(token0, 5001),
          outputAmount=CurrencyAmount.fromRawAmount(token1, 50000)
        ),
        RouteInfo(
          route=Route([pool_0_2, pool_1_2], token0, token1),
          inputAmount=CurrencyAmount.fromRawAmount(token0, 4999),
          outputAmount=CurrencyAmount.fromRawAmount(token1, 50000)
        )
      ],
      tradeType=TradeType.EXACT_OUTPUT
    ))


class TestTradeWithRoutes(unittest.TestCase):

  def setUp(self) -> None:
    super().setUp()

    self.singleRoute = Trade.createUncheckedTrade(poolFactoryProvider, UncheckedTradeConstructorArguments(
      route=Route([pool_0_1, pool_1_2], token0, token2),
      inputAmount=CurrencyAmount.fromRawAmount(token0, 100),
      outputAmount=CurrencyAmount.fromRawAmount(token2, 69),
      tradeType=TradeType.EXACT_INPUT
    ))

    self.multiRoute = Trade.createUncheckedTradeWithMultipleRoutes(poolFactoryProvider, TradeConstructorArgs(
      routes=[
        RouteInfo(
          route=Route([pool_0_1, pool_1_2], token0, token2),
          inputAmount=CurrencyAmount.fromRawAmount(token0, 50),
          outputAmount=CurrencyAmount.fromRawAmount(token2, 35)
        ),
        RouteInfo(
          route=Route([pool_0_2], token0, token2),
          inputAmount=CurrencyAmount.fromRawAmount(token0, 50),
          outputAmount=CurrencyAmount.fromRawAmount(token2, 34)
        )
      ],
      tradeType=TradeType.EXACT_INPUT
    ))

    self.exactIn = Trade.createUncheckedTrade(poolFactoryProvider, UncheckedTradeConstructorArguments(
      route=Route([pool_0_1, pool_1_2], token0, token2),
      inputAmount=CurrencyAmount.fromRawAmount(token0, 100),
      outputAmount=CurrencyAmount.fromRawAmount(token2, 69),
      tradeType=TradeType.EXACT_INPUT
    ))

    self.exactInMultiRoute = Trade.createUncheckedTradeWithMultipleRoutes(poolFactoryProvider, TradeConstructorArgs(
      routes=[
        RouteInfo(
          route=Route([pool_0_1, pool_1_2], token0, token2),
          inputAmount=CurrencyAmount.fromRawAmount(token0, 50),
          outputAmount=CurrencyAmount.fromRawAmount(token2, 35)
        ),
        RouteInfo(
          route=Route([pool_0_2], token0, token2),
          inputAmount=CurrencyAmount.fromRawAmount(token0, 50),
          outputAmount=CurrencyAmount.fromRawAmount(token2, 34)
        )
      ],
      tradeType=TradeType.EXACT_INPUT
    ))

    self.exactOut = Trade.createUncheckedTrade(poolFactoryProvider, UncheckedTradeConstructorArguments(
      route=Route([pool_0_1, pool_1_2], token0, token2),
      inputAmount=CurrencyAmount.fromRawAmount(token0, 156),
      outputAmount=CurrencyAmount.fromRawAmount(token2, 100),
      tradeType=TradeType.EXACT_OUTPUT
    ))

    self.exactOutMultiRoute = Trade.createUncheckedTradeWithMultipleRoutes(poolFactoryProvider, TradeConstructorArgs(
      routes=[
        RouteInfo(
          route=Route([pool_0_1, pool_1_2], token0, token2),
          inputAmount=CurrencyAmount.fromRawAmount(token0, 78),
          outputAmount=CurrencyAmount.fromRawAmount(token2, 50)
        ),
        RouteInfo(
          route=Route([pool_0_2], token0, token2),
          inputAmount=CurrencyAmount.fromRawAmount(token0, 78),
          outputAmount=CurrencyAmount.fromRawAmount(token2, 50)
        )
      ],
      tradeType=TradeType.EXACT_OUTPUT
    ))

  
  def test_canAccessRouteForSingleRouteTradeIfLessThan0(self):
    expect(self.singleRoute.route).toBeDefined()

  def test_canAccessRoutesForBothSingleAndMultiRouteTrades(self):
    expect(self.singleRoute.swaps).toBeDefined()
    expect(self.singleRoute.swaps).toHaveLength(1)
    expect(self.multiRoute.swaps).toBeDefined()
    expect(self.multiRoute.swaps).toHaveLength(2)

  def test_throwsIfAccessRouteOnMultiRouteTrade(self):
    expect(lambda: self.multiRoute.route).toThrow(AssertionError, 'MULTIPLE_ROUTES')

  def test_throwsIfLessThan0_5(self):
    expect(lambda: self.exactIn.minimumAmountOut(Percent(-1, 100))).toThrow(AssertionError, 'SLIPPAGE_TOLERANCE')
  
  def test_returnsExactIf0_5(self):
    expect(self.exactIn.worstExecutionPrice(Percent(0, 100))).toEqual(self.exactIn.executionPrice)
  
  def test_returnsExactIfNonzero(self):
    expect(self.exactIn.worstExecutionPrice(Percent(0, 100))).toEqual(Price(token0, token2, 100, 69))
    expect(self.exactIn.worstExecutionPrice(Percent(5, 100))).toEqual(Price(token0, token2, 100, 65))
    expect(self.exactIn.worstExecutionPrice(Percent(200, 100))).toEqual(Price(token0, token2, 100, 23))
  
  def test_returnsExactIfNonzeroWithMultipleRoutes_1(self):
    expect(self.exactInMultiRoute.worstExecutionPrice(Percent(0, 100))).toEqual(Price(token0, token2, 100, 69))
    expect(self.exactInMultiRoute.worstExecutionPrice(Percent(5, 100))).toEqual(Price(token0, token2, 100, 65))
    expect(self.exactInMultiRoute.worstExecutionPrice(Percent(200, 100))).toEqual(Price(token0, token2, 100, 23))
  
  def test_throwsIfLessThan0_0(self):
    expect(lambda: self.exactOut.worstExecutionPrice(Percent(-1, 100))).toThrow(AssertionError, 'SLIPPAGE_TOLERANCE')
  
  def test_returnsExactIf0_0(self):
    expect(self.exactOut.worstExecutionPrice(Percent(0, 100))).toEqual(self.exactOut.executionPrice)
  
  def test_returnsSlippageAmountIfNonzero(self):
    expect(
      self.exactOut.worstExecutionPrice(Percent(0, 100)).equalTo(Price(token0, token2, 156, 100))
    ).toBeTruthy()
    expect(
      self.exactOut.worstExecutionPrice(Percent(5, 100)).equalTo(Price(token0, token2, 163, 100))
    ).toBeTruthy()
    expect(
      self.exactOut.worstExecutionPrice(Percent(200, 100)).equalTo(Price(token0, token2, 468, 100))
    ).toBeTruthy()
  
  def test_returnsExactIfNonzeroWithMultipleRoutes_0(self):
    expect(
      self.exactOutMultiRoute.worstExecutionPrice(Percent(0, 100)).equalTo(Price(token0, token2, 156, 100))
    ).toBeTruthy()
    expect(
      self.exactOutMultiRoute.worstExecutionPrice(Percent(5, 100)).equalTo(Price(token0, token2, 163, 100))
    ).toBeTruthy()
    expect(
      self.exactOutMultiRoute.worstExecutionPrice(Percent(200, 100)).equalTo(Price(token0, token2, 468, 100))
    ).toBeTruthy()

class TestTradeWithRoutesInput2(unittest.TestCase):

  def setUp(self) -> None:
    super().setUp()

    self.exactIn = Trade.createUncheckedTradeWithMultipleRoutes(poolFactoryProvider, TradeConstructorArgs(
      routes=[
        RouteInfo(
          route=Route([pool_0_1, pool_1_2], token0, token2),
          inputAmount=CurrencyAmount.fromRawAmount(token0, 100),
          outputAmount=CurrencyAmount.fromRawAmount(token2, 69)
        )
      ],
      tradeType=TradeType.EXACT_INPUT
    ))

    self.exactInMultipleRoutes = Trade.createUncheckedTradeWithMultipleRoutes(poolFactoryProvider, TradeConstructorArgs(
      routes=[
        RouteInfo(
          route=Route([pool_0_1, pool_1_2], token0, token2),
          inputAmount=CurrencyAmount.fromRawAmount(token0, 90),
          outputAmount=CurrencyAmount.fromRawAmount(token2, 62)
        ),
        RouteInfo(
          route=Route([pool_0_2], token0, token2),
          inputAmount=CurrencyAmount.fromRawAmount(token0, 10),
          outputAmount=CurrencyAmount.fromRawAmount(token2, 7)
        )
      ],
      tradeType=TradeType.EXACT_INPUT
    ))

  def test_isCached(self):
    expect(self.exactIn.priceImpact == self.exactIn.priceImpact).toStrictEqual(True)
  
  def test_isCorrect(self):
    expect(self.exactIn.priceImpact.toFixed(1)).toEqual('17.2')

  def test_isCachedWithMultipleRoutes(self):
    expect(self.exactInMultipleRoutes.priceImpact == self.exactInMultipleRoutes.priceImpact).toStrictEqual(True)
  
  def test_isCorrectWithMultipleRoutes(self):
    expect(self.exactInMultipleRoutes.priceImpact.toFixed(1)).toEqual('19.8')
  

class TestTradeWithRoutesOutput2(unittest.TestCase):

  def setUp(self) -> None:
    super().setUp()

    self.exactOut = Trade.createUncheckedTradeWithMultipleRoutes(poolFactoryProvider, TradeConstructorArgs(
      routes=[
        RouteInfo(
          route=Route([pool_0_1, pool_1_2], token0, token2),
          inputAmount=CurrencyAmount.fromRawAmount(token0, 156),
          outputAmount=CurrencyAmount.fromRawAmount(token2, 100)
        )
      ],
      tradeType=TradeType.EXACT_OUTPUT
    ))
    
    self.exactOutMultipleRoutes = Trade.createUncheckedTradeWithMultipleRoutes(poolFactoryProvider, TradeConstructorArgs(
      routes=[
        RouteInfo(
          route=Route([pool_0_1, pool_1_2], token0, token2),
          inputAmount=CurrencyAmount.fromRawAmount(token0, 140),
          outputAmount=CurrencyAmount.fromRawAmount(token2, 90)
        ),
        RouteInfo(
          route=Route([pool_0_2], token0, token2),
          inputAmount=CurrencyAmount.fromRawAmount(token0, 16),
          outputAmount=CurrencyAmount.fromRawAmount(token2, 10)
        )
      ],
      tradeType=TradeType.EXACT_OUTPUT
    ))

  def test_isCached(self):
    expect(self.exactOut.priceImpact == self.exactOut.priceImpact).toStrictEqual(True)
  
  def test_isCorrect(self):
    expect(self.exactOut.priceImpact.toFixed(3)).toEqual('23.077')

  def test_isCachedWithMultipleRoutes(self):
    expect(self.exactOutMultipleRoutes.priceImpact == self.exactOutMultipleRoutes.priceImpact).toStrictEqual(True)
  
  def test_isCorrectWithMultipleRoutes(self):
    expect(self.exactOutMultipleRoutes.priceImpact.toFixed(3)).toEqual('25.521')

  def test_throwsWithEmptyPools(self):
    expect(lambda:
      Trade.bestTradeExactIn(poolFactoryProvider, [], CurrencyAmount.fromRawAmount(token0, (10000)), token2)
    ).toThrow(AssertionError, 'POOLS')
  
  def test_throwsWithMaxHopsOf0(self):
    expect(lambda:
      Trade.bestTradeExactIn(poolFactoryProvider, [pool_0_2], CurrencyAmount.fromRawAmount(token0, (10000)), token2, BestTradeOptions(maxHops=0)
    )).toThrow(AssertionError, 'MAX_HOPS')

  def test_providesBestRoute(self):
    result = Trade.bestTradeExactIn(
      poolFactoryProvider, 
      [pool_0_1, pool_0_2, pool_1_2],
      CurrencyAmount.fromRawAmount(token0, 10000),
      token2
    )

    expect(result).toHaveLength(2)
    expect(result[0].swaps[0].route.pools).toHaveLength(1) # 0 -> 2 at 10:11
    expect(result[0].swaps[0].route.tokenPath).toEqual([token0, token2])
    expect(result[0].inputAmount.equalTo(CurrencyAmount.fromRawAmount(token0, (10000)))).toBeTruthy()
    expect(result[0].outputAmount.equalTo(CurrencyAmount.fromRawAmount(token2, (9972)))).toBeTruthy()
    expect(result[1].swaps[0].route.pools).toHaveLength(2) # 0 -> 1 -> 2 at 12:12:10
    expect(result[1].swaps[0].route.tokenPath).toEqual([token0, token1, token2])
    expect(result[1].inputAmount.equalTo(CurrencyAmount.fromRawAmount(token0, (10000)))).toBeTruthy()
    expect(result[1].outputAmount.equalTo(CurrencyAmount.fromRawAmount(token2, (7004)))).toBeTruthy()

  def test_respectsMaxHops_0(self):
    result = Trade.bestTradeExactIn(
      poolFactoryProvider, 
      [pool_0_1, pool_0_2, pool_1_2],
      CurrencyAmount.fromRawAmount(token0, (10)),
      token2,
      BestTradeOptions(maxHops=1)
    )

    expect(result).toHaveLength(1)
    expect(result[0].swaps[0].route.pools).toHaveLength(1) # 0 -> 2 at 10:11
    expect(result[0].swaps[0].route.tokenPath).toEqual([token0, token2])

  def test_complexRouting(self):
    sICX = Token("cx79ada8b605380c84507d42534080ada30c77602c", 18, "sICX", "sICX")
    USDC = Token("cxa818e190782c7bc64c1ec12512c7f8f3171fc8cf", 18, "USDC", "USDC")
    ICX = Token("cx1111111111111111111111111111111111111111", 18, "ICX", "ICX")
    WETH = Token("cx1126c5dc7115daea7f55d6b6cf0eb63adeb3529f", 18, "WETH", "WETH")
    bnUSD = Token("cxc8373f6f2654a9c8b689059aef58aefb9f878e12", 18, "bnUSD", "bnUSD")
    CRV = Token("cxc8373f6f2654a9c8b689059aef58aefb9f878e12", 18, "CRV", "CRV")

    sICX_USDC = Pool (
      sICX, USDC,
      FeeAmount.MEDIUM,
      '61210590602354947969986',
      '29088496039794855',
      -281485,
      [
        Tick(TickConstructorArgs(
          index=-288360,
          liquidityGross=29088496039794855,
          liquidityNet=29088496039794855,
        )),
        Tick(TickConstructorArgs(
          index=-274500,
          liquidityGross=29088496039794855,
          liquidityNet=-29088496039794855,
        ))
      ]
    )

    ICX_USDC = Pool (
      ICX, USDC,
      FeeAmount.MEDIUM,
      '61191168163216135731103',
      '264440873089043',
      -281491,
      [
        Tick(TickConstructorArgs(
          index=-288360,
          liquidityGross=264440873089043,
          liquidityNet=264440873089043,
        )),
        Tick(TickConstructorArgs(
          index=-274500,
          liquidityGross=264440873089043,
          liquidityNet=-264440873089043,
        ))
      ]
    )

    WETH_CRV = Pool (
      WETH, CRV,
      FeeAmount.MEDIUM,
      '2926083861933460079174379110400',
      '13958146132191485413231',
      72185,
      [
        Tick(TickConstructorArgs(
          index=65280,
          liquidityGross=13958146132191485413231,
          liquidityNet=13958146132191485413231,
        )),
        Tick(TickConstructorArgs(
          index=79140,
          liquidityGross=13958146132191485413231,
          liquidityNet=-13958146132191485413231,
        ))
      ]
    )

    bnUSD_USDC = Pool (
      bnUSD, USDC,
      FeeAmount.LOW,
      '79249731195721224553149',
      '214688025193493151',
      -276319,
      [
        Tick(TickConstructorArgs(
          index=-277380,
          liquidityGross=214688025193493151,
          liquidityNet=214688025193493151,
        )),
        Tick(TickConstructorArgs(
          index=-275370,
          liquidityGross=214688025193493151,
          liquidityNet=-214688025193493151,
        ))
      ]
    )

    ICX_bnUSD = Pool (
      ICX, bnUSD,
      FeeAmount.MEDIUM,
      '62203837691364529249136597252',
      '10269690441519762194883',
      -4839,
      [
        Tick(TickConstructorArgs(
          index=-6960,
          liquidityGross=10269690441519762194883,
          liquidityNet=10269690441519762194883,
        )),
        Tick(TickConstructorArgs(
          index=-3540,
          liquidityGross=10269690441519762194883,
          liquidityNet=-10269690441519762194883,
        ))
      ]
    )

    ICX_WETH = Pool (
      ICX, WETH,
      FeeAmount.LOW,
      '78538556644749228166681187476',
      '1707481566716281749161',
      -175,
      [
        Tick(TickConstructorArgs(
          index=-6930,
          liquidityGross=1707481566716281749161,
          liquidityNet=1707481566716281749161,
        )),
        Tick(TickConstructorArgs(
          index=-6930,
          liquidityGross=1707481566716281749161,
          liquidityNet=-1707481566716281749161,
        ))
      ]
    )

    addresses = ["cx_sICX_USDC", "cx_ICX_USDC", "cx_WETH_CRV", "cx_bnUSD_USDC", "cx_ICX_bnUSD", "cx_ICX_WETH"]
    pools = [sICX_USDC, ICX_USDC, WETH_CRV, bnUSD_USDC, ICX_bnUSD, ICX_WETH]

    class RoutingPoolFactoryProvider(PoolFactoryProvider):
      def getPool (self, tokenA: Token, tokenB: Token, fee: FeeAmount):
        for i in range(len(pools)):
          pool = pools[i]
          if pool.token0.equals(tokenA) and pool.token1.equals(tokenB) and pool.fee == fee:
            return addresses[i]

        raise Exception("Pool not found")

    Trade.bestTradeExactIn(
      RoutingPoolFactoryProvider(), 
      pools,
      CurrencyAmount.fromRawAmount(ICX, 10000),
      sICX
    )

  def test_insufficientInputForOnePool(self):
    result = Trade.bestTradeExactIn(
      poolFactoryProvider, 
      [pool_0_1, pool_0_2, pool_1_2],
      CurrencyAmount.fromRawAmount(token0, 1),
      token2
    )
    expect(result).toHaveLength(2)
    expect(result[0].swaps[0].route.pools).toHaveLength(1) # 0 -> 2 at 10:11
    expect(result[0].swaps[0].route.tokenPath).toEqual([token0, token2])
    expect(result[0].outputAmount).toEqual(CurrencyAmount.fromRawAmount(token2, 0))

  def test_respectsN(self):
    result = Trade.bestTradeExactIn(
      poolFactoryProvider, 
      [pool_0_1, pool_0_2, pool_1_2],
      CurrencyAmount.fromRawAmount(token0, (10)),
      token2,
      BestTradeOptions(maxNumResults=1)
    )

    expect(result).toHaveLength(1)

  def test_noPath(self):
    result = Trade.bestTradeExactIn(
      poolFactoryProvider, 
      [pool_0_1, pool_0_3, pool_1_3],
      CurrencyAmount.fromRawAmount(token0, (10)),
      token2
    )
    expect(result).toHaveLength(0)

  def test_worksForICXCurrencyInput(self):
    result = Trade.bestTradeExactIn(
      poolFactoryProvider, 
      [pool_wicx_0, pool_0_1, pool_0_3, pool_1_3],
      CurrencyAmount.fromRawAmount(ICX, (100)),
      token3
    )
    expect(result).toHaveLength(2)
    expect(result[0].inputAmount.currency).toEqual(ICX)
    expect(result[0].swaps[0].route.tokenPath).toEqual([WICX, token0, token1, token3])
    expect(result[0].outputAmount.currency).toEqual(token3)
    expect(result[1].inputAmount.currency).toEqual(ICX)
    expect(result[1].swaps[0].route.tokenPath).toEqual([WICX, token0, token3])
    expect(result[1].outputAmount.currency).toEqual(token3)

  def test_worksForICXCurrencyOutput(self):
    result = Trade.bestTradeExactIn(
      poolFactoryProvider, 
      [pool_wicx_0, pool_0_1, pool_0_3, pool_1_3],
      CurrencyAmount.fromRawAmount(token3, (100)),
      ICX
    )
    expect(result).toHaveLength(2)
    expect(result[0].inputAmount.currency).toEqual(token3)
    expect(result[0].swaps[0].route.tokenPath).toEqual([token3, token0, WICX])
    expect(result[0].outputAmount.currency).toEqual(ICX)
    expect(result[1].inputAmount.currency).toEqual(token3)
    expect(result[1].swaps[0].route.tokenPath).toEqual([token3, token1, token0, WICX])
    expect(result[1].outputAmount.currency).toEqual(ICX)

class TestTradeMaximumAmountIn(unittest.TestCase):

  def setUp(self) -> None:
    super().setUp()

    self.exactIn = Trade.fromRoute(
      poolFactoryProvider, 
      Route([pool_0_1, pool_1_2], token0, token2),
      CurrencyAmount.fromRawAmount(token0, (100)),
      TradeType.EXACT_INPUT
    )
  
  def test_throwsIfLessThan0_1(self):
    expect(lambda: self.exactIn.maximumAmountIn(Percent(-1, 100))).toThrow(
      AssertionError,
      'SLIPPAGE_TOLERANCE'
    )

  def test_returnsExactIf0_1(self):
    expect(self.exactIn.maximumAmountIn(Percent(0, 100))).toEqual(self.exactIn.inputAmount)
  
  def test_returnsExactIfNonzero(self):
    expect(
      self.exactIn
        .maximumAmountIn(Percent(0, 100))
        .equalTo(CurrencyAmount.fromRawAmount(token0, (100)))
    ).toBeTruthy()
  
    expect(
      self.exactIn
        .maximumAmountIn(Percent(5, 100))
        .equalTo(CurrencyAmount.fromRawAmount(token0, (100)))
    ).toBeTruthy()
  
    expect(
      self.exactIn
        .maximumAmountIn(Percent(200, 100))
        .equalTo(CurrencyAmount.fromRawAmount(token0, (100)))
    ).toBeTruthy()

class TestTradeExactOuptut(unittest.TestCase):

  def setUp(self) -> None:
    super().setUp()

    self.exactOut: Trade = Trade.fromRoute(
      poolFactoryProvider, 
      Route([pool_0_1, pool_1_2], token0, token2),
      CurrencyAmount.fromRawAmount(token2, 10000),
      TradeType.EXACT_OUTPUT
    )

  def test_throwsIfLessThan0_2(self):
    expect(lambda: self.exactOut.maximumAmountIn(Percent(-1, 10000))).toThrow(AssertionError, 'SLIPPAGE_TOLERANCE')

  def test_returnsExactIf0_2(self):
    expect(self.exactOut.maximumAmountIn(Percent(0, 10000))).toEqual(self.exactOut.inputAmount)

  def test_returnsSlippageAmountIfNonzero(self):
    ca = self.exactOut.maximumAmountIn(Percent(0, 100))
    
    expect(self.exactOut.maximumAmountIn(Percent(0, 100))
        .equalTo(CurrencyAmount.fromRawAmount(token0, 15488))
    ).toBeTruthy()
    expect(self.exactOut.maximumAmountIn(Percent(5, 100))
        .equalTo(CurrencyAmount.fromRawAmount(token0, 16262))
    ).toBeTruthy()
    expect(self.exactOut.maximumAmountIn(Percent(200, 100))
        .equalTo(CurrencyAmount.fromRawAmount(token0, 46464))
    ).toBeTruthy()

class TestTradeMinimumAmountOutExactInput(unittest.TestCase):

  def setUp(self) -> None:
    super().setUp()

    self.exactIn = Trade.fromRoute(
      poolFactoryProvider, 
      Route([pool_0_1, pool_1_2], token0, token2),
      CurrencyAmount.fromRawAmount(token0, 10000),
      TradeType.EXACT_INPUT)

  def test_throwsIfLessThan0_3(self):
    expect(lambda: self.exactIn.minimumAmountOut(Percent(-1, 100))).toThrow(AssertionError, 'SLIPPAGE_TOLERANCE')

  def test_returnsExactIf0_3(self):
    expect(self.exactIn.minimumAmountOut(Percent(0, 10000))).toEqual(self.exactIn.outputAmount)

  def test_returnsExactIfNonzero(self):
    expect(self.exactIn.minimumAmountOut(Percent(0, 100))).toEqual(
      CurrencyAmount.fromRawAmount(token2, 7004)
    )
    expect(self.exactIn.minimumAmountOut(Percent((5), 100))).toEqual(
      CurrencyAmount.fromRawAmount(token2, 6670)
    )
    expect(self.exactIn.minimumAmountOut(Percent((200), 100))).toEqual(
      CurrencyAmount.fromRawAmount(token2, 2334)
    )

class TestTradeMinimumAmountOutExactOutput(unittest.TestCase):

  def setUp(self) -> None:
    super().setUp()

    self.exactOut = Trade.fromRoute(
      poolFactoryProvider, 
      Route([pool_0_1, pool_1_2], token0, token2),
      CurrencyAmount.fromRawAmount(token2, (100)),
      TradeType.EXACT_OUTPUT
    )

  def test_throwsIfLessThan0_4(self):
    expect(lambda: self.exactOut.minimumAmountOut(Percent(-1, 100))).toThrow(
      AssertionError,
      'SLIPPAGE_TOLERANCE'
    )
  
  def test_returnsExactIf0_4(self):
    expect(self.exactOut.minimumAmountOut(Percent(0, 100))).toEqual(self.exactOut.outputAmount)
  
  def test_returnsSlippageAmountIfNonzero(self):
    expect(
      self.exactOut
        .minimumAmountOut(Percent(0, 100))
        .equalTo(CurrencyAmount.fromRawAmount(token2, (100)))
    ).toBeTruthy()
  
    expect(
      self.exactOut
        .minimumAmountOut(Percent(5, 100))
        .equalTo(CurrencyAmount.fromRawAmount(token2, (100)))
    ).toBeTruthy()
  
    expect(
      self.exactOut
        .minimumAmountOut(Percent(200, 100))
        .equalTo(CurrencyAmount.fromRawAmount(token2, (100)))
    ).toBeTruthy()

  def test_throwsWithEmptyPools(self):
    expect(lambda:
      Trade.bestTradeExactOut(poolFactoryProvider, [], token0, CurrencyAmount.fromRawAmount(token2, (100)))
    ).toThrow(AssertionError, 'POOLS')
  
  def test_throwsWithMaxHopsOf0(self):
    expect(lambda:
      Trade.bestTradeExactOut(poolFactoryProvider, [pool_0_2], token0, CurrencyAmount.fromRawAmount(token2, (100)), BestTradeOptions(maxHops=0))
    ).toThrow(AssertionError, 'MAX_HOPS')

  def test_providesBestRoute(self):
    result = Trade.bestTradeExactOut(
      poolFactoryProvider, 
      [pool_0_1, pool_0_2, pool_1_2],
      token0,
      CurrencyAmount.fromRawAmount(token2, 10000)
    )
    expect(result).toHaveLength(2)
    expect(result[0].swaps[0].route.pools).toHaveLength(1) # 0 -> 2 at 10:11
    expect(result[0].swaps[0].route.tokenPath).toEqual([token0, token2])
    expect(result[0].inputAmount.equalTo(CurrencyAmount.fromRawAmount(token0, 10032))).toBeTruthy()
    expect(result[0].outputAmount.equalTo(CurrencyAmount.fromRawAmount(token2, 10000))).toBeTruthy()
    expect(result[1].swaps[0].route.pools).toHaveLength(2) # 0 -> 1 -> 2 at 12:12:10
    expect(result[1].swaps[0].route.tokenPath).toEqual([token0, token1, token2])
    expect(result[1].inputAmount.equalTo(CurrencyAmount.fromRawAmount(token0, 15488))).toBeTruthy()
    expect(result[1].outputAmount.equalTo(CurrencyAmount.fromRawAmount(token2, 10000))).toBeTruthy()

  def test_respectsMaxHops_1(self):
    result = Trade.bestTradeExactOut(
      poolFactoryProvider, 
      [pool_0_1, pool_0_2, pool_1_2],
      token0,
      CurrencyAmount.fromRawAmount(token2, 10),
      BestTradeOptions(maxHops=1)
    )

    expect(result).toHaveLength(1)
    expect(result[0].swaps[0].route.pools).toHaveLength(1) # 0 -> 2 at 10:11
    expect(result[0].swaps[0].route.tokenPath).toEqual([token0, token2])

  def skip_insufficientLiquidity(self):
    result = Trade.bestTradeExactOut(
      poolFactoryProvider, 
      [pool_0_1, pool_0_2, pool_1_2],
      token0,
      CurrencyAmount.fromRawAmount(token2, 1200)
    )
    expect(result).toHaveLength(0)

  def skip_insufficientLiquidityInOnePoolButNotTheOther(self):
    result = Trade.bestTradeExactOut(
      poolFactoryProvider, 
      [pool_0_1, pool_0_2, pool_1_2],
      token0,
      CurrencyAmount.fromRawAmount(token2, (1050))
    )
    expect(result).toHaveLength(1)

  def test_respectsN(self):
    result = Trade.bestTradeExactOut(
      poolFactoryProvider, 
      [pool_0_1, pool_0_2, pool_1_2],
      token0,
      CurrencyAmount.fromRawAmount(token2, (10)),
      BestTradeOptions(maxNumResults=1)
    )

    expect(result).toHaveLength(1)

  def test_noPath(self):
    result = Trade.bestTradeExactOut(
      poolFactoryProvider, 
      [pool_0_1, pool_0_3, pool_1_3],
      token0,
      CurrencyAmount.fromRawAmount(token2, (10))
    )
    expect(result).toHaveLength(0)

  def test_worksForICXCurrencyInput(self):
    result = Trade.bestTradeExactOut(
      poolFactoryProvider, 
      [pool_wicx_0, pool_0_1, pool_0_3, pool_1_3],
      ICX,
      CurrencyAmount.fromRawAmount(token3, 10000)
    )
    expect(result).toHaveLength(2)
    expect(result[0].inputAmount.currency).toEqual(ICX)
    expect(result[0].swaps[0].route.tokenPath).toEqual([WICX, token0, token1, token3])
    expect(result[0].outputAmount.currency).toEqual(token3)
    expect(result[1].inputAmount.currency).toEqual(ICX)
    expect(result[1].swaps[0].route.tokenPath).toEqual([WICX, token0, token3])
    expect(result[1].outputAmount.currency).toEqual(token3)
  def test_worksForICXCurrencyOutput(self):
    result = Trade.bestTradeExactOut(
      poolFactoryProvider, 
      [pool_wicx_0, pool_0_1, pool_0_3, pool_1_3],
      token3,
      CurrencyAmount.fromRawAmount(ICX, (100))
    )
    expect(result).toHaveLength(2)
    expect(result[0].inputAmount.currency).toEqual(token3)
    expect(result[0].swaps[0].route.tokenPath).toEqual([token3, token0, WICX])
    expect(result[0].outputAmount.currency).toEqual(ICX)
    expect(result[1].inputAmount.currency).toEqual(token3)
    expect(result[1].swaps[0].route.tokenPath).toEqual([token3, token1, token0, WICX])
    expect(result[1].outputAmount.currency).toEqual(ICX)

