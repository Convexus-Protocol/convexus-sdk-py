import unittest
from convexus.icontoolkit.expect import expect

from convexus.sdk.utils.tickMath import TickMath
from convexus.sdk.utils.nearestUsableTick import nearestUsableTick

class TestNearestusabletick(unittest.TestCase):
  def test_throwsIfTickSpacingIs0(self):
    expect(lambda: nearestUsableTick(1, 0)).toThrow(AssertionError, 'TICK_SPACING')

  def test_throwsIfTickSpacingIsNegative(self):
    expect(lambda: nearestUsableTick(1, -5)).toThrow(AssertionError, 'TICK_SPACING')

  def test_throwsIfEitherIsNonInteger(self):
    expect(lambda: nearestUsableTick(1.5, 1)).toThrow(AssertionError, 'INTEGERS')
    expect(lambda: nearestUsableTick(1, 1.5)).toThrow(AssertionError, 'INTEGERS')

  def test_throwsIfTickIsGreaterThanTickMathMAX_TICK(self):
    expect(lambda: nearestUsableTick(TickMath.MAX_TICK + 1, 1)).toThrow(AssertionError, 'TICK_BOUND')
    expect(lambda: nearestUsableTick(TickMath.MIN_TICK - 1, 1)).toThrow(AssertionError, 'TICK_BOUND')

  def test_roundsAtPositiveHalf(self):
    expect(nearestUsableTick(5, 10)).toEqual(10)

  def test_roundsDownBelowPositiveHalf(self):
    expect(nearestUsableTick(4, 10)).toEqual(0)

  def test_roundsUpForNegativeHalf(self):
    expect(nearestUsableTick(-5, 10)).toEqual(-0)

  def test_roundsUpForNegativeHalf(self):
    expect(nearestUsableTick(-6, 10)).toEqual(-10)

  def test_cannotRoundPastMIN_TICK(self):
    expect(nearestUsableTick(TickMath.MIN_TICK, TickMath.MAX_TICK // 2 + 100)).toEqual(-(TickMath.MAX_TICK // 2 + 100))

  def test_cannotRoundPastMAX_TICK(self):
    expect(nearestUsableTick(TickMath.MAX_TICK, TickMath.MAX_TICK // 2 + 100)).toEqual(TickMath.MAX_TICK // 2 + 100)

