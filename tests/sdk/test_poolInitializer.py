import unittest
from convexus.icontoolkit.expect import expect
from convexus.sdk.entities.position import Position, PositionConstructorArgs
from convexus.sdk.utils.tickMath import TickMath
from convexus.sdkcore.constants import MaxUint256

from convexus.sdkcore.entities.currency import Token
from convexus.sdk.constants import TICK_SPACINGS, FeeAmount
from convexus.sdk.utils.encodeSqrtRatioX96 import encodeSqrtRatioX96
from convexus.sdk.entities.pool import Pool
from convexus.sdk.poolInitializer import PoolInitializer
from convexus.sdk.utils.maxLiquidityForAmounts import maxLiquidityForAmounts
from convexus.sdk.utils.nearestUsableTick import nearestUsableTick
from convexus.sdk.utils.priceTickConversions import priceToClosestTick
from convexus.sdkcore.entities.fractions.price import Price
from convexus.sdkcore.entities.fractions.percent import Percent
from convexus.sdk.nonfungiblePositionManager import MintOptions, NonfungiblePositionManager

token0 = Token('cx0000000000000000000000000000000000000001', 18, 't0', 'token0')
token1 = Token('cx0000000000000000000000000000000000000002', 18, 't1', 'token1')
# Medium fee (0.3%)
fee = FeeAmount.MEDIUM
# Default pool price : 1 token0 = 1 token1 (1:1)
poolPrice = encodeSqrtRatioX96(1, 1)
# Initial liquidity : 0
liquidity = 0
# Current tick doesn't need to be computed for deployment
tickCurrent = 0
# Create a pool
pool_0_1 = Pool(token0, token1, fee, poolPrice, liquidity, tickCurrent)

class TestPoolinitializer(unittest.TestCase):  # Create two tokens

  def test_succeeds(self):
    # Pool initializer needs a Pool instance
    calldata = PoolInitializer.createCallParameters(pool_0_1)

    expect(calldata).toStrictEqual(
      [
        {
          "to": "PoolInitializer",
          "method": "createAndInitializePoolIfNecessary",
          "params": {
            "fee": "0xbb8",
            "sqrtPriceX96": "0x1000000000000000000000000",
            "token0": "cx0000000000000000000000000000000000000001",
            "token1": "cx0000000000000000000000000000000000000002"
          }
        }
      ]
    )

  def test_succeedsAndDepositLiquidity(self):
    # Initialize the pool
    PoolInitializer.createCallParameters(pool_0_1)

    # Provide liquidity between 500 and 800
    lowerBoundPrice = 500
    higherBoundPrice = 800

    EXA = 10**18
    amount0 = EXA * 5 # 5 token0
    amount1 = MaxUint256 # compute amount1 needed

    # Compute the max liquidity for 5 token0
    liquidity = maxLiquidityForAmounts (
      poolPrice, # Pool price
      encodeSqrtRatioX96(lowerBoundPrice, 1), # lower bound price
      encodeSqrtRatioX96(higherBoundPrice, 1), # upper bound price
      amount0, amount1, # amounts of token provided
      True
    )

    # Compute lower & upper ticks from prices
    tickLower = nearestUsableTick(priceToClosestTick(Price(token0, token1, 1, lowerBoundPrice)), TICK_SPACINGS[fee])
    tickUpper = nearestUsableTick(priceToClosestTick(Price(token0, token1, 1, higherBoundPrice)), TICK_SPACINGS[fee])

    # adress that will receive the position NFT
    recipient = 'hx0000000000000000000000000000000000000003'
    slippageTolerance = Percent(1, 100)
    deadline = 123

    NonfungiblePositionManager.addCallParameters(
      Position(PositionConstructorArgs(
        pool=pool_0_1,
        tickLower=tickLower,
        tickUpper=tickUpper,
        liquidity=liquidity
      )),
      MintOptions(
        recipient=recipient,
        slippageTolerance=slippageTolerance,
        deadline=deadline
      )
    )

  def test_createInitializeMint(self):
    # Init price: 1 token0 = 600 token1
    sqrtRatioX96: int = encodeSqrtRatioX96(600, 1)
    
    # Provide liquidity between 500 and 800
    lowerBoundPrice = 500
    higherBoundPrice = 800
    
    tickLower = nearestUsableTick(priceToClosestTick(Price(token0, token1, 1, lowerBoundPrice)), TICK_SPACINGS[fee])
    tickUpper = nearestUsableTick(priceToClosestTick(Price(token0, token1, 1, higherBoundPrice)), TICK_SPACINGS[fee])
    
    # Create a virtual pool
    pool = Pool(token0, token1, fee, sqrtRatioX96, 0, TickMath.getTickAtSqrtRatio(sqrtRatioX96))
    
    EXA = 10**18
    amount0 = EXA * 5 # 5 token0
    amount1 = MaxUint256 # compute amount1 needed
    
    # Compute the max liquidity given the amounts
    liquidity = maxLiquidityForAmounts (
      pool.sqrtRatioX96, # Pool price
      encodeSqrtRatioX96(lowerBoundPrice, 1), # lower bound price
      encodeSqrtRatioX96(higherBoundPrice, 1), # upper bound price
      amount0, amount1, # amounts of token provided
      True
    )

    position = Position(PositionConstructorArgs(
      pool,
      tickLower,
      tickUpper,
      liquidity
    ))

    # adress that will receive the position NFT
    recipient = 'hx0000000000000000000000000000000000000003'
    deadline = 123
    
    # Initialize the pool + mint position
    calldatas = PoolInitializer.createAndMintCallParameters(position, recipient, deadline)
    expect(calldatas[0]).toBe(
      {
        "to": "PoolInitializer",
        "method": "createAndInitializePoolIfNecessaryAndMintPosition",
        "params": {
            "token0": "cx0000000000000000000000000000000000000001",
            "token1": "cx0000000000000000000000000000000000000002",
            "fee": "0xbb8",
            "sqrtPriceX96": "0x187eb1990b697a000000000000",
            "tickLower": "0xf2d0",
            "tickUpper": "0x10518",
            "amount0Desired": "0x452d3f9ea9235439",
            "amount1Desired": "0x692a76b89ac3c052fb",
            "amount0Min": "0x0",
            "amount1Min": "0x0",
            "recipient": "hx0000000000000000000000000000000000000003",
            "deadline": "0x7b"
        }
      }
    )
