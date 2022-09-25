import unittest

from sdkcore.entities.currency import Token
from sdkcore.entities.icx import Icx

ADDRESS_ZERO = 'hx0000000000000000000000000000000000000000'
ADDRESS_ONE = 'hx0000000000000000000000000000000000000001'

t0 = Token(ADDRESS_ZERO, 18)
t1 = Token(ADDRESS_ONE, 18)

class TestCurrency(unittest.TestCase):

  def test_icxOnSameChainsIsIcx(self):
    self.assertTrue(Icx().equals(Icx()))
    
  def test_icxIsNotToken0(self):
    self.assertFalse(Icx().equals(t0))
    
  def test_token1IsNotToken0(self):
    self.assertFalse(t1.equals(t0))
    
  def test_token0IsToken0(self):
    self.assertTrue(t0.equals(t0))
    
  def test_token0IsEqualToAnotherToken0(self):
    self.assertTrue(t0.equals(Token(ADDRESS_ZERO, 18, 'symbol', 'name')))
    
  

