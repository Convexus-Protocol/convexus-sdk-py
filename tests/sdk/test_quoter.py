import unittest
from convexus.icontoolkit.expect import expect

from convexus.sdk.constants import TICK_SPACINGS, FeeAmount
from convexus.sdk.entities.route import Route
from convexus.sdkcore.constants import TradeType
from convexus.sdkcore.entities.currency import Token
from convexus.sdk.utils.encodeSqrtRatioX96 import encodeSqrtRatioX96
from convexus.sdkcore.entities.fractions.currencyAmount import CurrencyAmount
from convexus.sdkcore.entities.icx import Icx
from convexus.sdk.entities.pool import Pool
from convexus.sdk.utils.tickMath import TickMath
from convexus.sdk.utils.nearestUsableTick import nearestUsableTick
from convexus.sdk.entities.tick import TickConstructorArgs
from convexus.sdk.entities.trade import Trade
from convexus.sdk.quoter import QuoteOptions, SwapQuoter

from TestPoolFactoryProvider import TestPoolFactoryProvider

token0 = Token('cx0000000000000000000000000000000000000001', 18, 't0', 'token0')
token1 = Token('cx0000000000000000000000000000000000000002', 18, 't1', 'token1')

poolFactoryProvider = TestPoolFactoryProvider()

feeAmount = FeeAmount.MEDIUM
sqrtRatioX96 = encodeSqrtRatioX96(1, 1)
liquidity = 1_000_000
ICX = Icx()
WICX = ICX.wrapped

def makePool (token0: Token, token1: Token):
  return Pool(token0, token1, feeAmount, sqrtRatioX96, liquidity, TickMath.getTickAtSqrtRatio(sqrtRatioX96), [
    TickConstructorArgs(
      index=nearestUsableTick(TickMath.MIN_TICK, TICK_SPACINGS[feeAmount]),
      liquidityNet=liquidity,
      liquidityGross=liquidity
    ),
    TickConstructorArgs(
      index=nearestUsableTick(TickMath.MAX_TICK, TICK_SPACINGS[feeAmount]),
      liquidityNet=-liquidity,
      liquidityGross=liquidity
    )
  ])

pool_0_1 = makePool(token0, token1)
pool_1_wicx = makePool(token1, WICX)


class TestQuoter(unittest.TestCase):
      def test_singleHopExactInput(self):
        trade = Trade.fromRoute(
          poolFactoryProvider,
          Route([pool_0_1], token0, token1),
          CurrencyAmount.fromRawAmount(token0, 100),
          TradeType.EXACT_INPUT
        )
        calldata = SwapQuoter.quoteCallParameters(
          trade.swaps[0].route,
          trade.inputAmount,
          trade.tradeType
        )

        expect(calldata).toStrictEqual([
          {
            "to": "Quoter",
            "method": "quoteExactInputSingle",
            "params": {
                "params": {
                    "amountIn": "0xbb8",
                    "fee": "0x64",
                    "sqrtPriceLimitX96": "0x0",
                    "tokenIn": "cx0000000000000000000000000000000000000001",
                    "tokenOut": "cx0000000000000000000000000000000000000002"
                }
            }
          }
        ])

      def test_singleHopExactOutput(self):
        trade = Trade.fromRoute(
          poolFactoryProvider,
          Route([pool_0_1], token0, token1),
          CurrencyAmount.fromRawAmount(token1, 100),
          TradeType.EXACT_OUTPUT
        )
        calldata = SwapQuoter.quoteCallParameters(
          trade.swaps[0].route,
          trade.outputAmount,
          trade.tradeType
        )

        expect(calldata).toStrictEqual([
          {
            "to": "Quoter",
            "method": "quoteExactOutputSingle",
            "params": {
                "params": {
                    "amount": "0xbb8",
                    "fee": "0x64",
                    "sqrtPriceLimitX96": "0x0",
                    "tokenIn": "cx0000000000000000000000000000000000000001",
                    "tokenOut": "cx0000000000000000000000000000000000000002"
                }
            }
          }
        ])

      def test_multiHopExactInput(self):
        trade = Trade.fromRoute(
          poolFactoryProvider,
          Route([pool_0_1, pool_1_wicx], token0, WICX),
          CurrencyAmount.fromRawAmount(token0, 100),
          TradeType.EXACT_INPUT
        )
        calldata = SwapQuoter.quoteCallParameters(trade.route, trade.inputAmount, trade.tradeType)

        expect(calldata).toStrictEqual([
          {
            "to": "Quoter",
            "method": "quoteExactInput",
            "params": {
              "params": {
                "amountIn": "0x64",
                "path": "0x01000000000000000000000000000000000000000100000bb801000000000000000000000000000000000000000200000bb8011111111111111111111111111111111111111111"
              }
            }
          }
        ])

      def test_multiHopExactOutput(self):
        trade = Trade.fromRoute(
          poolFactoryProvider,
          Route([pool_0_1, pool_1_wicx], token0, WICX),
          CurrencyAmount.fromRawAmount(WICX, 100),
          TradeType.EXACT_OUTPUT
        )
        calldata = SwapQuoter.quoteCallParameters(trade.route, trade.outputAmount, trade.tradeType)

        expect(calldata).toStrictEqual([
          {
            "to": "Quoter",
            "method": "quoteExactOutput",
            "params": {
                "params": {
                    "amountOut": "0x64",
                    "path": "0x01111111111111111111111111111111111111111100000bb801000000000000000000000000000000000000000200000bb8010000000000000000000000000000000000000001"
                }
            }
          }
        ])
      def test_sqrtPriceLimitX96(self):
        trade = Trade.fromRoute(
          poolFactoryProvider,
          Route([pool_0_1], token0, token1),
          CurrencyAmount.fromRawAmount(token0, 100),
          TradeType.EXACT_INPUT
        )
        calldata = SwapQuoter.quoteCallParameters(trade.route, trade.inputAmount, trade.tradeType, QuoteOptions(
          sqrtPriceLimitX96=2**128
        ))

        expect(calldata).toStrictEqual([
          {
            "to": "Quoter",
            "method": "quoteExactInputSingle",
            "params": {
                "params": {
                    "amountIn": "0xbb8",
                    "fee": "0x64",
                    "sqrtPriceLimitX96": "0x100000000000000000000000000000000",
                    "tokenIn": "cx0000000000000000000000000000000000000001",
                    "tokenOut": "cx0000000000000000000000000000000000000002"
                }
            }
          }
        ])

