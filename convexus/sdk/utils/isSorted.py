def isSorted(list, comparator):
  """
  * Determines if a tick list is sorted
  * @param list The tick list
  * @param comparator The comparator
  * @returns true if sorted
  """
  for i in range(len(list) - 1):
    if comparator(list[i], list[i + 1]) > 0:
      return False

  return True
