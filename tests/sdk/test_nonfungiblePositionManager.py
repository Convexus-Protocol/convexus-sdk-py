import unittest
from convexus.icontoolkit.BigInt import BigInt
from convexus.icontoolkit.expect import expect
from convexus.sdk.entities.position import Position, PositionConstructorArgs
from convexus.sdk.utils.tickMath import TickMath
from convexus.sdkcore.constants import MaxUint256

from convexus.sdkcore.entities.currency import Token
from convexus.sdkcore.entities.fractions.currencyAmount import CurrencyAmount
from convexus.sdkcore.entities.icx import Icx
from convexus.sdk.constants import TICK_SPACINGS, FeeAmount
from convexus.sdk.utils.encodeSqrtRatioX96 import encodeSqrtRatioX96
from convexus.sdk.entities.pool import Pool
from convexus.sdk.utils.maxLiquidityForAmounts import maxLiquidityForAmounts
from convexus.sdk.utils.nearestUsableTick import nearestUsableTick
from convexus.sdk.utils.priceTickConversions import priceToClosestTick
from convexus.sdkcore.entities.fractions.price import Price
from convexus.sdkcore.entities.fractions.percent import Percent
from convexus.sdk.nonfungiblePositionManager import CollectOptions, CollectOptionsNoTokenId, IncreaseOptions, MintOptions, NonfungiblePositionManager, RemoveLiquidityOptions, SafeTransferOptions

token0 = Token('cx0000000000000000000000000000000000000001', 18, 't0', 'token0')
token1 = Token('cx0000000000000000000000000000000000000002', 18, 't1', 'token1')
token2 = Token('cx0000000000000000000000000000000000000003', 18, 't2', 'token2')

fee = FeeAmount.MEDIUM
feeHigh = FeeAmount.MEDIUM
ICX = Icx()
WICX = ICX.wrapped

pool_0_1 = Pool(token0, token1, fee, encodeSqrtRatioX96(1, 1), 0, 0, [])
pool_0_1_fee_high = Pool(token0, token1, feeHigh, encodeSqrtRatioX96(1, 1), 0, 0, [])
pool_1_wicx = Pool(token1, WICX, fee, encodeSqrtRatioX96(1, 1), 0, 0, [])

recipient = 'hx0000000000000000000000000000000000000003'
sender = 'hx0000000000000000000000000000000000000004'
tokenId = 1
slippageTolerance = Percent(1, 100)
deadline = 123

class TestNonfungiblepositionmanager(unittest.TestCase):

  def test_throwsIfLiquidityIs0(self):
    expect(lambda:
      NonfungiblePositionManager.addCallParameters(
        Position(PositionConstructorArgs(
          pool=pool_0_1,
          tickLower=-TICK_SPACINGS[FeeAmount.MEDIUM],
          tickUpper=TICK_SPACINGS[FeeAmount.MEDIUM],
          liquidity=0
        )),
        MintOptions(recipient=recipient, slippageTolerance=slippageTolerance, deadline=deadline)
      )
    ).toThrow(AssertionError, 'ZERO_LIQUIDITY')

  def test_throwsIfPoolDoesNotInvolveICXAndUseNativeIsTrue(self):
    expect(lambda:
      NonfungiblePositionManager.addCallParameters(
        Position(PositionConstructorArgs(
          pool=pool_0_1,
          tickLower=-TICK_SPACINGS[FeeAmount.MEDIUM],
          tickUpper=TICK_SPACINGS[FeeAmount.MEDIUM],
          liquidity=1
        )),
        MintOptions(recipient=recipient, slippageTolerance=slippageTolerance, deadline=deadline, useNative=ICX)
      )
    ).toThrow(AssertionError, 'NO_WICX')

  def test_succeedsForMint(self):
    calldata = NonfungiblePositionManager.addCallParameters(
      Position(PositionConstructorArgs(
        pool=pool_0_1,
        tickLower=-TICK_SPACINGS[FeeAmount.MEDIUM],
        tickUpper=TICK_SPACINGS[FeeAmount.MEDIUM],
        liquidity=1
      )),
      MintOptions(recipient=recipient, slippageTolerance=slippageTolerance, deadline=deadline)
    )

    expect(calldata[0]).toStrictEqual({
      "method": "transfer",
      "params": {
          "_data": "0x7b226d6574686f64223a226465706f736974222c22706172616d73223a7b7d7d",
          "_to": "NonfungiblePositionManager",
          "_value": "0x1"
      },
      "to": "cx0000000000000000000000000000000000000001"
    })

    expect(calldata[1]).toStrictEqual({
        "method": "transfer",
        "params": {
            "_data": "0x7b226d6574686f64223a226465706f736974222c22706172616d73223a7b7d7d",
            "_to": "NonfungiblePositionManager",
            "_value": "0x1"
        },
        "to": "cx0000000000000000000000000000000000000002"
      })

    expect(calldata[2]).toStrictEqual({
      "to": "NonfungiblePositionManager",
      "method": "mint",
      "params": {
        "params": {
          "amount0Desired": "0x1",
          "amount0Min": "0x0",
          "amount1Desired": "0x1",
          "amount1Min": "0x0",
          "deadline": "0x7b",
          "fee": "0xbb8",
          "recipient": "hx0000000000000000000000000000000000000003",
          "tickLower": "-0x3c",
          "tickUpper": "0x3c",
          "token0": "cx0000000000000000000000000000000000000001",
          "token1": "cx0000000000000000000000000000000000000002"
        }
      }
    })

  def test_succeedsForMintPoolCRVWETH(self):
    # https://i.imgur.com/xTZj9Hp.png

    highFee = FeeAmount.HIGH # 1% fee

    # Current Price: 1364 CRV per WETH
    pool_1_2_price = BigInt("2926833475291797893971652918731") # ~ equals to encodeSqrtRatioX96(1364, 1)
    pool_1_2_liquidity = BigInt("270755706369106903362800")
    pool_1_2_tick = 72190
    pool_1_2 = Pool(token1, token2, highFee, pool_1_2_price, pool_1_2_liquidity, pool_1_2_tick, [])

    # Provide liquidity between 953 and 1843
    lowerBoundPrice = 953
    higherBoundPrice = 1843

    EXA = BigInt("1000000000000000000")
    amount0 = EXA * BigInt("1") # 1 ETH provided
    amount1 = MaxUint256 # should result in ~1605 CRV

    # Compute the max liquidity for 1 ETH
    liquidity = maxLiquidityForAmounts (
      pool_1_2_price, # Pool price
      encodeSqrtRatioX96(lowerBoundPrice, 1), # lower bound price
      encodeSqrtRatioX96(higherBoundPrice, 1), # upper bound price
      amount0, amount1, # amounts of token provided
      True
    )

    # Compute lower & upper ticks from prices
    tickLower = nearestUsableTick(priceToClosestTick(Price(token1, token2, 1, lowerBoundPrice)), TICK_SPACINGS[highFee])
    tickUpper = nearestUsableTick(priceToClosestTick(Price(token1, token2, 1, higherBoundPrice)), TICK_SPACINGS[highFee])

    calldata = NonfungiblePositionManager.addCallParameters(
      Position(PositionConstructorArgs(
        pool=pool_1_2,
        tickLower=tickLower,
        tickUpper=tickUpper,
        liquidity=liquidity
      )),
      MintOptions(recipient=recipient, slippageTolerance=slippageTolerance, deadline=deadline)
    )

    expect(calldata[0]).toStrictEqual({
      "method": "transfer",
      "params": {
          "_data": "0x7b226d6574686f64223a226465706f736974222c22706172616d73223a7b7d7d",
          "_to": "NonfungiblePositionManager",
          "_value": "0xde5e8740bb558e1"
      },
      "to": "cx0000000000000000000000000000000000000002"
    })

    expect(calldata[1]).toStrictEqual({
        "method": "transfer",
        "params": {
            "_data": "0x7b226d6574686f64223a226465706f736974222c22706172616d73223a7b7d7d",
            "_to": "NonfungiblePositionManager",
            "_value": "0x5726f15f7a749b4cdd"
        },
        "to": "cx0000000000000000000000000000000000000003"
    })

    expect(calldata[2]).toStrictEqual(
      {
        "to": "NonfungiblePositionManager",
        "method": "mint",
        "params": {
          "params": {
            "amount0Desired": "0xde5e8740bb558e1", # 1.0014620772700884
            "amount0Min": "0xd67824c75ca9589", # 0.9658839099995973
            "amount1Desired": "0x5726f15f7a749b4cdd", # 1607.6728634351073
            "amount1Min": "0x547e5f6be63da9b4f4", # 1558.632617799791
            "deadline": "0x7b",
            "fee": "0x2710", # 1%
            "recipient": "hx0000000000000000000000000000000000000003",
            "tickLower": "0x10bf8",
            "tickUpper": "0x125c0",
            "token0": "cx0000000000000000000000000000000000000002",
            "token1": "cx0000000000000000000000000000000000000003"
          }
        }
      }
    )

  def test_succeedsForFullRange(self):
    calldata = NonfungiblePositionManager.addCallParameters(
      Position(PositionConstructorArgs(
        pool=pool_0_1,
        tickLower=nearestUsableTick(TickMath.MIN_TICK, TICK_SPACINGS[fee]),
        tickUpper=nearestUsableTick(TickMath.MAX_TICK, TICK_SPACINGS[fee]),
        liquidity=1
      )),
      MintOptions(recipient=recipient, slippageTolerance=slippageTolerance, deadline=deadline)
    )

    expect(calldata[0]).toStrictEqual({
      "method": "transfer",
      "params": {
          "_data": "0x7b226d6574686f64223a226465706f736974222c22706172616d73223a7b7d7d",
          "_to": "NonfungiblePositionManager",
          "_value": "0x1"
      },
      "to": "cx0000000000000000000000000000000000000001"
    })

    expect(calldata[1]).toStrictEqual({
        "method": "transfer",
        "params": {
            "_data": "0x7b226d6574686f64223a226465706f736974222c22706172616d73223a7b7d7d",
            "_to": "NonfungiblePositionManager",
            "_value": "0x1"
        },
        "to": "cx0000000000000000000000000000000000000002"
    })

    expect(calldata[2]).toStrictEqual(
      {
        "to": "NonfungiblePositionManager",
        "method": "mint",
        "params": {
          "params": {
            "amount0Desired": "0x1",
            "amount0Min": "0x1",
            "amount1Desired": "0x1",
            "amount1Min": "0x1",
            "deadline": "0x7b",
            "fee": "0xbb8",
            "recipient": "hx0000000000000000000000000000000000000003",
            "tickLower": "-0xd89b4",
            "tickUpper": "0xd89b4",
            "token0": "cx0000000000000000000000000000000000000001",
            "token1": "cx0000000000000000000000000000000000000002"
          }
        }
      }
    )

  def test_succeedsForFullRangeHighFee(self):
    calldata = NonfungiblePositionManager.addCallParameters(
      Position(PositionConstructorArgs(
        pool=pool_0_1_fee_high,
        tickLower=nearestUsableTick(TickMath.MIN_TICK, TICK_SPACINGS[feeHigh]),
        tickUpper=nearestUsableTick(TickMath.MAX_TICK, TICK_SPACINGS[feeHigh]),
        liquidity=1
      )),
      MintOptions(recipient=recipient, slippageTolerance=slippageTolerance, deadline=deadline)
    )

    expect(calldata[0]).toStrictEqual({
      "method": "transfer",
      "params": {
          "_data": "0x7b226d6574686f64223a226465706f736974222c22706172616d73223a7b7d7d",
          "_to": "NonfungiblePositionManager",
          "_value": "0x1"
      },
      "to": "cx0000000000000000000000000000000000000001"
    })

    expect(calldata[1]).toStrictEqual({
        "method": "transfer",
        "params": {
            "_data": "0x7b226d6574686f64223a226465706f736974222c22706172616d73223a7b7d7d",
            "_to": "NonfungiblePositionManager",
            "_value": "0x1"
        },
        "to": "cx0000000000000000000000000000000000000002"
    })

    expect(calldata[2]).toStrictEqual(
      {
        "to": "NonfungiblePositionManager",
        "method": "mint",
        "params": {
          "params": {
            "amount0Desired": "0x1",
            "amount0Min": "0x1",
            "amount1Desired": "0x1",
            "amount1Min": "0x1",
            "deadline": "0x7b",
            "fee": "0xbb8",
            "recipient": "hx0000000000000000000000000000000000000003",
            "tickLower": "-0xd89b4",
            "tickUpper": "0xd89b4",
            "token0": "cx0000000000000000000000000000000000000001",
            "token1": "cx0000000000000000000000000000000000000002"
          }
        }
      }
    )

  def test_succeedsForIncrease(self):
    pool = Pool(
      token0, 
      token1, 
      FeeAmount.MEDIUM,
      BigInt("0x24eeafd75f26d0000000000000"),
      BigInt("0x131651bddb3edbbd5d"),
      0x119f9
    )

    newPosition = Position(PositionConstructorArgs(
      pool=pool,
      tickLower=0x13470,
      tickUpper=0x13524,
      liquidity=BigInt("19087752567891193668198803")
    ))

    calldata = NonfungiblePositionManager.addCallParameters(
      newPosition,
      IncreaseOptions(tokenId=tokenId, slippageTolerance=slippageTolerance, deadline=deadline)
    )

    expectedValue = hex(newPosition.amount0.quotient)

    expect(calldata[0]).toStrictEqual({
      "method": "transfer",
      "params": {
          "_data": "0x7b226d6574686f64223a226465706f736974222c22706172616d73223a7b7d7d",
          "_to": "NonfungiblePositionManager",
          "_value": expectedValue
      },
      "to": "cx0000000000000000000000000000000000000001"
    })

    expect(calldata[1]).toStrictEqual({
        "to": "NonfungiblePositionManager",
        "method": "increaseLiquidity",
        "params": {
          "params": {
            "amount0Desired": hex(newPosition.amount0.quotient),
            "amount0Min": hex(newPosition.amount0.quotient),
            "amount1Desired": "0x0",
            "amount1Min": "0x0",
            "deadline": "0x7b",
            "tokenId": "0x1"
          }
        }
      })

  def test_useNative(self):
    calldata = NonfungiblePositionManager.addCallParameters(
      Position(PositionConstructorArgs(
        pool=pool_1_wicx,
        tickLower=-TICK_SPACINGS[FeeAmount.MEDIUM],
        tickUpper=TICK_SPACINGS[FeeAmount.MEDIUM],
        liquidity=1
      )),
      MintOptions(recipient=recipient, slippageTolerance=slippageTolerance, deadline=deadline, useNative=ICX)
    )

    expect(calldata[0]).toStrictEqual({
      "method": "transfer",
      "params": {
          "_data": "0x7b226d6574686f64223a226465706f736974222c22706172616d73223a7b7d7d",
          "_to": "NonfungiblePositionManager",
          "_value": "0x1"
      },
      "to": "cx0000000000000000000000000000000000000002"
    })

    expect(calldata[1]).toStrictEqual({
        "to": "NonfungiblePositionManager",
        "method": "depositIcx",
        "value": "0x1"
    })

    expect(calldata[2]).toStrictEqual(
      {
        "to": "NonfungiblePositionManager",
        "method": "mint",
        "params": {
          "params": {
            "amount0Desired": "0x1",
            "amount0Min": "0x0",
            "amount1Desired": "0x1",
            "amount1Min": "0x0",
            "deadline": "0x7b",
            "fee": "0xbb8",
            "recipient": "hx0000000000000000000000000000000000000003",
            "tickLower": "-0x3c",
            "tickUpper": "0x3c",
            "token0": "cx0000000000000000000000000000000000000002",
            "token1": "cx1111111111111111111111111111111111111111"
          }
        }
      }
    )

  def test_works(self):
    calldata = NonfungiblePositionManager.collectCallParameters(CollectOptions(
      tokenId=tokenId,
      expectedCurrencyOwed0=CurrencyAmount.fromRawAmount(token0, 0),
      expectedCurrencyOwed1=CurrencyAmount.fromRawAmount(token1, 0),
      recipient=recipient
    ))

    expect(calldata).toStrictEqual(
      [
        {
            "to": "NonfungiblePositionManager",
            "method": "collect",
            "params": {
                "params": {
                  "amount0Max": "0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
                  "amount1Max": "0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
                  "recipient": "hx0000000000000000000000000000000000000003",
                  "tokenId": "0x1"
                }
            }
        }
      ]
    )

  def test_worksWithICX(self):
    calldata = NonfungiblePositionManager.collectCallParameters(CollectOptions(
      tokenId=tokenId,
      expectedCurrencyOwed0=CurrencyAmount.fromRawAmount(token1, 0),
      expectedCurrencyOwed1=CurrencyAmount.fromRawAmount(ICX, 0),
      recipient=recipient
    ))

    expect(calldata).toStrictEqual(
      [
        {
          "to": "NonfungiblePositionManager",
          "method": "collect",
          "params": {
            "params": {
              "amount0Max": "0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
              "amount1Max": "0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
              "recipient": "hx0000000000000000000000000000000000000003",
              "tokenId": "0x1"
            }
          }
        }
      ]
    )

  def test_throwsFor0Liquidity(self):
    expect(lambda:
      NonfungiblePositionManager.removeCallParameters(
        Position(PositionConstructorArgs(
          pool=pool_0_1,
          tickLower=-TICK_SPACINGS[FeeAmount.MEDIUM],
          tickUpper=TICK_SPACINGS[FeeAmount.MEDIUM],
          liquidity=0
        )),
        RemoveLiquidityOptions(
          tokenId=tokenId,
          liquidityPercentage=Percent(1),
          slippageTolerance=slippageTolerance,
          deadline=deadline,
          collectOptions=CollectOptionsNoTokenId(
            expectedCurrencyOwed0=CurrencyAmount.fromRawAmount(token0, 0),
            expectedCurrencyOwed1=CurrencyAmount.fromRawAmount(token1, 0),
            recipient=recipient
          )
        )
      )
    ).toThrow(AssertionError, 'ZERO_LIQUIDITY')

  def test_throwsFor0LiquidityFromSmallPercentage(self):
    expect(lambda:
      NonfungiblePositionManager.removeCallParameters(
        Position(PositionConstructorArgs(
          pool=pool_0_1,
          tickLower=-TICK_SPACINGS[FeeAmount.MEDIUM],
          tickUpper=TICK_SPACINGS[FeeAmount.MEDIUM],
          liquidity=50
        )),
        RemoveLiquidityOptions(
          tokenId=tokenId,
          liquidityPercentage=Percent(1, 100),
          slippageTolerance=slippageTolerance,
          deadline=deadline,
          collectOptions=CollectOptionsNoTokenId(
            expectedCurrencyOwed0=CurrencyAmount.fromRawAmount(token0, 0),
            expectedCurrencyOwed1=CurrencyAmount.fromRawAmount(token1, 0),
            recipient=recipient
          )
        )
      )
    ).toThrow(AssertionError, 'ZERO_LIQUIDITY')

  def test_throwsForBadBurn(self):
    expect(lambda:
      NonfungiblePositionManager.removeCallParameters(
        Position(PositionConstructorArgs(
          pool=pool_0_1,
          tickLower=-TICK_SPACINGS[FeeAmount.MEDIUM],
          tickUpper=TICK_SPACINGS[FeeAmount.MEDIUM],
          liquidity=50
        )),
        RemoveLiquidityOptions(
          tokenId=tokenId,
          liquidityPercentage=Percent(99, 100),
          slippageTolerance=slippageTolerance,
          deadline=deadline,
          burnToken=True,
          collectOptions=CollectOptionsNoTokenId(
            expectedCurrencyOwed0=CurrencyAmount.fromRawAmount(token0, 0),
            expectedCurrencyOwed1=CurrencyAmount.fromRawAmount(token1, 0),
            recipient=recipient
          )
        )
      )
    ).toThrow(AssertionError, 'CANNOT_BURN')

  def test_works(self):
    calldata = NonfungiblePositionManager.removeCallParameters(
      Position(PositionConstructorArgs(
        pool=pool_0_1,
        tickLower=-TICK_SPACINGS[FeeAmount.MEDIUM],
        tickUpper=TICK_SPACINGS[FeeAmount.MEDIUM],
        liquidity=100
      )),
      RemoveLiquidityOptions(
        tokenId=tokenId,
        liquidityPercentage=Percent(1),
        slippageTolerance=slippageTolerance,
        deadline=deadline,
        collectOptions=CollectOptionsNoTokenId(
          expectedCurrencyOwed0=CurrencyAmount.fromRawAmount(token0, 0),
          expectedCurrencyOwed1=CurrencyAmount.fromRawAmount(token1, 0),
          recipient=recipient
        )
      )
    )

    expect(calldata).toStrictEqual(
      [
        {
          "to": "NonfungiblePositionManager",
          "method": "decreaseLiquidity",
          "params": {
            "params": {
              "amount0Min": "0x0",
              "amount1Min": "0x0",
              "deadline": "0x7b",
              "liquidity": "0x64",
              "tokenId": "0x1"
            }
          }
        },
        {
          "to": "NonfungiblePositionManager",
          "method": "collect",
          "params": {
            "params": {
              "amount0Max": "0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
              "amount1Max": "0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
              "recipient": "hx0000000000000000000000000000000000000003",
              "tokenId": "0x1"
            }
          }
        }
      ]
    )

  def test_worksForPartial(self):
    calldata = NonfungiblePositionManager.removeCallParameters(
      Position(PositionConstructorArgs(
        pool=pool_0_1,
        tickLower=-TICK_SPACINGS[FeeAmount.MEDIUM],
        tickUpper=TICK_SPACINGS[FeeAmount.MEDIUM],
        liquidity=100
      )),
      RemoveLiquidityOptions(
        tokenId=tokenId,
        liquidityPercentage=Percent(1, 2),
        slippageTolerance=slippageTolerance,
        deadline=deadline,
        collectOptions=CollectOptionsNoTokenId(
          expectedCurrencyOwed0=CurrencyAmount.fromRawAmount(token0, 0),
          expectedCurrencyOwed1=CurrencyAmount.fromRawAmount(token1, 0),
          recipient=recipient
        )
      )
    )

    expect(calldata).toStrictEqual(
      [
        {
            "to": "NonfungiblePositionManager",
            "method": "decreaseLiquidity",
            "params": {
                "params": {
                    "amount0Min": "0x0",
                    "amount1Min": "0x0",
                    "deadline": "0x7b",
                    "liquidity": "0x32",
                    "tokenId": "0x1"
                }
            }
        },
        {
            "to": "NonfungiblePositionManager",
            "method": "collect",
            "params": {
                "params": {
                    "amount0Max": "0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
                    "amount1Max": "0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
                    "recipient": "hx0000000000000000000000000000000000000003",
                    "tokenId": "0x1"
                }
            }
        }
      ]
    )

  def test_worksWithICX(self):
    icxAmount = CurrencyAmount.fromRawAmount(ICX, 0)
    tokenAmount = CurrencyAmount.fromRawAmount(token1, 0)

    calldata = NonfungiblePositionManager.removeCallParameters(
      Position(PositionConstructorArgs(
        pool=pool_1_wicx,
        tickLower=-TICK_SPACINGS[FeeAmount.MEDIUM],
        tickUpper=TICK_SPACINGS[FeeAmount.MEDIUM],
        liquidity=100
      )),
      RemoveLiquidityOptions(
        tokenId=tokenId,
        liquidityPercentage=Percent(1),
        slippageTolerance=slippageTolerance,
        deadline=deadline,
        collectOptions=CollectOptionsNoTokenId(
          expectedCurrencyOwed0=tokenAmount if pool_1_wicx.token0.equals(token1) else icxAmount,
          expectedCurrencyOwed1=icxAmount if pool_1_wicx.token0.equals(token1) else tokenAmount,
          recipient=recipient
        )
      )
    )

    expect(calldata).toStrictEqual(
      [
        {
            "to": "NonfungiblePositionManager",
            "method": "decreaseLiquidity",
            "params": {
                "params": {
                    "amount0Min": "0x0",
                    "amount1Min": "0x0",
                    "deadline": "0x7b",
                    "liquidity": "0x64",
                    "tokenId": "0x1"
                }
            }
        },
        {
            "to": "NonfungiblePositionManager",
            "method": "collect",
            "params": {
                "params": {
                    "amount0Max": "0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
                    "amount1Max": "0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
                    "recipient": "hx0000000000000000000000000000000000000003",
                    "tokenId": "0x1"
                }
            }
        }
      ]
    )

  def test_worksForPartialWithICX(self):
    icxAmount = CurrencyAmount.fromRawAmount(ICX, 0)
    tokenAmount = CurrencyAmount.fromRawAmount(token1, 0)

    calldata = NonfungiblePositionManager.removeCallParameters(
      Position(PositionConstructorArgs(
        pool=pool_1_wicx,
        tickLower=-TICK_SPACINGS[FeeAmount.MEDIUM],
        tickUpper=TICK_SPACINGS[FeeAmount.MEDIUM],
        liquidity=100
      )),
      RemoveLiquidityOptions(
        tokenId=tokenId,
        liquidityPercentage=Percent(1, 2),
        slippageTolerance=slippageTolerance,
        deadline=deadline,
        collectOptions=CollectOptionsNoTokenId(
          expectedCurrencyOwed0=tokenAmount if pool_1_wicx.token0.equals(token1) else icxAmount,
          expectedCurrencyOwed1=icxAmount if pool_1_wicx.token0.equals(token1) else tokenAmount,
          recipient=recipient
        )
      )
    )

    expect(calldata).toStrictEqual(
      [
        {
            "to": "NonfungiblePositionManager",
            "method": "decreaseLiquidity",
            "params": {
                "params": {
                    "amount0Min": "0x0",
                    "amount1Min": "0x0",
                    "deadline": "0x7b",
                    "liquidity": "0x32",
                    "tokenId": "0x1"
                }
            }
        },
        {
            "to": "NonfungiblePositionManager",
            "method": "collect",
            "params": {
                "params": {
                    "amount0Max": "0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
                    "amount1Max": "0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
                    "recipient": "hx0000000000000000000000000000000000000003",
                    "tokenId": "0x1"
                }
            }
        }
      ]
    )

  def test_succeedsNoDataParam(self):
    options = SafeTransferOptions(
      sender,
      recipient,
      tokenId
    )
    calldata = NonfungiblePositionManager.safeTransferFromParameters(options)

    expect(calldata).toStrictEqual(
      [
        {
            "to": "NonfungiblePositionManager",
            "method": "safeTransferFrom",
            "params": {
                "_data": "",
                "from": "hx0000000000000000000000000000000000000004",
                "to": "hx0000000000000000000000000000000000000003",
                "tokenId": "0x1"
            }
        }
    ]
    )
  
  def test_succeedsDataParam(self):
    data = '0x0000000000000000000000000000000000009004'
    options = SafeTransferOptions(
      sender,
      recipient,
      tokenId,
      data
    )
    calldata = NonfungiblePositionManager.safeTransferFromParameters(options)

    expect(calldata).toStrictEqual(
      [
        {
            "to": "NonfungiblePositionManager",
            "method": "safeTransferFrom",
            "params": {
                "_data": "0x0000000000000000000000000000000000009004",
                "from": "hx0000000000000000000000000000000000000004",
                "to": "hx0000000000000000000000000000000000000003",
                "tokenId": "0x1"
            }
        }
      ]
    )

