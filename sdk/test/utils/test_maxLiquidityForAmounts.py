import unittest

from sdk.utils.encodeSqrtRatioX96 import encodeSqrtRatioX96
from sdk.utils.maxLiquidityForAmounts import maxLiquidityForAmounts
from sdkcore.constants import MaxUint256

class TestEncodeSqrtRatioX96(unittest.TestCase):

  def test_imprecise_priceInside_100token0_200token1(self):
    self.assertEqual(
      maxLiquidityForAmounts(
        encodeSqrtRatioX96(1, 1),
        encodeSqrtRatioX96(100, 110),
        encodeSqrtRatioX96(110, 100),
        100,
        200,
        False
      ), 
      2148
    )

  def test_imprecise_priceInside_100token0_maxtoken1(self):
    self.assertEqual(
        maxLiquidityForAmounts(
          encodeSqrtRatioX96(1, 1),
          encodeSqrtRatioX96(100, 110),
          encodeSqrtRatioX96(110, 100),
          100,
          MaxUint256,
          False
        ), 
      2148
    )

  def test_imprecise_priceInside_maxtoken0_200token1(self):
    self.assertEqual(
        maxLiquidityForAmounts(
          encodeSqrtRatioX96(1, 1),
          encodeSqrtRatioX96(100, 110),
          encodeSqrtRatioX96(110, 100),
          MaxUint256,
          200,
          False
        ), 
      4297
    )

  def test_imprecise_priceBelow_100token0_200token1(self):
    self.assertEqual(
        maxLiquidityForAmounts(
          encodeSqrtRatioX96(99, 110),
          encodeSqrtRatioX96(100, 110),
          encodeSqrtRatioX96(110, 100),
          100,
          200,
          False
        ), 
      1048
    )

  def test_imprecise_priceBelow_100token0_maxtoken1(self):
    self.assertEqual(
        maxLiquidityForAmounts(
          encodeSqrtRatioX96(99, 110),
          encodeSqrtRatioX96(100, 110),
          encodeSqrtRatioX96(110, 100),
          100,
          MaxUint256,
          False
        ), 
      1048
    )

  def test_imprecise_priceBelow_maxtoken0_200token1(self):
    self.assertEqual(
        maxLiquidityForAmounts(
          encodeSqrtRatioX96(99, 110),
          encodeSqrtRatioX96(100, 110),
          encodeSqrtRatioX96(110, 100),
          MaxUint256,
          200,
          False
        ), 
      1214437677402049537867770675689825446306618235148421502747047340104175905226807
    )

  def test_100Token0200Token1_2(self):
    self.assertEqual(
        maxLiquidityForAmounts(
          encodeSqrtRatioX96(111, 100),
          encodeSqrtRatioX96(100, 110),
          encodeSqrtRatioX96(110, 100),
          100,
          200,
          False
        ), 
      2097
    )

  def test_100Token0MaxToken1_3(self):
    self.assertEqual(
        maxLiquidityForAmounts(
          encodeSqrtRatioX96(111, 100),
          encodeSqrtRatioX96(100, 110),
          encodeSqrtRatioX96(110, 100),
          100,
          MaxUint256,
          False
        ),
      1214437677402049395210666424382790702218161189832585414652320869013789600108423
    )

  def test_maxToken0200Token1_3(self):
    self.assertEqual(
        maxLiquidityForAmounts(
          encodeSqrtRatioX96(111, 100),
          encodeSqrtRatioX96(100, 110),
          encodeSqrtRatioX96(110, 100),
          MaxUint256,
          200,
          False
        ), 
      2097
    )

  def test_100Token0200Token1_3(self):
    self.assertEqual(
        maxLiquidityForAmounts(
          encodeSqrtRatioX96(1, 1),
          encodeSqrtRatioX96(100, 110),
          encodeSqrtRatioX96(110, 100),
          100,
          200,
          True
        ), 
      2148
    )

  def test_100Token0MaxToken1_0(self):
    self.assertEqual(
        maxLiquidityForAmounts(
          encodeSqrtRatioX96(1, 1),
          encodeSqrtRatioX96(100, 110),
          encodeSqrtRatioX96(110, 100),
          100,
          MaxUint256,
          True
        ), 
      2148
    )
      
  def test_maxToken0200Token1_0(self):
    self.assertEqual(
        maxLiquidityForAmounts(
          encodeSqrtRatioX96(1, 1),
          encodeSqrtRatioX96(100, 110),
          encodeSqrtRatioX96(110, 100),
          MaxUint256,
          200,
          True
        ), 
      4297
    )
      
    
  def test_100Token0200Token1_0(self):
    self.assertEqual(
        maxLiquidityForAmounts(
          encodeSqrtRatioX96(99, 110),
          encodeSqrtRatioX96(100, 110),
          encodeSqrtRatioX96(110, 100),
          100,
          200,
          True
        ), 
      1048
    )
      
  def test_100Token0MaxToken1_1(self):
    self.assertEqual(
        maxLiquidityForAmounts(
          encodeSqrtRatioX96(99, 110),
          encodeSqrtRatioX96(100, 110),
          encodeSqrtRatioX96(110, 100),
          100,
          MaxUint256,
          True
        ), 
      1048
    )
      
  def test_maxToken0200Token1_1(self):
    self.assertEqual(
        maxLiquidityForAmounts(
          encodeSqrtRatioX96(99, 110),
          encodeSqrtRatioX96(100, 110),
          encodeSqrtRatioX96(110, 100),
          MaxUint256,
          200,
          True
        ), 
      1214437677402049537867770675696771108746709892686845009503743929281911097914501
    )
      
    
  def test_100Token0200Token1_1(self):
    self.assertEqual(
        maxLiquidityForAmounts(
          encodeSqrtRatioX96(111, 100),
          encodeSqrtRatioX96(100, 110),
          encodeSqrtRatioX96(110, 100),
          100,
          200,
          True
        ), 
      2097
    )
      
  def test_100Token0MaxToken1_2(self):
    self.assertEqual(
        maxLiquidityForAmounts(
          encodeSqrtRatioX96(111, 100),
          encodeSqrtRatioX96(100, 110),
          encodeSqrtRatioX96(110, 100),
          100,
          MaxUint256,
          True
        ), 
      1214437677402049395210666424382790702218161189832585414652320869013789600108423
    )
      
  def test_maxToken0200Token1_2(self):
    self.assertEqual(
        maxLiquidityForAmounts(
          encodeSqrtRatioX96(111, 100),
          encodeSqrtRatioX96(100, 110),
          encodeSqrtRatioX96(110, 100),
          MaxUint256,
          200,
          True
        ), 
      2097
    )
      