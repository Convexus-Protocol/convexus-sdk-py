import unittest
from convexus.icontoolkit.expect import expect

from convexus.icontoolkit.BigInt import BigInt
from convexus.sdk.utils.isSorted import isSorted

class TestIssorted(unittest.TestCase):

  def test_emptyList(self):
    expect(isSorted([], lambda a, b: a - b)).toEqual(True)
  
  def test_listWithOneElement(self):
    expect(isSorted([1], lambda a, b: a - b)).toEqual(True)
  
  def test_listWithTwoSortedElements(self):
    expect(isSorted([1, 2], lambda a, b: a - b)).toEqual(True)
  
  def test_listWithTwoEqualElements(self):
    expect(isSorted([2, 2], lambda a, b: a - b)).toEqual(True)
  
  def test_listWithTwoUnsortedElements(self):
    expect(isSorted([2, 1], lambda a, b: a - b)).toEqual(False)
  
  def test_listWithManyElementsWithOneUnsortedPair(self):
    expect(isSorted([1, 2, 3, 4, 6, 5, 7], lambda a, b: a - b)).toEqual(False)
  
  def test_listWithManyElementsWithOneUnsortedPairAtTheEnd(self):
    expect(isSorted([1, 2, 3, 4, 5, 7, 6], lambda a, b: a - b)).toEqual(False)
  
  def test_listWithManyElementsWithOneUnsortedPairAtTheBeginning(self):
    expect(isSorted([2, 1, 3, 4, 5, 6, 7], lambda a, b: a - b)).toEqual(False)
  
  def test_listWithManyElementsWithDuplicates(self):
    expect(isSorted([1, 2, 2, 3, 4, 5, 6, 7], lambda a, b: a - b)).toEqual(True)
  
  def test_listWithOppositeComparator(self):
    expect(isSorted([1, 2, 2, 3, 4, 5, 6, 7], lambda a, b: b - a)).toEqual(False)
  
  def test_reverseSortedListWithOppositeComparator(self):
    expect(isSorted(list(reversed([1, 2, 2, 3, 4, 5, 6, 7])), lambda a, b: b - a)).toEqual(True)

