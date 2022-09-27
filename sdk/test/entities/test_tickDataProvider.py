import unittest
from icontoolkit.test.expect import expect
from sdk.entities.tickDataProvider import NoTickDataProvider

provider = NoTickDataProvider()

class TestTickdataprovider(unittest.TestCase):
  
  def test_throwsOnGetTick(self):
    expect(lambda: provider.getTick(0)).toThrow(Exception, 'No tick data provider was given')
  
  def test_throwsOnNextInitializedTickWithinOneWord(self):
    expect(lambda: provider.nextInitializedTickWithinOneWord(0, False, 1)).toThrow(Exception, 'No tick data provider was given')

