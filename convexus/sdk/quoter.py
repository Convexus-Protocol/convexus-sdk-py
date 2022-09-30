from abc import ABCMeta
from dataclasses import dataclass
from typing import List
from convexus.icontoolkit.calldata import toHex

from convexus.icontoolkit.constants import BigintIsh
from convexus.icontoolkit.interface import CallData, Interface

from convexus.sdkcore.entities.fractions.currencyAmount import CurrencyAmount
from convexus.sdkcore.constants import TradeType

from convexus.sdk.entities.route import Route
from convexus.sdk.artifacts.contracts.Quoter import IQuoter
from convexus.sdk.utils.encodeRouteToPath import encodeRouteToPath

@dataclass
class QuoteOptions:
  """
  * Optional arguments to send to the quoter.
  """

  """
   * The optional price limit for the trade.
  """
  sqrtPriceLimitX96: BigintIsh | None = None

"""
 * Represents the Convexus Quoter contract with a method for returning the formatted
 * calldata needed to call the quoter contract.
"""
class SwapQuoter(metaclass=ABCMeta):
  INTERFACE: Interface = Interface(IQuoter, "Quoter")

  @staticmethod
  def setContractAddress (contractAddress: str):
    SwapQuoter.INTERFACE = Interface(IQuoter, contractAddress)

  @staticmethod
  def quoteCallParameters (
    route: Route,
    amount: CurrencyAmount,
    tradeType: TradeType,
    options: QuoteOptions = QuoteOptions()
  ) -> List[CallData]:
    """
    * Produces the on-chain method name of the appropriate function within QuoterV2,
    * and the relevant hex encoded parameters.
    * @template TInput The input token, either ICX or an IRC-2
    * @template TOutput The output token, either ICX or an IRC-2
    * @param route The swap route, a list of pools through which a swap can occur
    * @param amount The amount of the quote, either an amount in, or an amount out
    * @param tradeType The trade type, either exact input or exact output
    * @returns The formatted calldata
    """
    singleHop = len(route.pools) == 1
    quoteAmount: str = toHex(amount.quotient)
    calldata: CallData

    if singleHop:
      if (tradeType == TradeType.EXACT_INPUT):
        calldata = SwapQuoter.INTERFACE.encodeFunctionData('quoteExactInputSingle', [
          [
            route.tokenPath[0].address,
            route.tokenPath[1].address,
            quoteAmount,
            route.pools[0].fee,
            toHex(options.sqrtPriceLimitX96 if options.sqrtPriceLimitX96 else 0)
          ]
      ])
      else:
        calldata = SwapQuoter.INTERFACE.encodeFunctionData('quoteExactOutputSingle', [
          [
            route.tokenPath[0].address,
            route.tokenPath[1].address,
            quoteAmount,
            route.pools[0].fee,
            toHex(options.sqrtPriceLimitX96 if options.sqrtPriceLimitX96 else 0)
          ]
      ])
    else:
      assert options.sqrtPriceLimitX96 == None, 'MULTIHOP_PRICE_LIMIT'
      path: str = encodeRouteToPath(route, tradeType == TradeType.EXACT_OUTPUT)

      if (tradeType == TradeType.EXACT_INPUT):
        calldata = SwapQuoter.INTERFACE.encodeFunctionData('quoteExactInput', [
          [path, quoteAmount]
        ])
      else:
        calldata = SwapQuoter.INTERFACE.encodeFunctionData('quoteExactOutput', [
          [path, quoteAmount]
        ])
    
    return [calldata]
