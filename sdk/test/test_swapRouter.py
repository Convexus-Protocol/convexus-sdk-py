import unittest
import json

from icontoolkit.test.expect import expect
from sdk.constants import TICK_SPACINGS, FeeAmount
from sdk.entities.route import Route
from sdk.entities.trade import Trade
from sdk.payments import FeeOptions
from sdk.swapRouter import SwapOptions, SwapRouter
from sdk.test.entities.TestPoolFactoryProvider import TestPoolFactoryProvider
from sdkcore.constants import TradeType
from sdkcore.entities.fractions.currencyAmount import CurrencyAmount

from sdkcore.entities.icx import Icx
from sdkcore.entities.currency import Token
from sdkcore.entities.fractions.percent import Percent

from sdk.utils.encodeSqrtRatioX96 import encodeSqrtRatioX96
from sdk.entities.pool import Pool
from sdk.utils.tickMath import TickMath
from sdk.entities.tick import TickConstructorArgs
from sdk.utils.nearestUsableTick import nearestUsableTick

ICX = Icx()
WICX = ICX.wrapped
token0 = Token('cx0000000000000000000000000000000000000001', 18, 't0', 'token0')
token1 = Token('cx0000000000000000000000000000000000000002', 18, 't1', 'token1')

feeAmount = FeeAmount.MEDIUM
sqrtRatioX96 = encodeSqrtRatioX96(1, 1)
liquidity = 1_000_000

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
poolFactoryProvider = TestPoolFactoryProvider()

slippageTolerance = Percent(1, 100)
recipient = 'hx0000000000000000000000000000000000000003'
deadline = 123

class TestSwapRouter(unittest.TestCase):

  def test_singlehopExactInput(self):
    trade = Trade.fromRoute(
      poolFactoryProvider,
      Route([pool_0_1], token0, token1),
      CurrencyAmount.fromRawAmount(token0, 100),
      TradeType.EXACT_INPUT
    )
    calldata = SwapRouter.swapCallParameters(trade, SwapOptions(
      slippageTolerance,
      recipient,
      deadline,
      None,
      None
    ))

    unhexPayload = json.loads(bytes.fromhex(calldata[0]["params"]["_data"].replace("0x", "")).decode('utf-8'))

    expect(unhexPayload).toStrictEqual(
      {
        "method": "exactInputSingle",
        "params": {
          "params": {
            "amountIn": "0x64",
            "amountOutMinimum": "0x61",
            "deadline": "0x7b",
            "fee": "0xbb8",
            "recipient": "hx0000000000000000000000000000000000000003",
            "sqrtPriceLimitX96": "0x0",
            "tokenIn": "cx0000000000000000000000000000000000000001",
            "tokenOut": "cx0000000000000000000000000000000000000002"
          }
        }
      }
    )

    expect(calldata[0]["params"]["_value"]).toBe("0x64")
  

  def test_singleHopExactOutput(self):
    trade = Trade.fromRoute(
      poolFactoryProvider,
      Route([pool_0_1], token0, token1),
      CurrencyAmount.fromRawAmount(token1, 100),
      TradeType.EXACT_OUTPUT
    )
    calldata = SwapRouter.swapCallParameters(trade, SwapOptions(
      slippageTolerance,
      recipient,
      deadline,
      None,
      None
    ))

    unhexPayload = json.loads(bytes.fromhex(calldata[0]["params"]["_data"].replace("0x", "")).decode('utf-8'))

    expect(unhexPayload).toStrictEqual(
      {
        "method": "exactOutputSingle",
        "params": {
          "params": {
            "amountInMaximum": "0x67",
            "amountOut": "0x64",
            "deadline": "0x7b",
            "fee": "0xbb8",
            "recipient": "hx0000000000000000000000000000000000000003",
            "sqrtPriceLimitX96": "0x0",
            "tokenIn": "cx0000000000000000000000000000000000000001",
            "tokenOut": "cx0000000000000000000000000000000000000002"
          }
        }
      }
    )
    
    expect(calldata[0]["params"]["_value"]).toBe("0x67")
  

  def test_ICXInMultihopExactInput(self):
    trade = Trade.fromRoute(
      poolFactoryProvider,
      Route([pool_1_wicx, pool_0_1], ICX, token0),
      CurrencyAmount.fromRawAmount(ICX, 100),
      TradeType.EXACT_INPUT
    )
    calldata = SwapRouter.swapCallParameters(trade, SwapOptions(
      slippageTolerance,
      recipient,
      deadline,
      None,
      None
    ))

    expect(calldata).toStrictEqual([
      {
        "to": "SwapRouter",
        "method": "exactInputIcx",
        "value": "0x64",
        "params": {
          "params": {
            "amountOutMinimum": "0x5f",
            "deadline": "0x7b",
            "path": "0x01111111111111111111111111111111111111111100000bb801000000000000000000000000000000000000000200000bb8010000000000000000000000000000000000000001",
            "recipient": "hx0000000000000000000000000000000000000003"
          }
        }
      }
    ])
  

  def test_multihopExactInput(self):
    amountIn = CurrencyAmount.fromRawAmount(token0, 100)
    trade = Trade.fromRoute(
      poolFactoryProvider,
      Route([pool_0_1, pool_1_wicx], token0, WICX),
      amountIn,
      TradeType.EXACT_INPUT
    )
    calldata = SwapRouter.swapCallParameters(trade, SwapOptions(
      slippageTolerance,
      recipient,
      deadline,
      None,
      None
    ))

    unhexPayload = json.loads(bytes.fromhex(calldata[0]["params"]["_data"].replace("0x", "")).decode('utf-8'))

    expect(unhexPayload).toStrictEqual(
      {
        "method": "exactInput",
        "params": {
          "params": {
            "path": "0x01000000000000000000000000000000000000000100000bb801000000000000000000000000000000000000000200000bb8011111111111111111111111111111111111111111",
            "recipient": "hx0000000000000000000000000000000000000003",
            "deadline": "0x7b",
            "amountIn": "0x64",
            "amountOutMinimum": "0x5f"
          }
        }
      }
    )

    expect(calldata[0]["params"]["_value"]).toBe(hex(amountIn.quotient))
  

  def test_ICXInMultihopExactOutput(self):
    trade = Trade.fromRoute(
      poolFactoryProvider,
      Route([pool_1_wicx, pool_0_1], ICX, token0),
      CurrencyAmount.fromRawAmount(token0, 100),
      TradeType.EXACT_OUTPUT
    )
    calldata = SwapRouter.swapCallParameters(trade, SwapOptions(
      slippageTolerance,
      recipient,
      deadline,
      None,
      None
    ))

    expect(calldata).toStrictEqual([
      {
        "to": "SwapRouter",
        "method": "exactOutputIcx",
        "value": "0x69",
        "params": {
          "params": {
            "amountOut": "0x64",
            "deadline": "0x7b",
            "path": "0x01000000000000000000000000000000000000000100000bb801000000000000000000000000000000000000000200000bb8011111111111111111111111111111111111111111",
            "recipient": "hx0000000000000000000000000000000000000003"
          }
        }
      }
    ])
  

  def test_multihopExactOutput(self):
    trade = Trade.fromRoute(
      poolFactoryProvider,
      Route([pool_0_1, pool_1_wicx], token0, WICX),
      CurrencyAmount.fromRawAmount(WICX, 100),
      TradeType.EXACT_OUTPUT
    )
    calldata = SwapRouter.swapCallParameters(trade, SwapOptions(
      slippageTolerance,
      recipient,
      deadline,
      None,
      None
    ))

    unhexPayload = json.loads(bytes.fromhex(calldata[0]["params"]["_data"].replace("0x", "")).decode('utf-8'))

    expect(unhexPayload).toStrictEqual(
      {
        "method": "exactOutput",
        "params": {
          "params": {
            "amountInMaximum": "0x69",
            "amountOut": "0x64",
            "deadline": "0x7b",
            "path": "0x01111111111111111111111111111111111111111100000bb801000000000000000000000000000000000000000200000bb8010000000000000000000000000000000000000001",
            "recipient": "hx0000000000000000000000000000000000000003"
          }
        }
      }
    )
    
    expect(calldata[0]["params"]["_value"]).toBe("0x69")
  

  def test_ICXInExactInput(self):
    trade = Trade.fromRoute(
      poolFactoryProvider,
      Route([pool_1_wicx], ICX, token1),
      CurrencyAmount.fromRawAmount(ICX, 100),
      TradeType.EXACT_INPUT
    )
    calldata = SwapRouter.swapCallParameters(trade, SwapOptions(
      slippageTolerance,
      recipient,
      deadline,
      None,
      None
    ))

    expect(calldata).toStrictEqual([
      {
        "to": "SwapRouter",
        "method": "exactInputSingleIcx",
        "value": "0x64",
        "params": {
          "params": {
            "amountOutMinimum": "0x61",
            "deadline": "0x7b",
            "fee": "0xbb8",
            "recipient": "hx0000000000000000000000000000000000000003",
            "sqrtPriceLimitX96": "0x0",
            "tokenOut": "cx0000000000000000000000000000000000000002"
          }
        }
      }
    ])
  

  def test_ICXInExactOutput(self):
    trade = Trade.fromRoute(
      poolFactoryProvider,
      Route([pool_1_wicx], ICX, token1),
      CurrencyAmount.fromRawAmount(token1, 100),
      TradeType.EXACT_OUTPUT
    )
    calldata = SwapRouter.swapCallParameters(trade, SwapOptions(
      slippageTolerance,
      recipient,
      deadline,
      None,
      None
    ))

    expect(calldata).toStrictEqual([
      {
        "to": "SwapRouter",
        "method": "exactOutputSingleIcx",
        "value": "0x67",
        "params": {
          "params": {
            "amountOut": "0x64",
            "deadline": "0x7b",
            "fee": "0xbb8",
            "recipient": "hx0000000000000000000000000000000000000003",
            "sqrtPriceLimitX96": "0x0",
            "tokenOut": "cx0000000000000000000000000000000000000002"
          }
        }
      }
    ])
  

  def test_ICXOutExactInput(self):
    trade = Trade.fromRoute(
      poolFactoryProvider,
      Route([pool_1_wicx], token1, ICX),
      CurrencyAmount.fromRawAmount(token1, 100),
      TradeType.EXACT_INPUT
    )
    calldata = SwapRouter.swapCallParameters(trade, SwapOptions(
      slippageTolerance,
      recipient,
      deadline,
      None,
      None
    ))

    unhexPayload = json.loads(bytes.fromhex(calldata[0]["params"]["_data"].replace("0x", "")).decode('utf-8'))

    expect(unhexPayload).toStrictEqual(
      {
        "method": "exactInputSingle",
        "params": {
          "params": {
            "amountIn": "0x64",
            "amountOutMinimum": "0x61",
            "deadline": "0x7b",
            "fee": "0xbb8",
            "recipient": "hx0000000000000000000000000000000000000000",
            "sqrtPriceLimitX96": "0x0",
            "tokenIn": "cx0000000000000000000000000000000000000002",
            "tokenOut": "cx1111111111111111111111111111111111111111"
          }
        }
      }
    )
    
    expect(calldata[0]["params"]["_value"]).toBe("0x64")
  

  def test_ICXOutExactOutput(self):
    trade = Trade.fromRoute(
      poolFactoryProvider,
      Route([pool_1_wicx], token1, ICX),
      CurrencyAmount.fromRawAmount(ICX, 100),
      TradeType.EXACT_OUTPUT
    )
    calldata = SwapRouter.swapCallParameters(trade, SwapOptions(
      slippageTolerance,
      recipient,
      deadline,
      None,
      None
    ))

    unhexPayload = json.loads(bytes.fromhex(calldata[0]["params"]["_data"].replace("0x", "")).decode('utf-8'))

    expect(unhexPayload).toStrictEqual(
      {
        "method": "exactOutputSingle",
        "params": {
          "params": {
            "amountInMaximum": "0x67",
            "amountOut": "0x64",
            "deadline": "0x7b",
            "fee": "0xbb8",
            "recipient": "hx0000000000000000000000000000000000000000",
            "sqrtPriceLimitX96": "0x0",
            "tokenIn": "cx0000000000000000000000000000000000000002",
            "tokenOut": "cx1111111111111111111111111111111111111111"
          }
        }
      }
    )
    
    expect(calldata[0]["params"]["_value"]).toBe("0x67")
  
  def test_sqrtPriceLimitX96(self):
    trade = Trade.fromRoute(
      poolFactoryProvider,
      Route([pool_0_1], token0, token1),
      CurrencyAmount.fromRawAmount(token0, 100),
      TradeType.EXACT_INPUT
    )
    calldata = SwapRouter.swapCallParameters(trade, SwapOptions(
      slippageTolerance,
      recipient,
      deadline,
      2**128,
      None,
    ))
    
    unhexPayload = json.loads(bytes.fromhex(calldata[0]["params"]["_data"].replace("0x", "")).decode('utf-8'))

    expect(unhexPayload).toStrictEqual(
      {
        "method": "exactInputSingle",
        "params": {
          "params": {
            "amountIn": "0x64",
            "amountOutMinimum": "0x61",
            "deadline": "0x7b",
            "fee": "0xbb8",
            "recipient": "hx0000000000000000000000000000000000000003",
            "sqrtPriceLimitX96": "0x100000000000000000000000000000000",
            "tokenIn": "cx0000000000000000000000000000000000000001",
            "tokenOut": "cx0000000000000000000000000000000000000002"
          }
        }
      }
    )
    
    expect(calldata[0]["params"]["_value"]).toBe("0x64")
  

  def test_feeWithIcxOut(self):
    trade = Trade.fromRoute(
      poolFactoryProvider,
      Route([pool_1_wicx], token1, ICX),
      CurrencyAmount.fromRawAmount(token1, 100),
      TradeType.EXACT_INPUT
    )
    
    calldata = SwapRouter.swapCallParameters(trade, SwapOptions(
      slippageTolerance,
      recipient,
      deadline,
      None,
      FeeOptions(
        Percent(5, 1000),
        recipient
      )
    ))

    unhexPayload = json.loads(bytes.fromhex(calldata[0]["params"]["_data"].replace("0x", "")).decode('utf-8'))

    expect(unhexPayload).toStrictEqual(
      {
        "method": "exactInputSingle",
        "params": {
            "params": {
                "amountIn": "0x64",
                "amountOutMinimum": "0x61",
                "deadline": "0x7b",
                "fee": "0xbb8",
                "recipient": "hx0000000000000000000000000000000000000000",
                "sqrtPriceLimitX96": "0x0",
                "tokenIn": "cx0000000000000000000000000000000000000002",
                "tokenOut": "cx1111111111111111111111111111111111111111"
            }
        }
      }
    )
    
    expect(calldata[0]["params"]["_value"]).toBe("0x64")
  

  def test_feeWithIcxInUsingExactOutput(self):
    trade = Trade.fromRoute(
      poolFactoryProvider,
      Route([pool_1_wicx], ICX, token1),
      CurrencyAmount.fromRawAmount(token1, 10),
      TradeType.EXACT_OUTPUT
    )
    calldata = SwapRouter.swapCallParameters(trade, SwapOptions(
      slippageTolerance,
      recipient,
      deadline,
      None,
      FeeOptions(
        Percent(5, 1000),
        recipient
      )
    ))
    
    expect(calldata).toStrictEqual([
      {
        "to": "SwapRouter",
        "method": "exactOutputSingleIcx",
        "value": "0xc",
        "params": {
          "params": {
            "amountOut": "0xa",
            "deadline": "0x7b",
            "fee": "0xbb8",
            "recipient": "hx0000000000000000000000000000000000000000",
            "sqrtPriceLimitX96": "0x0",
            "tokenOut": "cx0000000000000000000000000000000000000002"
          }
        }
      }
    ])
  
  def test_fee(self):
    trade = Trade.fromRoute(
      poolFactoryProvider,
      Route([pool_0_1], token0, token1),
      CurrencyAmount.fromRawAmount(token0, 100),
      TradeType.EXACT_INPUT
    )
    calldata = SwapRouter.swapCallParameters(trade, SwapOptions(
      slippageTolerance,
      recipient,
      deadline,
      None,
      FeeOptions(
        Percent(5, 1000),
        recipient
      )
    ))

    unhexPayload = json.loads(bytes.fromhex(calldata[0]["params"]["_data"].replace("0x", "")).decode('utf-8'))

    expect(unhexPayload).toStrictEqual(
      {
        "method": "exactInputSingle",
        "params": {
          "params": {
            "amountIn": "0x64",
            "amountOutMinimum": "0x61",
            "deadline": "0x7b",
            "fee": "0xbb8",
            "recipient": "hx0000000000000000000000000000000000000000",
            "sqrtPriceLimitX96": "0x0",
            "tokenIn": "cx0000000000000000000000000000000000000001",
            "tokenOut": "cx0000000000000000000000000000000000000002"
          }
        }
      }
    )
    
    expect(calldata[0]["params"]["_value"]).toBe("0x64")