import unittest
from convexus.icontoolkit.expect import expect
from convexus.sdkcore.utils.sqrt import sqrt
from convexus.sdkcore.constants import MaxUint256
import math

class TestSqrt(unittest.TestCase):

  def test_correctFor0_1000(self):
    for i in range(1000):
      expect(sqrt(i)).toEqual((int(math.sqrt(i))))

  def test_correctForAllEvenPowersOf2(self):
    for i in range(1000):
      root = 2**i
      rootSquared = root**2
      expect(sqrt(rootSquared)).toEqual(root)

  def test_correctForMaxUint256(self):
    expect(sqrt(MaxUint256)).toEqual(int('340282366920938463463374607431768211455'))
  