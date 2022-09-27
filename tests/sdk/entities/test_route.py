import unittest

from convexus.icontoolkit.expect import expect
from convexus.sdk.constants import TICK_SPACINGS, FeeAmount
from convexus.sdkcore.entities.currency import Token

from convexus.sdk.utils.encodeSqrtRatioX96 import encodeSqrtRatioX96
from convexus.sdk.entities.pool import Pool
from convexus.sdk.utils.tickMath import TickMath

from convexus.sdk.utils.nearestUsableTick import nearestUsableTick
from convexus.sdk.entities.position import Position, PositionConstructorArgs
from convexus.sdkcore.entities.fractions.percent import Percent
from convexus.sdkcore.entities.icx import Icx
from convexus.sdk.entities.route import Route

ICX = Icx()
token0 = Token('cx0000000000000000000000000000000000000001', 18, 't0')
token1 = Token('cx0000000000000000000000000000000000000002', 18, 't1')
token2 = Token('cx0000000000000000000000000000000000000003', 18, 't2')
wicx = ICX.wrapped

class TestRoute(unittest.TestCase):

  def setUp(self) -> None:
    super().setUp()
    self.pool_0_1 = Pool(token0, token1, FeeAmount.MEDIUM, encodeSqrtRatioX96(1, 1), 0, 0, [])
    self.pool_0_wicx = Pool(token0, wicx, FeeAmount.MEDIUM, encodeSqrtRatioX96(1, 1), 0, 0, [])
    self.pool_1_wicx = Pool(token1, wicx, FeeAmount.MEDIUM, encodeSqrtRatioX96(1, 1), 0, 0, [])

  def test_constructsAPathFromTheTokens(self):
    route = Route([self.pool_0_1], token0, token1)
    expect(route.pools).toEqual([self.pool_0_1])
    expect(route.tokenPath).toEqual([token0, token1])
    expect(route.input).toEqual(token0)
    expect(route.output).toEqual(token1)
    
  def test_shouldFailIfTheInputIsNotInTheFirstPool(self):
    expect(lambda: Route([self.pool_0_1], wicx, token1)).toThrow(AssertionError)

  def test_shouldFailIfOutputIsNotInTheLastPool(self):
    expect(lambda: Route([self.pool_0_1], token0, wicx)).toThrow(AssertionError)

  def test_canHaveATokenAsBothInputAndOutput(self):
    route = Route([self.pool_0_wicx, self.pool_0_1, self.pool_1_wicx], wicx, wicx)
    expect(route.pools).toEqual([self.pool_0_wicx, self.pool_0_1, self.pool_1_wicx])
    expect(route.input).toEqual(wicx)
    expect(route.output).toEqual(wicx)

  def test_supportsIcxInput(self):
    route = Route([self.pool_0_wicx], ICX, token0)
    expect(route.pools).toEqual([self.pool_0_wicx])
    expect(route.input).toEqual(ICX)
    expect(route.output).toEqual(token0)

  def test_supportsIcxOutput(self):
    route = Route([self.pool_0_wicx], token0, ICX)
    expect(route.pools).toEqual([self.pool_0_wicx])
    expect(route.input).toEqual(token0)
    expect(route.output).toEqual(ICX)

class TestMidPriceRoute(unittest.TestCase):

  def setUp(self) -> None:
    super().setUp()

    self.pool_0_1 = Pool(
      token0,
      token1,
      FeeAmount.MEDIUM,
      encodeSqrtRatioX96(1, 5),
      0,
      TickMath.getTickAtSqrtRatio(encodeSqrtRatioX96(1, 5)),
      []
    )
    self.pool_1_2 = Pool(
      token1,
      token2,
      FeeAmount.MEDIUM,
      encodeSqrtRatioX96(15, 30),
      0,
      TickMath.getTickAtSqrtRatio(encodeSqrtRatioX96(15, 30)),
      []
    )
    self.pool_0_wicx = Pool(
      token0,
      wicx,
      FeeAmount.MEDIUM,
      encodeSqrtRatioX96(3, 1),
      0,
      TickMath.getTickAtSqrtRatio(encodeSqrtRatioX96(3, 1)),
      []
    )
    self.pool_1_wicx = Pool(
      token1,
      wicx,
      FeeAmount.MEDIUM,
      encodeSqrtRatioX96(1, 7),
      0,
      TickMath.getTickAtSqrtRatio(encodeSqrtRatioX96(1, 7)),
      []
    )

  def test_correctFor0Lt1(self):
    price = Route([self.pool_0_1], token0, token1).midPrice
    expect(price.toFixed(4)).toEqual('0.2')
    expect(price.baseCurrency.equals(token0)).toEqual(True)
    expect(price.quoteCurrency.equals(token1)).toEqual(True)

  def test_isCached(self):
    route = Route([self.pool_0_1], token0, token1)
    expect(route.midPrice).toStrictEqual(route.midPrice)

  def test_correctFor1Lt0(self):
    price = Route([self.pool_0_1], token1, token0).midPrice
    expect(price.toFixed(4)).toEqual('5')
    expect(price.baseCurrency.equals(token1)).toEqual(True)
    expect(price.quoteCurrency.equals(token0)).toEqual(True)

  def test_correctFor0Lt1Lt2(self):
    price = Route([self.pool_0_1, self.pool_1_2], token0, token2).midPrice
    expect(price.toFixed(4)).toEqual('0.1')
    expect(price.baseCurrency.equals(token0)).toEqual(True)
    expect(price.quoteCurrency.equals(token2)).toEqual(True)

  def test_correctFor2Lt1Lt0(self):
    price = Route([self.pool_1_2, self.pool_0_1], token2, token0).midPrice
    expect(price.toFixed(4)).toEqual('10')
    expect(price.baseCurrency.equals(token2)).toEqual(True)
    expect(price.quoteCurrency.equals(token0)).toEqual(True)

  def test_correctForIcxLt0(self):
    price = Route([self.pool_0_wicx], ICX, token0).midPrice
    expect(price.toFixed(4)).toEqual('0.3333')
    expect(price.baseCurrency.equals(ICX)).toEqual(True)
    expect(price.quoteCurrency.equals(token0)).toEqual(True)

  def test_correctFor1LtWicx(self):
    price = Route([self.pool_1_wicx], token1, wicx).midPrice
    expect(price.toFixed(4)).toEqual('0.1429')
    expect(price.baseCurrency.equals(token1)).toEqual(True)
    expect(price.quoteCurrency.equals(wicx)).toEqual(True)

  def test_correctForIcxLt0Lt1LtWicx(self):
    price = Route([self.pool_0_wicx, self.pool_0_1, self.pool_1_wicx], ICX, wicx).midPrice
    expect(price.toFixed(6)).toEqual('0.009524')
    expect(price.baseCurrency.equals(ICX)).toEqual(True)
    expect(price.quoteCurrency.equals(wicx)).toEqual(True)

  def test_correctForWicxLt0Lt1LtIcx(self):
    price = Route([self.pool_0_wicx, self.pool_0_1, self.pool_1_wicx], wicx, ICX).midPrice
    expect(price.toFixed(6)).toEqual('0.009524')
    expect(price.baseCurrency.equals(wicx)).toEqual(True)
    expect(price.quoteCurrency.equals(ICX)).toEqual(True)
