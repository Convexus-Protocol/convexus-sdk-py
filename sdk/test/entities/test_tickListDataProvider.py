import unittest
from icontoolkit.test.expect import expect
from sdk.entities.tick import TickConstructorArgs

from sdk.entities.tickListDataProvider import TickListDataProvider

class TestTicklistdataprovider(unittest.TestCase):
  
  def test_canTakeAnEmptyListOfTicks(self):
    TickListDataProvider([], 1)

  def test_throwsFor0TickSpacing(self):
    expect(lambda: TickListDataProvider([], 0)).toThrow(AssertionError, 'TICK_SPACING_NONZERO')
  
  def test_throwsForUnevenTickList(self):
    expect(lambda:
        TickListDataProvider(
          [
            TickConstructorArgs(index=-1, liquidityNet=-1, liquidityGross=1),
            TickConstructorArgs(index=1, liquidityNet=2, liquidityGross=1),
          ],
          1
        )
    ).toThrow(AssertionError, 'ZERO_NET')

  def test_throwsIfTickNotInList(self):
    provider = TickListDataProvider(
      [
        TickConstructorArgs(index=-1, liquidityNet=-1, liquidityGross=1),
        TickConstructorArgs(index=1, liquidityNet=1, liquidityGross=1),
      ],
      1
    )
    expect(lambda: provider.getTick(0)).toThrow(AssertionError, 'NOT_CONTAINED')
  
  def test_getsTheSmallestTickFromTheList(self):
    provider = TickListDataProvider(
      [
        TickConstructorArgs(index=-1, liquidityNet=-1, liquidityGross=1),
        TickConstructorArgs(index=1, liquidityNet=1, liquidityGross=1),
      ],
      1
    )
    tick = provider.getTick(-1)
    expect(tick.liquidityNet).toEqual(-1)
    expect(tick.liquidityGross).toEqual(1)
  
  def test_getsTheLargestTickFromTheList(self):
    provider = TickListDataProvider(
      [
        TickConstructorArgs(index=-1, liquidityNet=-1, liquidityGross=1),
        TickConstructorArgs(index=1, liquidityNet=1, liquidityGross=1),
      ],
      1
    )
    tick = provider.getTick(1)
    expect(tick.liquidityNet).toEqual(1)
    expect(tick.liquidityGross).toEqual(1)

