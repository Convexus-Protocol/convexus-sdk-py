
import unittest
from typing import Any

class Expected(unittest.TestCase):
  def __init__(self, a: Any) -> None:
    super().__init__()
    self.maxDiff = None
    self.a = a

  def toEqual(self, b: Any):
    self.assertEqual(self.a, b)

  def toBe(self, b: Any):
    self.assertEqual(self.a, b)

  def toStrictEqual(self, b: Any):
    self.assertEqual(self.a, b)

  def toThrow(self, assertion, message = None):
    with self.assertRaises(assertion) as cm:
      self.a()
    if message:
      self.assertEqual(str(cm.exception), message)

  def toBeDefined(self):
    self.assertTrue(self.a is not None)

  def toBeTruthy(self):
    self.assertTrue(not not self.a)

  def toHaveLength(self, length: int):
    self.assertTrue(len(self.a) == length)


def expect(a: Any) -> Expected:
  return Expected(a)
