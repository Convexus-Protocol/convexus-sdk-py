from functools import reduce
from typing import List, cast
from dataclasses import dataclass

from convexus.sdkcore.constants import TradeType
from convexus.sdkcore.utils.sortedInsert import sortedInsert
from convexus.sdkcore.entities.errors import InsufficientInputAmountError
from convexus.sdkcore.entities.fractions.fraction import Fraction
from convexus.sdkcore.entities.fractions.price import Price
from convexus.sdkcore.entities.fractions.percent import Percent
from convexus.sdkcore.entities.fractions.currencyAmount import CurrencyAmount
from convexus.sdkcore.entities.currency import Currency
from convexus.sdk.entities.factoryProvider import PoolFactoryProvider

from convexus.sdk.entities.route import Route
from convexus.sdk.entities.pool import Pool

def tradeComparator (
  a: 'Trade',
  b: 'Trade'
) -> int:
  """
  * Trades comparator, an extension of the input output comparator that also considers other dimensions of the trade in ranking them
  * @template Currency The input token, either ICX or an IRC-2
  * @template Currency The output token, either ICX or an IRC-2
  * @template TradeType The trade type, either exact input or exact output
  * @param a The first trade to compare
  * @param b The second trade to compare
  * @returns A sorted ordering for two neighboring elements in a trade array
  """
  # must have same input and output token for comparison
  assert a.inputAmount.currency.equals(b.inputAmount.currency), 'INPUT_CURRENCY'
  assert a.outputAmount.currency.equals(b.outputAmount.currency), 'OUTPUT_CURRENCY'

  if (a.outputAmount.equalTo(b.outputAmount)):
    if (a.inputAmount.equalTo(b.inputAmount)):
      # consider the number of hops since each hop costs gas
      aHops = reduce(lambda total, cur: total + len(cur.route.tokenPath), a.swaps, 0)
      bHops = reduce(lambda total, cur: total + len(cur.route.tokenPath), b.swaps, 0)
      return aHops - bHops

    # trade A requires less input than trade B, so A should come first
    if (a.inputAmount.lessThan(b.inputAmount)):
      return -1
    else:
      return 1
  else:
    # tradeA has less output than trade B, so should come second
    if (a.outputAmount.lessThan(b.outputAmount)):
      return 1
    else:
      return -1

@dataclass
class BestTradeOptions:
  # how many results to return
  maxNumResults: int = 3
  # the maximum number of hops a trade should contain
  maxHops: int = 3

@dataclass
class RouteInfo:
  route: Route
  inputAmount: CurrencyAmount
  outputAmount: CurrencyAmount

@dataclass
class TradeConstructorArgs:
  routes: List[RouteInfo]
  tradeType: TradeType

@dataclass
class RouteAmount:
  route: Route
  amount: CurrencyAmount

@dataclass
class UncheckedTradeConstructorArguments:
  route: Route
  inputAmount: CurrencyAmount
  outputAmount: CurrencyAmount
  tradeType: TradeType

class Trade:
  """
  * Represents a trade executed against a set of routes where some percentage of the input is
  * split across each route.
  *
  * Each route has its own set of pools. Pools can not be re-used across routes.
  *
  * Does not account for slippage, i.e., changes in price environment that can occur between
  * the time the trade is submitted and when it is executed.
  * @template Currency The input token, either ICX or an IRC-2
  * @template Currency The output token, either ICX or an IRC-2
  * @template TradeType The trade type, either exact input or exact output
  """
  
  def __init__(self, args: TradeConstructorArgs):
    """
    * Construct a trade by passing in the pre-computed property values
    * @param routes The routes through which the trade occurs
    * @param tradeType The type of trade, exact input or exact output
    """
    routes: List[RouteInfo] = args.routes
    tradeType: TradeType = args.tradeType

    inputCurrency = routes[0].inputAmount.currency
    outputCurrency = routes[0].outputAmount.currency

    assert all(map(lambda routeInfo: inputCurrency.wrapped.equals(routeInfo.route.input.wrapped), routes)), 'INPUT_CURRENCY_MATCH'
    assert all(map(lambda routeInfo: outputCurrency.wrapped.equals(routeInfo.route.output.wrapped), routes)), 'OUTPUT_CURRENCY_MATCH'

    """
    * The swaps of the trade, i.e. which routes and how much is swapped in each that
    * make up the trade.
    """
    self.swaps: List[RouteInfo] = routes

    """
    * The type of the trade, either exact in or exact out.
    """
    self.tradeType: TradeType = tradeType

    """
    * The cached result of the input amount computation
    * @private
    """
    self.__inputAmount: CurrencyAmount | None = None
    
    """
    * The cached result of the output amount computation
    * @private
    """
    self.__outputAmount: CurrencyAmount | None = None
    
    """
    * The cached result of the computed execution price
    * @private
    """
    self.__executionPrice: Price | None = None
    
    """
    * The cached result of the price impact computation
    * @private
    """
    self.__priceImpact: Percent | None = None

  def __repr__(self) -> str:
    return str(self.__dict__)

  @property
  def route(self) -> Route:
    """
    * @deprecated Deprecated in favor of 'swaps' property. If the trade consists of multiple routes
    * this will return an error.
    *
    * When the trade consists of just a single route, this returns the route of the trade,
    * i.e. which pools the trade goes through.
    """
    assert len(self.swaps) == 1, 'MULTIPLE_ROUTES'
    return self.swaps[0].route

  @property
  def inputAmount(self) -> CurrencyAmount:
    """
    * The input amount for the trade assuming no slippage.
    """
    if self.__inputAmount:
      return self.__inputAmount

    inputCurrency = self.swaps[0].inputAmount.currency
    totalInputFromRoutes = reduce (lambda total, cur:
      total.add(cur),
      map(lambda swap: swap.inputAmount, self.swaps),
      CurrencyAmount.fromRawAmount(inputCurrency, 0)
    )

    self.__inputAmount = totalInputFromRoutes
    return self.__inputAmount

  @property
  def outputAmount(self) -> CurrencyAmount:
    """
    * The output amount for the trade assuming no slippage.
    """
    if (self.__outputAmount):
      return self.__outputAmount

    outputCurrency = self.swaps[0].outputAmount.currency
    totalOutputFromRoutes = reduce(lambda total, cur:
      total.add(cur),
      map(lambda swap: swap.outputAmount, self.swaps),
      CurrencyAmount.fromRawAmount(outputCurrency, 0)
    )

    self.__outputAmount = totalOutputFromRoutes
    return self.__outputAmount

  @property
  def executionPrice(self) -> Price:
    """
    * The price expressed in terms of output amount/input amount.
    """
    if not self.__executionPrice:
      self.__executionPrice = Price (
        self.inputAmount.currency,
        self.outputAmount.currency,
        self.inputAmount.quotient,
        self.outputAmount.quotient
      )
    return cast(Price, self.__executionPrice)

  @property
  def priceImpact(self) -> Percent:
    """
    * Returns the percent difference between the route's mid price and the price impact
    """
    if (self.__priceImpact):
      return self.__priceImpact

    spotOutputAmount = CurrencyAmount.fromRawAmount(self.outputAmount.currency, 0)
    for swap in self.swaps:
      midPrice = swap.route.midPrice
      spotOutputAmount = spotOutputAmount.add(midPrice.quote(swap.inputAmount))

    priceImpact = spotOutputAmount.subtract(self.outputAmount).divide(spotOutputAmount)
    self.__priceImpact = Percent(priceImpact.numerator, priceImpact.denominator)
    return self.__priceImpact

  @staticmethod
  def exactIn (
    poolFactoryProvider: PoolFactoryProvider,
    route: Route,
    amountIn: CurrencyAmount
  ) -> 'Trade':
    """
    * Constructs an exact in trade with the given amount in and route
    * @template Currency The input token, either ICX or an IRC-2
    * @template Currency The output token, either ICX or an IRC-2
    * @param factoryProvider A Convexus Pool Factory provider
    * @param route The route of the exact in trade
    * @param amountIn The amount being passed in
    * @returns The exact in trade
    """
    return Trade.fromRoute(poolFactoryProvider, route, amountIn, TradeType.EXACT_INPUT)

  @staticmethod
  def exactOut (
    poolFactoryProvider: PoolFactoryProvider,
    route: Route,
    amountOut: CurrencyAmount
  ) -> 'Trade':
    """
    * Constructs an exact out trade with the given amount out and route
    * @template Currency The input token, either ICX or an IRC-2
    * @template Currency The output token, either ICX or an IRC-2
    * @param route The route of the exact out trade
    * @param amountOut The amount returned by the trade
    * @returns The exact out trade
    """
    return Trade.fromRoute(poolFactoryProvider, route, amountOut, TradeType.EXACT_OUTPUT)

  @staticmethod
  def fromRoute (
    poolFactoryProvider: PoolFactoryProvider,
    route: Route,
    amount: CurrencyAmount,
    tradeType: TradeType
  ) -> 'Trade':
    """
    * Constructs a trade by simulating swaps through the given route
    * @template Currency The input token, either ICX or an IRC-2.
    * @template Currency The output token, either ICX or an IRC-2.
    * @template TradeType The type of the trade, either exact in or exact out.
    * @param route route to swap through
    * @param amount the amount specified, either input or output, depending on tradeType
    * @param tradeType whether the trade is an exact input or exact output swap
    * @returns The route
    """
    amounts: List[CurrencyAmount] = [None] * len(route.tokenPath)
    inputAmount: CurrencyAmount
    outputAmount: CurrencyAmount

    if (tradeType == TradeType.EXACT_INPUT):
      assert amount.currency.equals(route.input), 'INPUT'
      amounts[0] = amount.wrapped
      for i in range(len(route.tokenPath) - 1):
        pool = route.pools[i]
        outputAmount, _ = pool.getOutputAmount(amounts[i])
        amounts[i + 1] = outputAmount

      inputAmount = CurrencyAmount.fromFractionalAmount(route.input, amount.numerator, amount.denominator)
      outputAmount = CurrencyAmount.fromFractionalAmount(
        route.output,
        amounts[len(amounts) - 1].numerator,
        amounts[len(amounts) - 1].denominator
      )
    else:
      assert amount.currency.equals(route.output), 'OUTPUT'
      amounts[len(amounts) - 1] = amount.wrapped
      for i in range(len(route.tokenPath) - 1, 0, -1):
        pool = route.pools[i - 1]
        inputAmount, _ = pool.getInputAmount(amounts[i])
        amounts[i - 1] = inputAmount

      inputAmount = CurrencyAmount.fromFractionalAmount(route.input, amounts[0].numerator, amounts[0].denominator)
      outputAmount = CurrencyAmount.fromFractionalAmount(route.output, amount.numerator, amount.denominator)

    trade = Trade(TradeConstructorArgs(
      routes=[RouteInfo(route=route, inputAmount=inputAmount, outputAmount=outputAmount)],
      tradeType=tradeType
    ))

    trade.checkRoute(poolFactoryProvider)

    return trade

  @staticmethod
  def fromRoutes (
    poolFactoryProvider: PoolFactoryProvider,
    routes: List[RouteAmount],
    tradeType: TradeType
  ) -> 'Trade':
    """
    * Constructs a trade from routes by simulating swaps
    *
    * @template Currency The input token, either ICX or an IRC-2.
    * @template Currency The output token, either ICX or an IRC-2.
    * @template TradeType The type of the trade, either exact in or exact out.
    * @param routes the routes to swap through and how much of the amount should be routed through each
    * @param tradeType whether the trade is an exact input or exact output swap
    * @returns The trade
    """
    populatedRoutes: List[RouteInfo] = []

    for routeAmount in routes:
      amount = routeAmount.amount
      route = routeAmount.route
      amounts: List[CurrencyAmount] = [None] * len(route.tokenPath)
      inputAmount: CurrencyAmount
      outputAmount: CurrencyAmount

      if (tradeType == TradeType.EXACT_INPUT):
        assert amount.currency.equals(route.input), 'INPUT'
        inputAmount = CurrencyAmount.fromFractionalAmount(route.input, amount.numerator, amount.denominator)
        amounts[0] = CurrencyAmount.fromFractionalAmount(route.input.wrapped, amount.numerator, amount.denominator)

        for i in range(len(route.tokenPath) - 1):
          pool = route.pools[i]
          outputAmount, pool = pool.getOutputAmount(amounts[i])
          amounts[i + 1] = outputAmount

        outputAmount = CurrencyAmount.fromFractionalAmount(
          route.output,
          amounts[len(amounts) - 1].numerator,
          amounts[len(amounts) - 1].denominator
        )
      else:
        assert amount.currency.equals(route.output), 'OUTPUT'
        outputAmount = CurrencyAmount.fromFractionalAmount(route.output, amount.numerator, amount.denominator)
        amounts[len(amounts) - 1] = CurrencyAmount.fromFractionalAmount(
          route.output.wrapped,
          amount.numerator,
          amount.denominator
        )

        for i in range(len(route.tokenPath) - 1, 0, -1):
          pool = route.pools[i - 1]
          inputAmount, pool = pool.getInputAmount(amounts[i])
          amounts[i - 1] = inputAmount

        inputAmount = CurrencyAmount.fromFractionalAmount(route.input, amounts[0].numerator, amounts[0].denominator)

      populatedRoutes.append(RouteInfo(route, inputAmount, outputAmount))

    trade = Trade(TradeConstructorArgs(
      populatedRoutes,
      tradeType
    ))

    trade.checkRoute(poolFactoryProvider)
    return trade

  @staticmethod
  def createUncheckedTrade (
    poolFactoryProvider: PoolFactoryProvider,
    constructorArguments: UncheckedTradeConstructorArguments
  ) -> 'Trade':
    """
    * Creates a trade without computing the result of swapping through the route. Useful when you have simulated the trade
    * elsewhere and do not have any tick data
    * @template Currency The input token, either ICX or an IRC-2
    * @template Currency The output token, either ICX or an IRC-2
    * @template TradeType The type of the trade, either exact in or exact out
    * @param constructorArguments The arguments passed to the trade constructor
    * @returns The unchecked trade
    """
    trade = Trade(TradeConstructorArgs(
      routes = [RouteInfo (
        inputAmount=constructorArguments.inputAmount,
        outputAmount=constructorArguments.outputAmount,
        route=constructorArguments.route
      )],
      tradeType=constructorArguments.tradeType
    ))

    trade.checkRoute(poolFactoryProvider)
    return trade

  @staticmethod
  def createUncheckedTradeWithMultipleRoutes (
    poolFactoryProvider: PoolFactoryProvider,
    constructorArguments: TradeConstructorArgs
  ) -> 'Trade':
    """
    * Creates a trade without computing the result of swapping through the routes. Useful when you have simulated the trade
    * elsewhere and do not have any tick data
    * @template Currency The input token, either ICX or an IRC-2
    * @template Currency The output token, either ICX or an IRC-2
    * @template TradeType The type of the trade, either exact in or exact out
    * @param constructorArguments The arguments passed to the trade constructor
    * @returns The unchecked trade
    """
    trade = Trade(constructorArguments)
    trade.checkRoute(poolFactoryProvider)
    return trade

  def checkRoute (
    self,
    poolFactoryProvider: PoolFactoryProvider
  ):
    """
    * Need to be called after the constructor to check for the route uniqueness
    * @param factoryProvider A Factory Provider
    * @param routes The routes through which the trade occurs
    """
    numPools = reduce(lambda total, cur:
      total + cur,
      map(lambda swap: len(swap.route.pools), self.swaps),
      0)

    poolAddressSet = set()
    for swap in self.swaps:
      route = swap.route
      for pool in route.pools:
        poolAddressSet.add(Pool.getAddress(poolFactoryProvider, pool.token0, pool.token1, pool.fee))

    assert numPools == len(poolAddressSet), 'POOLS_DUPLICATED'

  def minimumAmountOut (self, slippageTolerance: Percent, amountOut: CurrencyAmount = None) -> CurrencyAmount:
    """
    * Get the minimum amount that must be received from this trade for the given slippage tolerance
    * @param slippageTolerance The tolerance of unfavorable slippage from the execution price of this trade
    * @returns The amount out
    """
    if not amountOut:
      amountOut = self.outputAmount

    assert not slippageTolerance.lessThan(0), 'SLIPPAGE_TOLERANCE'

    if (self.tradeType == TradeType.EXACT_OUTPUT):
      return amountOut
    else:
      slippageAdjustedAmountOut = Fraction(1).add(slippageTolerance).invert().multiply(amountOut.quotient).quotient
      return CurrencyAmount.fromRawAmount(amountOut.currency, slippageAdjustedAmountOut)

  def maximumAmountIn (self, slippageTolerance: Percent, amountIn: CurrencyAmount = None) -> CurrencyAmount:
    """
    * Get the maximum amount in that can be spent via this trade for the given slippage tolerance
    * @param slippageTolerance The tolerance of unfavorable slippage from the execution price of this trade
    * @returns The amount in
    """
    if amountIn is None:
      amountIn = self.inputAmount

    assert not slippageTolerance.lessThan(0), 'SLIPPAGE_TOLERANCE'

    if (self.tradeType == TradeType.EXACT_INPUT):
      return amountIn
    else:
      slippageAdjustedAmountIn = Fraction(1).add(slippageTolerance).multiply(amountIn.quotient).quotient
      return CurrencyAmount.fromRawAmount(amountIn.currency, slippageAdjustedAmountIn)

  def worstExecutionPrice(self, slippageTolerance: Percent) -> Price:
    """
    * Return the execution price after accounting for slippage tolerance
    * @param slippageTolerance the allowed tolerated slippage
    * @returns The execution price
    """
    return Price (
      self.inputAmount.currency,
      self.outputAmount.currency,
      self.maximumAmountIn(slippageTolerance).quotient,
      self.minimumAmountOut(slippageTolerance).quotient
    )

  @staticmethod
  def bestTradeExactIn (
    poolFactoryProvider: PoolFactoryProvider,
    pools: List[Pool],
    currencyAmountIn: CurrencyAmount,
    currencyOut: Currency,
    options: BestTradeOptions = BestTradeOptions(3, 3),
    # used in recursion.
    currentPools: List[Pool] = None,
    nextAmountIn: CurrencyAmount = None,
    bestTrades: List['Trade'] = None
  ) -> List['Trade']:
    """
    * Given a list of pools, and a fixed amount in, returns the top `maxNumResults` trades that go from an input token
    * amount to an output token, making at most `maxHops` hops.
    * Note this does not consider aggregation, as routes are linear. It's possible a better route exists by splitting
    * the amount in among multiple routes.
    * @param pools the pools to consider in finding the best trade
    * @param nextAmountIn exact amount of input currency to spend
    * @param currencyOut the desired currency out
    * @param maxNumResults maximum number of results to return
    * @param maxHops maximum number of hops a returned trade can make, e.g. 1 hop goes through a single pool
    * @param currentPools used in recursion; the current list of pools
    * @param currencyAmountIn used in recursion; the original value of the currencyAmountIn parameter
    * @param bestTrades used in recursion; the current list of best trades
    * @returns The exact in trade
    """
    if nextAmountIn is None:
      nextAmountIn = currencyAmountIn
    if currentPools is None:
      currentPools = []
    if bestTrades is None:
      bestTrades = []

    maxNumResults = options.maxNumResults
    maxHops = options.maxHops

    assert len(pools) > 0, 'POOLS'
    assert maxHops > 0, 'MAX_HOPS'
    assert currencyAmountIn == nextAmountIn or len(currentPools) > 0, 'INVALID_RECURSION'

    amountIn = nextAmountIn.wrapped
    tokenOut = currencyOut.wrapped
    for i in range(len(pools)):
      pool = pools[i]
      # pool irrelevant
      if (not pool.token0.equals(amountIn.currency) and not pool.token1.equals(amountIn.currency)):
        continue

      amountOut: CurrencyAmount
      try:
        amountOut, _ = pool.getOutputAmount(amountIn)
      except InsufficientInputAmountError as error:
        # input too low
        if (error.isInsufficientInputAmountError):
          continue
        raise error

      # we have arrived at the output token, so this is the final trade of one of the paths
      if (amountOut.currency.isToken and amountOut.currency.equals(tokenOut)):
        sortedInsert (
          bestTrades,
          Trade.fromRoute(
            poolFactoryProvider,
            Route(currentPools + [pool], currencyAmountIn.currency, currencyOut),
            currencyAmountIn,
            TradeType.EXACT_INPUT
          ),
          maxNumResults,
          tradeComparator
        )
      elif (maxHops > 1 and len(pools) > 1):
        poolsExcludingThisPool = pools[0:i] + pools[i + 1: len(pools)]

        # otherwise, consider all the other paths that lead from this token as long as we have not exceeded maxHops
        Trade.bestTradeExactIn (
          poolFactoryProvider,
          poolsExcludingThisPool,
          currencyAmountIn,
          currencyOut,
          BestTradeOptions (
            maxNumResults,
            maxHops - 1
          ),
          currentPools + [pool],
          amountOut,
          bestTrades
        )

    return bestTrades

  @staticmethod
  def bestTradeExactOut (
    poolFactoryProvider: PoolFactoryProvider,
    pools: List[Pool],
    currencyIn: Currency,
    currencyAmountOut: CurrencyAmount,
    options: BestTradeOptions = BestTradeOptions(3, 3),
    # used in recursion.
    currentPools: List[Pool] = None,
    nextAmountOut: CurrencyAmount = None,
    bestTrades: List['Trade'] = None
  ) -> List['Trade']:
    """
    * similar to the above method but instead targets a fixed output amount
    * given a list of pools, and a fixed amount out, returns the top `maxNumResults` trades that go from an input token
    * to an output token amount, making at most `maxHops` hops
    * note this does not consider aggregation, as routes are linear. it's possible a better route exists by splitting
    * the amount in among multiple routes.
    * @param pools the pools to consider in finding the best trade
    * @param currencyIn the currency to spend
    * @param currencyAmountOut the desired currency amount out
    * @param nextAmountOut the exact amount of currency out
    * @param maxNumResults maximum number of results to return
    * @param maxHops maximum number of hops a returned trade can make, e.g. 1 hop goes through a single pool
    * @param currentPools used in recursion; the current list of pools
    * @param bestTrades used in recursion; the current list of best trades
    * @returns The exact out trade
    """
    if nextAmountOut is None:
      nextAmountOut = currencyAmountOut

    if bestTrades is None:
      bestTrades = []

    if currentPools is None:
      currentPools = []

    maxNumResults = options.maxNumResults
    maxHops = options.maxHops

    assert len(pools) > 0, 'POOLS'
    assert maxHops > 0, 'MAX_HOPS'
    assert currencyAmountOut == nextAmountOut or len(currentPools) > 0, 'INVALID_RECURSION'

    amountOut = nextAmountOut.wrapped
    tokenIn = currencyIn.wrapped
    for i in range(len(pools)):
      pool = pools[i]
      # pool irrelevant
      if (not pool.token0.equals(amountOut.currency) and not pool.token1.equals(amountOut.currency)):
        continue

      amountIn: CurrencyAmount
      try:
        amountIn, _ = pool.getInputAmount(amountOut)
      except InsufficientInputAmountError as error:
        # input too low
        if (error.isInsufficientInputAmountError):
          continue
        raise error
        
      # we have arrived at the input token, so this is the first trade of one of the paths
      if (amountIn.currency.equals(tokenIn)):
        sortedInsert(
          bestTrades,
          Trade.fromRoute(
            poolFactoryProvider,
            Route([pool] + currentPools, currencyIn, currencyAmountOut.currency),
            currencyAmountOut,
            TradeType.EXACT_OUTPUT
          ),
          maxNumResults,
          tradeComparator
        )
      elif (maxHops > 1 and len(pools) > 1):
        poolsExcludingThisPool = pools[0:i] + pools[i+1:]

        # otherwise, consider all the other paths that arrive at this token as long as we have not exceeded maxHops
        Trade.bestTradeExactOut(
          poolFactoryProvider,
          poolsExcludingThisPool,
          currencyIn,
          currencyAmountOut,
          BestTradeOptions (
            maxNumResults,
            maxHops - 1
          ),
          [pool] + currentPools,
          amountIn,
          bestTrades
        )

    return bestTrades
