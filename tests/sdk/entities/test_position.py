import unittest

from convexus.icontoolkit.expect import expect
from convexus.sdk.constants import TICK_SPACINGS, FeeAmount
from convexus.sdkcore.entities.currency import Token

from convexus.sdk.utils.encodeSqrtRatioX96 import encodeSqrtRatioX96
from convexus.sdk.entities.pool import Pool
from convexus.sdk.utils.tickMath import TickMath

from convexus.sdk.utils.nearestUsableTick import nearestUsableTick
from convexus.sdk.entities.position import Position, PositionConstructorArgs
from convexus.sdkcore.entities.fractions.percent import Percent

USDC = Token('cxa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48', 6, 'USDC', 'USD Coin')
DAI = Token('cx6b175474e89094c44da98b954eedeac495271d0f', 18, 'DAI', 'DAI Stablecoin')
POOL_SQRT_RATIO_START = encodeSqrtRatioX96(int(100e6), int(100e18))
POOL_TICK_CURRENT = TickMath.getTickAtSqrtRatio(POOL_SQRT_RATIO_START)
TICK_SPACING = TICK_SPACINGS[FeeAmount.LOW]
DAI_USDC_POOL = Pool(DAI, USDC, FeeAmount.LOW, POOL_SQRT_RATIO_START, 0, POOL_TICK_CURRENT, [])

class TestPosition(unittest.TestCase):

  def test_canBeConstructedAround0Tick(self):
      position = Position(PositionConstructorArgs(
        pool=DAI_USDC_POOL,
        liquidity=1,
        tickLower=-10,
        tickUpper=10
      ))
      expect(position.liquidity).toEqual(1)
      
  def test_canUseMinAndMaxTicks(self):
    position = Position(PositionConstructorArgs(
      pool=DAI_USDC_POOL,
      liquidity=1,
      tickLower=nearestUsableTick(TickMath.MIN_TICK, TICK_SPACING),
      tickUpper=nearestUsableTick(TickMath.MAX_TICK, TICK_SPACING)
    ))
    expect(position.liquidity).toEqual(1)

  def test_tickLowerMustBeLessThanTickUpper(self):
    expect(
      lambda:
        Position(PositionConstructorArgs(
          pool=DAI_USDC_POOL,
          liquidity=1,
          tickLower=10,
          tickUpper=-10
        ))
    ).toThrow(AssertionError, 'TICK_ORDER')

  def test_tickLowerCannotEqualTickUpper(self):
    expect(
      lambda:
        Position(PositionConstructorArgs(
          pool=DAI_USDC_POOL,
          liquidity=1,
          tickLower=-10,
          tickUpper=-10
        ))
    ).toThrow(AssertionError, 'TICK_ORDER')

  def test_tickLowerMustBeMultipleOfTickSpacing(self):
    expect(
      lambda:
        Position(PositionConstructorArgs(
          pool=DAI_USDC_POOL,
          liquidity=1,
          tickLower=-5,
          tickUpper=10
        ))
    ).toThrow(AssertionError, 'TICK_LOWER')

  def test_tickLowerMustBeGreaterThanMIN_TICK(self):
    expect(
      lambda:
        Position(PositionConstructorArgs(
          pool=DAI_USDC_POOL,
          liquidity=1,
          tickLower=nearestUsableTick(TickMath.MIN_TICK, TICK_SPACING) - TICK_SPACING,
          tickUpper=10
        ))
    ).toThrow(AssertionError, 'TICK_LOWER')

  def test_tickUpperMustBeMultipleOfTickSpacing(self):
    expect(
      lambda:
        Position(PositionConstructorArgs(
          pool=DAI_USDC_POOL,
          liquidity=1,
          tickLower=-10,
          tickUpper=15
        ))
    ).toThrow(AssertionError, 'TICK_UPPER')

  def test_tickUpperMustBeLessThanMAX_TICK(self):
    expect(
      lambda:
        Position(PositionConstructorArgs(
          pool=DAI_USDC_POOL,
          liquidity=1,
          tickLower=-10,
          tickUpper=nearestUsableTick(TickMath.MAX_TICK, TICK_SPACING) + TICK_SPACING
        ))
    ).toThrow(AssertionError, 'TICK_UPPER')

  def test_isCorrectForPriceAbove(self):
    expect(
      Position(PositionConstructorArgs(
        pool=DAI_USDC_POOL,
        liquidity=100e12,
        tickLower=nearestUsableTick(POOL_TICK_CURRENT, TICK_SPACING) + TICK_SPACING,
        tickUpper=nearestUsableTick(POOL_TICK_CURRENT, TICK_SPACING) + TICK_SPACING * 2
      )).amount0.quotient
    ).toEqual(49949961958869842)

  def test_isCorrectForPriceBelow(self):
    expect(
      Position(PositionConstructorArgs(
        pool=DAI_USDC_POOL,
        liquidity=int(100e18),
        tickLower=nearestUsableTick(POOL_TICK_CURRENT, TICK_SPACING) - TICK_SPACING * 2,
        tickUpper=nearestUsableTick(POOL_TICK_CURRENT, TICK_SPACING) - TICK_SPACING
      )).amount0.quotient
    ).toEqual(0)

  def test_isCorrectForInRangePosition(self):
      expect(
        Position(PositionConstructorArgs(
          pool=DAI_USDC_POOL,
          liquidity=int(100e18),
          tickLower=nearestUsableTick(POOL_TICK_CURRENT, TICK_SPACING) - TICK_SPACING * 2,
          tickUpper=nearestUsableTick(POOL_TICK_CURRENT, TICK_SPACING) + TICK_SPACING * 2
        )).amount0.quotient
      ).toEqual(120054069145292520957015)
  
  def test_isCorrectForPriceAbove(self):
      expect(
        Position(PositionConstructorArgs(
          pool=DAI_USDC_POOL,
          liquidity=int(100e18),
          tickLower=nearestUsableTick(POOL_TICK_CURRENT, TICK_SPACING) + TICK_SPACING,
          tickUpper=nearestUsableTick(POOL_TICK_CURRENT, TICK_SPACING) + TICK_SPACING * 2
        )).amount1.quotient
      ).toEqual(0)
  
  def test_isCorrectForPriceBelow(self):
      expect(
        Position(PositionConstructorArgs(
          pool=DAI_USDC_POOL,
          liquidity=int(100e18),
          tickLower=nearestUsableTick(POOL_TICK_CURRENT, TICK_SPACING) - TICK_SPACING * 2,
          tickUpper=nearestUsableTick(POOL_TICK_CURRENT, TICK_SPACING) - TICK_SPACING
        )).amount1.quotient
      ).toEqual(49970077053)

  def test_isCorrectForInRangePosition(self):
      expect(
        Position(PositionConstructorArgs(
          pool=DAI_USDC_POOL,
          liquidity=int(100e18),
          tickLower=nearestUsableTick(POOL_TICK_CURRENT, TICK_SPACING) - TICK_SPACING * 2,
          tickUpper=nearestUsableTick(POOL_TICK_CURRENT, TICK_SPACING) + TICK_SPACING * 2
        )).amount1.quotient
      ).toEqual(79831926243)


class TestPositionWithNoSlippage(unittest.TestCase):

  def setUp(self) -> None:
    super().setUp()
    self.slippageTolerance = Percent(0)

  def test_isCorrectForPositionsBelow(self):
    position = Position(PositionConstructorArgs(
      pool=DAI_USDC_POOL,
      liquidity=int(100e18),
      tickLower=nearestUsableTick(POOL_TICK_CURRENT, TICK_SPACING) + TICK_SPACING,
      tickUpper=nearestUsableTick(POOL_TICK_CURRENT, TICK_SPACING) + TICK_SPACING * 2
    ))
    
    amounts = position.mintAmountsWithSlippage(self.slippageTolerance)
    amount0 = amounts.amount0
    amount1 = amounts.amount1

    expect(amount0).toEqual(49949961958869841738198)
    expect(amount1).toEqual(0)
      
  def test_isCorrectForPositionsAbove(self):
    position = Position(PositionConstructorArgs(
      pool=DAI_USDC_POOL,
      liquidity=int(100e18),
      tickLower=nearestUsableTick(POOL_TICK_CURRENT, TICK_SPACING) - TICK_SPACING * 2,
      tickUpper=nearestUsableTick(POOL_TICK_CURRENT, TICK_SPACING) - TICK_SPACING
    ))

    amounts = position.mintAmountsWithSlippage(self.slippageTolerance)
    amount0 = amounts.amount0
    amount1 = amounts.amount1

    expect(amount0).toEqual(0)
    expect(amount1).toEqual(49970077053)
  
  def test_isCorrectForPositionsWithin(self):
    position = Position(PositionConstructorArgs(
      pool=DAI_USDC_POOL,
      liquidity=int(100e18),
      tickLower=nearestUsableTick(POOL_TICK_CURRENT, TICK_SPACING) - TICK_SPACING * 2,
      tickUpper=nearestUsableTick(POOL_TICK_CURRENT, TICK_SPACING) + TICK_SPACING * 2
    ))

    amounts = position.mintAmountsWithSlippage(self.slippageTolerance)
    amount0 = amounts.amount0
    amount1 = amounts.amount1

    expect(amount0).toEqual(120054069145292520306322)
    expect(amount1).toEqual(79831926243)
    
class TestPositionWithSmallSlippage(unittest.TestCase):

  def setUp(self) -> None:
    super().setUp()
    self.slippageTolerance = Percent(5, 10000)

  def test_isCorrectForPositionsBelow(self):
    position = Position(PositionConstructorArgs(
      pool=DAI_USDC_POOL,
      liquidity=int(100e18),
      tickLower=nearestUsableTick(POOL_TICK_CURRENT, TICK_SPACING) + TICK_SPACING,
      tickUpper=nearestUsableTick(POOL_TICK_CURRENT, TICK_SPACING) + TICK_SPACING * 2
    ))

    amounts = position.mintAmountsWithSlippage(self.slippageTolerance)
    amount0 = amounts.amount0
    amount1 = amounts.amount1

    expect(amount0).toEqual(49949961958869841738198)
    expect(amount1).toEqual(0)
      
  def test_isCorrectForPositionsAbove(self):
    position = Position(PositionConstructorArgs(
      pool=DAI_USDC_POOL,
      liquidity=int(100e18),
      tickLower=nearestUsableTick(POOL_TICK_CURRENT, TICK_SPACING) - TICK_SPACING * 2,
      tickUpper=nearestUsableTick(POOL_TICK_CURRENT, TICK_SPACING) - TICK_SPACING
    ))

    amounts = position.mintAmountsWithSlippage(self.slippageTolerance)
    amount0 = amounts.amount0
    amount1 = amounts.amount1

    expect(amount0).toEqual(0)
    expect(amount1).toEqual(49970077053)
  
  def test_isCorrectForPositionsWithin(self):
    position = Position(PositionConstructorArgs(
      pool=DAI_USDC_POOL,
      liquidity=int(100e18),
      tickLower=nearestUsableTick(POOL_TICK_CURRENT, TICK_SPACING) - TICK_SPACING * 2,
      tickUpper=nearestUsableTick(POOL_TICK_CURRENT, TICK_SPACING) + TICK_SPACING * 2
    ))

    amounts = position.mintAmountsWithSlippage(self.slippageTolerance)
    amount0 = amounts.amount0
    amount1 = amounts.amount1

    expect(amount0).toEqual(95063440240746174725620)
    expect(amount1).toEqual(54828800461)
    
class TestPositionWithMediumSlippage(unittest.TestCase):

  def setUp(self) -> None:
    super().setUp()
    self.slippageTolerance = Percent(5, 100)

  def test_isCorrectForPoolAtMinPrice(self):
    position = Position(PositionConstructorArgs(
      pool=Pool(DAI, USDC, FeeAmount.LOW, TickMath.MIN_SQRT_RATIO, 0, TickMath.MIN_TICK, []),
      liquidity=int(100e18),
      tickLower=nearestUsableTick(POOL_TICK_CURRENT, TICK_SPACING) + TICK_SPACING,
      tickUpper=nearestUsableTick(POOL_TICK_CURRENT, TICK_SPACING) + TICK_SPACING * 2
    ))

    amounts = position.burnAmountsWithSlippage(self.slippageTolerance)
    amount0 = amounts.amount0
    amount1 = amounts.amount1

    expect(amount0).toEqual(49949961958869841754182)
    expect(amount1).toEqual(0)
      
  def test_isCorrectForPoolAtMaxPrice(self):
        position = Position(PositionConstructorArgs(
          pool=Pool(
            DAI,
            USDC,
            FeeAmount.LOW,
            TickMath.MAX_SQRT_RATIO - 1,
            0,
            TickMath.MAX_TICK - 1,
            []
          ),
          liquidity=int(100e18),
          tickLower=nearestUsableTick(POOL_TICK_CURRENT, TICK_SPACING) + TICK_SPACING,
          tickUpper=nearestUsableTick(POOL_TICK_CURRENT, TICK_SPACING) + TICK_SPACING * 2
        ))
        amounts = position.burnAmountsWithSlippage(self.slippageTolerance)
        amount0 = amounts.amount0
        amount1 = amounts.amount1

        expect(amount0).toEqual(0)
        expect(amount1).toEqual(50045084660)
  
class TestPositioBurnnWithNoSlippage2(unittest.TestCase):

  def setUp(self) -> None:
    super().setUp()
    self.slippageTolerance = Percent(0)

  def test_isCorrectForPositionsBelow(self):
    position = Position(PositionConstructorArgs(
      pool=DAI_USDC_POOL,
      liquidity=int(100e18),
      tickLower=nearestUsableTick(POOL_TICK_CURRENT, TICK_SPACING) + TICK_SPACING,
      tickUpper=nearestUsableTick(POOL_TICK_CURRENT, TICK_SPACING) + TICK_SPACING * 2
    ))
      
    amounts = position.burnAmountsWithSlippage(self.slippageTolerance)
    amount0 = amounts.amount0
    amount1 = amounts.amount1

    expect(amount0).toEqual(49949961958869841754182)
    expect(amount1).toEqual(0)
      
  def test_isCorrectForPositionsAbove(self):
    position = Position(PositionConstructorArgs(
      pool=DAI_USDC_POOL,
      liquidity=int(100e18),
      tickLower=nearestUsableTick(POOL_TICK_CURRENT, TICK_SPACING) - TICK_SPACING * 2,
      tickUpper=nearestUsableTick(POOL_TICK_CURRENT, TICK_SPACING) - TICK_SPACING
    ))
    
    amounts = position.burnAmountsWithSlippage(self.slippageTolerance)
    amount0 = amounts.amount0
    amount1 = amounts.amount1

    expect(amount0).toEqual(0)
    expect(amount1).toEqual(49970077053)
      
  def test_isCorrectForPositionsWithin(self):
    position = Position(PositionConstructorArgs(
      pool=DAI_USDC_POOL,
      liquidity=int(100e18),
      tickLower=nearestUsableTick(POOL_TICK_CURRENT, TICK_SPACING) - TICK_SPACING * 2,
      tickUpper=nearestUsableTick(POOL_TICK_CURRENT, TICK_SPACING) + TICK_SPACING * 2
    ))
    
    amounts = position.burnAmountsWithSlippage(self.slippageTolerance)
    amount0 = amounts.amount0
    amount1 = amounts.amount1

    expect(amount0).toEqual(120054069145292520957015)
    expect(amount1).toEqual(79831926243)
    
class TestPositionBurnWithSmallSlippage(unittest.TestCase):

  def setUp(self) -> None:
    super().setUp()
    self.slippageTolerance = Percent(5, 10000)

  def test_isCorrectForPositionsBelow(self):
    position = Position(PositionConstructorArgs(
      pool=DAI_USDC_POOL,
      liquidity=int(100e18),
      tickLower=nearestUsableTick(POOL_TICK_CURRENT, TICK_SPACING) + TICK_SPACING,
      tickUpper=nearestUsableTick(POOL_TICK_CURRENT, TICK_SPACING) + TICK_SPACING * 2
    ))
    amounts = position.burnAmountsWithSlippage(self.slippageTolerance)
    amount0 = amounts.amount0
    amount1 = amounts.amount1

    expect(amount0).toEqual(49949961958869841754182)
    expect(amount1).toEqual(0)
      
  def test_isCorrectForPositionsAbove(self):
    position = Position(PositionConstructorArgs(
      pool=DAI_USDC_POOL,
      liquidity=int(100e18),
      tickLower=nearestUsableTick(POOL_TICK_CURRENT, TICK_SPACING) - TICK_SPACING * 2,
      tickUpper=nearestUsableTick(POOL_TICK_CURRENT, TICK_SPACING) - TICK_SPACING
    ))
    amounts = position.burnAmountsWithSlippage(self.slippageTolerance)
    amount0 = amounts.amount0
    amount1 = amounts.amount1

    expect(amount0).toEqual(0)
    expect(amount1).toEqual(49970077053)
      
  def test_isCorrectForPositionsWithin(self):
    position = Position(PositionConstructorArgs(
      pool=DAI_USDC_POOL,
      liquidity=int(100e18),
      tickLower=nearestUsableTick(POOL_TICK_CURRENT, TICK_SPACING) - TICK_SPACING * 2,
      tickUpper=nearestUsableTick(POOL_TICK_CURRENT, TICK_SPACING) + TICK_SPACING * 2
    ))
    amounts = position.burnAmountsWithSlippage(self.slippageTolerance)
    amount0 = amounts.amount0
    amount1 = amounts.amount1

    expect(amount0).toEqual(95063440240746175240864)
    expect(amount1).toEqual(54828800461)
    
class TestPositionBurnWithMediumSlippage(unittest.TestCase):

  def setUp(self) -> None:
    super().setUp()
    self.slippageTolerance = Percent(5, 100)

  def test_isCorrectForPoolAtMinPrice(self):
    position = Position(PositionConstructorArgs(
      pool=Pool(DAI, USDC, FeeAmount.LOW, TickMath.MIN_SQRT_RATIO, 0, TickMath.MIN_TICK, []),
      liquidity=int(100e18),
      tickLower=nearestUsableTick(POOL_TICK_CURRENT, TICK_SPACING) + TICK_SPACING,
      tickUpper=nearestUsableTick(POOL_TICK_CURRENT, TICK_SPACING) + TICK_SPACING * 2
    ))
    amounts = position.mintAmountsWithSlippage(self.slippageTolerance)
    amount0 = amounts.amount0
    amount1 = amounts.amount1

    expect(amount0).toEqual(49949961958869841738198)
    expect(amount1).toEqual(0)
      
  def test_isCorrectForPoolAtMaxPrice(self):
    position = Position(PositionConstructorArgs(
      pool=Pool(
        DAI,
        USDC,
        FeeAmount.LOW,
        TickMath.MAX_SQRT_RATIO - 1,
        0,
        TickMath.MAX_TICK - 1,
        []
      ),
      liquidity=int(100e18),
      tickLower=nearestUsableTick(POOL_TICK_CURRENT, TICK_SPACING) + TICK_SPACING,
      tickUpper=nearestUsableTick(POOL_TICK_CURRENT, TICK_SPACING) + TICK_SPACING * 2
    ))

    amounts = position.mintAmountsWithSlippage(self.slippageTolerance)
    amount0 = amounts.amount0
    amount1 = amounts.amount1

    expect(amount0).toEqual(0)
    expect(amount1).toEqual(50045084660)
  
  def test_isCorrectForPriceAbove(self):
    amounts = Position(PositionConstructorArgs(
      pool=DAI_USDC_POOL,
      liquidity=int(100e18),
      tickLower=nearestUsableTick(POOL_TICK_CURRENT, TICK_SPACING) + TICK_SPACING,
      tickUpper=nearestUsableTick(POOL_TICK_CURRENT, TICK_SPACING) + TICK_SPACING * 2
    )).mintAmounts
    amount0 = amounts.amount0
    amount1 = amounts.amount1
    expect(amount0).toEqual(49949961958869841754182)
    expect(amount1).toEqual(0)
  
  def test_isCorrectForPriceBelow(self):
    amounts = Position(PositionConstructorArgs(
      pool=DAI_USDC_POOL,
      liquidity=int(100e18),
      tickLower=nearestUsableTick(POOL_TICK_CURRENT, TICK_SPACING) - TICK_SPACING * 2,
      tickUpper=nearestUsableTick(POOL_TICK_CURRENT, TICK_SPACING) - TICK_SPACING
    )).mintAmounts
    
    amount0 = amounts.amount0
    amount1 = amounts.amount1
    expect(amount0).toEqual(0)
    expect(amount1).toEqual(49970077053)

  def test_isCorrectForInRangePosition(self):
    amounts = Position(PositionConstructorArgs(
      pool=DAI_USDC_POOL,
      liquidity=int(100e18),
      tickLower=nearestUsableTick(POOL_TICK_CURRENT, TICK_SPACING) - TICK_SPACING * 2,
      tickUpper=nearestUsableTick(POOL_TICK_CURRENT, TICK_SPACING) + TICK_SPACING * 2
    )).mintAmounts
      
    amount0 = amounts.amount0
    amount1 = amounts.amount1

    # note these are rounded up
    expect(amount0).toEqual(120054069145292520957015)
    expect(amount1).toEqual(79831926243)
