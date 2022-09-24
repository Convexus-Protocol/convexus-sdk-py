import unittest
from sdk.utils.tickMath import TickMath 
from sdk.entities.tick import Tick
from sdk.utils.tickList import TickList

class TestTickList(unittest.TestCase):

  def setUp(self) -> None:
    super().setUp()
    
    self.lowTick = Tick(TickMath.MIN_TICK + 1, 10, 10)
    self.midTick = Tick(0, 5, -5)
    self.highTick = Tick(TickMath.MAX_TICK - 1, 5, -5)
    self.ticks = [self.lowTick, self.midTick, self.highTick]
  
  def test_validate_errorsForIncompleteLists(self):
    with self.assertRaises(AssertionError) as cm:
      TickList.validateList([self.lowTick], 1)
    self.assertEqual(str(cm.exception), "ZERO_NET")
  
  def test_validate_errorsForSorted(self):
    with self.assertRaises(AssertionError) as cm:
      TickList.validateList([self.highTick, self.lowTick, self.midTick], 1)
    self.assertEqual(str(cm.exception), "SORTED")
  
  def test_validate_errorsIfTicksAreNotOnMultiplesOfTickSpacing(self):
    with self.assertRaises(AssertionError) as cm:
      TickList.validateList([self.highTick, self.lowTick, self.midTick], 1337)
    self.assertEqual(str(cm.exception), "TICK_SPACING")
  
  def test_isBelowSmallest(self):
    ticks = [self.lowTick, self.midTick, self.highTick]
    self.assertTrue(TickList.isBelowSmallest(ticks, TickMath.MIN_TICK))
    self.assertFalse(TickList.isBelowSmallest(ticks, TickMath.MIN_TICK + 1))
  
  def test_isAtOrAboveLargest(self):
    ticks = [self.lowTick, self.midTick, self.highTick]
    self.assertFalse(TickList.isAtOrAboveLargest(ticks, TickMath.MAX_TICK - 2))
    self.assertTrue(TickList.isAtOrAboveLargest(ticks, TickMath.MAX_TICK - 1))

  def test_nextInitializedTick_lowMinusTteEqualTrue(self):
      with self.assertRaises(AssertionError) as cm:
        TickList.nextInitializedTick(self.ticks, TickMath.MIN_TICK, True)
      self.assertEqual(str(cm.exception), 'BELOW_SMALLEST')

      self.assertEqual(TickList.nextInitializedTick(self.ticks, TickMath.MIN_TICK + 1, True), self.lowTick)
      self.assertEqual(TickList.nextInitializedTick(self.ticks, TickMath.MIN_TICK + 2, True), self.lowTick)

  def test_nextInitializedTick_lowMinusTteEquaFalse(self):
      self.assertEqual(TickList.nextInitializedTick(self.ticks, TickMath.MIN_TICK, False), self.lowTick)
      self.assertEqual(TickList.nextInitializedTick(self.ticks, TickMath.MIN_TICK + 1, False), self.midTick)

  def test_nextInitializedTick_MidMinusLteTrue(self):
      self.assertEqual(TickList.nextInitializedTick(self.ticks, 0, True), self.midTick)
      self.assertEqual(TickList.nextInitializedTick(self.ticks, 1, True), self.midTick)

  def test_nextInitializedTick_MidMinusLteFalse(self):
      self.assertEqual(TickList.nextInitializedTick(self.ticks, -1, False), self.midTick)
      self.assertEqual(TickList.nextInitializedTick(self.ticks, 1, False), self.highTick)

  def test_nextInitializedTick_MidHighLteTrue(self):
      self.assertEqual(TickList.nextInitializedTick(self.ticks, TickMath.MAX_TICK - 1, True), self.highTick)
      self.assertEqual(TickList.nextInitializedTick(self.ticks, TickMath.MAX_TICK, True), self.highTick)

  def test_nextInitializedTick_MidHighLteFalse(self):
      with self.assertRaises(AssertionError) as cm:
        TickList.nextInitializedTick(self.ticks, TickMath.MAX_TICK - 1, False)
      self.assertEqual(str(cm.exception), 'AT_OR_ABOVE_LARGEST')

      self.assertEqual(TickList.nextInitializedTick(self.ticks, TickMath.MAX_TICK - 2, False), self.highTick)
      self.assertEqual(TickList.nextInitializedTick(self.ticks, TickMath.MAX_TICK - 3, False), self.highTick)

  def test_nextInitializedTickWithinOneWord_WordsAround0LteTrue(self):
    self.assertEqual(TickList.nextInitializedTickWithinOneWord(self.ticks, -257, True, 1), [-512, False])
    self.assertEqual(TickList.nextInitializedTickWithinOneWord(self.ticks, -256, True, 1), [-256, False])
    self.assertEqual(TickList.nextInitializedTickWithinOneWord(self.ticks, -1, True, 1), [-256, False])
    self.assertEqual(TickList.nextInitializedTickWithinOneWord(self.ticks, 0, True, 1), [0, True])
    self.assertEqual(TickList.nextInitializedTickWithinOneWord(self.ticks, 1, True, 1), [0, True])
    self.assertEqual(TickList.nextInitializedTickWithinOneWord(self.ticks, 255, True, 1), [0, True])
    self.assertEqual(TickList.nextInitializedTickWithinOneWord(self.ticks, 256, True, 1), [256, False])
    self.assertEqual(TickList.nextInitializedTickWithinOneWord(self.ticks, 257, True, 1), [256, False])

  def test_nextInitializedTickWithinOneWord_WordsAround0LteFalse(self):
    self.assertEqual(TickList.nextInitializedTickWithinOneWord(self.ticks, -258, False, 1), [-257, False])
    self.assertEqual(TickList.nextInitializedTickWithinOneWord(self.ticks, -257, False, 1), [-1, False])
    self.assertEqual(TickList.nextInitializedTickWithinOneWord(self.ticks, -256, False, 1), [-1, False])
    self.assertEqual(TickList.nextInitializedTickWithinOneWord(self.ticks, -2, False, 1), [-1, False])
    self.assertEqual(TickList.nextInitializedTickWithinOneWord(self.ticks, -1, False, 1), [0, True])
    self.assertEqual(TickList.nextInitializedTickWithinOneWord(self.ticks, 0, False, 1), [255, False])
    self.assertEqual(TickList.nextInitializedTickWithinOneWord(self.ticks, 1, False, 1), [255, False])
    self.assertEqual(TickList.nextInitializedTickWithinOneWord(self.ticks, 254, False, 1), [255, False])
    self.assertEqual(TickList.nextInitializedTickWithinOneWord(self.ticks, 255, False, 1), [511, False])
    self.assertEqual(TickList.nextInitializedTickWithinOneWord(self.ticks, 256, False, 1), [511, False])
      
  def test_nextInitializedTickWithinOneWord_PerformsCorrectlyWithTickSpacing1(self):
    ticks = [Tick(0, 0, 0), Tick(511, 0, 0)]
    
    self.assertEqual(TickList.nextInitializedTickWithinOneWord(ticks, 0, False, 1), [255, False])
    self.assertEqual(TickList.nextInitializedTickWithinOneWord(ticks, 0, False, 2), [510, False])

if __name__ == '__main__':
    unittest.main()