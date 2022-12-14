import unittest
from convexus.icontoolkit.expect import expect
from convexus.sdk.entities.tick import Tick, TickConstructorArgs
from convexus.sdk.utils.tickMath import TickMath

class TestTick(unittest.TestCase):
    def test_throwsIfTickIsBelowMinTick(self):
      expect(lambda: Tick(TickConstructorArgs(
        index=TickMath.MIN_TICK - 1,
        liquidityGross=0,
        liquidityNet=0
      ))).toThrow(AssertionError, 'TICK')

    def test_throwsIfTickIsAboveMaxTick(self):
      expect(lambda: Tick(TickConstructorArgs(
      index=TickMath.MAX_TICK + 1,
      liquidityGross=0,
      liquidityNet=0
    ))).toThrow(AssertionError, 'TICK')

