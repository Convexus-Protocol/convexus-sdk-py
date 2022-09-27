from typing import Any, Callable, List

def sortedInsert(items: List[Any], add: Any, maxSize: int, comparator: Callable[[Any, Any], int]) -> Any | None:
  """
    Given an array of items sorted by `comparator`, 
    insert an item into its sort index and constrain the size to
    `maxSize` by removing the last item
  """
  assert maxSize > 0, 'MAX_SIZE_ZERO'
  # this is an assert because the interface cannot return multiple removed items if len(items) exceeds maxSize
  assert len(items) <= maxSize, 'ITEMS_SIZE'

  # short circuit first item add
  if len(items) == 0:
    items.append(add)
    return None
  else:
    isFull = (len(items) == maxSize)
    # short circuit if full and the additional item does not come before the last item
    if isFull and comparator(items[len(items) - 1], add) <= 0:
      return add

    lo = 0
    hi = len(items)

    while lo < hi:
      mid = (lo + hi) >> 1
      if comparator(items[mid], add) <= 0:
        lo = mid + 1
      else:
        hi = mid

    items.insert(lo, add)
    return items.pop() if isFull else None
