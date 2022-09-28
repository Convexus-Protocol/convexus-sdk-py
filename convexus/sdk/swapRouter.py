"""
 * Options for producing the arguments to send calls to the router.
"""
from abc import ABCMeta
from dataclasses import dataclass
from convexus.icontoolkit.calldata import toHex
from convexus.sdk.entities.route import Route

from convexus.sdk.payments import FeeOptions
from convexus.sdk.constants import ADDRESS_ZERO

from collections.abc import Sequence
from typing import List

from convexus.icontoolkit.constants import BigintIsh
from convexus.icontoolkit.interface import CallData, Interface
from convexus.icontoolkit.validateAndParseAddress import validateAndParseAddress
from convexus.sdkcore.constants import TradeType

from convexus.sdkcore.entities.icx import Icx
from convexus.sdkcore.entities.fractions.percent import Percent

from convexus.sdk.artifacts.contracts.SwapRouter import ISwapRouter
from convexus.sdk.entities.trade import Trade
from convexus.sdk.utils.encodeRouteToPath import encodeRouteToPath

@dataclass
class SwapOptions:
  """
   * How much the execution price is allowed to move unfavorably from the trade execution price.
  """
  slippageTolerance: Percent

  """
   * The account that should receive the output.
  """
  recipient: str

  """
   * When the transaction expires, in epoch seconds.
  """
  deadline: BigintIsh

  """
   * The optional price limit for the trade.
  """
  sqrtPriceLimitX96: BigintIsh | None

  """
   * Optional information for taking a fee on output.
  """
  fee: FeeOptions | None

class SwapRouter(metaclass=ABCMeta):
  """
  * Represents the Convexus SwapRouter, and has static methods for helping execute trades.
  """
  INTERFACE: Interface = Interface(ISwapRouter, "SwapRouter")

  @staticmethod 
  def setContractAddress (contractAddress: str):
    SwapRouter.INTERFACE = Interface(ISwapRouter, contractAddress)

  @staticmethod 
  def swapCallParameters(
    trades: Trade | List[Trade],
    options: SwapOptions
  ) -> List[CallData]:
    """
    * Produces the on-chain method name to call and the hex encoded parameters to pass as arguments for a given trade.
    * @param trade to produce call parameters for
    * @param options options for the call parameters
    """
    if (not isinstance(trades, Sequence)):
      trades = [trades]

    sampleTrade = trades[0]
    tokenIn = sampleTrade.inputAmount.currency.wrapped
    tokenOut = sampleTrade.outputAmount.currency.wrapped

    # All trades should have the same starting and ending token.
    assert all(map(lambda trade: trade.inputAmount.currency.wrapped.equals(tokenIn), trades)), 'TOKEN_IN_DIFF'
    assert all(map(lambda trade: trade.outputAmount.currency.wrapped.equals(tokenOut), trades)), 'TOKEN_OUT_DIFF'

    calldatas: List[CallData] = []

    # flags for whether funds should be send first to the router
    outputIsNative = sampleTrade.outputAmount.currency.isNative
    routerMustCustody = outputIsNative or (not not options.fee)

    recipient: str = validateAndParseAddress(options.recipient)
    deadline = toHex(options.deadline)

    for trade in trades:
      for swap in trade.swaps:
        route = swap.route
        inputAmount = swap.inputAmount
        outputAmount = swap.outputAmount

        amountIn: str = toHex(trade.maximumAmountIn(options.slippageTolerance, inputAmount).quotient)
        amountOut: str = toHex(trade.minimumAmountOut(options.slippageTolerance, outputAmount).quotient)

        # flag for whether the trade is single hop or not
        singleHop = len(route.pools) == 1

        if (singleHop):
          if (trade.tradeType == TradeType.EXACT_INPUT):
            calldatas.append(SwapRouter.encodeExactInputSingle(route, routerMustCustody, recipient, deadline, amountOut, amountIn, options))
          else:
            calldatas.append(SwapRouter.encodeExactOutputSingle(route, routerMustCustody, recipient, deadline, amountOut, amountIn, options))
        else:
          assert options.sqrtPriceLimitX96 is None, 'MULTIHOP_PRICE_LIMIT'
          if (trade.tradeType == TradeType.EXACT_INPUT):
            calldatas.append(SwapRouter.encodeExactInput(trade, route, routerMustCustody, recipient, deadline, amountIn, amountOut))
          else:
            calldatas.append(SwapRouter.encodeExactOutput(trade, route, routerMustCustody, recipient, deadline, amountOut, amountIn))

    return calldatas

  @staticmethod
  def encodeExactOutput (
    trade: Trade,
    route: Route,
    routerMustCustody: bool, 
    recipient: str, 
    deadline: str, 
    amountOut: str, 
    amountIn: str
  ) -> CallData:
    
    path: str = encodeRouteToPath(route, trade.tradeType == TradeType.EXACT_OUTPUT)

    if (Icx.isWrappedAddress(route.tokenPath[0].address)):
      exactOutputParams = [
        [
          path,
          ADDRESS_ZERO if routerMustCustody else recipient,
          deadline,
          amountOut
        ]
      ]

      return SwapRouter.INTERFACE.encodeFunctionDataPayable(
        amountIn,
        'exactOutputIcx',
        exactOutputParams
      )
    else:
      exactOutputParams = [[
        path,
        ADDRESS_ZERO if routerMustCustody else recipient,
        deadline,
        amountOut,
        amountIn
      ]]

      exactOutputInputs = [{
        'fields': [
          { 'name': 'path', 'type': 'bytes' },
          { 'name': 'recipient', 'type': 'Address' },
          { 'name': 'deadline', 'type': 'int' },
          { 'name': 'amountOut', 'type': 'int' },
          { 'name': 'amountInMaximum', 'type': 'int' }
        ],
        'name': 'params',
        'type': 'struct'
      }]
  
      return SwapRouter.INTERFACE.encodeTokenFallbackFunctionData(
        route.tokenPath[0].address,
        amountIn,
        'exactOutput',
        exactOutputInputs,
        exactOutputParams
      )

  @staticmethod
  def encodeExactInput (
    trade: Trade,
    route: Route,
    routerMustCustody: bool,
    recipient: str,
    deadline: str,
    amountIn: str,
    amountOut: str,
  ) -> CallData:
    path: str = encodeRouteToPath(route, trade.tradeType == TradeType.EXACT_OUTPUT)

    if (Icx.isWrappedAddress(route.tokenPath[0].address)):
      exactInputParams = [[
        path,
        ADDRESS_ZERO if routerMustCustody else recipient,
        deadline,
        amountOut
      ]]

      return SwapRouter.INTERFACE.encodeFunctionDataPayable(
        amountIn,
        'exactInputIcx',
        exactInputParams
      )
    else:
      exactInputParams = [[
        path,
        ADDRESS_ZERO if routerMustCustody else recipient,
        deadline,
        amountIn,
        amountOut
      ]]

      exactInputInputs = [{
        'fields': [
          { 'name': 'path', 'type': 'bytes' },
          { 'name': 'recipient', 'type': 'Address' },
          { 'name': 'deadline', 'type': 'int' },
          { 'name': 'amountIn', 'type': 'int' },
          { 'name': 'amountOutMinimum', 'type': 'int' }
        ],
        'name': 'params',
        'type': 'struct'
      }]
      
      return SwapRouter.INTERFACE.encodeTokenFallbackFunctionData(
        route.tokenPath[0].address,
        amountIn,
        'exactInput',
        exactInputInputs,
        exactInputParams
      )

  @staticmethod
  def encodeExactOutputSingle (
    route: Route,
    routerMustCustody: bool,
    recipient: str,
    deadline: str,
    amountOut: str,
    amountIn: str,
    options: SwapOptions
  ) -> CallData:
    if (Icx.isWrappedAddress(route.tokenPath[0].address)):
      exactOutputSingleParams = [[
        route.tokenPath[1].address,
        route.pools[0].fee,
        ADDRESS_ZERO if routerMustCustody else recipient,
        deadline,
        amountOut,
        toHex(options.sqrtPriceLimitX96 if options.sqrtPriceLimitX96 else 0)
      ]]

      return SwapRouter.INTERFACE.encodeFunctionDataPayable(
        amountIn,
        'exactOutputSingleIcx',
        exactOutputSingleParams
      )
    else:
      exactOutputSingleParams = [[
        route.tokenPath[0].address,
        route.tokenPath[1].address,
        route.pools[0].fee,
        ADDRESS_ZERO if routerMustCustody else recipient,
        deadline,
        amountOut,
        amountIn,
        toHex(options.sqrtPriceLimitX96 if options.sqrtPriceLimitX96 else 0)
      ]]
  
      exactOutputSingleInputs = [{
        'fields': [
          { 'name': 'tokenIn', 'type': 'Address' },
          { 'name': 'tokenOut', 'type': 'Address' },
          { 'name': 'fee', 'type': 'int' },
          { 'name': 'recipient', 'type': 'Address' },
          { 'name': 'deadline', 'type': 'int' },
          { 'name': 'amountOut', 'type': 'int' },
          { 'name': 'amountInMaximum', 'type': 'int' },
          { 'name': 'sqrtPriceLimitX96', 'type': 'int' }
        ],
        'name': 'params',
        'type': 'struct'
      }]

      return SwapRouter.INTERFACE.encodeTokenFallbackFunctionData(
        route.tokenPath[0].address,
        amountIn,
        'exactOutputSingle',
        exactOutputSingleInputs,
        exactOutputSingleParams
      )

  @staticmethod
  def encodeExactInputSingle (
    route: Route, 
    routerMustCustody: bool, 
    recipient: str,
    deadline: str,
    amountOut: str,
    amountIn: str,
    options: SwapOptions) -> CallData:
    if (Icx.isWrappedAddress(route.tokenPath[0].address)):
      exactInputSingleParams = [
        [
          route.tokenPath[1].address,
          route.pools[0].fee,
          ADDRESS_ZERO if routerMustCustody else recipient,
          deadline,
          amountOut,
          toHex(options.sqrtPriceLimitX96 if options.sqrtPriceLimitX96 else 0)
        ]
      ]

      return SwapRouter.INTERFACE.encodeFunctionDataPayable(
        amountIn,
        'exactInputSingleIcx',
        exactInputSingleParams
      )
    else:
      exactInputSingleParams = [
        [
          route.tokenPath[0].address,
          route.tokenPath[1].address,
          route.pools[0].fee,
          ADDRESS_ZERO if routerMustCustody else recipient,
          deadline,
          amountIn,
          amountOut,
          toHex(options.sqrtPriceLimitX96 if options.sqrtPriceLimitX96 else 0)
        ]
      ]

      exactInputSingleInputs = [{
        'fields': [
          { 'name': 'tokenIn', 'type': 'Address' },
          { 'name': 'tokenOut', 'type': 'Address' },
          { 'name': 'fee', 'type': 'int' },
          { 'name': 'recipient', 'type': 'Address' },
          { 'name': 'deadline', 'type': 'int' },
          { 'name': 'amountIn', 'type': 'int' },
          { 'name': 'amountOutMinimum', 'type': 'int' },
          { 'name': 'sqrtPriceLimitX96', 'type': 'int' }
        ],
        'name': 'params',
        'type': 'struct'
      }]

      return SwapRouter.INTERFACE.encodeTokenFallbackFunctionData(
        route.tokenPath[0].address,
        amountIn,
        'exactInputSingle',
        exactInputSingleInputs,
        exactInputSingleParams
      )
