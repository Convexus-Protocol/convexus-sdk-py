import unittest
from icontoolkit.test.expect import expect
from sdkcore.utils.sortedInsert import sortedInsert

def comp (a: int, b: int):
  return a - b

class TestSortedInsert(unittest.TestCase):

  def test_throwsIfMaxSizeIs0(self):
    expect(lambda: sortedInsert([], 1, 0, comp)).toThrow(AssertionError, 'MAX_SIZE_ZERO')

  def test_throwsIfItemsLengthGtMaxSize(self):
    expect(lambda: sortedInsert([1, 2], 1, 1, comp)).toThrow(AssertionError, 'ITEMS_SIZE')

  def test_addsIfEmpty(self):
    arr = []
    expect(sortedInsert(arr, 3, 2, comp)).toEqual(None)
    expect(arr).toEqual([3])

  def test_addsIfNotFull(self):
    arr = [1, 5]
    expect(sortedInsert(arr, 3, 3, comp)).toEqual(None)
    expect(arr).toEqual([1, 3, 5])

  def test_addsIfWillNotBeFullAfter(self):
    arr = [1]
    expect(sortedInsert(arr, 0, 3, comp)).toEqual(None)
    expect(arr).toEqual([0, 1])

  def test_returnsAddIfSortsAfterLast(self):
    arr = [1, 2, 3]
    expect(sortedInsert(arr, 4, 3, comp)).toEqual(4)
    expect(arr).toEqual([1, 2, 3])

  def test_removesFromEndIfFull(self):
    arr = [1, 3, 4]
    expect(sortedInsert(arr, 2, 3, comp)).toEqual(4)
    expect(arr).toEqual([1, 2, 3])

  def test_usesComparator(self):
    arr = [4, 2, 1]
    expect(sortedInsert(arr, 3, 3, lambda a, b: comp(a, b) * -1)).toEqual(1)
    expect(arr).toEqual([4, 3, 2])

  def test_emptyAdd(self):
    arr = []
    expect(sortedInsert(arr, 3, 1, comp)).toEqual(None)
    expect(arr).toEqual([3])

  def test_fullAddGreater(self):
    arr = [2]
    expect(sortedInsert(arr, 3, 1, comp)).toEqual(3)
    expect(arr).toEqual([2])

  def test_fullAddLesser(self):
    arr = [4]
    expect(sortedInsert(arr, 3, 1, comp)).toEqual(4)
    expect(arr).toEqual([3])
